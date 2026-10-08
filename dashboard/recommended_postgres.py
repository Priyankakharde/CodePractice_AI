import os

import pandas as pd
import psycopg2
import streamlit as st

from dotenv import load_dotenv


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="PostgreSQL Recommendation",
    page_icon="🐘",
    layout="wide",
)


# ============================================================
# CURRENT USER
# ============================================================

CURRENT_USER_EMAIL = "priyanka@codepractice.local"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():

    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5433"),
        database=os.getenv("DB_NAME", "codepractice"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD"),
        connect_timeout=5,
    )


# ============================================================
# GET CURRENT USER
# ============================================================

def get_current_user():

    connection = None

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                name,
                email
            FROM users
            WHERE email = %s
            LIMIT 1;
            """,
            (CURRENT_USER_EMAIL,),
        )

        row = cursor.fetchone()

        if row:

            return {
                "id": row[0],
                "name": row[1],
                "email": row[2],
            }

        return None

    finally:

        if connection:
            connection.close()


# ============================================================
# GET POSTGRESQL RECOMMENDATION DATA
# ============================================================

def get_postgres_performance(user_id):

    connection = None

    try:

        connection = get_connection()

        cursor = connection.cursor()

        query = """
            SELECT
                l.title AS topic,

                CASE
                    WHEN p.id IS NULL
                        THEN 'Not Started'

                    WHEN p.completed = TRUE
                        THEN 'Completed'

                    ELSE 'Started'
                END AS lesson_status,

                COALESCE(p.completed, FALSE) AS completed

            FROM lessons l

            LEFT JOIN progress p
                ON p.lesson_id = l.id
                AND p.user_id = %s

            WHERE l.subject = 'PostgreSQL'

            ORDER BY
                l.lesson_order,
                l.id;
        """

        cursor.execute(
            query,
            (user_id,),
        )

        rows = cursor.fetchall()

        columns = [
            "topic",
            "lesson_status",
            "completed",
        ]

        df = pd.DataFrame(
            rows,
            columns=columns,
        )

        # ----------------------------------------------------
        # TRY YOURSELF ACCURACY
        # ----------------------------------------------------

        df["accuracy"] = df["completed"].apply(
            lambda value: 100 if value else 0
        )

        # ----------------------------------------------------
        # RECOMMENDATION
        # ----------------------------------------------------

        def get_recommendation(row):

            if row["lesson_status"] == "Not Started":
                return "🟡 Later"

            if row["accuracy"] == 0:
                return "🔴 Recommend"

            return "🟢 Don't Recommend"

        df["recommendation"] = df.apply(
            get_recommendation,
            axis=1,
        )

        return df

    except Exception as error:

        st.error(
            f"Unable to load PostgreSQL practice data: {error}"
        )

        return pd.DataFrame(
            columns=[
                "topic",
                "lesson_status",
                "completed",
                "accuracy",
                "recommendation",
            ]
        )

    finally:

        if connection:
            connection.close()


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background: #050b14;
    }

    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: #eef5ff;
        margin-bottom: 6px;
    }

    .subtitle {
        color: #9aacbf;
        font-size: 15px;
        margin-bottom: 42px;
        line-height: 1.6;
    }

    .section-title {
        color: #eef5ff;
        font-size: 19px;
        font-weight: 700;
        margin-top: 10px;
        margin-bottom: 14px;
    }

    .practice-table-wrapper {
        width: 100%;
        margin-top: 8px;
        border: 1px solid #1d3552;
        border-radius: 12px;
        overflow: hidden;
        background: #0b111b;
    }

    .practice-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 14px;
    }

    .practice-table thead {
        background: #171c26;
    }

    .practice-table th {
        color: #aebbd0;
        text-align: left;
        font-weight: 600;
        padding: 14px 16px;
        border-bottom: 1px solid #27364a;
    }

    .practice-table td {
        color: #eef4fb;
        padding: 13px 16px;
        border-bottom: 1px solid #202b3b;
    }

    .practice-table tbody tr:hover {
        background: #111d2d;
    }

    .practice-table tbody tr:last-child td {
        border-bottom: none;
    }

    .sidebar-brand {
        color: #f1f6ff;
        font-size: 20px;
        font-weight: 800;
        margin-top: 20px;
        margin-bottom: 8px;
    }

    .sidebar-tagline {
        color: #8ea3bb;
        font-size: 13px;
        line-height: 1.5;
        margin-bottom: 22px;
    }

    .sidebar-divider {
        height: 1px;
        background: #1c3047;
        margin: 18px 0;
    }

    .sidebar-active {
        color: #f1f6ff;
        background: #102238;
        border: 1px solid #1d4163;
        border-radius: 8px;
        padding: 10px 12px;
        font-size: 14px;
        font-weight: 600;
    }

    [data-testid="stSidebar"] .stButton > button {
        background: transparent;
        border: none;
        color: #9fc8ef;
        text-align: left;
        font-size: 14px;
        font-weight: 500;
        padding: 8px 10px;
        border-radius: 7px;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background: #102238;
        color: #ffffff;
        border: none;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# LOAD DATABASE DATA
# ============================================================

try:

    user = get_current_user()

    if not user:

        st.error(
            "User was not found in the PostgreSQL database."
        )

        st.stop()

    performance = get_postgres_performance(
        user["id"]
    )

except Exception as error:

    st.error(
        "Unable to connect to the PostgreSQL database."
    )

    st.caption(
        f"Database error: {error}"
    )

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-brand">
            &lt;/&gt; CodePractice
        </div>

        <div class="sidebar-tagline">
            Learn. Practice. Grow.
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "←  Dashboard",
        key="recommended_postgres_dashboard",
        use_container_width=True,
    ):

        if "dashboard_page" in st.session_state:

            st.switch_page(
                st.session_state["dashboard_page"]
            )

        else:

            st.switch_page("app.py")

    st.markdown(
        """
        <div class="sidebar-divider"></div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sidebar-active">
            🐘 PostgreSQL Practice
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# PAGE HEADER
# ============================================================

st.markdown(
    """
    <div class="main-title">
        🐘 PostgreSQL Recommendation
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="subtitle">
        Your PostgreSQL practice performance is analyzed to recommend
        what you should practice next.
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# POSTGRESQL PRACTICE DATA
# ============================================================

st.markdown(
    """
    <div class="section-title">
        PostgreSQL Practice Data
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# PREPARE TABLE DATA
# ============================================================

display_df = performance[
    [
        "topic",
        "lesson_status",
        "accuracy",
        "recommendation",
    ]
].copy()

display_df.columns = [
    "Topic",
    "Lesson Status",
    "Try Yourself",
    "Recommendation",
]

display_df["Try Yourself"] = (
    display_df["Try Yourself"].astype(str)
    + "%"
)


# ============================================================
# CREATE HTML TABLE ROWS
# ============================================================

table_rows = ""

for _, row in display_df.iterrows():

    table_rows += (
        f'<tr>'
        f'<td>{row["Topic"]}</td>'
        f'<td>{row["Lesson Status"]}</td>'
        f'<td>{row["Try Yourself"]}</td>'
        f'<td>{row["Recommendation"]}</td>'
        f'</tr>'
    )


# ============================================================
# CREATE HTML TABLE
# ============================================================

table_html = f"""<table class="practice-table">
<thead>
<tr>
<th>Topic</th>
<th>Lesson Status</th>
<th>Try Yourself</th>
<th>Recommendation</th>
</tr>
</thead>
<tbody>
{table_rows}
</tbody>
</table>"""


# ============================================================
# DISPLAY HTML TABLE
# ============================================================

st.markdown(
    table_html,
    unsafe_allow_html=True,
)
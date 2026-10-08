import os

import streamlit as st
import psycopg2
from dotenv import load_dotenv


# =========================================================
# CONFIGURATION
# =========================================================

load_dotenv()

st.set_page_config(
    page_title="Bookmarks | CodePractice AI",
    page_icon="🔖",
    layout="wide",
)


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5433"),
        database=os.getenv("DB_NAME", "codepractice"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD"),
        connect_timeout=5,
    )


# =========================================================
# PAGE STYLE
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background: #050b14;
    }

    .block-container {
        padding-top: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 1400px;
    }

    /* Main title */

    .bookmark-title {
        font-size: 34px;
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 4px;
    }

    .bookmark-subtitle {
        font-size: 14px;
        color: #94a3b8;
        margin-bottom: 28px;
    }

    /* Section label */

    .section-label {
        color: #6e87a5;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 0.5px;
        margin-top: 10px;
        margin-bottom: 12px;
    }

    /* Empty state */

    .empty-card {
        background: #111827;
        border: 1px solid #243244;
        border-radius: 14px;
        padding: 60px 20px;
        text-align: center;
        margin-top: 10px;
    }

    .empty-icon {
        font-size: 44px;
        margin-bottom: 12px;
    }

    .empty-title {
        color: #f8fafc;
        font-size: 21px;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .empty-text {
        color: #94a3b8;
        font-size: 14px;
    }

    /* Bookmark card */

    .bookmark-card {
        background: #111827;
        border: 1px solid #243244;
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 14px;
    }

    .bookmark-subject {
        color: #6ee7b7;
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        margin-bottom: 7px;
    }

    .bookmark-name {
        color: #f8fafc;
        font-size: 19px;
        font-weight: 700;
        margin-bottom: 7px;
    }

    .bookmark-description {
        color: #94a3b8;
        font-size: 14px;
        line-height: 1.6;
    }

    .bookmark-date {
        color: #64748b;
        font-size: 12px;
        margin-top: 12px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            font-size:22px;
            font-weight:800;
            color:#f8fafc;
            margin-bottom:28px;
        ">
            &lt;/&gt; CodePractice
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="
            color:#6e87a5;
            font-size:12px;
            line-height:1.5;
            margin-bottom:30px;
        ">
            Learn. Practice. Grow.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------
    # DASHBOARD
    # -----------------------------------------------------

    if st.button(
        "← Dashboard",
        key="bookmark_dashboard",
        use_container_width=True,
    ):
        st.switch_page(st.session_state["dashboard_page"])

    st.markdown(
        "<hr style='border:0;border-top:1px solid #1f334a;margin:18px 0;'>",
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------
    # BOOKMARKS
    # -----------------------------------------------------

    st.markdown(
        """
        <div style="
            color:#60a5fa;
            font-size:14px;
            font-weight:700;
            margin-bottom:18px;
        ">
            🔖 Bookmarks
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------
    # PYTHON
    # -----------------------------------------------------

    if st.button(
        "🐍  Python",
        key="bookmark_python",
        use_container_width=True,
    ):
        st.switch_page("python_learning.py")

    # -----------------------------------------------------
    # POSTGRESQL
    # -----------------------------------------------------

    if st.button(
        "🐘  PostgreSQL",
        key="bookmark_postgres",
        use_container_width=True,
    ):
        st.switch_page("postgres_learning.py")


# =========================================================
# DATABASE FUNCTIONS
# =========================================================

def get_bookmarks():

    connection = None

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                b.id,
                l.subject,
                l.title,
                l.description,
                b.created_at
            FROM bookmarks b
            JOIN users u
                ON u.id = b.user_id
            JOIN lessons l
                ON l.id = b.lesson_id
            WHERE u.email = %s
            ORDER BY b.created_at DESC;
            """,
            ("priyanka@codepractice.local",),
        )

        return cursor.fetchall()

    except Exception as error:

        st.error(
            f"Could not load bookmarks: {error}"
        )

        return []

    finally:

        if connection:
            connection.close()


def remove_bookmark(bookmark_id):

    connection = None

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM bookmarks
            WHERE id = %s
              AND user_id = (
                  SELECT id
                  FROM users
                  WHERE email = %s
              );
            """,
            (
                bookmark_id,
                "priyanka@codepractice.local",
            ),
        )

        connection.commit()

    except Exception as error:

        if connection:
            connection.rollback()

        st.error(
            f"Could not remove bookmark: {error}"
        )

    finally:

        if connection:
            connection.close()


# =========================================================
# PAGE HEADER
# =========================================================

st.markdown(
    """
    <div class="bookmark-title">
        🔖 Bookmarks
    </div>

    <div class="bookmark-subtitle">
        Your saved Python and PostgreSQL lessons.
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# BOOKMARK LIST
# =========================================================

bookmarks = get_bookmarks()


st.markdown(
    """
    <div class="section-label">
        SAVED LESSONS
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# EMPTY STATE
# =========================================================

if not bookmarks:

    st.markdown(
        '<div style="background:#111827;border:1px solid #243244;border-radius:14px;padding:60px 20px;text-align:center;margin-top:10px;"><div style="font-size:44px;margin-bottom:12px;">🔖</div><div style="color:#f8fafc;font-size:21px;font-weight:700;margin-bottom:8px;">No bookmarks yet</div><div style="color:#94a3b8;font-size:14px;">Bookmark lessons while learning and they will appear here.</div></div>',
        unsafe_allow_html=True,
    )


# =========================================================
# SAVED BOOKMARKS
# =========================================================

else:

    for bookmark in bookmarks:

        bookmark_id = bookmark[0]
        subject = bookmark[1]
        title = bookmark[2]
        description = bookmark[3]
        created_at = bookmark[4]

        st.markdown(
            '<div class="bookmark-card">',
            unsafe_allow_html=True,
        )

        left, right = st.columns(
            [5, 1],
            vertical_alignment="center",
        )

        with left:

            st.markdown(
                f"""
                <div class="bookmark-subject">
                    {subject}
                </div>

                <div class="bookmark-name">
                    {title}
                </div>

                <div class="bookmark-description">
                    {description or "No description available."}
                </div>

                <div class="bookmark-date">
                    Bookmarked on {
                        created_at.strftime("%d %b %Y")
                        if created_at
                        else "Unknown date"
                    }
                </div>
                """,
                unsafe_allow_html=True,
            )

        with right:

            if st.button(
                "Remove",
                key=f"remove_bookmark_{bookmark_id}",
                use_container_width=True,
            ):

                remove_bookmark(bookmark_id)

                st.rerun()

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )
import os
from datetime import date

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from dotenv import load_dotenv

try:
    import psycopg2
except ImportError:
    psycopg2 = None


# ============================================================
# CODEPRACTICE AI
# My Progress
# Database-connected learning analytics dashboard
# ============================================================

load_dotenv()

st.set_page_config(
    page_title="My Progress | CodePractice AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# COURSE DATA
# These are seeded into PostgreSQL's lessons table once.
# The progress page then reads progress from PostgreSQL.
# ============================================================

PYTHON_COURSE = {
    "Python Basics": ["Variables", "Data Types", "Input / Output"],
    "Operators": [
        "Arithmetic Operators",
        "Assignment Operators",
        "Comparison Operators",
        "Logical Operators",
    ],
    "Control Statements": ["if / elif / else", "for Loop", "while Loop"],
    "Data Structures": ["Lists", "Tuples", "Dictionaries", "Sets"],
    "Functions": ["Define Function", "Arguments", "Return Value", "Lambda"],
    "Modules & Libraries": [
        "Import Modules",
        "Built-in Modules",
        "External Libraries",
    ],
    "File Handling": ["Read File", "Write File", "Open / Close File"],
    "Exception Handling": ["try", "except", "finally"],
    "List Comprehension": ["Basic Syntax", "With Condition"],
    "OOP Basics": ["Class", "Object", "Inheritance"],
    "Built-in Functions": [
        "len()",
        "type()",
        "range()",
        "int()",
        "float()",
        "str()",
        "sum()",
        "min()",
        "max()",
    ],
    "NumPy": ["Arrays", "Indexing", "Array Operations"],
    "Pandas": ["Series", "DataFrame", "Read CSV", "Select Data", "Filter Data"],
    "Data Cleaning": ["Missing Values", "Duplicates", "Data Transformation"],
    "Data Analysis": ["Mean", "Median", "Mode", "describe()", "groupby()"],
    "Data Visualization": [
        "Line Chart",
        "Bar Chart",
        "Histogram",
        "Scatter Plot",
    ],
    "ML Basics": ["Features", "Target", "Model", "Prediction"],
    "Types of ML": [
        "Supervised Learning",
        "Unsupervised Learning",
        "Reinforcement Learning — basic idea",
    ],
    "Supervised Learning": ["Regression", "Classification"],
    "Unsupervised Learning": ["Clustering", "K-Means — basic idea"],
    "Dataset Preparation": [
        "Features & Target",
        "Train / Test Split",
        "Preprocessing",
        "Scaling",
    ],
    "Model Training": ["Create Model", "fit()", "Training Data"],
    "Evaluation": ["Accuracy", "Precision", "Recall", "MAE", "MSE", "R²"],
    "Overfitting & Underfitting": ["Overfitting", "Underfitting"],
    "Scikit-learn Basics": ["Import Model", "Create Model", "fit()", "predict()"],
    "ML Workflow": [
        "Collect Data",
        "Clean Data",
        "Explore Data",
        "Prepare Data",
        "Train Model",
        "Evaluate Model",
        "Predict",
    ],
}

POSTGRES_COURSE = {
    "PostgreSQL Basics": [
        "Introduction",
        "Database & Tables",
        "Data Types",
        "SELECT",
        "WHERE",
        "Operators",
        "ORDER BY",
        "LIMIT",
        "INSERT",
        "UPDATE",
        "DELETE",
    ],
    "Data Analysis": [
        "Aggregate Functions",
        "GROUP BY",
        "HAVING",
        "JOIN",
        "Subqueries",
        "CASE",
        "NULL Handling",
    ],
    "PostgreSQL for ML": [
        "Date & Time",
        "String Functions",
        "CTE",
        "Window Functions",
        "Data Cleaning",
        "Preparing Data for ML",
    ],
}


# ============================================================
# DATABASE
# ============================================================

def get_connection():
    if psycopg2 is None:
        raise RuntimeError(
            "psycopg2-binary is not installed. "
            "Run: pip install psycopg2-binary"
        )

    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5433"),
        database=os.getenv("DB_NAME", "codepractice"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD"),
        connect_timeout=5,
    )


def ensure_database_setup():
    """
    Creates the tables if needed and seeds the learning lessons.
    Existing data is preserved.
    """
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(150) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS lessons (
                id SERIAL PRIMARY KEY,
                subject VARCHAR(20) NOT NULL,
                title VARCHAR(150) NOT NULL,
                description TEXT,
                lesson_order INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS practice_submissions (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                lesson_id INTEGER REFERENCES lessons(id) ON DELETE CASCADE,
                code TEXT NOT NULL,
                status VARCHAR(30),
                execution_time FLOAT,
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS progress (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                lesson_id INTEGER REFERENCES lessons(id) ON DELETE CASCADE,
                completed BOOLEAN DEFAULT FALSE,
                attempts INTEGER DEFAULT 0,
                last_attempted TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        )

        cursor.execute(
            """
            INSERT INTO users (name, email)
            VALUES (%s, %s)
            ON CONFLICT (email) DO NOTHING;
            """,
            ("Priyanka Kharde", "priyanka@codepractice.local"),
        )

        order_no = 1

        for subject, course in [
            ("Python", PYTHON_COURSE),
            ("PostgreSQL", POSTGRES_COURSE),
        ]:
            for parent, topics in course.items():
                for topic in topics:
                    description = f"{parent} → {topic}"

                    cursor.execute(
                        """
                        INSERT INTO lessons
                            (subject, title, description, lesson_order)
                        SELECT %s, %s, %s, %s
                        WHERE NOT EXISTS (
                            SELECT 1
                            FROM lessons
                            WHERE subject = %s AND title = %s
                        );
                        """,
                        (
                            subject,
                            topic,
                            description,
                            order_no,
                            subject,
                            topic,
                        ),
                    )

                    order_no += 1

        connection.commit()

    finally:
        connection.close()


def get_user():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id, name, email
            FROM users
            WHERE email = %s
            LIMIT 1;
            """,
            ("priyanka@codepractice.local",),
        )

        row = cursor.fetchone()

        if not row:
            cursor.execute(
                """
                INSERT INTO users (name, email)
                VALUES (%s, %s)
                RETURNING id, name, email;
                """,
                ("Priyanka Kharde", "priyanka@codepractice.local"),
            )
            row = cursor.fetchone()
            connection.commit()

        return {
            "id": row[0],
            "name": row[1],
            "email": row[2],
        }

    finally:
        connection.close()


def load_progress_data(user_id):
    connection = get_connection()

    try:
        query = """
            SELECT
                l.id AS lesson_id,
                l.subject,
                l.title,
                l.description,
                l.lesson_order,
                COALESCE(p.completed, FALSE) AS completed,
                COALESCE(p.attempts, 0) AS attempts,
                p.last_attempted
            FROM lessons l
            LEFT JOIN progress p
                ON p.lesson_id = l.id
                AND p.user_id = %s
            ORDER BY
                CASE
                    WHEN l.subject = 'Python' THEN 1
                    ELSE 2
                END,
                l.lesson_order,
                l.id;
        """

        return pd.read_sql_query(query, connection, params=(user_id,))

    finally:
        connection.close()


def load_submission_stats(user_id):
    connection = get_connection()

    try:
        query = """
            SELECT
                COUNT(*) AS total_submissions,
                COUNT(*) FILTER (
                    WHERE LOWER(COALESCE(status, '')) IN
                    ('passed', 'success', 'solved', 'correct')
                ) AS successful_submissions,
                COALESCE(AVG(execution_time), 0) AS avg_execution_time,
                MAX(submitted_at) AS last_submission
            FROM practice_submissions
            WHERE user_id = %s;
        """

        return pd.read_sql_query(query, connection, params=(user_id,))

    finally:
        connection.close()


def load_recent_activity(user_id):
    connection = get_connection()

    try:
        query = """
            SELECT
                l.subject,
                l.title,
                p.completed,
                p.attempts,
                p.last_attempted
            FROM progress p
            JOIN lessons l
                ON l.id = p.lesson_id
            WHERE p.user_id = %s
            ORDER BY p.last_attempted DESC NULLS LAST
            LIMIT 8;
        """

        return pd.read_sql_query(query, connection, params=(user_id,))

    finally:
        connection.close()


def load_streak(user_id):
    connection = get_connection()

    try:
        query = """
            SELECT DISTINCT DATE(last_attempted) AS activity_date
            FROM progress
            WHERE user_id = %s
              AND last_attempted IS NOT NULL

            UNION

            SELECT DISTINCT DATE(submitted_at) AS activity_date
            FROM practice_submissions
            WHERE user_id = %s
              AND submitted_at IS NOT NULL

            ORDER BY activity_date DESC;
        """

        df = pd.read_sql_query(
            query,
            connection,
            params=(user_id, user_id),
        )

        if df.empty:
            return 0

        dates = [
            row.date()
            if hasattr(row, "date")
            else row
            for row in pd.to_datetime(df["activity_date"])
        ]

        today = date.today()

        if dates[0] not in (today, pd.Timestamp(today).date()):
            return 0

        streak = 1

        for index in range(1, len(dates)):
            difference = (dates[index - 1] - dates[index]).days

            if difference == 1:
                streak += 1
            else:
                break

        return streak

    finally:
        connection.close()


# ============================================================
# UI HELPERS
# ============================================================

def safe(value):
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def metric_card(icon, value, label, accent="blue"):
    return f"""
    <div class="metric-card">
        <div class="metric-icon {accent}">{icon}</div>
        <div>
            <div class="metric-value">{value}</div>
            <div class="metric-label">{safe(label)}</div>
        </div>
    </div>
    """


def progress_bar(value, accent="blue"):
    value = max(0, min(100, float(value)))
    return f"""
    <div class="progress-track">
        <div class="progress-fill {accent}" style="width:{value:.1f}%"></div>
    </div>
    """


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 80% 0%,
                rgba(36, 112, 215, .13),
                transparent 28%
            ),
            #050b14;
        color: #edf4fc;
    }

    [data-testid="stAppViewContainer"] {
        background: #050b14;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    footer {
        visibility: hidden;
    }

    .block-container {
        max-width: 1480px;
        padding: 20px 28px 35px;
    }

    /* SIDEBAR */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #071426 0%,
                #07111e 100%
            );
        border-right: 1px solid #142940;
    }

    section[data-testid="stSidebar"] > div:first-child {
        padding: 18px 16px;
    }

    .brand {
        padding: 4px 7px 18px;
        border-bottom: 1px solid #17304a;
        margin-bottom: 17px;
    }

    .brand-row {
        display: flex;
        align-items: center;
        gap: 9px;
    }

    .brand-logo {
        color: #36a0ff;
        font-size: 26px;
        font-weight: 900;
    }

    .brand-title {
        color: #f4f8ff;
        font-size: 19px;
        font-weight: 800;
    }

    .brand-sub {
        color: #6f87a5;
        font-size: 9px;
        margin-left: 35px;
        margin-top: 2px;
    }

    .sidebar-heading {
        color: #7189a7;
        font-size: 9px;
        font-weight: 800;
        letter-spacing: .8px;
        text-transform: uppercase;
        margin: 0 7px 8px;
    }

    section[data-testid="stSidebar"] .stButton > button {
        width: 100%;
        min-height: 38px;
        border: 1px solid transparent;
        border-radius: 8px;
        background: transparent;
        color: #a9bbd0;
        text-align: left;
        font-size: 12px;
        font-weight: 600;
        padding: 7px 10px;
        margin: 2px 0;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background: #0d2239;
        border-color: #183d62;
        color: #ffffff;
    }

    .sidebar-active {
        background: #0d2a49;
        border: 1px solid #1b4c78;
        border-radius: 8px;
        color: #ffffff;
        padding: 9px 11px;
        margin-bottom: 3px;
        font-size: 12px;
        font-weight: 700;
    }

    /* TOP */

    .top-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 19px;
    }

    .page-kicker {
        color: #439cff;
        font-size: 9px;
        font-weight: 800;
        letter-spacing: 1.2px;
    }

    .page-title {
        color: #f4f8ff;
        font-size: 27px;
        font-weight: 850;
        margin-top: 3px;
    }

    .page-subtitle {
        color: #7389a5;
        font-size: 11px;
        margin-top: 3px;
    }

    .profile-chip {
        display: flex;
        align-items: center;
        gap: 9px;
        border: 1px solid #203a58;
        background: #0b1a2c;
        border-radius: 9px;
        padding: 7px 11px;
    }

    .avatar {
        width: 29px;
        height: 29px;
        border-radius: 50%;
        background: #277ff1;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 800;
        font-size: 12px;
    }

    .profile-name {
        color: #f2f7ff;
        font-size: 10px;
        font-weight: 800;
    }

    .profile-sub {
        color: #7189a6;
        font-size: 8px;
        margin-top: 2px;
    }

    /* METRICS */

    .metric-card {
        min-height: 93px;
        border: 1px solid #19334e;
        border-radius: 11px;
        background: #091827;
        display: flex;
        align-items: center;
        gap: 13px;
        padding: 15px;
    }

    .metric-icon {
        width: 42px;
        height: 42px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
    }

    .metric-icon.blue {
        background: #102f55;
    }

    .metric-icon.green {
        background: #0d4036;
    }

    .metric-icon.orange {
        background: #432a16;
    }

    .metric-icon.purple {
        background: #2d2451;
    }

    .metric-value {
        color: #f5f8fd;
        font-size: 23px;
        font-weight: 850;
        line-height: 1;
    }

    .metric-label {
        color: #758ca7;
        font-size: 9px;
        margin-top: 5px;
    }

    /* CARDS */

    .card {
        border: 1px solid #19334e;
        border-radius: 11px;
        background: #091827;
        padding: 15px;
        margin-top: 15px;
    }

    .card-title {
        color: #edf4fc;
        font-size: 13px;
        font-weight: 800;
    }

    .card-subtitle {
        color: #6f87a3;
        font-size: 9px;
        margin-top: 3px;
        margin-bottom: 11px;
    }

    .subject-row {
        padding: 11px 0;
        border-bottom: 1px solid #152b42;
    }

    .subject-row:last-child {
        border-bottom: none;
    }

    .subject-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .subject-name {
        color: #eaf2fb;
        font-size: 11px;
        font-weight: 750;
    }

    .subject-percent {
        color: #91a7c0;
        font-size: 10px;
        font-weight: 700;
    }

    .progress-track {
        width: 100%;
        height: 6px;
        border-radius: 10px;
        background: #1a2d42;
        overflow: hidden;
        margin-top: 7px;
    }

    .progress-fill {
        height: 100%;
        border-radius: 10px;
    }

    .progress-fill.blue {
        background: #3291ff;
    }

    .progress-fill.green {
        background: #20cda0;
    }

    .progress-fill.orange {
        background: #f09b43;
    }

    .progress-fill.purple {
        background: #9b7cff;
    }

    /* DONUT */

    .chart-card {
        border: 1px solid #19334e;
        border-radius: 11px;
        background: #091827;
        padding: 13px;
        margin-top: 15px;
    }

    /* ACTIVITY */

    .activity-item {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px 0;
        border-bottom: 1px solid #152b42;
    }

    .activity-item:last-child {
        border-bottom: none;
    }

    .activity-icon {
        width: 32px;
        height: 32px;
        border-radius: 8px;
        background: #102944;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .activity-name {
        color: #e8f1fb;
        font-size: 10px;
        font-weight: 750;
    }

    .activity-meta {
        color: #6f87a2;
        font-size: 8px;
        margin-top: 3px;
    }

    .activity-status {
        margin-left: auto;
        color: #38d7ae;
        font-size: 9px;
        font-weight: 700;
    }

    .empty {
        color: #7188a3;
        font-size: 10px;
        padding: 14px 0;
    }

    /* ACHIEVEMENTS */

    .achievement {
        border: 1px solid #1a344e;
        border-radius: 9px;
        background: #0b1a2b;
        padding: 12px;
        min-height: 104px;
    }

    .achievement-icon {
        font-size: 23px;
    }

    .achievement-title {
        color: #edf4fc;
        font-size: 10px;
        font-weight: 800;
        margin-top: 6px;
    }

    .achievement-text {
        color: #7189a5;
        font-size: 8px;
        line-height: 1.4;
        margin-top: 4px;
    }

    /* ACTION */

    .refresh-note {
        color: #637b98;
        font-size: 8px;
        text-align: right;
        margin-top: 5px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DATABASE LOAD
# ============================================================

try:
    ensure_database_setup()
    user = get_user()
    progress_df = load_progress_data(user["id"])
    submission_df = load_submission_stats(user["id"])
    recent_df = load_recent_activity(user["id"])
    streak = load_streak(user["id"])

except Exception as error:
    st.error(
        "PostgreSQL connection/setup failed.\n\n"
        f"{error}\n\n"
        "Check your .env file and make sure PostgreSQL is running on port 5433."
    )
    st.stop()


# ============================================================
# CALCULATE METRICS
# ============================================================

total_lessons = len(progress_df)

completed_lessons = int(progress_df["completed"].sum()) if total_lessons else 0

overall_progress = (
    (completed_lessons / total_lessons) * 100
    if total_lessons
    else 0
)

python_df = progress_df[
    progress_df["subject"].str.lower() == "python"
].copy()

postgres_df = progress_df[
    progress_df["subject"].str.lower() == "postgresql"
].copy()

python_total = len(python_df)
python_completed = int(python_df["completed"].sum()) if python_total else 0
python_progress = (
    python_completed / python_total * 100
    if python_total
    else 0
)

postgres_total = len(postgres_df)
postgres_completed = int(postgres_df["completed"].sum()) if postgres_total else 0
postgres_progress = (
    postgres_completed / postgres_total * 100
    if postgres_total
    else 0
)

total_attempts = int(progress_df["attempts"].sum()) if total_lessons else 0

total_submissions = int(
    submission_df.iloc[0]["total_submissions"]
) if not submission_df.empty else 0

successful_submissions = int(
    submission_df.iloc[0]["successful_submissions"]
) if not submission_df.empty else 0

success_rate = (
    successful_submissions / total_submissions * 100
    if total_submissions
    else 0
)

avg_execution = float(
    submission_df.iloc[0]["avg_execution_time"]
) if not submission_df.empty else 0

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            font-size:22px;
            font-weight:800;
            color:#f8fafc;
            margin-bottom:10px;
        ">
            &lt;/&gt; CodePractice
        </div>

        <div style="
            color:#6e87a5;
            font-size:12px;
            margin-bottom:28px;
        ">
            Learn. Practice. Grow.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # DASHBOARD
    # --------------------------------------------------------

    if st.button(
        "← Dashboard",
        key="progress_dashboard_back",
        use_container_width=True,
    ):
        if "dashboard_page" in st.session_state:
            st.switch_page(st.session_state["dashboard_page"])

    st.markdown(
        """
        <div style="
            border-top:1px solid #1f334a;
            margin:18px 0;
        "></div>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # MY PROGRESS
    # --------------------------------------------------------

    st.markdown(
        """
        <div style="
            color:#60a5fa;
            font-size:14px;
            font-weight:700;
            margin-bottom:16px;
        ">
            📊 My Progress
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # PYTHON
    # --------------------------------------------------------

    if st.button(
        "🐍  Python",
        key="progress_python",
        use_container_width=True,
    ):
        st.switch_page("python_learning.py")

    # --------------------------------------------------------
    # POSTGRESQL
    # --------------------------------------------------------

    if st.button(
        "🐘  PostgreSQL",
        key="progress_postgres",
        use_container_width=True,
    ):
        st.switch_page("postgres_learning.py")
        
        
# ============================================================
# HEADER
# ============================================================

left, right = st.columns([4.5, 1.2], gap="medium")

with left:
    st.markdown(
        '<div class="page-kicker">LEARNING ANALYTICS</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-title">📊 My Progress</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="page-subtitle">
            Track your Python and PostgreSQL learning journey,
            practice activity and improvement over time.
        </div>
        """,
        unsafe_allow_html=True,
    )

with right:
    st.markdown(
        f"""
        <div class="profile-chip">
            <div class="avatar">P</div>
            <div>
                <div class="profile-name">{safe(user["name"])}</div>
                <div class="profile-sub">Learning Dashboard ✨</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# KPI CARDS
# ============================================================

m1, m2, m3, m4 = st.columns(4, gap="small")

with m1:
    st.markdown(
        metric_card(
            "🎯",
            f"{overall_progress:.0f}%",
            "Overall Progress",
            "blue",
        ),
        unsafe_allow_html=True,
    )

with m2:
    st.markdown(
        metric_card(
            "✅",
            completed_lessons,
            "Lessons Completed",
            "green",
        ),
        unsafe_allow_html=True,
    )

with m3:
    st.markdown(
        metric_card(
            "🔥",
            f"{streak} days",
            "Learning Streak",
            "orange",
        ),
        unsafe_allow_html=True,
    )

with m4:
    st.markdown(
        metric_card(
            "💻",
            total_attempts,
            "Practice Attempts",
            "purple",
        ),
        unsafe_allow_html=True,
    )


# ============================================================
# COURSE PROGRESS + DONUT
# ============================================================

left_col, right_col = st.columns([1.55, 1], gap="medium")

with left_col:

    course_progress_html = f"""
<div class="card">
    <div class="card-title">📚 Course Progress</div>

    <div class="card-subtitle">
        Completion is calculated directly from the PostgreSQL progress table.
    </div>

    <div class="subject-row">
        <div class="subject-top">
            <div class="subject-name">🐍 Python</div>
            <div class="subject-percent">
                {python_completed} / {python_total}
                &nbsp;•&nbsp; {python_progress:.0f}%
            </div>
        </div>

        <div class="progress-track">
            <div class="progress-fill blue"
                 style="width:{python_progress:.1f}%">
            </div>
        </div>
    </div>

    <div class="subject-row">
        <div class="subject-top">
            <div class="subject-name">🐘 PostgreSQL</div>
            <div class="subject-percent">
                {postgres_completed} / {postgres_total}
                &nbsp;•&nbsp; {postgres_progress:.0f}%
            </div>
        </div>

        <div class="progress-track">
            <div class="progress-fill green"
                 style="width:{postgres_progress:.1f}%">
            </div>
        </div>
    </div>

    <div class="subject-row">
        <div class="subject-top">
            <div class="subject-name">🏆 Total Course</div>
            <div class="subject-percent">
                {completed_lessons} / {total_lessons}
                &nbsp;•&nbsp; {overall_progress:.0f}%
            </div>
        </div>

        <div class="progress-track">
            <div class="progress-fill purple"
                 style="width:{overall_progress:.1f}%">
            </div>
        </div>
    </div>
</div>
"""

    st.html(course_progress_html)
    
with right_col:

    fig = go.Figure(
        go.Pie(
            labels=["Completed", "Remaining"],
            values=[
                completed_lessons,
                max(total_lessons - completed_lessons, 0),
            ],
            hole=0.72,
            textinfo="none",
            marker=dict(
                colors=["#3291ff", "#1b3047"],
                line=dict(color="#091827", width=2),
            ),
        )
    )

    fig.update_layout(
        height=250,
        margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor="#091827",
        plot_bgcolor="#091827",
        showlegend=False,
        annotations=[
            dict(
                text=f"{overall_progress:.0f}%",
                x=0.5,
                y=0.53,
                font=dict(
                    size=28,
                    color="#ffffff",
                ),
                showarrow=False,
            ),
            dict(
                text="Complete",
                x=0.5,
                y=0.39,
                font=dict(
                    size=10,
                    color="#7189a5",
                ),
                showarrow=False,
            ),
        ],
    )

    st.markdown(
        '<div class="chart-card"><div class="card-title">📈 Overall Completion</div>',
        unsafe_allow_html=True,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False,
        },
    )

    st.markdown(
        f"""
        <div class="refresh-note">
            {completed_lessons} lessons completed • {total_lessons} total lessons
        </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# PRACTICE ANALYTICS
# ============================================================

a1, a2, a3 = st.columns(3, gap="small")

with a1:
    st.markdown(
        metric_card(
            "🧠",
            total_submissions,
            "Code Submissions",
            "blue",
        ),
        unsafe_allow_html=True,
    )

with a2:
    st.markdown(
        metric_card(
            "🚀",
            f"{success_rate:.0f}%",
            "Submission Success Rate",
            "green",
        ),
        unsafe_allow_html=True,
    )

with a3:
    st.markdown(
        metric_card(
            "⚡",
            f"{avg_execution:.3f}s",
            "Average Execution Time",
            "orange",
        ),
        unsafe_allow_html=True,
    )


# ============================================================
# RECENT ACTIVITY
# ============================================================

st.markdown(
    """
    <div class="card">
        <div class="card-title">🕒 Recent Learning Activity</div>
        <div class="card-subtitle">
            Your latest lesson attempts stored in PostgreSQL.
        </div>
    """,
    unsafe_allow_html=True,
)

if recent_df.empty:

    st.markdown(
        """
        <div class="empty">
            No learning activity yet. Start a Python or PostgreSQL lesson
            and your activity will appear here.
        </div>
        """,
        unsafe_allow_html=True,
    )

else:

    for _, row in recent_df.iterrows():

        subject = str(row["subject"])
        title = str(row["title"])
        completed = bool(row["completed"])
        attempts = int(row["attempts"])

        icon = "🐍" if subject == "Python" else "🐘"
        status = "Completed" if completed else "In Progress"

        if pd.notna(row["last_attempted"]):
            timestamp = pd.to_datetime(row["last_attempted"])
            time_text = timestamp.strftime("%d %b %Y • %I:%M %p")
        else:
            time_text = "No attempt recorded"

        st.markdown(
            f"""
            <div class="activity-item">
                <div class="activity-icon">{icon}</div>
                <div>
                    <div class="activity-name">{safe(title)}</div>
                    <div class="activity-meta">
                        {safe(subject)} • {attempts} attempt(s)
                        • {safe(time_text)}
                    </div>
                </div>
                <div class="activity-status">{status}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# ACHIEVEMENTS
# ============================================================

st.markdown(
    """
    <div class="card">
        <div class="card-title">🏅 Learning Milestones</div>
        <div class="card-subtitle">
            Automatically calculated from your database activity.
        </div>
    """,
    unsafe_allow_html=True,
)

ach1, ach2, ach3, ach4 = st.columns(4, gap="small")

milestones = [
    (
        "🐣",
        "First Step",
        "Complete your first lesson.",
        completed_lessons >= 1,
    ),
    (
        "🔥",
        "3-Day Streak",
        "Study or practice for 3 consecutive days.",
        streak >= 3,
    ),
    (
        "🎯",
        "10 Lessons",
        "Complete 10 lessons.",
        completed_lessons >= 10,
    ),
    (
        "🏆",
        "Course Finisher",
        "Complete every seeded lesson.",
        total_lessons > 0 and completed_lessons == total_lessons,
    ),
]

for column, milestone in zip(
    [ach1, ach2, ach3, ach4],
    milestones,
):
    icon, title, description, unlocked = milestone

    with column:
        opacity = "1" if unlocked else ".42"

        st.markdown(
            f"""
            <div class="achievement" style="opacity:{opacity}">
                <div class="achievement-icon">{icon}</div>
                <div class="achievement-title">
                    {safe(title)}
                    {" ✓" if unlocked else " 🔒"}
                </div>
                <div class="achievement-text">
                    {safe(description)}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div style="
        text-align:center;
        color:#596b82;
        font-size:9px;
        margin-top:20px;
        padding-top:12px;
        border-top:1px solid #16263a;
    ">
        CodePractice AI • PostgreSQL-powered learning analytics
    </div>
    """,
    unsafe_allow_html=True,
)

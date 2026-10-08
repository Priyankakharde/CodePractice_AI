import os
import time
from pathlib import Path

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

try:
    import psycopg2
except ImportError:
    psycopg2 = None
    
    
# ============================================================
# CURRENT USER
# ============================================================

CURRENT_USER_EMAIL = "priyanka@codepractice.local"
CURRENT_USER_NAME = "Priyanka"    


# =========================================================
# CONFIG
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

st.set_page_config(
    page_title="PostgreSQL Learning | CodePractice AI",
    page_icon="🐘",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# COURSE DATA
# =========================================================

COURSE = {
    "LEVEL 1 — POSTGRESQL BASICS": {
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
    },
    "LEVEL 2 — SQL FOR DATA ANALYSIS": {
        "Data Analysis": [
            "Aggregate Functions",
            "GROUP BY",
            "HAVING",
            "JOIN",
            "Subqueries",
            "CASE",
            "NULL Handling",
        ],
    },
    "LEVEL 3 — POSTGRESQL FOR ML": {
        "PostgreSQL for ML": [
            "Date & Time",
            "String Functions",
            "CTE",
            "Window Functions",
            "Data Cleaning",
            "Preparing Data for ML",
        ],
    },
}


LESSONS = {
    "Introduction": {
        "concept": "PostgreSQL is a relational database system used to store and query structured data.",
        "points": [
            "Database → stores related data.",
            "Table → stores data in rows and columns.",
            "SQL → language used to work with the data.",
        ],
        "example": "SELECT 'Hello PostgreSQL' AS message;",
        "output": "Hello PostgreSQL",
        "explanation": "SQL statements tell PostgreSQL what data you want to read or change.",
        "syntax": "SELECT column_name\nFROM table_name;",
        "ml": "ML projects often use SQL to collect training data and features from databases.",
    },
    "Database & Tables": {
        "concept": "A database contains tables. A table stores records in rows and attributes in columns.",
        "points": [
            "Database → collection of related tables.",
            "Table → rows + columns.",
            "Primary key → uniquely identifies a row.",
        ],
        "example": "CREATE TABLE students (\n    id SERIAL PRIMARY KEY,\n    name VARCHAR(100),\n    score INTEGER\n);",
        "output": "Table created successfully.",
        "explanation": "A table definition describes the columns and the type of data each column can store.",
        "syntax": "CREATE TABLE table_name (\n    column_name DATA_TYPE\n);",
        "ml": "Good table structure makes datasets easier to query, clean and prepare for ML.",
    },
    "Data Types": {
        "concept": "Data types tell PostgreSQL what kind of value a column can store.",
        "points": [
            "INTEGER → whole numbers.",
            "NUMERIC → precise numbers.",
            "VARCHAR / TEXT → text.",
            "BOOLEAN → TRUE or FALSE.",
            "DATE / TIMESTAMP → dates and times.",
        ],
        "example": "SELECT\n    27 AS age,\n    99.5 AS score,\n    'Python' AS subject,\n    TRUE AS active;",
        "output": "27 | 99.5 | Python | true",
        "explanation": "Choosing the correct type helps PostgreSQL store and process data correctly.",
        "syntax": "column_name DATA_TYPE",
        "ml": "Correct data types are important when creating clean numerical, categorical and time-based ML features.",
    },
    "SELECT": {
        "concept": "SELECT is used to read data from a table.",
        "points": [
            "SELECT columns you need.",
            "Use * to select all columns.",
            "FROM specifies the table.",
        ],
        "example": "SELECT name, score\nFROM students;",
        "output": "Returns the selected columns from students.",
        "explanation": "SELECT is one of the most important SQL commands because data analysis starts with reading data.",
        "syntax": "SELECT column1, column2\nFROM table_name;",
        "ml": "Use SELECT to extract the columns that will become ML features or targets.",
    },
    "WHERE": {
        "concept": "WHERE filters rows that match a condition.",
        "points": [
            "Filters records.",
            "Works with comparison operators.",
            "Can combine conditions.",
        ],
        "example": "SELECT name, score\nFROM students\nWHERE score >= 70;",
        "output": "Only students with score >= 70",
        "explanation": "WHERE reduces the dataset to records that satisfy your condition.",
        "syntax": "SELECT *\nFROM table_name\nWHERE condition;",
        "ml": "Filtering helps create the exact training population or remove unwanted records.",
    },
    "Operators": {
        "concept": "SQL operators are used for calculations, comparisons and logical conditions.",
        "points": [
            "=, !=, <>, >, <, >=, <= → comparison.",
            "AND, OR, NOT → logical conditions.",
            "+, -, *, / → arithmetic.",
        ],
        "example": "SELECT name, score\nFROM students\nWHERE score >= 70\n  AND score < 90;",
        "output": "Students whose score is from 70 to 89",
        "explanation": "Operators let you build useful filters and calculations.",
        "syntax": "WHERE condition1\n  AND condition2;",
        "ml": "Operators are frequently used when filtering and engineering features from raw data.",
    },
    "ORDER BY": {
        "concept": "ORDER BY sorts query results.",
        "points": [
            "ASC → ascending.",
            "DESC → descending.",
            "Can sort by multiple columns.",
        ],
        "example": "SELECT name, score\nFROM students\nORDER BY score DESC;",
        "output": "Rows sorted from highest score to lowest score.",
        "explanation": "Sorting helps inspect data and find highest or lowest values.",
        "syntax": "ORDER BY column_name DESC;",
        "ml": "Useful for checking top values, ranking observations and inspecting model-related data.",
    },
    "LIMIT": {
        "concept": "LIMIT controls how many rows PostgreSQL returns.",
        "points": [
            "Useful for previews.",
            "Reduces output size.",
            "Often used while exploring a table.",
        ],
        "example": "SELECT *\nFROM students\nLIMIT 5;",
        "output": "First 5 rows",
        "explanation": "LIMIT is useful when a table contains many records and you only want a quick preview.",
        "syntax": "SELECT *\nFROM table_name\nLIMIT number;",
        "ml": "Use LIMIT to inspect a dataset before building a data-processing pipeline.",
    },
    "INSERT": {
        "concept": "INSERT adds new rows to a table.",
        "points": [
            "Adds records.",
            "Specify columns when possible.",
            "VALUES contains the new data.",
        ],
        "example": "INSERT INTO students (name, score)\nVALUES ('Priyanka', 90);",
        "output": "1 row inserted.",
        "explanation": "INSERT is used when new records need to be stored in a database.",
        "syntax": "INSERT INTO table_name (column1, column2)\nVALUES (value1, value2);",
        "ml": "Applications can store new observations, predictions or user activity for later analysis.",
    },
    "UPDATE": {
        "concept": "UPDATE changes existing rows.",
        "points": [
            "SET changes a column.",
            "WHERE selects the rows to change.",
            "Always check the WHERE condition.",
        ],
        "example": "UPDATE students\nSET score = 95\nWHERE name = 'Priyanka';",
        "output": "1 row updated.",
        "explanation": "UPDATE changes stored values without creating a new row.",
        "syntax": "UPDATE table_name\nSET column = value\nWHERE condition;",
        "ml": "Useful when correcting or updating source data before feature preparation.",
    },
    "DELETE": {
        "concept": "DELETE removes rows from a table.",
        "points": [
            "WHERE selects rows to remove.",
            "Without WHERE, many rows can be deleted.",
            "Use carefully.",
        ],
        "example": "DELETE FROM students\nWHERE score < 30;",
        "output": "Matching rows deleted.",
        "explanation": "DELETE permanently removes matching rows when the transaction is committed.",
        "syntax": "DELETE FROM table_name\nWHERE condition;",
        "ml": "Can be used to remove invalid records during controlled data-cleaning workflows.",
    },
    "Aggregate Functions": {
        "concept": "Aggregate functions calculate a result from multiple rows.",
        "points": [
            "COUNT → number of rows.",
            "SUM → total.",
            "AVG → average.",
            "MIN / MAX → smallest / largest.",
        ],
        "example": "SELECT\n    COUNT(*) AS total_students,\n    AVG(score) AS average_score,\n    MAX(score) AS highest_score\nFROM students;",
        "output": "Summary statistics for the table.",
        "explanation": "Aggregate functions turn many records into useful summary values.",
        "syntax": "SELECT COUNT(*), AVG(column)\nFROM table_name;",
        "ml": "Summary statistics help understand datasets and validate feature distributions.",
    },
    "GROUP BY": {
        "concept": "GROUP BY creates groups so aggregate functions can be calculated for each group.",
        "points": [
            "Groups similar values.",
            "Usually used with COUNT, SUM or AVG.",
            "Produces one result per group.",
        ],
        "example": "SELECT department, AVG(score) AS avg_score\nFROM students\nGROUP BY department;",
        "output": "Average score for each department.",
        "explanation": "GROUP BY is useful when you want statistics separately for categories.",
        "syntax": "SELECT category, AVG(value)\nFROM table_name\nGROUP BY category;",
        "ml": "Useful for exploring category-level patterns before feature engineering.",
    },
    "HAVING": {
        "concept": "HAVING filters groups after GROUP BY.",
        "points": [
            "WHERE filters rows.",
            "HAVING filters groups.",
            "Often used with aggregate functions.",
        ],
        "example": "SELECT department, AVG(score) AS avg_score\nFROM students\nGROUP BY department\nHAVING AVG(score) >= 70;",
        "output": "Only groups with average score >= 70.",
        "explanation": "HAVING applies conditions to grouped results.",
        "syntax": "GROUP BY category\nHAVING aggregate_condition;",
        "ml": "Useful when selecting categories or groups based on calculated statistics.",
    },
    "JOIN": {
        "concept": "JOIN combines related data from multiple tables.",
        "points": [
            "INNER JOIN → matching rows.",
            "LEFT JOIN → keeps all rows from the left table.",
            "JOIN uses related columns.",
        ],
        "example": "SELECT s.name, c.course_name\nFROM students s\nJOIN courses c\n  ON s.course_id = c.id;",
        "output": "Student names with their course names.",
        "explanation": "Real datasets are often split across several related tables, so JOIN is essential.",
        "syntax": "SELECT ...\nFROM table_a a\nJOIN table_b b\nON a.id = b.a_id;",
        "ml": "JOIN is commonly used to build a complete training dataset from multiple database tables.",
    },
    "Subqueries": {
        "concept": "A subquery is a query inside another query.",
        "points": [
            "Can return a value.",
            "Can return multiple rows.",
            "Useful for comparing against calculated results.",
        ],
        "example": "SELECT name, score\nFROM students\nWHERE score > (\n    SELECT AVG(score)\n    FROM students\n);",
        "output": "Students scoring above the average.",
        "explanation": "A subquery lets one query use the result of another query.",
        "syntax": "SELECT *\nFROM table_name\nWHERE column > (SELECT ...);",
        "ml": "Useful for selecting records based on dataset-level statistics.",
    },
    "CASE": {
        "concept": "CASE creates conditional values inside a SQL query.",
        "points": [
            "Works like if / elif / else.",
            "Creates derived columns.",
            "Useful for categories.",
        ],
        "example": "SELECT name, score,\nCASE\n    WHEN score >= 80 THEN 'High'\n    WHEN score >= 50 THEN 'Medium'\n    ELSE 'Low'\nEND AS level\nFROM students;",
        "output": "Each student receives a High, Medium or Low label.",
        "explanation": "CASE lets you create useful categories from existing values.",
        "syntax": "CASE\n    WHEN condition THEN value\n    ELSE value\nEND",
        "ml": "Useful for feature engineering and creating simple categorical features.",
    },
    "NULL Handling": {
        "concept": "NULL represents a missing or unknown value.",
        "points": [
            "NULL is not zero.",
            "Use IS NULL / IS NOT NULL.",
            "COALESCE can provide a replacement value.",
        ],
        "example": "SELECT name,\n       COALESCE(score, 0) AS score\nFROM students;",
        "output": "Missing scores are displayed as 0.",
        "explanation": "Handling missing values is an important part of preparing data.",
        "syntax": "COALESCE(column, replacement)",
        "ml": "Missing-value handling is an important step before training many ML models.",
    },
    "Date & Time": {
        "concept": "PostgreSQL provides DATE and TIMESTAMP types and functions for time-based data.",
        "points": [
            "DATE → date only.",
            "TIMESTAMP → date + time.",
            "Useful for extracting year, month and day.",
        ],
        "example": "SELECT CURRENT_DATE AS today,\n       CURRENT_TIMESTAMP AS current_time;",
        "output": "Current date and timestamp.",
        "explanation": "Time information can be converted into useful features.",
        "syntax": "SELECT DATE_COLUMN,\n       EXTRACT(YEAR FROM DATE_COLUMN)\nFROM table_name;",
        "ml": "Date features such as year, month, weekday and elapsed time can improve ML datasets.",
    },
    "String Functions": {
        "concept": "String functions clean and transform text values.",
        "points": [
            "LOWER / UPPER → change case.",
            "TRIM → remove extra spaces.",
            "LENGTH → count characters.",
            "CONCAT → combine text.",
        ],
        "example": "SELECT\n    LOWER('Machine Learning') AS lower_text,\n    LENGTH('Python') AS text_length;",
        "output": "machine learning | 6",
        "explanation": "String functions are useful when raw text data is inconsistent.",
        "syntax": "SELECT LOWER(column_name)\nFROM table_name;",
        "ml": "Text cleaning is often required before using categorical or text-derived features.",
    },
    "CTE": {
        "concept": "A Common Table Expression (CTE) creates a temporary named result for a query.",
        "points": [
            "Starts with WITH.",
            "Makes complex queries easier to read.",
            "Can be reused by the main query.",
        ],
        "example": "WITH high_scores AS (\n    SELECT *\n    FROM students\n    WHERE score >= 80\n)\nSELECT *\nFROM high_scores;",
        "output": "Students with score >= 80.",
        "explanation": "CTEs break complex data preparation into clear steps.",
        "syntax": "WITH name AS (\n    SELECT ...\n)\nSELECT * FROM name;",
        "ml": "CTEs are useful for readable multi-step feature engineering queries.",
    },
    "Window Functions": {
        "concept": "Window functions calculate values across related rows without collapsing them.",
        "points": [
            "ROW_NUMBER → row ranking.",
            "RANK → ranking with ties.",
            "SUM / AVG OVER → calculations across a window.",
        ],
        "example": "SELECT name, score,\n       RANK() OVER (ORDER BY score DESC) AS rank\nFROM students;",
        "output": "Each student keeps their row and receives a rank.",
        "explanation": "Window functions are powerful for ranking, comparisons and time-based analysis.",
        "syntax": "FUNCTION() OVER (\n    PARTITION BY column\n    ORDER BY column\n)",
        "ml": "Useful for creating ranking, rolling and group-relative features.",
    },
    "Data Cleaning": {
        "concept": "SQL can clean, filter and transform raw database data before analysis.",
        "points": [
            "Handle NULL values.",
            "Remove duplicates.",
            "Fix inconsistent text.",
            "Filter invalid records.",
        ],
        "example": "SELECT DISTINCT\n    TRIM(LOWER(name)) AS clean_name\nFROM students\nWHERE name IS NOT NULL;",
        "output": "Cleaned unique names.",
        "explanation": "Cleaning creates a more reliable dataset for analysis and model training.",
        "syntax": "SELECT DISTINCT ...\nFROM table_name\nWHERE column IS NOT NULL;",
        "ml": "Clean input data generally leads to more reliable ML features and evaluation.",
    },
    "Preparing Data for ML": {
        "concept": "SQL can create a final feature table that Python or an ML pipeline can load.",
        "points": [
            "Select useful features.",
            "Join related data.",
            "Handle missing values.",
            "Create derived features.",
        ],
        "example": "SELECT\n    age,\n    income,\n    COALESCE(score, 0) AS score,\n    CASE\n        WHEN score >= 70 THEN 1\n        ELSE 0\n    END AS target\nFROM students;",
        "output": "A model-ready feature and target dataset.",
        "explanation": "The final SQL query can become the data source for a Python ML pipeline.",
        "syntax": "SELECT feature_1,\n       feature_2,\n       derived_feature\nFROM cleaned_data;",
        "ml": "This is the bridge from PostgreSQL data to pandas, preprocessing and machine-learning models.",
    },
}


# =========================================================
# COURSE ORDER / LOOKUPS
# =========================================================

LESSON_ORDER = []
PARENT_LOOKUP = {}
LEVEL_LOOKUP = {}

for level, parents in COURSE.items():
    for parent, topics in parents.items():
        for topic in topics:
            LESSON_ORDER.append(topic)
            PARENT_LOOKUP[topic] = parent
            LEVEL_LOOKUP[topic] = level


def lesson_for(topic):
    return LESSONS.get(topic, LESSONS["Introduction"])


# =========================================================
# SESSION STATE
# =========================================================

if "current_pg" not in st.session_state:
    st.session_state.current_pg = LESSON_ORDER[0]

if "expanded_pg" not in st.session_state:
    st.session_state.expanded_pg = {
        "PostgreSQL Basics": True,
        "Data Analysis": False,
        "PostgreSQL for ML": False,
    }

if "sql_query" not in st.session_state:
    st.session_state.sql_query = LESSONS["Introduction"]["example"]

if "sql_result" not in st.session_state:
    st.session_state.sql_result = None

if "sql_message" not in st.session_state:
    st.session_state.sql_message = ""


def goto(topic):
    st.session_state.current_pg = topic
    st.session_state.sql_query = LESSONS[topic]["example"]
    st.session_state.sql_result = None
    st.session_state.sql_message = ""
    
    
def clear_sql_editor():
    editor_key = f"sql_editor_{st.session_state.current_pg}"

    st.session_state[editor_key] = ""
    st.session_state.sql_query = ""
    st.session_state.sql_result = None
    st.session_state.sql_message = ""    


def safe_html(value):
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


# =========================================================
# DATABASE
# =========================================================

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


def run_sql(query):
    """
    Practice execution is transactional and rolled back automatically.
    This keeps the learning database safe from permanent changes.
    """

    connection = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        started = time.perf_counter()

        cursor.execute(query)

        execution_time = time.perf_counter() - started

        if cursor.description:

            columns = [
                item[0]
                for item in cursor.description
            ]

            rows = cursor.fetchall()

            result = pd.DataFrame(
                rows,
                columns=columns,
            )

            message = (
                f"Query successful • {len(result)} row(s) • "
                f"{execution_time:.3f}s"
            )

        else:

            result = pd.DataFrame(
                [
                    {
                        "status":
                        f"{cursor.rowcount} row(s) affected"
                    }
                ]
            )

            message = (
                f"Query successful • "
                f"{cursor.rowcount} row(s) affected • "
                f"{execution_time:.3f}s"
            )

        connection.rollback()
        cursor.close()

        return result, message, None

    except Exception as error:

        if connection:

            connection.rollback()

        return None, "", str(error)

    finally:

        if connection:

            connection.close()


# =========================================================
# DATABASE HELPERS FOR USER
# =========================================================

def get_user_id():
    """
    Get the current CodePractice user ID.
    """

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id
            FROM users
            WHERE email = %s
            LIMIT 1;
            """,
            (
                "priyanka@codepractice.local",
            ),
        )

        row = cursor.fetchone()

        if row:

            return row[0]

        return None

    except Exception:

        return None

    finally:

        if cursor:

            cursor.close()

        if connection:

            connection.close()


def get_postgres_lesson_id(topic):
    """
    Get the database lesson ID for the
    current PostgreSQL topic.
    """

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id
            FROM lessons
            WHERE subject = %s
              AND title = %s
            LIMIT 1;
            """,
            (
                "PostgreSQL",
                topic,
            ),
        )

        row = cursor.fetchone()

        if row:

            return row[0]

        return None

    except Exception:

        return None

    finally:

        if cursor:

            cursor.close()

        if connection:

            connection.close()
            
            
def get_postgres_lesson_id(topic):

    connection = None
    cursor = None

    try:
        ...
        
    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()            
            
def get_query_challenge(topic):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                q.task,
                q.hint,
                q.expected_query,
                q.points
            FROM query_challenges q
            INNER JOIN lessons l
                ON q.lesson_id = l.id
            WHERE l.subject = 'PostgreSQL'
              AND l.title = %s
            LIMIT 1;
            """,
            (topic,),
        )

        row = cursor.fetchone()

        if not row:
            return None

        return {
            "task": row[0],
            "hint": row[1],
            "expected_query": row[2],
            "points": row[3],
        }

    except Exception:
        return None

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()     
            
def normalize_sql(query):
    """
    Normalize SQL so small formatting differences
    do not affect answer checking.
    """
    if not query:
        return ""

    return " ".join(
        query.strip().lower().split()
    )                   
    
def save_lesson_progress(topic, completed=False):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        user_id = get_user_id()
        lesson_id = get_postgres_lesson_id(topic)

        if not user_id or not lesson_id:
            return False

        cursor.execute(
            """
            SELECT id
            FROM progress
            WHERE user_id = %s
              AND lesson_id = %s
            LIMIT 1;
            """,
            (
                user_id,
                lesson_id,
            ),
        )

        existing = cursor.fetchone()

        if existing:

            cursor.execute(
                """
                UPDATE progress
                SET completed = %s
                WHERE user_id = %s
                  AND lesson_id = %s;
                """,
                (
                    completed,
                    user_id,
                    lesson_id,
                ),
            )

        else:

            cursor.execute(
                """
                INSERT INTO progress (
                    user_id,
                    lesson_id,
                    completed
                )
                VALUES (
                    %s,
                    %s,
                    %s
                );
                """,
                (
                    user_id,
                    lesson_id,
                    completed,
                ),
            )

        connection.commit()

        return True

    except Exception as error:

        if connection:
            connection.rollback()

        return False

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()    
            
# ============================================================
# SAVE POSTGRESQL TRY YOURSELF PROGRESS
# ============================================================

def save_lesson_progress(topic, completed=False):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        # ----------------------------------------------------
        # GET CURRENT USER
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT id
            FROM users
            WHERE email = %s
            LIMIT 1;
            """,
            (CURRENT_USER_EMAIL,),
        )

        user_row = cursor.fetchone()

        if not user_row:
            return False

        user_id = user_row[0]

        # ----------------------------------------------------
        # GET POSTGRESQL LESSON
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT id
            FROM lessons
            WHERE subject = 'PostgreSQL'
              AND title = %s
            LIMIT 1;
            """,
            (topic,),
        )

        lesson_row = cursor.fetchone()

        if not lesson_row:
            return False

        lesson_id = lesson_row[0]

        # ----------------------------------------------------
        # CHECK EXISTING PROGRESS
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT id
            FROM progress
            WHERE user_id = %s
              AND lesson_id = %s
            LIMIT 1;
            """,
            (
                user_id,
                lesson_id,
            ),
        )

        progress_row = cursor.fetchone()

        # ----------------------------------------------------
        # UPDATE EXISTING PROGRESS
        # ----------------------------------------------------

        if progress_row:

            cursor.execute(
                """
                UPDATE progress
                SET
                    completed = %s,
                    attempts = attempts + 1,
                    last_attempted = CURRENT_TIMESTAMP
                WHERE id = %s;
                """,
                (
                    completed,
                    progress_row[0],
                ),
            )

        # ----------------------------------------------------
        # CREATE NEW PROGRESS
        # ----------------------------------------------------

        else:

            cursor.execute(
                """
                INSERT INTO progress
                    (
                        user_id,
                        lesson_id,
                        completed,
                        attempts,
                        last_attempted
                    )
                VALUES
                    (
                        %s,
                        %s,
                        %s,
                        1,
                        CURRENT_TIMESTAMP
                    );
                """,
                (
                    user_id,
                    lesson_id,
                    completed,
                ),
            )

        connection.commit()

        return True

    except Exception as error:

        if connection:
            connection.rollback()

        st.error(
            f"Unable to save PostgreSQL progress: {error}"
        )

        return False

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()            


# =========================================================
# BOOKMARK HELPERS
# =========================================================

def is_bookmarked(topic):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        user_id = get_user_id()
        lesson_id = get_postgres_lesson_id(topic)

        if not user_id or not lesson_id:
            return False

        cursor.execute(
            """
            SELECT id
            FROM bookmarks
            WHERE user_id = %s
              AND lesson_id = %s
            LIMIT 1;
            """,
            (
                user_id,
                lesson_id,
            ),
        )

        return cursor.fetchone() is not None

    except Exception:

        return False

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


def save_bookmark(topic):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        user_id = get_user_id()
        lesson_id = get_postgres_lesson_id(topic)

        if not user_id or not lesson_id:
            return False

        cursor.execute(
            """
            SELECT id
            FROM bookmarks
            WHERE user_id = %s
              AND lesson_id = %s
            LIMIT 1;
            """,
            (
                user_id,
                lesson_id,
            ),
        )

        if cursor.fetchone():

            return True

        cursor.execute(
            """
            INSERT INTO bookmarks (
                user_id,
                lesson_id,
                topic_name
            )
            VALUES (
                %s,
                %s,
                %s
            );
            """,
            (
                user_id,
                lesson_id,
                topic,
            ),
        )

        connection.commit()

        return True

    except Exception:

        if connection:
            connection.rollback()

        return False

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


def remove_bookmark(topic):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        user_id = get_user_id()
        lesson_id = get_postgres_lesson_id(topic)

        if not user_id or not lesson_id:
            return False

        cursor.execute(
            """
            DELETE FROM bookmarks
            WHERE user_id = %s
              AND lesson_id = %s;
            """,
            (
                user_id,
                lesson_id,
            ),
        )

        connection.commit()

        return True

    except Exception:

        if connection:
            connection.rollback()

        return False

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# =========================================================
# NOTES HELPERS
# =========================================================

def load_note(topic):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        user_id = get_user_id()
        lesson_id = get_postgres_lesson_id(topic)

        if not user_id or not lesson_id:
            return ""

        cursor.execute(
            """
            SELECT note_text
            FROM lesson_notes
            WHERE user_id = %s
              AND lesson_id = %s
            ORDER BY id DESC
            LIMIT 1;
            """,
            (
                user_id,
                lesson_id,
            ),
        )

        row = cursor.fetchone()

        if row:
            return row[0] or ""

        return ""

    except Exception:

        return ""

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


def save_note(topic, notes):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        user_id = get_user_id()
        lesson_id = get_postgres_lesson_id(topic)

        if not user_id or not lesson_id:
            return False

        cursor.execute(
            """
            SELECT id
            FROM lesson_notes
            WHERE user_id = %s
              AND lesson_id = %s
            ORDER BY id DESC
            LIMIT 1;
            """,
            (
                user_id,
                lesson_id,
            ),
        )

        row = cursor.fetchone()

        if row:

            cursor.execute(
                """
                UPDATE lesson_notes
                SET
                    note_text = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s;
                """,
                (
                    notes,
                    row[0],
                ),
            )

        else:

            cursor.execute(
                """
                INSERT INTO lesson_notes (
                    user_id,
                    lesson_id,
                    note_text
                )
                VALUES (
                    %s,
                    %s,
                    %s
                );
                """,
                (
                    user_id,
                    lesson_id,
                    notes,
                ),
            )

        connection.commit()

        return True

    except Exception:

        if connection:
            connection.rollback()

        return False

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()

# =========================================================
# SAVE TRY YOURSELF PRACTICE
# =========================================================

def save_sql_practice(
    topic,
    query_text,
    success=False,
):
    """
    Save every Try Yourself SQL query
    in PostgreSQL.
    """

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        user_id = get_user_id()

        lesson_id = get_postgres_lesson_id(
            topic
        )

        if not user_id or not lesson_id:

            return False

        cursor.execute(
            """
            INSERT INTO sql_practice_history (
                user_id,
                lesson_id,
                topic_name,
                query_text,
                success
            )
            VALUES (
                %s,
                %s,
                %s,
                %s,
                %s
            );
            """,
            (
                user_id,
                lesson_id,
                topic,
                query_text,
                success,
            ),
        )

        connection.commit()

        return True

    except Exception:

        if connection:

            connection.rollback()

        return False

    finally:

        if cursor:

            cursor.close()

        if connection:

            connection.close()


# =========================================================
# SAVE QUERY CHALLENGE ATTEMPTS
# =========================================================

def save_challenge_attempt(
    topic,
    query_text,
    success=False,
):
    """
    Save Query Challenge attempts
    in PostgreSQL.
    """

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        user_id = get_user_id()

        lesson_id = get_postgres_lesson_id(
            topic
        )

        if not user_id or not lesson_id:

            return False

        cursor.execute(
            """
            INSERT INTO query_challenge_attempts (
                user_id,
                lesson_id,
                topic_name,
                query_text,
                success
            )
            VALUES (
                %s,
                %s,
                %s,
                %s,
                %s
            );
            """,
            (
                user_id,
                lesson_id,
                topic,
                query_text,
                success,
            ),
        )

        connection.commit()

        return True

    except Exception:

        if connection:

            connection.rollback()

        return False

    finally:

        if cursor:

            cursor.close()

        if connection:

            connection.close()


# =========================================================
# CREATE PRACTICE HISTORY TABLE
# =========================================================

def ensure_practice_history_table():

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sql_practice_history (

                id SERIAL PRIMARY KEY,

                user_id INTEGER NOT NULL,

                lesson_id INTEGER NOT NULL,

                topic_name VARCHAR(255) NOT NULL,

                query_text TEXT NOT NULL,

                success BOOLEAN DEFAULT FALSE,

                created_at TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (user_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE,

                FOREIGN KEY (lesson_id)
                    REFERENCES lessons(id)
                    ON DELETE CASCADE
            );
            """
        )

        connection.commit()

    except Exception:

        if connection:

            connection.rollback()

    finally:

        if cursor:

            cursor.close()

        if connection:

            connection.close()


# =========================================================
# CREATE QUERY CHALLENGES TABLE
# =========================================================

def ensure_query_challenges_table():

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS query_challenges (

                id SERIAL PRIMARY KEY,

                lesson_id INTEGER NOT NULL,

                topic_name VARCHAR(255) NOT NULL,

                challenge_task TEXT NOT NULL,

                challenge_hint TEXT,

                expected_query TEXT NOT NULL,

                points INTEGER DEFAULT 10,

                created_at TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (lesson_id)
                    REFERENCES lessons(id)
                    ON DELETE CASCADE
            );
            """
        )

        connection.commit()

    except Exception as error:

        if connection:

            connection.rollback()

        print(
            f"Query challenge table error: {error}"
        )

    finally:

        if cursor:

            cursor.close()

        if connection:

            connection.close()


# =========================================================
# GET QUERY CHALLENGE FROM DATABASE
# =========================================================

def get_query_challenge(topic):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                challenge_task,
                challenge_hint,
                expected_query,
                points
            FROM query_challenges
            WHERE topic_name = %s
            LIMIT 1;
            """,
            (
                topic,
            ),
        )

        row = cursor.fetchone()

        if not row:

            return None

        return {
            "task": row[0],
            "hint": row[1],
            "expected_query": row[2],
            "points": row[3],
        }

    except Exception as error:

        print(
            f"Challenge load error: {error}"
        )

        return None

    finally:

        if cursor:

            cursor.close()

        if connection:

            connection.close()


# =========================================================
# SAVE / UPDATE QUERY CHALLENGE
# =========================================================

def save_query_challenge(
    topic,
    challenge_task,
    challenge_hint,
    expected_query,
    points=10,
):
    """
    Save one PostgreSQL Query Challenge
    in the database.
    """

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        lesson_id = get_postgres_lesson_id(
            topic
        )

        if not lesson_id:

            return False

        cursor.execute(
            """
            SELECT id
            FROM query_challenges
            WHERE lesson_id = %s
            LIMIT 1;
            """,
            (
                lesson_id,
            ),
        )

        existing = cursor.fetchone()

        if existing:

            cursor.execute(
                """
                UPDATE query_challenges
                SET
                    topic_name = %s,
                    challenge_task = %s,
                    challenge_hint = %s,
                    expected_query = %s,
                    points = %s
                WHERE lesson_id = %s;
                """,
                (
                    topic,
                    challenge_task,
                    challenge_hint,
                    expected_query,
                    points,
                    lesson_id,
                ),
            )

        else:

            cursor.execute(
                """
                INSERT INTO query_challenges (
                    lesson_id,
                    topic_name,
                    challenge_task,
                    challenge_hint,
                    expected_query,
                    points
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                );
                """,
                (
                    lesson_id,
                    topic,
                    challenge_task,
                    challenge_hint,
                    expected_query,
                    points,
                ),
            )

        connection.commit()

        return True

    except Exception as error:

        if connection:

            connection.rollback()

        print(
            f"Challenge save error: {error}"
        )

        return False

    finally:

        if cursor:

            cursor.close()

        if connection:

            connection.close()


# =========================================================
# CREATE DATABASE TABLES
# =========================================================

ensure_practice_history_table()

ensure_query_challenges_table()

# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(circle at 75% -10%, rgba(37,99,235,.08), transparent 30%),
            #07101b;
        color:#f5f8fc;
    }

    .block-container {
        max-width:1480px;
        padding:.55rem .8rem 2rem;
    }

    section[data-testid="stSidebar"] {
        background:#07111e;
        border-right:1px solid #20324a;
    }

    section[data-testid="stSidebar"] .block-container {
        padding:.55rem .5rem 1rem;
    }

    .brand {
        padding:5px 8px 11px;
    }

    .brand-row {
        display:flex;
        align-items:center;
        gap:9px;
    }

    .brand-logo {
        width:31px;
        height:31px;
        border-radius:7px;
        display:flex;
        align-items:center;
        justify-content:center;
        background:#13243a;
        color:#60a5fa;
        font-weight:900;
        font-size:12px;
    }

    .brand-title {
        color:#f8fafc;
        font-size:18px;
        font-weight:800;
    }

    .brand-sub {
        color:#8295ad;
        font-size:10px;
        margin-left:40px;
        margin-top:-2px;
    }

    section[data-testid="stSidebar"] hr {
        border-color:#1c2d43;
        margin:7px 4px 9px;
    }

    section[data-testid="stSidebar"] button {
        min-height:31px !important;
        height:31px !important;
        padding:3px 8px !important;
        margin:1px 0 !important;
        border-radius:5px !important;
        border:1px solid transparent !important;
        background:transparent !important;
        color:#b9c8d9 !important;
        font-size:13px !important;
        font-weight:500 !important;
        text-align:left !important;
    }

    section[data-testid="stSidebar"] button:hover {
        background:#102137 !important;
        border-color:#1d3552 !important;
        color:#ffffff !important;
    }

    .level-title {
        color:#8ea3bc;
        font-size:11px;
        font-weight:800;
        margin:10px 7px 4px;
    }

    .sidebar-line {
        height:1px;
        background:#17283d;
        margin:7px 5px;
    }

    .top-search {
        height:35px;
        display:flex;
        align-items:center;
        padding:0 12px;
        border:1px solid #203650;
        border-radius:6px;
        background:#0c1929;
        color:#7f93ab;
        font-size:11px;
    }

    .top-icon {
        height:35px;
        display:flex;
        align-items:center;
        justify-content:center;
        border:1px solid #203650;
        border-radius:6px;
        background:#0c1929;
        color:#dbe7f3;
    }

    .user-chip {
        height:35px;
        display:flex;
        align-items:center;
        gap:7px;
        padding:0 8px;
        border:1px solid #203650;
        border-radius:6px;
        background:#0c1929;
    }

    .avatar {
        width:24px;
        height:24px;
        border-radius:50%;
        display:flex;
        align-items:center;
        justify-content:center;
        background:#2563eb;
        color:white;
        font-size:11px;
        font-weight:800;
    }

    .user-name {
        font-size:10px;
        font-weight:750;
        color:#eef5fc;
    }

    .user-sub {
        font-size:8px;
        color:#7d91aa;
    }

    .breadcrumb {
        color:#8ea3ba;
        font-size:11px;
        margin:4px 0 9px;
    }

    .course-title {
        color:#f8fafc;
        font-size:27px;
        line-height:1.15;
        font-weight:800;
        margin:0;
    }

    .course-desc {
        color:#91a5bb;
        font-size:12px;
        line-height:1.5;
        margin-top:5px;
    }

    .section-title {
        color:#f5f8fc;
        font-size:16px;
        font-weight:800;
        margin-bottom:5px;
    }

    .card {
        background:linear-gradient(145deg,#0b1726,#091421);
        border:1px solid #203650;
        border-radius:7px;
        padding:11px 13px;
        margin-bottom:9px;
    }

    .card-title {
        color:#f2f7fc;
        font-size:14px;
        font-weight:800;
        margin-bottom:5px;
    }

    .card-text {
        color:#c6d4e3;
        font-size:12px;
        line-height:1.6;
        white-space:pre-line;
    }

    .topic-box {
        background:#0a1625;
        border:1px solid #203650;
        border-radius:7px;
        padding:10px 12px;
        margin-bottom:9px;
    }

    .topic-row {
        background:#091421;
        border:1px solid #1b3049;
        border-radius:5px;
        padding:6px 8px;
        color:#c8d8e9;
        font-size:11px;
        margin:4px 0;
    }

    .ml-box {
        background:linear-gradient(145deg,#0b211b,#091914);
        border:1px solid #20513f;
        border-left:3px solid #18c48f;
        border-radius:7px;
        padding:10px 12px;
        margin-top:9px;
    }

    .ml-title {
        color:#79efc0;
        font-size:14px;
        font-weight:800;
        margin-bottom:5px;
    }

    .editor-title {
        color:#f3f7fb;
        font-size:14px;
        font-weight:800;
    }

    .editor-sub {
        color:#8296ad;
        font-size:10px;
        margin-top:2px;
    }

    .output-head {
        display:flex;
        justify-content:space-between;
        align-items:center;
        color:#f3f7fb;
        font-size:13px;
        font-weight:800;
    }

    .success {
        color:#38df9d;
        font-size:9px;
    }

    textarea {
        font-size:12px !important;
        line-height:1.5 !important;
        font-family:Consolas,"Courier New",monospace !important;
    }

    div[data-testid="stCode"] {
        border:1px solid #203650;
        border-radius:6px;
    }

    div[data-testid="stCode"] pre {
        font-size:11px !important;
        line-height:1.5 !important;
    }

    .stButton button {
        min-height:35px;
        border-radius:5px;
        border:1px solid #263c59;
        background:#0d1928;
        color:#e5edf7;
        font-size:11px;
        font-weight:700;
    }

    .stButton button:hover {
        background:#14253b;
        border-color:#2e78dc;
        color:white;
    }

    div[data-testid="stProgress"] {
        margin:4px 0 9px;
    }

    #MainMenu,
    footer {
        visibility:hidden;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# TOP BAR
# =========================================================

search_col, bell_col, user_col = st.columns(
    [7.5, .5, 1.8],
    gap="small",
)

with search_col:
    st.markdown(
        """
        <div class="top-search">
            🔍 &nbsp; Search PostgreSQL topics (e.g. SELECT, JOIN, GROUP BY...)
        </div>
        """,
        unsafe_allow_html=True,
    )

with bell_col:
    st.markdown(
        '<div class="top-icon">♧</div>',
        unsafe_allow_html=True,
    )

with user_col:
    st.markdown(
        """
        <div class="user-chip">
            <div class="avatar">P</div>
            <div>
                <div class="user-name">Priyanka</div>
                <div class="user-sub">Keep Learning ✨</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# SIDEBAR
# =========================================================

current = st.session_state.current_pg

with st.sidebar:

    st.markdown(
        """
        <div class="brand">
            <div class="brand-row">
                <div class="brand-logo">&lt;/&gt;</div>
                <div class="brand-title">CodePractice</div>
            </div>
            <div class="brand-sub">Learn. Practice. Grow.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Dashboard button
    if st.button(
        "←  Dashboard",
        key="pg_dashboard_back",
        use_container_width=True,
    ):

        if "dashboard_page" in st.session_state:

            st.switch_page(
                st.session_state["dashboard_page"]
            )

    st.markdown("---")

    st.markdown(
        """
        <div style="
            color:#f2f7fc;
            font-size:15px;
            font-weight:800;
            padding:2px 7px 5px;
        ">
            🐘 PostgreSQL
        </div>
        """,
        unsafe_allow_html=True,
    )

    for level, parents in COURSE.items():

        st.markdown(
            f'<div class="level-title">{safe_html(level)}</div>',
            unsafe_allow_html=True,
        )

        for parent, children in parents.items():

            expanded = st.session_state.expanded_pg.get(parent, False)

            if st.button(
                ("▼ " if expanded else "› ") + parent,
                key=f"pg_expand_{parent}",
                use_container_width=True,
            ):
                st.session_state.expanded_pg[parent] = not expanded
                st.rerun()

            if expanded:

                for child in children:

                    active = current == child

                    if st.button(
                        ("● " if active else "  ") + child,
                        key=f"pg_child_{parent}_{child}",
                        use_container_width=True,
                    ):
                        goto(child)
                        st.rerun()

        st.markdown(
            '<div class="sidebar-line"></div>',
            unsafe_allow_html=True,
        )

# =========================================================
# CURRENT LESSON
# =========================================================

lesson = lesson_for(current)
index = LESSON_ORDER.index(current)
total = len(LESSON_ORDER)
progress = (index + 1) / total

parent = PARENT_LOOKUP[current]
level = LEVEL_LOOKUP[current]

st.markdown(
    f"""
    <div class="breadcrumb">
        🏠 &nbsp; PostgreSQL
        &nbsp;›&nbsp; {safe_html(parent)}
        &nbsp;›&nbsp; {safe_html(current)}
    </div>
    """,
    unsafe_allow_html=True,
)

st.progress(
    progress,
    text=f"Course Progress • {index + 1} / {total} lessons",
)


# =========================================================
# NAVIGATION
# =========================================================

previous_topic = LESSON_ORDER[index - 1] if index > 0 else None
next_topic = LESSON_ORDER[index + 1] if index < total - 1 else None


# =========================================================
# MAIN COLUMNS
# =========================================================

lesson_col, editor_col = st.columns(
    [1.55, 1],
    gap="small",
)


# =========================================================
# LESSON CONTENT
# =========================================================

with lesson_col:

    left_nav, title_col, right_nav = st.columns(
        [1, 2.8, 1],
        gap="small",
    )

    with left_nav:
        if previous_topic:
            if st.button(
                "‹ Previous",
                use_container_width=True,
            ):
                goto(previous_topic)
                st.rerun()

    with title_col:
        st.markdown(
            f"""
            <div class="course-title">
                {safe_html(current)}
            </div>
            <div class="course-desc">
                {safe_html(lesson["concept"])}
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right_nav:
        if next_topic:
            if st.button(
                "Next ›",
                use_container_width=True,
            ):
                goto(next_topic)
                st.rerun()

    st.markdown(
        '<div class="section-title" style="margin-top:13px;">Example</div>',
        unsafe_allow_html=True,
    )

    st.code(
        lesson["example"],
        language="sql",
    )

    st.markdown(
        f"""
        <div class="topic-box">
            <div style="
                color:#8196ae;
                font-size:10px;
                font-weight:800;
                margin-bottom:5px;
            ">
                OUTPUT
            </div>
            <div style="
                color:#d6e3ef;
                font-family:Consolas,monospace;
                font-size:11px;
                white-space:pre-line;
            ">
                {safe_html(lesson["output"])}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="card">
            <div class="card-title">📖 Main Concept</div>
            <div class="card-text">
                {safe_html(lesson["concept"])}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="topic-box">
            <div class="card-title">🧩 {safe_html(parent)}</div>
            {"".join(
                f'<div class="topic-row">• {safe_html(item)}</div>'
                for item in COURSE[level][parent]
            )}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="card">
            <div class="card-title">💡 Simple Explanation</div>
            <div class="card-text">
                {safe_html(lesson["explanation"])}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-title">💻 Syntax</div>',
        unsafe_allow_html=True,
    )

    st.code(
        lesson["syntax"],
        language="sql",
    )

    points_html = "".join(
        f"<div class='topic-row'>• {safe_html(point)}</div>"
        for point in lesson["points"]
    )

    st.markdown(
        f"""
        <div class="topic-box">
            <div class="card-title">📌 Important Points</div>
            {points_html}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="ml-box">
            <div class="ml-title">🤖 Use in Data Science & Machine Learning</div>
            <div class="card-text">
                {safe_html(lesson["ml"])}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if next_topic:

        st.markdown(
            f"""
            <div class="card" style="margin-top:10px;">
                <div style="
                    color:#7f93aa;
                    font-size:9px;
                    text-transform:uppercase;
                ">
                    Next Topic
                </div>
                <div style="
                    color:#f4f8fc;
                    font-size:13px;
                    font-weight:800;
                    margin-top:3px;
                ">
                    🚀 {safe_html(next_topic)}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# =========================================================
# SQL WORKSPACE
# =========================================================

with editor_col:

    tab_try, tab_challenge, tab_notes, tab_bookmark = st.tabs(
        [
            "▶ Try Yourself",
            "🏆 Query Challenge",
            "📝 Notes",
            "🔖 Bookmark",
        ]
    )

    # =====================================================
# TRY YOURSELF
# =====================================================

with tab_try:

    st.markdown(
        """
        <div class="card">
            <div class="editor-title">▶ Try Yourself</div>
            <div class="editor-sub">
                Change the SQL query and run it.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -------------------------------------------------
    # SQL EDITOR KEY
    # -------------------------------------------------

    editor_key = f"sql_editor_{current}"

    if editor_key not in st.session_state:
        st.session_state[editor_key] = st.session_state.sql_query

    # -------------------------------------------------
    # CLEAR FUNCTION
    # -------------------------------------------------

    def clear_sql_editor():

        st.session_state[editor_key] = ""
        st.session_state.sql_query = ""
        st.session_state.sql_result = None
        st.session_state.sql_message = ""

    # -------------------------------------------------
    # SQL EDITOR
    # -------------------------------------------------

    query = st.text_area(
        "SQL Editor",
        height=275,
        key=editor_key,
        label_visibility="collapsed",
    )

    # -------------------------------------------------
    # BUTTONS
    # -------------------------------------------------

    run_col, clear_col = st.columns(
        [1, 1],
        gap="small",
    )

    with run_col:

        run_sql_button = st.button(
            "▶ Run Query",
            type="primary",
            use_container_width=True,
            key=f"run_sql_{current}",
        )

    with clear_col:

        clear_sql_button = st.button(
            "↻ Clear",
            use_container_width=True,
            key=f"clear_sql_{current}",
            on_click=clear_sql_editor,
        )

        # -------------------------------------------------
    # RUN SQL QUERY
    # -------------------------------------------------

    if run_sql_button:

        if not query.strip():

            st.warning(
                "⚠️ Please enter a SQL query."
            )

        else:

            st.session_state.sql_query = query

            result, message, error = run_sql(query)

            # ---------------------------------------------
            # QUERY FAILED
            # ---------------------------------------------

            if error:

                st.session_state.sql_result = None

                st.session_state.sql_message = (
                    f"❌ {error}"
                )

            # ---------------------------------------------
            # QUERY SUCCESSFUL
            # ---------------------------------------------

            else:

                st.session_state.sql_result = result

                st.session_state.sql_message = (
                    f"✅ {message}"
                )

                # Save successful Try Yourself progress
                save_lesson_progress(
                    current,
                    completed=True,
                )

    # -------------------------------------------------
    # OUTPUT HEADER
    # -------------------------------------------------

    st.markdown(
        """
        <div class="card" style="margin-top:9px;">
            <div class="output-head">
                <span>Output</span>
                <span class="success">● SQL Ready</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -------------------------------------------------
    # OUTPUT MESSAGE
    # -------------------------------------------------

    if st.session_state.sql_message:

        st.info(
            st.session_state.sql_message
        )

    # -------------------------------------------------
    # QUERY RESULT
    # -------------------------------------------------

    if st.session_state.sql_result is not None:

        st.dataframe(
            st.session_state.sql_result,
            use_container_width=True,
            hide_index=True,
        )

    # -------------------------------------------------
    # EMPTY OUTPUT
    # -------------------------------------------------

    else:

        st.markdown(
            """
            <div class="card">
                <div class="card-text">
                    Run your SQL query to see the result here.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# =====================================================
# QUERY CHALLENGE
# =====================================================

with tab_challenge:

    # -------------------------------------------------
    # LOAD CHALLENGE
    # -------------------------------------------------

    challenge = get_query_challenge(current)

    # -------------------------------------------------
    # CHALLENGE TITLE
    # -------------------------------------------------

    st.markdown(
        """
        <div style="
            color:#f5f8fc;
            font-size:30px;
            font-weight:800;
            line-height:1.2;
            margin-bottom:7px;
        ">
            🏆 Query Challenge
        </div>

        <div style="
            color:#8296ad;
            font-size:13px;
            margin-bottom:18px;
        ">
            Complete this small task without copying the example.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -------------------------------------------------
    # NO CHALLENGE FOUND
    # -------------------------------------------------

    if challenge is None:

        st.warning(
            "⚠️ No Query Challenge is available for this lesson."
        )

        st.info(
            "Please add this lesson's challenge to the "
            "query_challenges table in PostgreSQL."
        )

    else:

        # -------------------------------------------------
        # GET DATABASE VALUES
        # -------------------------------------------------

        challenge_task = challenge.get(
            "task",
            "",
        )

        challenge_hint = challenge.get(
            "hint",
            "",
        )

        expected_query = challenge.get(
            "expected_query",
            "",
        )

        challenge_points = challenge.get(
            "points",
            10,
        )

        # -------------------------------------------------
        # YOUR TASK
        # -------------------------------------------------

        st.markdown(
            """
            <div style="
                color:#3b7aff;
                font-size:15px;
                font-weight:800;
                margin-bottom:14px;
            ">
                🎯 Your Task
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div style="
                color:#f4f8fc;
                font-size:14px;
                line-height:1.7;
                margin-bottom:10px;
            ">
                {challenge_task}
            </div>
            """,
            unsafe_allow_html=True,
        )

        # -------------------------------------------------
        # POINTS
        # -------------------------------------------------

        st.markdown(
            f"""
            <div style="
                color:#8296ad;
                font-size:11px;
                margin-bottom:10px;
            ">
                🏆 Points: {challenge_points}
            </div>
            """,
            unsafe_allow_html=True,
        )

        # -------------------------------------------------
        # HINT
        # -------------------------------------------------

        if challenge_hint:

            st.info(
                f"💡 Hint: {challenge_hint}"
            )

        # -------------------------------------------------
        # SQL EDITOR
        # -------------------------------------------------

        challenge_key = f"challenge_sql_{current}"

        if challenge_key not in st.session_state:

            st.session_state[challenge_key] = ""

        challenge_query = st.text_area(
            "Your SQL solution",
            height=220,
            placeholder="Write your SQL solution here...",
            key=challenge_key,
            label_visibility="collapsed",
        )

        # -------------------------------------------------
        # BUTTONS
        # -------------------------------------------------

        challenge_col1, challenge_col2 = st.columns(
            2,
            gap="small",
        )

        with challenge_col1:

            run_challenge = st.button(
                "▶ Run Challenge",
                key=f"run_challenge_{current}",
                type="primary",
                use_container_width=True,
            )

        with challenge_col2:

            clear_challenge = st.button(
                "↻ Clear",
                key=f"clear_challenge_{current}",
                use_container_width=True,
            )

        # -------------------------------------------------
        # CLEAR
        # -------------------------------------------------

        if clear_challenge:

            st.session_state[challenge_key] = ""

            st.rerun()

        # -------------------------------------------------
        # RUN / CHECK CHALLENGE
        # -------------------------------------------------

        if run_challenge:

            if not challenge_query.strip():

                st.warning(
                    "⚠️ Please write your SQL solution first."
                )

            elif not expected_query.strip():

                st.error(
                    "❌ Correct solution is missing from the database."
                )

            else:

                user_query = normalize_sql(
                    challenge_query
                )

                correct_query = normalize_sql(
                    expected_query
                )

                # -----------------------------------------
                # CORRECT ANSWER
                # -----------------------------------------

                if user_query == correct_query:

                    st.success(
                        "🎉 Correct! Challenge completed successfully."
                    )

                    
                    # -----------------------------------------
                    # SAVE SUCCESSFUL ATTEMPT
                    # -----------------------------------------

                    save_challenge_attempt(
                        current,
                        challenge_query,
                        True,
                    )

                    # -----------------------------------------
                    # SAVE LESSON PROGRESS
                    # -----------------------------------------

                    save_lesson_progress(
                        current,
                        completed=True,
                    )

                # -----------------------------------------
                # WRONG ANSWER
                # -----------------------------------------

                else:

                    st.error(
                        "❌ Not quite correct."
                    )

                    st.info(
                        "💡 Check your SQL query and try again."
                    )

                    # -----------------------------------------
                    # SAVE FAILED ATTEMPT
                    # -----------------------------------------

                    save_challenge_attempt(
                        current,
                        challenge_query,
                        False,
                    )

        # -------------------------------------------------
        # SHOW SOLUTION
        # -------------------------------------------------

        show_solution = st.button(
            "💡 Show Solution",
            key=f"show_solution_{current}",
            use_container_width=True,
        )

        if show_solution:

            st.markdown(
                """
                <div style="
                    background:#10243a;
                    border:1px solid #1d466d;
                    border-left:3px solid #3b7aff;
                    border-radius:8px;
                    padding:16px;
                    margin-top:12px;
                ">

                    <div style="
                        color:#3b7aff;
                        font-size:15px;
                        font-weight:800;
                    ">
                        💡 Correct Solution
                    </div>

                    <div style="
                        color:#8296ad;
                        font-size:11px;
                        margin-top:6px;
                    ">
                        Compare your answer with the correct SQL.
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

            st.code(
                expected_query,
                language="sql",
            )
    
# =====================================================
# NOTES
# =====================================================

with tab_notes:

    # -------------------------------------------------
    # HEADER
    # -------------------------------------------------

    st.markdown(
        """
        <div class="card">
            <div class="card-title">📝 Notes</div>
            <div class="card-text">
                Write and save your notes for this PostgreSQL topic.
                Your notes are stored in PostgreSQL.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -------------------------------------------------
    # NOTE KEY
    # -------------------------------------------------

    note_key = f"notes_{current}"

    # -------------------------------------------------
    # LOAD NOTE ON FIRST OPEN
    # -------------------------------------------------

    if note_key not in st.session_state:

        saved_note = load_note(current)

        if saved_note is None:
            saved_note = ""

        st.session_state[note_key] = saved_note

    # -------------------------------------------------
    # NOTES EDITOR
    # IMPORTANT: THIS MUST NOT BE INSIDE THE IF ABOVE
    # -------------------------------------------------

    notes = st.text_area(
        "Your notes",
        height=240,
        placeholder="Write your notes here...",
        key=note_key,
        label_visibility="collapsed",
    )

    # -------------------------------------------------
    # BUTTONS
    # -------------------------------------------------

    notes_col1, notes_col2 = st.columns(
        2,
        gap="small",
    )

    with notes_col1:

        save_notes = st.button(
            "💾 Save Notes",
            key=f"save_notes_{current}",
            use_container_width=True,
            type="primary",
        )

    with notes_col2:

        clear_notes = st.button(
            "↻ Clear",
            key=f"clear_notes_{current}",
            use_container_width=True,
        )

    # -------------------------------------------------
    # SAVE
    # -------------------------------------------------

    if save_notes:

        if not notes.strip():

            st.warning(
                "⚠️ Please write some notes first."
            )

        else:

            result = save_note(
                current,
                notes,
            )

            if result:

                st.success(
                    "✅ Notes saved to PostgreSQL."
                )

            else:

                st.error(
                    "❌ Could not save notes."
                )

    # -------------------------------------------------
    # CLEAR
    # -------------------------------------------------

    if clear_notes:

        connection = None
        cursor = None

        try:

            connection = get_connection()
            cursor = connection.cursor()

            user_id = get_user_id()
            lesson_id = get_postgres_lesson_id(
                current
            )

            if user_id and lesson_id:

                cursor.execute(
                    """
                    DELETE FROM lesson_notes
                    WHERE user_id = %s
                      AND lesson_id = %s;
                    """,
                    (
                        user_id,
                        lesson_id,
                    ),
                )

                connection.commit()

            # Clear Streamlit value
            st.session_state.pop(
                note_key,
                None,
            )

            st.success(
                "🗑️ Notes cleared from PostgreSQL."
            )

            st.rerun()

        except Exception as error:

            if connection:
                connection.rollback()

            st.error(
                f"❌ Could not clear notes: {error}"
            )

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()
                

# =====================================================
# BOOKMARK
# =====================================================

with tab_bookmark:

    # -------------------------------------------------
    # TITLE
    # -------------------------------------------------

    st.markdown(
        """
        <div style="
            font-size:32px;
            font-weight:800;
            margin-bottom:8px;
        ">
            🔖 Bookmark
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="
            color:#9aaabd;
            font-size:14px;
            margin-bottom:20px;
        ">
            Save this topic to your Bookmarks so you can find it later.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -------------------------------------------------
    # CURRENT TOPIC
    # -------------------------------------------------

    st.info(
        f"📚 Current Topic: {current}"
    )

    # -------------------------------------------------
    # CHECK DATABASE
    # -------------------------------------------------

    bookmarked = is_bookmarked(current)

    # -------------------------------------------------
    # STATUS
    # -------------------------------------------------

    if bookmarked:

        st.success(
            f"✓ {current} is saved in your Bookmarks."
        )

        st.caption(
            "This bookmark is stored in PostgreSQL and linked to your account."
        )

    else:

        st.warning(
            f"{current} is not saved yet."
        )

        st.caption(
            "Save this lesson to your PostgreSQL bookmarks."
        )

    # -------------------------------------------------
    # BUTTONS
    # -------------------------------------------------

    save_col, remove_col = st.columns(
        2,
        gap="small",
    )

    with save_col:

        save_bookmark_button = st.button(
            "🔖 Save Bookmark",
            type="primary",
            use_container_width=True,
            key=f"save_bookmark_{current}",
        )

    with remove_col:

        remove_bookmark_button = st.button(
            "🗑️ Remove Bookmark",
            use_container_width=True,
            key=f"remove_bookmark_{current}",
        )

    # -------------------------------------------------
    # SAVE
    # -------------------------------------------------

    if save_bookmark_button:

        saved = save_bookmark(current)

        if saved:

            st.success(
                f"✓ {current} saved to PostgreSQL Bookmarks."
            )

            st.rerun()

        else:

            st.error(
                "❌ Could not save bookmark."
            )

    # -------------------------------------------------
    # REMOVE
    # -------------------------------------------------

    if remove_bookmark_button:

        removed = remove_bookmark(current)

        if removed:

            st.success(
                f"✓ {current} removed from PostgreSQL Bookmarks."
            )

            st.rerun()

        else:

            st.error(
                "❌ Could not remove bookmark."
            )

    # -------------------------------------------------
    # VIEW ALL BOOKMARKS
    # -------------------------------------------------

    st.divider()

    if st.button(
        "📚 View All My Bookmarks",
        use_container_width=True,
        key=f"view_all_bookmarks_{current}",
    ):

        st.switch_page("bookmarks.py")

    # -------------------------------------------------
    # DATABASE MESSAGE
    # -------------------------------------------------

    st.caption(
        "🔗 PostgreSQL • Your bookmarks are saved to your CodePractice account."
    )
        
# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div style="
        text-align:center;
        color:#596b82;
        font-size:9px;
        margin-top:18px;
        padding-top:10px;
        border-top:1px solid #16263a;
    ">
        CodePractice AI • PostgreSQL → Data Analysis → Machine Learning
    </div>
    """,
    unsafe_allow_html=True,
)

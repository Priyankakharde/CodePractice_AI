import os
import subprocess
import sys
import tempfile

import psycopg2
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_def toggle_bookmark(lesson_title):ORT", "5433"),
        database=os.getenv("DB_NAME", "codepractice"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD"),
        connect_timeout=5,
    )
    
# ============================================================
# SAVE PYTHON TRY YOURSELF PROGRESS
# ============================================================

def save_python_progress(topic):
    connection = None

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
            ("priyanka@codepractice.local",),
        )

        user_row = cursor.fetchone()

        if not user_row:
            return

        user_id = user_row[0]

        cursor.execute(
            """
            SELECT id
            FROM lessons
            WHERE subject = 'Python'
              AND title = %s
            LIMIT 1;
            """,
            (topic,),
        )

        lesson_row = cursor.fetchone()

        if not lesson_row:
            return

        lesson_id = lesson_row[0]

        cursor.execute(
            """
            SELECT id
            FROM progress
            WHERE user_id = %s
              AND lesson_id = %s
            LIMIT 1;
            """,
            (user_id, lesson_id),
        )

        progress_row = cursor.fetchone()

        if progress_row:

            cursor.execute(
                """
                UPDATE progress
                SET
                    completed = TRUE,
                    attempts = attempts + 1,
                    last_attempted = CURRENT_TIMESTAMP
                WHERE id = %s;
                """,
                (progress_row[0],),
            )

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
                        TRUE,
                        1,
                        CURRENT_TIMESTAMP
                    );
                """,
                (
                    user_id,
                    lesson_id,
                ),
            )

        connection.commit()

    except Exception:

        if connection:
            connection.rollback()

    finally:

        if connection:
            connection.close()    
            
            
# ============================================================
# MARK PYTHON LESSON AS STARTED
# ============================================================

def mark_python_lesson_started(topic):

    connection = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        # Get current user
        cursor.execute(
            """
            SELECT id
            FROM users
            WHERE email = %s
            LIMIT 1;
            """,
            ("priyanka@codepractice.local",),
        )

        user_row = cursor.fetchone()

        if not user_row:
            return

        user_id = user_row[0]

        # Get Python lesson
        cursor.execute(
            """
            SELECT id
            FROM lessons
            WHERE subject = 'Python'
              AND title = %s
            LIMIT 1;
            """,
            (topic,),
        )

        lesson_row = cursor.fetchone()

        if not lesson_row:
            return

        lesson_id = lesson_row[0]

        # Check whether progress already exists
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

        # Create a progress row only if this is a new lesson
        if not progress_row:

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
                        FALSE,
                        0,
                        CURRENT_TIMESTAMP
                    );
                """,
                (
                    user_id,
                    lesson_id,
                ),
            )

            connection.commit()

    except Exception:

        if connection:
            connection.rollback()

    finally:

        if connection:
            connection.close()            
    
    
# =========================================================
# BOOKMARK DATABASE SETUP
# =========================================================

def ensure_bookmark_database():

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        # -------------------------------------------------
        # CREATE BOOKMARKS TABLE
        # -------------------------------------------------

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS bookmarks (
                id SERIAL PRIMARY KEY,

                user_id INTEGER NOT NULL
                    REFERENCES users(id)
                    ON DELETE CASCADE,

                lesson_id INTEGER NOT NULL
                    REFERENCES lessons(id)
                    ON DELETE CASCADE,

                topic_name VARCHAR(255),

                created_at TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP
            );
            """
        )

        # -------------------------------------------------
        # ADD TOPIC NAME IF OLD TABLE ALREADY EXISTS
        # -------------------------------------------------

        cursor.execute(
            """
            ALTER TABLE bookmarks
            ADD COLUMN IF NOT EXISTS topic_name VARCHAR(255);
            """
        )

        # -------------------------------------------------
        # PREVENT DUPLICATE BOOKMARKS
        # -------------------------------------------------

        cursor.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS
            idx_bookmarks_user_lesson
            ON bookmarks(user_id, lesson_id);
            """
        )

        connection.commit()

    except Exception as error:

        if connection:
            connection.rollback()

        print(
            f"BOOKMARK DATABASE SETUP ERROR: {error}"
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# Prepare bookmark database
ensure_bookmark_database()

    
# =========================================================
# BOOKMARK FUNCTIONS
# =========================================================

def is_bookmarked(lesson_title):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        user_email = st.session_state.get(
            "user_email",
            "priyanka@codepractice.local",
        )

        cursor.execute(
            """
            SELECT b.id
            FROM bookmarks b

            JOIN users u
                ON u.id = b.user_id

            JOIN lessons l
                ON l.id = b.lesson_id

            WHERE u.email = %s
              AND l.subject = %s
              AND l.title = %s

            LIMIT 1;
            """,
            (
                user_email,
                "Python",
                lesson_title,
            ),
        )

        return cursor.fetchone() is not None

    except Exception as error:

        print(
            f"BOOKMARK CHECK ERROR: {error}"
        )

        return False

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


def toggle_bookmark(lesson_title):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        user_email = st.session_state.get(
            "user_email",
            "priyanka@codepractice.local",
        )

        # =================================================
        # GET USER
        # =================================================

        cursor.execute(
            """
            SELECT id
            FROM users
            WHERE email = %s
            LIMIT 1;
            """,
            (user_email,),
        )

        user_row = cursor.fetchone()

        if not user_row:

            raise Exception(
                f"User not found: {user_email}"
            )

        user_id = user_row[0]

        # =================================================
        # GET LESSON
        # =================================================

        cursor.execute(
            """
            SELECT id
            FROM lessons
            WHERE subject = %s
              AND title = %s
            LIMIT 1;
            """,
            (
                "Python",
                lesson_title,
            ),
        )

        lesson_row = cursor.fetchone()

        # =================================================
        # IF LESSON DOES NOT EXIST
        # CREATE IT
        # =================================================

        if not lesson_row:

            cursor.execute(
                """
                SELECT COALESCE(
                    MAX(lesson_order),
                    0
                ) + 1
                FROM lessons
                WHERE subject = %s;
                """,
                ("Python",),
            )

            next_order = cursor.fetchone()[0]

            cursor.execute(
                """
                INSERT INTO lessons (
                    subject,
                    title,
                    description,
                    lesson_order
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s
                )
                RETURNING id;
                """,
                (
                    "Python",
                    lesson_title,
                    f"Python → {lesson_title}",
                    next_order,
                ),
            )

            lesson_row = cursor.fetchone()

        lesson_id = lesson_row[0]

        # =================================================
        # CHECK EXISTING BOOKMARK
        # =================================================

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

        existing = cursor.fetchone()

        # =================================================
        # REMOVE BOOKMARK
        # =================================================

        if existing:

            cursor.execute(
                """
                DELETE FROM bookmarks
                WHERE id = %s;
                """,
                (existing[0],),
            )

            connection.commit()

            return False

        # =================================================
        # SAVE BOOKMARK
        # =================================================

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
            )
            ON CONFLICT (
                user_id,
                lesson_id
            )
            DO UPDATE SET
                topic_name = EXCLUDED.topic_name;
            """,
            (
                user_id,
                lesson_id,
                lesson_title,
            ),
        )

        connection.commit()

        return True

    except Exception as error:

        if connection:
            connection.rollback()

        print(
            f"BOOKMARK DATABASE ERROR: {error}"
        )

        return None

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()

# =========================================================
# CODEPRACTICE AI
# Python for Machine Learning
# W3Schools-style learning workspace
# =========================================================

st.set_page_config(
    page_title="Python for Machine Learning | CodePractice AI",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# COURSE STRUCTURE
# Only the Python + Data Science + ML concepts needed
# for a beginner machine-learning path.
# =========================================================

COURSE = {
    "🐍 LEVEL 1 — PYTHON BASICS": {
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
    },
    "📊 LEVEL 2 — DATA SCIENCE BASICS": {
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
    },
    "🤖 LEVEL 3 — MACHINE LEARNING BASICS": {
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
    },
}


# =========================================================
# MAIN LESSONS
# concept, types, syntax, example, output, explanation, ml
# =========================================================

LESSONS = {
    "Python Basics": {
        "concept": "Python is a simple programming language used for coding, data science and machine learning.",
        "types": ["Variables", "Data Types", "Input / Output"],
        "syntax": 'name = "Priyanka"\nage = 27\nprint(name)',
        "example": 'name = "Priyanka"\nage = 27\n\nprint(name)\nprint(age)',
        "output": "Priyanka\n27",
        "explanation": "Variables store values. Data types describe values. input() gets information and print() displays output.",
        "ml": "These are the basic Python building blocks used throughout machine learning.",
    },
    "Operators": {
        "concept": "Operators are symbols used to perform calculations, comparisons and logical checks.",
        "types": ["Arithmetic", "Assignment", "Comparison", "Logical"],
        "syntax": "a + b\na > b\na > 5 and b < 10",
        "example": "a = 10\nb = 5\n\nprint(a + b)\nprint(a > b)\nprint(a > 5 and b < 10)",
        "output": "15\nTrue\nTrue",
        "explanation": "Arithmetic operators calculate values. Comparison operators compare values. Logical operators combine conditions.",
        "ml": "Operators are used for calculations, filtering data and checking conditions.",
    },
    "Control Statements": {
        "concept": "Control statements decide which code runs and how many times it runs.",
        "types": ["if / elif / else", "for loop", "while loop"],
        "syntax": 'if condition:\n    print("Yes")\nelse:\n    print("No")',
        "example": 'score = 70\n\nif score >= 50:\n    print("Pass")\nelse:\n    print("Fail")',
        "output": "Pass",
        "explanation": "if checks a condition. else handles the other case. Loops repeat code over data.",
        "ml": "Conditions and loops are useful when checking, filtering and processing data.",
    },
    "Data Structures": {
        "concept": "Data structures are ways to store and organize multiple values in Python.",
        "types": [
            "List → ordered and changeable",
            "Tuple → ordered and fixed",
            "Dictionary → key and value",
            "Set → unique values",
        ],
        "syntax": "numbers = [1, 2, 3]\nstudent = {'name': 'Priyanka'}",
        "example": "numbers = [1, 2, 3]\nstudent = {'name': 'Priyanka'}\n\nprint(numbers)\nprint(student['name'])",
        "output": "[1, 2, 3]\nPriyanka",
        "explanation": "Lists store ordered values. Tuples are fixed. Dictionaries store key-value pairs. Sets store unique values.",
        "ml": "Data structures are used to store and organize data before it is passed to ML libraries.",
    },
    "Functions": {
        "concept": "A function is a reusable block of code that performs a specific task.",
        "types": ["Define a function", "Arguments", "Return value", "Lambda"],
        "syntax": "def add(a, b):\n    return a + b",
        "example": "def add(a, b):\n    return a + b\n\nresult = add(10, 5)\nprint(result)",
        "output": "15",
        "explanation": "A function receives values through arguments and can return a result.",
        "ml": "Functions help organize preprocessing, training, prediction and evaluation code.",
    },
    "Modules & Libraries": {
        "concept": "Modules and libraries provide reusable Python code so we do not need to build everything ourselves.",
        "types": ["Built-in modules", "Your own modules", "External libraries"],
        "syntax": "import math\nimport numpy as np",
        "example": "import math\n\nprint(math.sqrt(25))",
        "output": "5.0",
        "explanation": "import loads code from a module or library so its functions can be used.",
        "ml": "NumPy, Pandas, Matplotlib and Scikit-learn are important ML libraries.",
    },
    "File Handling": {
        "concept": "File handling allows Python to read and write files.",
        "types": ["Read → r", "Write → w", "Append → a", "Open / Close"],
        "syntax": "open('file.txt', 'r')",
        "example": "with open('demo.txt', 'w') as file:\n    file.write('Hello ML')\n\nwith open('demo.txt', 'r') as file:\n    print(file.read())",
        "output": "Hello ML",
        "explanation": "w writes data and r reads data. Using with closes the file automatically.",
        "ml": "Files are commonly used to load datasets and save results.",
    },
    "Exception Handling": {
        "concept": "Exception handling lets us handle errors without stopping the whole program.",
        "types": ["try → risky code", "except → handles an error", "finally → always runs"],
        "syntax": "try:\n    code\nexcept:\n    handle_error",
        "example": 'try:\n    number = int("abc")\nexcept ValueError:\n    print("Error occurred")\nfinally:\n    print("Done")',
        "output": "Error occurred\nDone",
        "explanation": "try runs risky code, except handles an error and finally runs at the end.",
        "ml": "Useful when loading datasets or handling unexpected input.",
    },
    "List Comprehension": {
        "concept": "List comprehension creates a new list in a short and readable way.",
        "types": ["Expression", "for loop", "Optional if condition"],
        "syntax": "[expression for item in items]",
        "example": "numbers = [1, 2, 3, 4]\n\nsquares = [n * n for n in numbers]\nprint(squares)",
        "output": "[1, 4, 9, 16]",
        "explanation": "The expression is applied to each item and the results are stored in a new list.",
        "ml": "Useful for simple data transformations and filtering.",
    },
    "OOP Basics": {
        "concept": "Object-oriented programming organizes code using classes and objects.",
        "types": ["Class → blueprint", "Object → instance", "Inheritance → reuse"],
        "syntax": "class Person:\n    pass",
        "example": 'class Person:\n    def __init__(self, name):\n        self.name = name\n\nperson = Person("Priyanka")\nprint(person.name)',
        "output": "Priyanka",
        "explanation": "A class defines structure and behavior. An object is created from the class.",
        "ml": "ML libraries use classes and objects for models, transformers and datasets.",
    },
    "Built-in Functions": {
        "concept": "Python provides ready-made functions for common programming tasks.",
        "types": ["len()", "type()", "range()", "int() / float() / str()", "sum() / min() / max()"],
        "syntax": "len(data)\nsum(numbers)",
        "example": "numbers = [1, 2, 3, 4]\n\nprint(len(numbers))\nprint(sum(numbers))\nprint(max(numbers))",
        "output": "4\n10\n4",
        "explanation": "Built-in functions solve common tasks without writing those functions yourself.",
        "ml": "These functions are useful during data processing and analysis.",
    },
    "NumPy": {
        "concept": "NumPy is a Python library used for numerical computing and arrays.",
        "types": ["Arrays", "Indexing", "Array operations"],
        "syntax": "import numpy as np\nx = np.array([1, 2, 3])",
        "example": "import numpy as np\n\nx = np.array([1, 2, 3])\nprint(x)\nprint(x * 2)",
        "output": "[1 2 3]\n[2 4 6]",
        "explanation": "NumPy arrays store numerical values and allow fast mathematical operations.",
        "ml": "NumPy is a foundation for numerical data used by many ML libraries.",
    },
    "Pandas": {
        "concept": "Pandas is a Python library used to work with structured tabular data.",
        "types": ["Series", "DataFrame", "Read CSV", "Select data", "Filter data"],
        "syntax": "import pandas as pd\ndf = pd.DataFrame(data)",
        "example": "import pandas as pd\n\ndf = pd.DataFrame({\n    'age': [20, 25],\n    'score': [80, 90]\n})\n\nprint(df)",
        "output": "   age  score\n0   20     80\n1   25     90",
        "explanation": "A DataFrame stores data in rows and columns and provides tools for working with datasets.",
        "ml": "Pandas is commonly used to load and prepare datasets before ML.",
    },
    "Data Cleaning": {
        "concept": "Data cleaning fixes common problems in raw data before analysis or ML.",
        "types": ["Missing values", "Duplicates", "Wrong values", "Data transformation"],
        "syntax": "df.isnull()\ndf.drop_duplicates()",
        "example": "import pandas as pd\n\ndf = pd.DataFrame({'score': [80, None, 80]})\n\ndf = df.drop_duplicates()\nprint(df)",
        "output": "   score\n0   80.0\n1    NaN",
        "explanation": "Cleaning prepares data so it can be used more reliably for analysis and modeling.",
        "ml": "Clean data is important before training a machine learning model.",
    },
    "Data Analysis": {
        "concept": "Data analysis means understanding data using statistics, grouping and simple comparisons.",
        "types": ["Mean", "Median", "Mode", "describe()", "groupby()"],
        "syntax": "df['score'].mean()\ndf.describe()",
        "example": "import pandas as pd\n\ndf = pd.DataFrame({'score': [60, 70, 80, 90]})\n\nprint(df['score'].mean())",
        "output": "75.0",
        "explanation": "Statistics help us understand the center, spread and general behavior of data.",
        "ml": "Data analysis helps us understand patterns before selecting and training an ML model.",
    },
    "Data Visualization": {
        "concept": "Data visualization represents data using charts so patterns are easier to understand.",
        "types": ["Line → trends", "Bar → categories", "Histogram → distribution", "Scatter → relationship"],
        "syntax": "plt.plot(x, y)\nplt.show()",
        "example": "import matplotlib.pyplot as plt\n\nx = [1, 2, 3]\ny = [2, 4, 6]\n\nplt.plot(x, y)\nplt.show()",
        "output": "A line chart is displayed.",
        "explanation": "Charts help us see trends, distributions and relationships in data.",
        "ml": "Visualization helps us understand data before building an ML model.",
    },
    "ML Basics": {
        "concept": "Machine Learning teaches computers to learn patterns from data and make predictions.",
        "types": ["Features → input X", "Target → output y", "Model → learns patterns", "Prediction → model output"],
        "syntax": "X → Model → Prediction",
        "example": "House Features → ML Model → House Price",
        "output": "Predicted house price",
        "explanation": "A model learns patterns from training data and uses those patterns to make predictions.",
        "ml": "This is the central idea behind practical machine learning projects.",
    },
    "Types of ML": {
        "concept": "Machine Learning can be divided into different learning approaches.",
        "types": ["Supervised → labeled data", "Unsupervised → unlabeled data", "Reinforcement → reward / penalty"],
        "syntax": "Supervised / Unsupervised / Reinforcement",
        "example": "Supervised → predict price\nUnsupervised → group customers\nReinforcement → learn from reward",
        "output": "Three common ML approaches",
        "explanation": "The learning type depends on the problem and whether a correct target is available.",
        "ml": "For this beginner course, supervised and unsupervised learning are the main focus.",
    },
    "Supervised Learning": {
        "concept": "Supervised Learning uses labeled data where the correct target is known.",
        "types": ["Regression → continuous values", "Classification → categories"],
        "syntax": "X → Model → y",
        "example": "Regression:\nHouse Features → Model → Price\n\nClassification:\nEmail Features → Model → Spam / Not Spam",
        "output": "Predicted value or category",
        "explanation": "The model learns the relationship between input features and a known target.",
        "ml": "Regression and classification are two core supervised ML tasks.",
    },
    "Unsupervised Learning": {
        "concept": "Unsupervised Learning works with data without a target label and looks for useful patterns or groups.",
        "types": ["Clustering → find groups", "Dimensionality Reduction → reduce features"],
        "syntax": "Data → Model → Patterns / Groups",
        "example": "Customer Data → K-Means → Customer Groups",
        "output": "Customer groups",
        "explanation": "The model discovers structure in data without being given the correct answer.",
        "ml": "K-Means is a common beginner example of clustering.",
    },
    "Dataset Preparation": {
        "concept": "Dataset preparation gets raw data ready for machine learning.",
        "types": ["Features & Target", "Train / Test Split", "Preprocessing", "Scaling"],
        "syntax": "Raw Data → Clean Data → X, y → Train / Test",
        "example": "Features = [area, rooms]\nTarget = price\n\nTrain = 80%\nTest = 20%",
        "output": "Model-ready dataset",
        "explanation": "We prepare clean features and targets and split data before training.",
        "ml": "Good dataset preparation helps a model learn from useful data.",
    },
    "Model Training": {
        "concept": "Model training means teaching an ML model using training data.",
        "types": ["Create model", "fit()", "Training data"],
        "syntax": "model.fit(X_train, y_train)",
        "example": "from sklearn.linear_model import LinearRegression\n\nmodel = LinearRegression()\nmodel.fit(X_train, y_train)",
        "output": "Trained model",
        "explanation": "fit() uses training data to learn patterns for a supervised model.",
        "ml": "Training is the main learning step in supervised machine learning.",
    },
    "Evaluation": {
        "concept": "Evaluation measures how well a model performs on data it has not learned from.",
        "types": ["Classification → Accuracy, Precision, Recall", "Regression → MAE, MSE, R²"],
        "syntax": "Actual values vs Predicted values",
        "example": "Classification → Accuracy\nRegression → MAE / MSE / R²",
        "output": "Performance metric",
        "explanation": "Metrics compare predictions with correct values to measure model performance.",
        "ml": "Evaluation tells us whether the model works well on new data.",
    },
    "Overfitting & Underfitting": {
        "concept": "Overfitting and underfitting are common model learning problems.",
        "types": ["Overfitting → learns training data too closely", "Underfitting → model is too simple"],
        "syntax": "Train performance vs Test performance",
        "example": "Overfitting:\nTraining → Very Good\nTesting → Poor\n\nUnderfitting:\nTraining → Poor\nTesting → Poor",
        "output": "Model learning problem",
        "explanation": "A useful model should learn important patterns and also perform well on new data.",
        "ml": "These concepts help explain why a model may perform poorly.",
    },
    "Scikit-learn Basics": {
        "concept": "Scikit-learn is a Python library that provides common machine learning algorithms and tools.",
        "types": ["Import model", "Create model", "fit()", "predict()"],
        "syntax": "model.fit(X, y)\nmodel.predict(X)",
        "example": "from sklearn.linear_model import LinearRegression\n\nmodel = LinearRegression()\nprint(model)",
        "output": "LinearRegression()",
        "explanation": "Scikit-learn provides ready-to-use models and tools for ML.",
        "ml": "Scikit-learn will be the main beginner ML library in this course.",
    },
    "ML Workflow": {
        "concept": "ML Workflow is the basic process used to build a machine learning solution.",
        "types": ["Collect Data", "Clean Data", "Explore Data", "Prepare Data", "Train Model", "Evaluate Model", "Predict"],
        "syntax": "Data → Clean → Prepare → Train → Evaluate → Predict",
        "example": "1. Collect Data\n2. Clean Data\n3. Explore Data\n4. Prepare Data\n5. Train Model\n6. Evaluate Model\n7. Predict",
        "output": "Complete ML workflow",
        "explanation": "The workflow takes us from raw data to a trained and evaluated model.",
        "ml": "This same workflow can be used in practical ML projects.",
    },
}


# =========================================================
# SUBTOPIC LESSONS
# Concise, real information for the items shown in the
# expandable sidebar. If a subtopic is not listed here,
# its parent lesson is used as a simple fallback.
# =========================================================

SUBLESSONS = {
    "Variables": {
        "concept": "A variable is a name used to store a value.",
        "types": ["Create a variable", "Change a value", "Use a variable"],
        "syntax": "name = value",
        "example": 'name = "Priyanka"\nage = 27\nprint(name)\nprint(age)',
        "output": "Priyanka\n27",
        "explanation": "Python creates a variable when you assign a value to a name.",
        "ml": "Variables store features, targets, parameters and intermediate results.",
    },
    "Data Types": {
        "concept": "A data type tells Python what kind of value is being stored.",
        "types": ["int", "float", "str", "bool", "list / tuple / dict / set"],
        "syntax": "age = 27\nprice = 99.5\nname = 'ML'",
        "example": "age = 27\nprice = 99.5\nname = 'ML'\nactive = True\n\nprint(type(age))\nprint(type(price))",
        "output": "<class 'int'>\n<class 'float'>",
        "explanation": "Different values have different types, and Python provides tools to inspect and convert them.",
        "ml": "Correct data types are important when preparing numerical and categorical ML data.",
    },
    "Input / Output": {
        "concept": "Input gets information from the user and output displays information.",
        "types": ["input() → user input", "print() → output", "Type conversion → int(), float()"],
        "syntax": "name = input('Name: ')\nprint(name)",
        "example": 'name = "Priyanka"\nprint("Hello", name)',
        "output": "Hello Priyanka",
        "explanation": "input() reads text and print() displays values on the screen.",
        "ml": "The same idea is used when collecting values for a prediction interface.",
    },
    "Arithmetic Operators": {
        "concept": "Arithmetic operators perform mathematical calculations.",
        "types": ["+ addition", "- subtraction", "* multiplication", "/ division", "** power"],
        "syntax": "a + b\na * b",
        "example": "a = 10\nb = 5\nprint(a + b)\nprint(a * b)",
        "output": "15\n50",
        "explanation": "Arithmetic operators calculate numerical results.",
        "ml": "Numerical calculations appear throughout data preprocessing and ML.",
    },
    "Assignment Operators": {
        "concept": "Assignment operators store or update a value in a variable.",
        "types": ["=", "+=", "-=", "*=", "/="],
        "syntax": "x = 10\nx += 5",
        "example": "x = 10\nx += 5\nprint(x)",
        "output": "15",
        "explanation": "Assignment operators make it easy to update existing values.",
        "ml": "Useful while updating counters, parameters and calculated values.",
    },
    "Comparison Operators": {
        "concept": "Comparison operators compare two values and return True or False.",
        "types": ["==", "!=", ">", "<", ">=", "<="],
        "syntax": "a > b",
        "example": "score = 80\nprint(score >= 50)\nprint(score == 100)",
        "output": "True\nFalse",
        "explanation": "Comparisons create Boolean results that can be used in conditions.",
        "ml": "Used for filtering data and checking prediction or metric conditions.",
    },
    "Logical Operators": {
        "concept": "Logical operators combine Boolean conditions.",
        "types": ["and", "or", "not"],
        "syntax": "condition1 and condition2",
        "example": "age = 25\nscore = 80\nprint(age > 18 and score >= 50)",
        "output": "True",
        "explanation": "and requires both conditions, or requires one, and not reverses a Boolean value.",
        "ml": "Useful for filtering rows and applying multiple data rules.",
    },
    "if / elif / else": {
        "concept": "Conditional statements choose code based on a condition.",
        "types": ["if", "elif", "else"],
        "syntax": "if condition:\n    code\nelif condition:\n    code\nelse:\n    code",
        "example": "score = 75\n\nif score >= 80:\n    print('A')\nelif score >= 50:\n    print('Pass')\nelse:\n    print('Fail')",
        "output": "Pass",
        "explanation": "Python checks conditions from top to bottom and executes the matching block.",
        "ml": "Useful for rule-based preprocessing and interpreting results.",
    },
    "for Loop": {
        "concept": "A for loop repeats code for each item in a sequence.",
        "types": ["range()", "List iteration", "String iteration"],
        "syntax": "for item in items:\n    code",
        "example": "for i in range(3):\n    print(i)",
        "output": "0\n1\n2",
        "explanation": "The loop runs once for every value in the sequence.",
        "ml": "Useful for simple data processing and repeated operations.",
    },
    "while Loop": {
        "concept": "A while loop repeats code while a condition remains true.",
        "types": ["Condition", "Repeated execution", "Stop condition"],
        "syntax": "while condition:\n    code",
        "example": "x = 1\nwhile x <= 3:\n    print(x)\n    x += 1",
        "output": "1\n2\n3",
        "explanation": "The condition is checked before each repetition.",
        "ml": "Useful for repeated processes, although many ML operations use library functions instead.",
    },
    "Lists": {
        "concept": "A list stores multiple ordered values and can be changed.",
        "types": ["Create", "Index", "Append", "Remove"],
        "syntax": "numbers = [1, 2, 3]",
        "example": "numbers = [10, 20, 30]\nprint(numbers[0])\nnumbers.append(40)\nprint(numbers)",
        "output": "10\n[10, 20, 30, 40]",
        "explanation": "List indexes start at 0 and list methods can add or remove items.",
        "ml": "Lists are useful for storing small collections of features and values.",
    },
    "Tuples": {
        "concept": "A tuple stores ordered values that normally should not be changed.",
        "types": ["Ordered", "Indexed", "Immutable"],
        "syntax": "point = (10, 20)",
        "example": "point = (10, 20)\nprint(point[0])",
        "output": "10",
        "explanation": "Tuples are similar to lists but are immutable.",
        "ml": "Useful when a fixed group of values should stay unchanged.",
    },
    "Dictionaries": {
        "concept": "A dictionary stores data as key-value pairs.",
        "types": ["Key", "Value", "get()", "Update"],
        "syntax": "student = {'name': 'Priyanka'}",
        "example": "student = {'name': 'Priyanka', 'age': 27}\nprint(student['name'])",
        "output": "Priyanka",
        "explanation": "A key is used to access its corresponding value.",
        "ml": "Useful for configuration, metadata and structured records.",
    },
    "Sets": {
        "concept": "A set stores unique values without duplicate items.",
        "types": ["Unique values", "Add", "Remove", "Set operations"],
        "syntax": "values = {1, 2, 3}",
        "example": "values = {1, 2, 2, 3}\nprint(values)",
        "output": "{1, 2, 3}",
        "explanation": "Duplicate values are automatically removed from a set.",
        "ml": "Useful when unique categories or values are needed.",
    },
    "Define Function": {
        "concept": "A function is defined with the def keyword.",
        "types": ["def", "Function name", "Parameters", "Body"],
        "syntax": "def greet():\n    print('Hello')",
        "example": "def greet():\n    print('Hello ML')\n\ngreet()",
        "output": "Hello ML",
        "explanation": "The function body runs when the function is called.",
        "ml": "Functions keep ML code organized into reusable steps.",
    },
    "Arguments": {
        "concept": "Arguments are values passed into a function.",
        "types": ["Positional arguments", "Keyword arguments", "Default values"],
        "syntax": "def add(a, b):\n    return a + b",
        "example": "def add(a, b):\n    return a + b\n\nprint(add(2, 3))",
        "output": "5",
        "explanation": "Arguments provide the input needed by a function.",
        "ml": "Functions can receive datasets, features or model settings as inputs.",
    },
    "Return Value": {
        "concept": "return sends a result from a function back to the caller.",
        "types": ["Return one value", "Return multiple values", "No return"],
        "syntax": "def square(x):\n    return x * x",
        "example": "def square(x):\n    return x * x\n\nresult = square(5)\nprint(result)",
        "output": "25",
        "explanation": "The returned value can be stored or used in another calculation.",
        "ml": "Preprocessing and prediction functions commonly return calculated results.",
    },
    "Lambda": {
        "concept": "A lambda is a small one-line anonymous function.",
        "types": ["One expression", "Short function", "Often used with map/filter"],
        "syntax": "lambda x: x * 2",
        "example": "square = lambda x: x * x\nprint(square(5))",
        "output": "25",
        "explanation": "Lambda is useful when a very small function is needed temporarily.",
        "ml": "Can be useful for simple data transformations.",
    },
    "Import Modules": {
        "concept": "import loads a module so its code can be used.",
        "types": ["import module", "from module import item", "Alias with as"],
        "syntax": "import math\nimport numpy as np",
        "example": "import math\nprint(math.sqrt(16))",
        "output": "4.0",
        "explanation": "Modules help split and reuse Python code.",
        "ml": "ML programs import NumPy, Pandas and Scikit-learn modules.",
    },
    "Built-in Modules": {
        "concept": "Python includes useful modules such as math and random.",
        "types": ["math", "random", "datetime", "os"],
        "syntax": "import math",
        "example": "import math\nprint(math.sqrt(25))",
        "output": "5.0",
        "explanation": "Built-in modules are available with Python and cover common tasks.",
        "ml": "Useful for mathematical operations and general data-processing tasks.",
    },
    "External Libraries": {
        "concept": "External libraries add functionality that is installed separately.",
        "types": ["NumPy", "Pandas", "Matplotlib", "Scikit-learn"],
        "syntax": "import numpy as np",
        "example": "import numpy as np\n\nx = np.array([1, 2, 3])\nprint(x)",
        "output": "[1 2 3]",
        "explanation": "Libraries provide specialized tools without requiring us to build everything ourselves.",
        "ml": "These libraries form the basic Python ML stack.",
    },
    "Read File": {
        "concept": "Reading a file gets stored information into a Python program.",
        "types": ["open()", "read()", "readline()", "readlines()"],
        "syntax": "with open('data.txt', 'r') as file:\n    data = file.read()",
        "example": "with open('data.txt', 'r') as file:\n    data = file.read()\n    print(data)",
        "output": "Contents of data.txt",
        "explanation": "The read mode opens an existing file and read() gets its contents.",
        "ml": "Useful for loading text or simple dataset files.",
    },
    "Write File": {
        "concept": "Writing saves text or results to a file.",
        "types": ["w → overwrite", "a → append"],
        "syntax": "with open('data.txt', 'w') as file:\n    file.write('ML')",
        "example": "with open('result.txt', 'w') as file:\n    file.write('ML result')\n\nprint('Saved')",
        "output": "Saved",
        "explanation": "Write mode creates or replaces a file, while append adds new content.",
        "ml": "Useful for saving predictions, logs and simple results.",
    },
    "Open / Close File": {
        "concept": "A file should be opened before use and closed after use.",
        "types": ["open()", "close()", "with statement"],
        "syntax": "with open('file.txt') as file:\n    data = file.read()",
        "example": "with open('demo.txt', 'w') as file:\n    file.write('Hello')\n\nprint('Done')",
        "output": "Done",
        "explanation": "The with statement safely manages the file and closes it automatically.",
        "ml": "Safe file handling is useful when working with datasets and outputs.",
    },
    "try": {
        "concept": "try contains code that may produce an exception.",
        "types": ["Risky operation", "Exception-aware code"],
        "syntax": "try:\n    risky_code",
        "example": "try:\n    print(10 / 2)\nexcept:\n    print('Error')",
        "output": "5.0",
        "explanation": "Python first attempts the code inside try.",
        "ml": "Useful when processing data that may contain unexpected values.",
    },
    "except": {
        "concept": "except handles an exception raised by code inside try.",
        "types": ["Specific exception", "General exception"],
        "syntax": "except ValueError:\n    print('Invalid value')",
        "example": "try:\n    value = int('abc')\nexcept ValueError:\n    print('Invalid value')",
        "output": "Invalid value",
        "explanation": "except runs when the matching error occurs.",
        "ml": "Useful for robust data loading and input processing.",
    },
    "finally": {
        "concept": "finally contains code that should run after try/except.",
        "types": ["Runs after success", "Runs after error"],
        "syntax": "finally:\n    cleanup()",
        "example": "try:\n    print('Work')\nfinally:\n    print('Finished')",
        "output": "Work\nFinished",
        "explanation": "finally runs whether or not an exception occurs.",
        "ml": "Useful for cleanup tasks such as closing resources.",
    },
    "Basic Syntax": {
        "concept": "List comprehension combines an expression and a loop into one line.",
        "types": ["Expression", "for", "Source sequence"],
        "syntax": "[x * 2 for x in numbers]",
        "example": "numbers = [1, 2, 3]\ndouble = [x * 2 for x in numbers]\nprint(double)",
        "output": "[2, 4, 6]",
        "explanation": "Each item is transformed by the expression and placed into a new list.",
        "ml": "Useful for short feature transformations.",
    },
    "With Condition": {
        "concept": "A condition can be added to a list comprehension to filter values.",
        "types": ["Expression", "for", "if filter"],
        "syntax": "[x for x in numbers if x > 2]",
        "example": "numbers = [1, 2, 3, 4]\nresult = [x for x in numbers if x > 2]\nprint(result)",
        "output": "[3, 4]",
        "explanation": "Only items that satisfy the condition are included.",
        "ml": "Useful for simple filtering and data preparation.",
    },
    "Class": {
        "concept": "A class is a blueprint used to create objects.",
        "types": ["Attributes", "Methods", "Constructor"],
        "syntax": "class Person:\n    pass",
        "example": "class Person:\n    def __init__(self, name):\n        self.name = name\n\np = Person('Priyanka')\nprint(p.name)",
        "output": "Priyanka",
        "explanation": "A class defines the structure and behavior of objects.",
        "ml": "Many ML libraries expose models and preprocessing tools as classes.",
    },
    "Object": {
        "concept": "An object is an instance created from a class.",
        "types": ["Create object", "Access attributes", "Call methods"],
        "syntax": "person = Person()",
        "example": "class Dog:\n    name = 'Max'\n\ndog = Dog()\nprint(dog.name)",
        "output": "Max",
        "explanation": "The object contains the data and behavior defined by its class.",
        "ml": "ML model objects store learned parameters and provide methods such as predict().",
    },
    "Inheritance": {
        "concept": "Inheritance lets one class reuse features from another class.",
        "types": ["Parent class", "Child class", "Reuse"],
        "syntax": "class Child(Parent):\n    pass",
        "example": "class Animal:\n    def speak(self):\n        print('Sound')\n\nclass Dog(Animal):\n    pass\n\nDog().speak()",
        "output": "Sound",
        "explanation": "The child class receives features from the parent class.",
        "ml": "Useful for understanding how larger Python libraries are structured.",
    },
    "Arrays": {
        "concept": "A NumPy array stores numerical values in an efficient structure.",
        "types": ["1D array", "2D array", "Shape"],
        "syntax": "np.array([1, 2, 3])",
        "example": "import numpy as np\n\nx = np.array([1, 2, 3])\nprint(x)\nprint(x.shape)",
        "output": "[1 2 3]\n(3,)",
        "explanation": "Arrays are designed for numerical operations and can have multiple dimensions.",
        "ml": "ML features are often represented as NumPy arrays.",
    },
    "Indexing": {
        "concept": "Indexing selects specific elements from an array.",
        "types": ["Single index", "Slice", "Row / column"],
        "syntax": "x[0]\nx[1:3]",
        "example": "import numpy as np\nx = np.array([10, 20, 30])\nprint(x[0])\nprint(x[1:3])",
        "output": "10\n[20 30]",
        "explanation": "Indexes start at 0 and slices can select a range of values.",
        "ml": "Used when selecting features, rows or parts of numerical data.",
    },
    "Array Operations": {
        "concept": "NumPy can perform mathematical operations on whole arrays.",
        "types": ["Addition", "Multiplication", "Mean", "Sum"],
        "syntax": "x * 2\nx.mean()",
        "example": "import numpy as np\nx = np.array([1, 2, 3])\nprint(x * 2)\nprint(x.mean())",
        "output": "[2 4 6]\n2.0",
        "explanation": "NumPy applies many operations efficiently to all elements.",
        "ml": "Array operations are common during feature preparation.",
    },
    "Series": {
        "concept": "A Pandas Series is a one-dimensional labeled data structure.",
        "types": ["Values", "Index", "Labels"],
        "syntax": "pd.Series([10, 20, 30])",
        "example": "import pandas as pd\nscore = pd.Series([80, 90, 70])\nprint(score)",
        "output": "0    80\n1    90\n2    70\ndtype: int64",
        "explanation": "A Series stores one column of data with an index.",
        "ml": "Useful for working with individual dataset columns.",
    },
    "DataFrame": {
        "concept": "A DataFrame is a table with rows and columns.",
        "types": ["Rows", "Columns", "Index"],
        "syntax": "pd.DataFrame(data)",
        "example": "import pandas as pd\ndf = pd.DataFrame({'age':[20,25], 'score':[80,90]})\nprint(df)",
        "output": "   age  score\n0   20     80\n1   25     90",
        "explanation": "A DataFrame is the main Pandas structure for tabular datasets.",
        "ml": "Most beginner ML datasets are explored and prepared as DataFrames.",
    },
    "Read CSV": {
        "concept": "Pandas can load CSV files directly into a DataFrame.",
        "types": ["CSV file", "read_csv()", "DataFrame"],
        "syntax": "df = pd.read_csv('data.csv')",
        "example": "import pandas as pd\n\ndf = pd.read_csv('data.csv')\nprint(df.head())",
        "output": "First rows of the dataset",
        "explanation": "read_csv() reads comma-separated data into a DataFrame.",
        "ml": "CSV is a common source of ML training data.",
    },
    "Select Data": {
        "concept": "Pandas lets us select columns and rows from a DataFrame.",
        "types": ["Column selection", "Multiple columns", "loc / iloc"],
        "syntax": "df['score']",
        "example": "import pandas as pd\ndf = pd.DataFrame({'age':[20,25], 'score':[80,90]})\nprint(df['score'])",
        "output": "0    80\n1    90",
        "explanation": "Selecting data lets us work with only the columns or rows we need.",
        "ml": "Used to create feature and target data.",
    },
    "Filter Data": {
        "concept": "Filtering keeps rows that satisfy a condition.",
        "types": ["Boolean condition", "Multiple conditions", "Filtered DataFrame"],
        "syntax": "df[df['score'] > 80]",
        "example": "import pandas as pd\ndf = pd.DataFrame({'score':[70,85,90]})\nprint(df[df['score'] > 80])",
        "output": "   score\n1     85\n2     90",
        "explanation": "The condition creates a Boolean mask and Pandas keeps matching rows.",
        "ml": "Filtering is useful when cleaning and exploring training data.",
    },
    "Missing Values": {
        "concept": "Missing values are empty or unknown values in a dataset.",
        "types": ["Detect → isnull()", "Remove → dropna()", "Fill → fillna()"],
        "syntax": "df.isnull().sum()",
        "example": "import pandas as pd\ndf = pd.DataFrame({'score':[80,None,90]})\ndf['score'] = df['score'].fillna(0)\nprint(df)",
        "output": "   score\n0   80.0\n1    0.0\n2   90.0",
        "explanation": "Missing values can be removed or replaced depending on the problem.",
        "ml": "Many ML models require missing values to be handled before training.",
    },
    "Duplicates": {
        "concept": "Duplicate rows repeat the same record and can distort analysis.",
        "types": ["Detect duplicates", "Remove duplicates"],
        "syntax": "df.drop_duplicates()",
        "example": "import pandas as pd\ndf = pd.DataFrame({'score':[80,80,90]})\ndf = df.drop_duplicates()\nprint(df)",
        "output": "   score\n0     80\n2     90",
        "explanation": "drop_duplicates() removes repeated rows.",
        "ml": "Cleaning duplicate records can prevent biased analysis and training.",
    },
    "Data Transformation": {
        "concept": "Data transformation changes data into a more useful form.",
        "types": ["Rename", "Convert type", "Create new column"],
        "syntax": "df['new'] = df['old'] * 2",
        "example": "import pandas as pd\ndf = pd.DataFrame({'score':[40,50]})\ndf['double'] = df['score'] * 2\nprint(df)",
        "output": "   score  double\n0     40      80\n1     50     100",
        "explanation": "Transformation creates or changes columns into useful representations.",
        "ml": "Feature transformation is a common preprocessing step.",
    },
    "Mean": {
        "concept": "Mean is the average of numerical values.",
        "types": ["Sum values", "Divide by count"],
        "syntax": "df['score'].mean()",
        "example": "scores = [60, 70, 80]\nprint(sum(scores) / len(scores))",
        "output": "70.0",
        "explanation": "The mean is calculated by adding values and dividing by their count.",
        "ml": "Mean is useful for understanding distributions and filling some missing values.",
    },
    "Median": {
        "concept": "Median is the middle value after sorting data.",
        "types": ["Sort values", "Find middle"],
        "syntax": "df['score'].median()",
        "example": "import pandas as pd\ndf = pd.DataFrame({'score':[60,100,70]})\nprint(df['score'].median())",
        "output": "70.0",
        "explanation": "Median is less affected by extreme values than the mean.",
        "ml": "Useful when exploring skewed data and missing-value strategies.",
    },
    "Mode": {
        "concept": "Mode is the value that appears most often.",
        "types": ["Count frequency", "Most common value"],
        "syntax": "df['category'].mode()",
        "example": "import pandas as pd\ndf = pd.DataFrame({'x':['A','B','A']})\nprint(df['x'].mode()[0])",
        "output": "A",
        "explanation": "Mode identifies the most frequently occurring value.",
        "ml": "Useful for understanding categorical data.",
    },
    "describe()": {
        "concept": "describe() gives a quick statistical summary of numerical columns.",
        "types": ["count", "mean", "std", "min", "max"],
        "syntax": "df.describe()",
        "example": "import pandas as pd\ndf = pd.DataFrame({'score':[60,70,80]})\nprint(df.describe())",
        "output": "Statistical summary of score",
        "explanation": "It provides common statistics that help us understand a dataset quickly.",
        "ml": "Useful during initial dataset exploration before training.",
    },
    "groupby()": {
        "concept": "groupby() groups rows by a column so we can calculate summaries for each group.",
        "types": ["Group", "Aggregate", "Compare"],
        "syntax": "df.groupby('category')['score'].mean()",
        "example": "import pandas as pd\ndf = pd.DataFrame({\n    'team':['A','A','B'],\n    'score':[80,90,70]\n})\nprint(df.groupby('team')['score'].mean())",
        "output": "team\nA    85.0\nB    70.0",
        "explanation": "Rows are grouped and an aggregation such as mean is calculated for each group.",
        "ml": "Useful for understanding patterns across categories.",
    },
    "Line Chart": {
        "concept": "A line chart shows change or trends across ordered values.",
        "types": ["X-axis", "Y-axis", "Line"],
        "syntax": "plt.plot(x, y)",
        "example": "import matplotlib.pyplot as plt\nplt.plot([1,2,3], [2,4,6])\nplt.show()",
        "output": "A line chart",
        "explanation": "Points are connected to show a trend.",
        "ml": "Useful for trends such as model loss over time.",
    },
    "Bar Chart": {
        "concept": "A bar chart compares values across categories.",
        "types": ["Categories", "Values", "Bars"],
        "syntax": "plt.bar(categories, values)",
        "example": "import matplotlib.pyplot as plt\nplt.bar(['A','B'], [10,20])\nplt.show()",
        "output": "A bar chart",
        "explanation": "Bar height represents the value of each category.",
        "ml": "Useful for comparing categories or model metrics.",
    },
    "Histogram": {
        "concept": "A histogram shows how numerical values are distributed.",
        "types": ["Bins", "Frequency", "Distribution"],
        "syntax": "plt.hist(values)",
        "example": "import matplotlib.pyplot as plt\nplt.hist([1,2,2,3,3,3])\nplt.show()",
        "output": "A histogram",
        "explanation": "Values are grouped into bins to show their frequency.",
        "ml": "Useful for understanding feature distributions.",
    },
    "Scatter Plot": {
        "concept": "A scatter plot shows the relationship between two numerical variables.",
        "types": ["X variable", "Y variable", "Points"],
        "syntax": "plt.scatter(x, y)",
        "example": "import matplotlib.pyplot as plt\nplt.scatter([1,2,3], [2,4,5])\nplt.show()",
        "output": "A scatter plot",
        "explanation": "Each point represents a pair of numerical values.",
        "ml": "Useful for spotting relationships and possible correlations between features.",
    },
    "Features": {
        "concept": "Features are the input variables used by a machine learning model.",
        "types": ["Numerical feature", "Categorical feature", "Multiple features"],
        "syntax": "X = data[['area', 'rooms']]",
        "example": "X = [[1000, 2], [1500, 3]]\nprint(X)",
        "output": "[[1000, 2], [1500, 3]]",
        "explanation": "Features provide information the model uses to learn and make predictions.",
        "ml": "Features are the X input in most supervised ML problems.",
    },
    "Target": {
        "concept": "The target is the value a supervised ML model tries to predict.",
        "types": ["Continuous target", "Categorical target"],
        "syntax": "y = data['price']",
        "example": "y = [250000, 350000]\nprint(y)",
        "output": "[250000, 350000]",
        "explanation": "The target is the known answer used while training a supervised model.",
        "ml": "The target is commonly called y.",
    },
    "Model": {
        "concept": "A model is an algorithm that learns patterns from training data.",
        "types": ["Regression model", "Classification model", "Clustering model"],
        "syntax": "model = LinearRegression()",
        "example": "from sklearn.linear_model import LinearRegression\nmodel = LinearRegression()\nprint(model)",
        "output": "LinearRegression()",
        "explanation": "The model contains the learning logic and learned parameters.",
        "ml": "Choosing and training the right model is a central ML task.",
    },
    "Prediction": {
        "concept": "Prediction is the output produced by a trained model for new input data.",
        "types": ["Regression prediction", "Classification prediction"],
        "syntax": "prediction = model.predict(X_new)",
        "example": "prediction = model.predict([[1500, 3]])\nprint(prediction)",
        "output": "Predicted value",
        "explanation": "After training, predict() uses learned patterns to produce an output.",
        "ml": "Prediction is the final step in many ML applications.",
    },
    "Regression": {
        "concept": "Regression predicts a continuous numerical value.",
        "types": ["Linear Regression", "Continuous target", "Numerical prediction"],
        "syntax": "model.fit(X_train, y_train)\nmodel.predict(X_test)",
        "example": "House Features → Linear Regression → Price",
        "output": "Predicted price",
        "explanation": "Regression learns a relationship between input features and a numerical target.",
        "ml": "Useful for problems such as price, demand or energy prediction.",
    },
    "Classification": {
        "concept": "Classification predicts a category or class.",
        "types": ["Binary classification", "Multi-class classification"],
        "syntax": "model.fit(X_train, y_train)\nmodel.predict(X_test)",
        "example": "Email Features → Classifier → Spam / Not Spam",
        "output": "Predicted class",
        "explanation": "The model learns how input examples relate to known categories.",
        "ml": "Useful for tasks such as fraud, spam or defect classification.",
    },
    "Clustering": {
        "concept": "Clustering groups similar data points without target labels.",
        "types": ["Similarity", "Groups", "No target label"],
        "syntax": "model.fit(X)\nlabels = model.labels_",
        "example": "Customer Data → Clustering → Group 1 / Group 2 / Group 3",
        "output": "Cluster labels",
        "explanation": "The algorithm finds groups based on similarities in the data.",
        "ml": "Useful when the dataset does not have a known target.",
    },
    "K-Means — basic idea": {
        "concept": "K-Means is a simple clustering algorithm that divides data into K groups.",
        "types": ["Choose K", "Assign points", "Update centers", "Repeat"],
        "syntax": "KMeans(n_clusters=3)",
        "example": "from sklearn.cluster import KMeans\nmodel = KMeans(n_clusters=2, random_state=42)\nmodel.fit(X)",
        "output": "Clustered data",
        "explanation": "K-Means repeatedly assigns points to the nearest cluster center and updates the centers.",
        "ml": "A beginner-friendly algorithm for unsupervised learning.",
    },
    "Supervised Learning": {
        "concept": "Supervised Learning uses labeled examples where the correct target is known.",
        "types": ["Regression", "Classification"],
        "syntax": "model.fit(X_train, y_train)",
        "example": "Features + Known Target → Model → Prediction",
        "output": "Predicted value or category",
        "explanation": "The model learns a mapping from input features to a known target.",
        "ml": "This is the main learning type used in many beginner ML projects.",
    },
    "Unsupervised Learning": {
        "concept": "Unsupervised Learning finds patterns in data without a known target.",
        "types": ["Clustering", "Dimensionality reduction"],
        "syntax": "model.fit(X)",
        "example": "Customer Data → K-Means → Customer Groups",
        "output": "Discovered groups or structure",
        "explanation": "The algorithm searches for structure instead of learning from known answers.",
        "ml": "Useful for grouping and exploring unlabeled data.",
    },
    "Reinforcement Learning — basic idea": {
        "concept": "Reinforcement Learning learns actions using rewards and penalties.",
        "types": ["Agent", "Environment", "Action", "Reward"],
        "syntax": "Action → Environment → Reward",
        "example": "Agent takes action → receives reward or penalty → learns",
        "output": "Learned behavior",
        "explanation": "The agent learns which actions produce better long-term rewards.",
        "ml": "It is useful to know the concept, but it is outside the main beginner ML path here.",
    },
    "Features & Target": {
        "concept": "Before training, separate input features X from the target y.",
        "types": ["X → features", "y → target"],
        "syntax": "X = df[['feature1', 'feature2']]\ny = df['target']",
        "example": "X = df[['area', 'rooms']]\ny = df['price']",
        "output": "X and y prepared",
        "explanation": "X contains information given to the model and y contains the answer to learn.",
        "ml": "This separation is required for most supervised ML training.",
    },
    "Train / Test Split": {
        "concept": "Train/test split separates data for learning and final checking.",
        "types": ["Training data", "Testing data", "Common split: 80/20"],
        "syntax": "train_test_split(X, y, test_size=0.2)",
        "example": "from sklearn.model_selection import train_test_split\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)",
        "output": "Training and testing sets",
        "explanation": "The model learns from training data and is checked on separate test data.",
        "ml": "This helps measure how well the model generalizes to unseen data.",
    },
    "Preprocessing": {
        "concept": "Preprocessing transforms raw data into a form suitable for ML.",
        "types": ["Missing values", "Encoding", "Scaling", "Feature preparation"],
        "syntax": "Clean → Transform → Model-ready data",
        "example": "Raw Data → Clean → Encode → Scale → Model",
        "output": "Prepared features",
        "explanation": "Preprocessing makes data consistent and usable by the chosen algorithm.",
        "ml": "Good preprocessing is often essential for model performance.",
    },
    "Scaling": {
        "concept": "Scaling puts numerical features onto comparable ranges.",
        "types": ["Standardization", "Normalization"],
        "syntax": "scaler.fit_transform(X_train)",
        "example": "from sklearn.preprocessing import StandardScaler\nscaler = StandardScaler()\nX_scaled = scaler.fit_transform(X)",
        "output": "Scaled numerical features",
        "explanation": "Standardization commonly transforms values to have mean near 0 and standard deviation near 1.",
        "ml": "Scaling is important for algorithms such as KNN, SVM and K-Means.",
    },
    "Create Model": {
        "concept": "Creating a model means choosing an algorithm and initializing it.",
        "types": ["Regression model", "Classification model", "Clustering model"],
        "syntax": "model = LinearRegression()",
        "example": "from sklearn.linear_model import LinearRegression\nmodel = LinearRegression()\nprint(model)",
        "output": "LinearRegression()",
        "explanation": "The model object is ready to learn from training data.",
        "ml": "The algorithm should match the ML problem you are solving.",
    },
    "fit()": {
        "concept": "fit() trains a model using data.",
        "types": ["Input X", "Target y", "Learn parameters"],
        "syntax": "model.fit(X_train, y_train)",
        "example": "model.fit(X_train, y_train)\nprint('Model trained')",
        "output": "Model trained",
        "explanation": "fit() is where the model learns patterns from the training data.",
        "ml": "It is one of the most important methods in Scikit-learn.",
    },
    "Training Data": {
        "concept": "Training data is the portion of the dataset used to teach the model.",
        "types": ["X_train", "y_train", "Learning examples"],
        "syntax": "model.fit(X_train, y_train)",
        "example": "X_train = [[1], [2], [3]]\ny_train = [2, 4, 6]\nprint(len(X_train))",
        "output": "3",
        "explanation": "Training examples contain inputs and, for supervised learning, their known targets.",
        "ml": "The quality of training data strongly affects what the model learns.",
    },
    "Accuracy": {
        "concept": "Accuracy is the fraction of classification predictions that are correct.",
        "types": ["Correct predictions", "Total predictions"],
        "syntax": "accuracy_score(y_test, y_pred)",
        "example": "from sklearn.metrics import accuracy_score\nprint(accuracy_score([1,1,0], [1,0,0]))",
        "output": "0.666...",
        "explanation": "Accuracy is correct predictions divided by total predictions.",
        "ml": "Useful for many balanced classification problems, but not every dataset.",
    },
    "Precision": {
        "concept": "Precision tells us how many predicted positive cases were actually positive.",
        "types": ["True positives", "False positives"],
        "syntax": "precision_score(y_test, y_pred)",
        "example": "Precision = True Positives / (True Positives + False Positives)",
        "output": "A value between 0 and 1",
        "explanation": "Higher precision means fewer false positive predictions among predicted positives.",
        "ml": "Useful when false positive predictions are important.",
    },
    "Recall": {
        "concept": "Recall tells us how many actual positive cases the model found.",
        "types": ["True positives", "False negatives"],
        "syntax": "recall_score(y_test, y_pred)",
        "example": "Recall = True Positives / (True Positives + False Negatives)",
        "output": "A value between 0 and 1",
        "explanation": "Higher recall means fewer actual positive cases are missed.",
        "ml": "Useful when missing a positive case is costly.",
    },
    "MAE": {
        "concept": "MAE measures the average absolute difference between actual and predicted values.",
        "types": ["Absolute error", "Average error"],
        "syntax": "mean_absolute_error(y_test, y_pred)",
        "example": "Actual = [100, 200]\nPredicted = [90, 210]\n\nMAE = (10 + 10) / 2",
        "output": "10.0",
        "explanation": "MAE is easy to interpret because it uses the same units as the target.",
        "ml": "Commonly used to evaluate regression models.",
    },
    "MSE": {
        "concept": "MSE is the average of squared prediction errors.",
        "types": ["Error", "Square error", "Average"],
        "syntax": "mean_squared_error(y_test, y_pred)",
        "example": "Actual = [10, 20]\nPredicted = [8, 22]\n\nMSE = (4 + 4) / 2",
        "output": "4.0",
        "explanation": "Squaring makes larger errors contribute more strongly.",
        "ml": "A common regression evaluation metric.",
    },
    "R²": {
        "concept": "R² measures how much of the target variation is explained by a regression model.",
        "types": ["Regression metric", "Explained variation"],
        "syntax": "r2_score(y_test, y_pred)",
        "example": "from sklearn.metrics import r2_score\nprint(r2_score([1,2,3], [1,2,3]))",
        "output": "1.0",
        "explanation": "An R² value of 1 means the predictions match the provided values perfectly.",
        "ml": "R² is commonly reported for regression models.",
    },
    "Overfitting": {
        "concept": "Overfitting happens when a model learns training data too closely and performs poorly on new data.",
        "types": ["Training performance high", "Testing performance lower"],
        "syntax": "Train → very good\nTest → poor",
        "example": "Training accuracy = 99%\nTesting accuracy = 72%",
        "output": "Possible overfitting",
        "explanation": "The model may have learned noise or very specific details instead of general patterns.",
        "ml": "Use validation, regularization, simpler models or more data when appropriate.",
    },
    "Underfitting": {
        "concept": "Underfitting happens when a model is too simple to learn the important pattern.",
        "types": ["Training performance poor", "Testing performance poor"],
        "syntax": "Train → poor\nTest → poor",
        "example": "Training accuracy = 60%\nTesting accuracy = 58%",
        "output": "Possible underfitting",
        "explanation": "The model has not captured enough useful structure from the data.",
        "ml": "A more suitable model or useful features may help.",
    },
    "Import Model": {
        "concept": "Scikit-learn models are imported from their module before use.",
        "types": ["Regression models", "Classification models", "Clustering models"],
        "syntax": "from sklearn.linear_model import LinearRegression",
        "example": "from sklearn.linear_model import LinearRegression\nmodel = LinearRegression()\nprint(model)",
        "output": "LinearRegression()",
        "explanation": "Importing makes the selected algorithm available in the Python program.",
        "ml": "Different problems require different Scikit-learn algorithms.",
    },
    "predict()": {
        "concept": "predict() generates outputs from a trained model for new input data.",
        "types": ["New features", "Predicted value", "Predicted class"],
        "syntax": "model.predict(X_test)",
        "example": "model.fit(X_train, y_train)\npredictions = model.predict(X_test)\nprint(predictions)",
        "output": "Model predictions",
        "explanation": "predict() applies learned model parameters to new input data.",
        "ml": "Prediction is the main way an application uses a trained ML model.",
    },
    "Collect Data": {
        "concept": "Collect data from a file, database, API, sensor or another source.",
        "types": ["CSV / files", "Database", "API / sensor"],
        "syntax": "Source → Dataset",
        "example": "CSV / Database / API → pandas DataFrame",
        "output": "Raw dataset",
        "explanation": "A project starts with useful data related to the problem.",
        "ml": "Good data is the starting point of a good ML workflow.",
    },
    "Clean Data": {
        "concept": "Clean raw data by handling missing, duplicate or incorrect values.",
        "types": ["Missing values", "Duplicates", "Invalid values"],
        "syntax": "Raw Data → Clean Data",
        "example": "df.drop_duplicates()\ndf.fillna(0)",
        "output": "Cleaner dataset",
        "explanation": "Cleaning reduces data problems before analysis and training.",
        "ml": "Clean datasets make model training more reliable.",
    },
    "Explore Data": {
        "concept": "Explore the dataset to understand its columns, values and patterns.",
        "types": ["head()", "describe()", "Charts"],
        "syntax": "df.head()\ndf.describe()",
        "example": "print(df.head())\nprint(df.describe())",
        "output": "Dataset overview",
        "explanation": "Exploration helps identify distributions, outliers and relationships.",
        "ml": "EDA helps decide which features and preprocessing steps are useful.",
    },
    "Prepare Data": {
        "concept": "Prepare features and targets in the format required by the model.",
        "types": ["Features", "Target", "Encoding", "Scaling"],
        "syntax": "X = features\ny = target",
        "example": "X = df[['area','rooms']]\ny = df['price']",
        "output": "X and y",
        "explanation": "Preparation converts cleaned data into model-ready inputs and targets.",
        "ml": "This step connects data analysis to model training.",
    },
    "Train Model": {
        "concept": "Train the selected model using the training data.",
        "types": ["Choose algorithm", "Create model", "fit()"],
        "syntax": "model.fit(X_train, y_train)",
        "example": "model = LinearRegression()\nmodel.fit(X_train, y_train)",
        "output": "Trained model",
        "explanation": "The algorithm learns patterns from the training examples.",
        "ml": "Training is the learning stage of the ML workflow.",
    },
    "Evaluate Model": {
        "concept": "Evaluate the trained model using suitable metrics and unseen data.",
        "types": ["Classification metrics", "Regression metrics"],
        "syntax": "Actual vs Predicted",
        "example": "y_pred = model.predict(X_test)\n# calculate a metric",
        "output": "Evaluation score",
        "explanation": "Evaluation shows how well the model performs on data it did not train on.",
        "ml": "Evaluation helps compare models and identify learning problems.",
    },
    "Predict": {
        "concept": "Use the trained model to predict a result for new data.",
        "types": ["New input", "predict()", "Result"],
        "syntax": "model.predict(new_data)",
        "example": "new_data = [[1500, 3]]\nprediction = model.predict(new_data)\nprint(prediction)",
        "output": "Prediction",
        "explanation": "The trained model applies what it learned to new input data.",
        "ml": "Prediction connects the ML model to a real application.",
    },
}


# =========================================================
# FILL ANY REMAINING SUBTOPICS WITH THEIR PARENT LESSON
# =========================================================

for _, parents in COURSE.items():
    for parent, children in parents.items():
        parent_lesson = LESSONS[parent]
        for child in children:
            if child not in SUBLESSONS:
                SUBLESSONS[child] = {
                    "concept": f"{child} is an important part of {parent}.",
                    "types": [child, f"Part of {parent}"],
                    "syntax": parent_lesson["syntax"],
                    "example": parent_lesson["example"],
                    "output": parent_lesson["output"],
                    "explanation": parent_lesson["explanation"],
                    "ml": parent_lesson["ml"],
                }


# =========================================================
# NAVIGATION DATA
# =========================================================

LESSON_ORDER = []
for _, parents in COURSE.items():
    for parent, children in parents.items():
        LESSON_ORDER.append(parent)
        LESSON_ORDER.extend(children)


PARENT_LOOKUP = {}
for _, parents in COURSE.items():
    for parent, children in parents.items():
        PARENT_LOOKUP[parent] = parent
        for child in children:
            PARENT_LOOKUP[child] = parent


LEVEL_LOOKUP = {}
for level, parents in COURSE.items():
    for parent, children in parents.items():
        LEVEL_LOOKUP[parent] = level
        for child in children:
            LEVEL_LOOKUP[child] = level


# =========================================================
# SESSION STATE
# =========================================================

if "current" not in st.session_state:
    st.session_state.current = "Python Basics"

if "output" not in st.session_state:
    st.session_state.output = ""

if "expanded" not in st.session_state:
    st.session_state.expanded = {
        parent: parent == "Python Basics"
        for parents in COURSE.values()
        for parent in parents
    }


# =========================================================
# HELPERS
# =========================================================

def goto(name):
    st.session_state.current = name
    st.session_state.output = ""


def lesson_for(name):
    if name in LESSONS:
        return LESSONS[name]
    return SUBLESSONS[name]


def safe_html(text):
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


# =========================================================


# =========================================================
# FINAL W3SCHOOLS-STYLE UI
# =========================================================

st.markdown(
    """
    <style>
    :root {
        --bg: #07101b;
        --panel: #0b1624;
        --panel-2: #0f1b2b;
        --border: #223650;
        --text: #f5f8fc;
        --muted: #8ea0b7;
        --blue: #1877f2;
        --green: #18c48f;
    }

    .stApp {
        background:
            radial-gradient(circle at 70% -10%, rgba(37,99,235,.08), transparent 30%),
            var(--bg);
        color: var(--text);
    }

    .block-container {
        max-width: 1480px;
        padding: .55rem .75rem 2rem;
    }

    section[data-testid="stSidebar"] {
        width:285px !important;
        min-width:285px !important;
        max-width:285px !important;
        background:#081321;
        border-right:1px solid #1d3048;
    }

    section[data-testid="stSidebar"] > div {
        width:285px !important;
    }

    section[data-testid="stSidebar"] .block-container {
        padding:.75rem .65rem 1.5rem;
    }

    .side-brand { padding:5px 8px 12px; }

    .side-brand-row {
        display:flex;
        align-items:center;
        gap:10px;
    }

    .side-logo {
        width:36px;
        height:36px;
        display:flex;
        align-items:center;
        justify-content:center;
        border-radius:9px;
        background:linear-gradient(135deg,#2563eb,#0ea5e9);
        color:white;
        font-size:15px;
        font-weight:800;
    }

    .side-title {
        font-size:19px;
        font-weight:800;
        color:#f8fafc;
    }

    .side-subtitle {
        font-size:11px;
        color:#91a3b9;
        margin-left:46px;
        margin-top:-2px;
    }

    section[data-testid="stSidebar"] hr {
        border-color:#1d2d43;
        margin:8px 4px 12px;
    }

    section[data-testid="stSidebar"] .stButton {
        margin:0 !important;
        padding:0 !important;
    }

    section[data-testid="stSidebar"] .stButton button {
        width:100% !important;
        min-height:34px !important;
        height:34px !important;
        padding:5px 10px !important;
        margin:2px 0 !important;
        border-radius:6px !important;
        border:1px solid transparent !important;
        background:transparent !important;
        color:#c4d0df !important;
        font-size:13px !important;
        font-weight:550 !important;
        text-align:left !important;
        box-shadow:none !important;
    }

    section[data-testid="stSidebar"] .stButton button:hover {
        background:#102238 !important;
        border-color:#203b5b !important;
        color:#ffffff !important;
    }

    section[data-testid="stSidebar"] .stButton button[kind="primary"] {
        background:#12345a !important;
        border-color:#2478dc !important;
        color:#ffffff !important;
        font-weight:700 !important;
    }

    .sidebar-level {
        color:#8ea4bd;
        font-size:12px;
        font-weight:800;
        letter-spacing:.2px;
        margin:12px 8px 7px;
        text-transform:uppercase;
    }

    .sidebar-parent-label {
        color:#a9bad0;
        font-size:12px;
        font-weight:700;
        margin:5px 8px 3px;
    }

    .topbar {
        height:50px;
        display:flex;
        align-items:center;
        gap:12px;
        border-bottom:1px solid #17273b;
        margin-bottom:10px;
    }

    .top-search-label {
        height:34px;
        display:flex;
        align-items:center;
        padding:0 13px;
        border:1px solid #203651;
        border-radius:6px;
        background:#0d1a2b;
        color:#72859d;
        font-size:11px;
    }

    .top-icon {
        width:34px;
        height:34px;
        display:flex;
        align-items:center;
        justify-content:center;
        border:1px solid #203651;
        border-radius:6px;
        background:#0d1a2b;
        color:#d7e2ef;
        font-size:15px;
    }

    .user-chip {
        height:34px;
        display:flex;
        align-items:center;
        gap:7px;
        padding:0 8px;
        border:1px solid #203651;
        border-radius:7px;
        background:#0d1a2b;
    }

    .user-avatar {
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
        font-weight:700;
        color:#eaf1fa;
    }

    .user-sub {
        font-size:8px;
        color:#7f91a8;
    }

    .breadcrumb {
        font-size:13px;
        color:#8fa5be;
        margin:5px 0 11px;
    }

    .breadcrumb strong {
        color:#a9bdd6;
    }

    .lesson-title {
        font-size:30px;
        line-height:1.15;
        font-weight:800;
        color:#f8fafc;
        margin:0;
    }

    .lesson-desc {
        font-size:13px;
        color:#9aadc3;
        margin-top:6px;
        line-height:1.45;
    }

    .lesson-card {
        background:linear-gradient(145deg,#0d1a2a,#0a1523);
        border:1px solid var(--border);
        border-radius:7px;
        padding:11px 13px;
        margin-bottom:9px;
    }

    .lesson-label {
        color:#f3f7fb;
        font-size:16px;
        font-weight:750;
        margin-bottom:7px;
    }

    .lesson-body {
        color:#cdd9e7;
        font-size:14px;
        line-height:1.6;
        white-space:pre-line;
    }

    .topic-list-card {
        background:#0a1625;
        border:1px solid var(--border);
        border-radius:7px;
        padding:10px 12px;
        margin-bottom:9px;
    }

    .topic-item {
        background:#091321;
        border:1px solid #1b3049;
        border-radius:5px;
        padding:6px 8px;
        margin:4px 0;
        color:#c8d8ea;
        font-size:13px;
    }

    .ml-card {
        background:linear-gradient(145deg,#0b201b,#091914);
        border:1px solid #20513f;
        border-left:3px solid var(--green);
        border-radius:7px;
        padding:10px 12px;
        margin-top:9px;
    }

    .ml-label {
        color:#7ff0c2;
        font-size:14px;
        font-weight:750;
        margin-bottom:5px;
    }

    .editor-shell {
        background:#091321;
        border:1px solid var(--border);
        border-radius:8px;
        overflow:hidden;
    }

    .editor-top {
        padding:8px 10px;
        border-bottom:1px solid #1b2c43;
        background:#0c1727;
        color:#eef5fc;
        font-size:13px;
        font-weight:700;
    }

    .editor-sub {
        color:#8498b0;
        font-size:10px;
        font-weight:400;
        margin-top:2px;
    }

    .output-shell {
        background:#091321;
        border:1px solid var(--border);
        border-radius:8px;
        padding:9px 10px;
        margin-top:9px;
    }

    .output-head {
        display:flex;
        align-items:center;
        justify-content:space-between;
        margin-bottom:5px;
    }

    .output-title {
        color:#eef5fc;
        font-size:13px;
        font-weight:750;
    }

    .success-badge {
        color:#37df9d;
        font-size:9px;
    }

    div[data-testid="stCode"] {
        border:1px solid #1d324b;
        border-radius:6px;
        margin:3px 0 10px;
    }

    div[data-testid="stCode"] pre {
        font-size:11px !important;
        line-height:1.45 !important;
    }

    textarea {
        font-size:12px !important;
        line-height:1.55 !important;
        font-family:Consolas, "Courier New", monospace !important;
    }

    .stButton button {
        min-height:36px;
        border-radius:5px;
        border:1px solid #263c59;
        background:#0e1928;
        color:#e5edf7;
        font-size:12px;
        font-weight:650;
        padding:5px 11px;
    }

    .stButton button:hover {
        border-color:#2d76dc;
        color:white;
        background:#14243a;
    }

    div[data-testid="stButton"] button[kind="primary"] {
        background:#1677f2;
        border-color:#1677f2;
        color:white;
    }

    button[data-baseweb="tab"] {
        font-size:12px !important;
        color:#a9b9ca !important;
        padding:7px 9px !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color:#f8fafc !important;
    }

    div[data-testid="stProgress"] {
        margin:4px 0 8px;
    }

    div[data-testid="stProgress"] p {
        font-size:12px !important;
        color:#9aadc3 !important;
    }

    #MainMenu,
    footer {
        visibility:hidden;
    }

    @media (max-width: 900px) {
        .top-search-label { display:none; }
        .user-name,.user-sub { display:none; }
        .lesson-title { font-size:22px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SIDEBAR
# =========================================================

current = st.session_state.current

with st.sidebar:

    st.markdown(
        """
        <div class="side-brand">
            <div class="side-brand-row">
                <div class="side-logo">&lt;/&gt;</div>
                <div class="side-title">CodePractice</div>
            </div>
            <div class="side-subtitle">Learn. Practice. Grow.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    if st.button(
        "←  Dashboard",
        key="python_dashboard_back",
        use_container_width=True,
    ):
        st.switch_page(st.session_state["dashboard_page"])

    st.markdown("---")

    st.markdown(
        """
        <div style="
            display:flex;
            align-items:center;
            gap:8px;
            padding:0 7px 5px;
            color:#f1f6fc;
            font-size:15px;
            font-weight:800;
        ">
            🐍 Python
        </div>
        """,
        unsafe_allow_html=True,
    )

    for level, parents in COURSE.items():

        st.markdown(
            f'<div class="sidebar-level">{safe_html(level)}</div>',
            unsafe_allow_html=True,
        )

        for parent, children in parents.items():

            expanded = st.session_state.expanded.get(parent, False)

            if st.button(
                ("▼  " if expanded else "▶  ") + parent,
                key=f"expand_{parent}",
                use_container_width=True,
            ):
                st.session_state.expanded[parent] = not expanded
                st.rerun()

            if expanded:
                for child in children:
                    is_current = current == child

                    if st.button(
                        ("●  " if is_current else "   ") + child,
                        key=f"child_{parent}_{child}",
                        use_container_width=True,
                        type="primary" if is_current else "secondary",
                    ):
                        goto(child)
                        st.rerun()


# =========================================================
# TOP BAR
# =========================================================

top_search, bell, user = st.columns([7.5, .45, 1.7], gap="small")

with top_search:
    st.markdown(
        """
        <div class="top-search-label">
            🔍 &nbsp; Search topics (e.g. loops, functions, NumPy, Pandas, ML...)
        </div>
        """,
        unsafe_allow_html=True,
    )

with bell:
    st.markdown(
        '<div class="top-icon">♧</div>',
        unsafe_allow_html=True,
    )

with user:
    st.markdown(
        """
        <div class="user-chip">
            <div class="user-avatar">P</div>
            <div>
                <div class="user-name">Priyanka</div>
                <div class="user-sub">Keep Learning ✨</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# CURRENT LESSON / PROGRESS
# =========================================================

current = st.session_state.current
lesson = lesson_for(current)

mark_python_lesson_started(current)

index = LESSON_ORDER.index(current)
total = len(LESSON_ORDER)
progress = (index + 1) / total

level_name = LEVEL_LOOKUP[current]
parent_name = PARENT_LOOKUP[current]

st.markdown(
    f"""
    <div class="breadcrumb">
        🏠 &nbsp; <strong>Python</strong>
        &nbsp;›&nbsp; <strong>{safe_html(parent_name)}</strong>
        &nbsp;›&nbsp; {safe_html(current)}
    </div>
    """,
    unsafe_allow_html=True,
)

st.progress(
    progress,
    text=f"Course Progress  •  {index + 1} / {total} lessons",
)


# =========================================================
# NAVIGATION
# =========================================================

previous_name = LESSON_ORDER[index - 1] if index > 0 else None
next_name = LESSON_ORDER[index + 1] if index < total - 1 else None


# =========================================================
# MAIN WORKSPACE
# =========================================================

lesson_col, editor_col = st.columns(
    [1.55, 1],
    gap="small",
)


# =========================================================
# LESSON
# =========================================================

with lesson_col:

    nav1, title_col, nav2 = st.columns(
        [1.0, 3.0, 1.0],
        gap="small",
    )

    with nav1:
        if previous_name:
            if st.button("‹ Previous", use_container_width=True):
                goto(previous_name)
                st.rerun()

    with title_col:
        st.markdown(
            f"""
            <div>
                <div class="lesson-title">
                    {safe_html(current)}
                </div>
                <div class="lesson-desc">
                    {safe_html(lesson["concept"])}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with nav2:
        if next_name:
            if st.button("Next ›", use_container_width=True):
                goto(next_name)
                st.rerun()
            
                        

    st.markdown(
        '<div class="lesson-label" style="margin-top:12px;">Example</div>',
        unsafe_allow_html=True,
    )

    st.code(lesson["example"], language="python")

    st.markdown(
        f"""
        <div class="topic-list-card">
            <div style="
                color:#879ab2;
                font-size:10px;
                font-weight:700;
                margin-bottom:4px;
            ">
                OUTPUT
            </div>
            <div style="
                color:#d7e5f3;
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
        <div class="lesson-card">
            <div class="lesson-label">📖 Main Concept</div>
            <div class="lesson-body">
                {safe_html(lesson["concept"])}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    parent_children = None
    for _, parents in COURSE.items():
        if parent_name in parents:
            parent_children = parents[parent_name]
            break

    if parent_children:

        topic_items = "".join(
            f'<div class="topic-item">• {safe_html(item)}</div>'
            for item in parent_children
        )

        st.markdown(
            f"""
            <div class="topic-list-card">
                <div class="lesson-label">
                    🧩 {safe_html(parent_name)}
                </div>
                {topic_items}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
        <div class="lesson-card">
            <div class="lesson-label">💡 Simple Explanation</div>
            <div class="lesson-body">
                {safe_html(lesson["explanation"])}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="lesson-label">💻 Syntax</div>',
        unsafe_allow_html=True,
    )

    st.code(lesson["syntax"], language="python")

    st.markdown(
        f"""
        <div class="ml-card">
            <div class="ml-label">🤖 Use in Machine Learning</div>
            <div class="lesson-body">
                {safe_html(lesson["ml"])}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if next_name:

        next_parent = PARENT_LOOKUP[next_name]

        st.markdown(
            f"""
            <div style="
                margin-top:11px;
                padding:10px 12px;
                border:1px solid #203650;
                border-radius:7px;
                background:#0b1726;
            ">
                <div style="font-size:9px;color:#72859d;text-transform:uppercase;">
                    Next Topic
                </div>
                <div style="margin-top:3px;color:#f1f6fc;font-size:13px;font-weight:750;">
                    🚀 {safe_html(next_name)}
                </div>
                <div style="margin-top:2px;color:#7f91a8;font-size:9px;">
                    {safe_html(next_parent)}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

                

# =========================================================
# EDITOR
# =========================================================

with editor_col:

    tab_try, tab_challenge, tab_notes, tab_bookmark = st.tabs(
        [
            "▶ Try Yourself",
            "🏆 Code Challenge",
            "📝 Notes",
            "🔖 Bookmark",
        ]
    )

    # =====================================================
    # TRY YOURSELF
    # DO NOT CHANGE THIS SECTION
    # =====================================================

    with tab_try:

        st.markdown(
            """
            <div class="editor-shell">
                <div class="editor-top">
                    ▶ Try Yourself
                    <div class="editor-sub">
                        Change the code and run it.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        code = st.text_area(
            "Python Code Editor",
            value=lesson["example"],
            height=265,
            key=f"editor_{current}",
            label_visibility="collapsed",
        )

        run_col, clear_col, copy_col = st.columns(
            [1, 1, 1],
            gap="small",
        )

        with run_col:

            run_button = st.button(
                "▶ Run",
                use_container_width=True,
                type="primary",
            )

        with clear_col:

            clear_button = st.button(
                "↻ Clear",
                use_container_width=True,
            )

        with copy_col:

            st.button(
                "▣ Copy",
                use_container_width=True,
                disabled=True,
            )

        if clear_button:

            st.session_state.output = ""
            st.rerun()

        if run_button:

            temp_path = None

            try:

                with tempfile.NamedTemporaryFile(
                    mode="w",
                    suffix=".py",
                    delete=False,
                    encoding="utf-8",
                ) as file:

                    file.write(code)
                    temp_path = file.name

                result = subprocess.run(
                    [sys.executable, temp_path],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )

                if result.returncode == 0:

                    st.session_state.output = (
                        result.stdout.strip()
                        or "Run successful — no output."
                    )
                    
                    save_python_progress(current)
                    
                else:

                    st.session_state.output = result.stderr.strip()

            except subprocess.TimeoutExpired:

                st.session_state.output = (
                    "Execution stopped: code took too long."
                )

            except Exception as error:

                st.session_state.output = f"Error: {error}"

            finally:

                if temp_path and os.path.exists(temp_path):
                    os.remove(temp_path)

        st.markdown(
            """
            <div class="output-shell">
                <div class="output-head">
                    <div class="output-title">Output</div>
                    <div class="success-badge">● Run Ready</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.session_state.output:

            st.code(
                st.session_state.output,
                language="text",
            )

        else:

            st.markdown(
                """
                <div class="lesson-card">
                    <div class="lesson-body">
                        Run your code to see the output here.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # =========================================================
# CODE CHALLENGE
# =========================================================

with tab_challenge:

    st.markdown(
        "### 🏆 Code Challenge"
    )

    st.caption(
        "Complete this small task without copying the example."
    )

    # -----------------------------------------------------
    # CHALLENGE DATA
    # -----------------------------------------------------

    challenge_data = {

        "Python Basics": {
            "task": (
                "Create a variable called name and store your "
                "name in it. Print the name."
            ),
            "hint": "Use a variable and print().",
            "expected_output": "Priyanka",
        },

        "Variables": {
            "task": (
                "Create two variables: name and age. "
                "Print both values."
            ),
            "hint": 'Example: name = "Priyanka"',
            "expected_output": "Priyanka\n27",
        },

        "Data Types": {
            "task": (
                "Create one string, one integer and one float. "
                "Print the type of each value using type()."
            ),
            "hint": "Use type(value).",
            "expected_output": "<class 'str'>\n<class 'int'>\n<class 'float'>",
        },

        "Input / Output": {
            "task": (
                "Ask the user for their name using input() "
                "and print a welcome message."
            ),
            "hint": "Use input() and print().",
            "expected_output": None,
        },

        "Arithmetic Operators": {
            "task": (
                "Create two numbers and print their addition, "
                "subtraction and multiplication."
            ),
            "hint": "Use +, - and *.",
            "expected_output": None,
        },

        "Comparison Operators": {
            "task": (
                "Create two numbers and check whether the "
                "first number is greater than the second."
            ),
            "hint": "Use the > operator.",
            "expected_output": None,
        },

        "Logical Operators": {
            "task": (
                "Create two boolean variables and print the "
                "result of using the and operator."
            ),
            "hint": "Example: True and False",
            "expected_output": None,
        },

        "if / elif / else": {
            "task": (
                "Create an age variable. Print 'Adult' if "
                "age is 18 or more, otherwise print 'Minor'."
            ),
            "hint": "Use if and else.",
            "expected_output": None,
        },

        "for Loop": {
            "task": (
                "Use a for loop to print the numbers from 1 to 5."
            ),
            "hint": "Use range(1, 6).",
            "expected_output": "1\n2\n3\n4\n5",
        },

        "while Loop": {
            "task": (
                "Use a while loop to print the numbers from 1 to 5."
            ),
            "hint": "Remember to increase the counter.",
            "expected_output": "1\n2\n3\n4\n5",
        },

        "Lists": {
            "task": (
                "Create a list containing 3 numbers and print "
                "the list and its length."
            ),
            "hint": "Use len().",
            "expected_output": None,
        },

        "Tuples": {
            "task": (
                "Create a tuple containing 3 values and print "
                "the tuple."
            ),
            "hint": "Use parentheses ().",
            "expected_output": None,
        },

        "Dictionaries": {
            "task": (
                "Create a dictionary containing name and age. "
                "Print the name value."
            ),
            "hint": "Use dictionary keys.",
            "expected_output": None,
        },

        "Sets": {
            "task": (
                "Create a set containing duplicate numbers "
                "and print the set."
            ),
            "hint": "Sets keep only unique values.",
            "expected_output": None,
        },

        "Define Function": {
            "task": (
                "Create a function called greet() that prints "
                "'Hello Python'. Call the function."
            ),
            "hint": "Use def.",
            "expected_output": "Hello Python",
        },

        "Arguments": {
            "task": (
                "Create a function that accepts two numbers "
                "and prints their sum."
            ),
            "hint": "Use function arguments.",
            "expected_output": None,
        },

        "Return Value": {
            "task": (
                "Create a function that accepts two numbers "
                "and returns their sum. Print the result."
            ),
            "hint": "Use return.",
            "expected_output": None,
        },

        "Lambda": {
            "task": (
                "Create a lambda function that multiplies "
                "two numbers and print the result."
            ),
            "hint": "Example: lambda a, b: a * b",
            "expected_output": None,
        },
    }

    challenge = challenge_data.get(
        current,
        {
            "task": (
                f"Write a small Python program that demonstrates "
                f"the topic: {current}."
            ),
            "hint": (
                f"Use the concepts you learned in {current}."
            ),
            "expected_output": None,
        },
    )

    # -----------------------------------------------------
    # TASK
    # -----------------------------------------------------

    st.info(
        f"🎯 **Your Task**\n\n{challenge['task']}"
    )

    st.caption(
        f"💡 Hint: {challenge['hint']}"
    )

    # -----------------------------------------------------
    # CHALLENGE EDITOR
    # -----------------------------------------------------

    challenge_code = st.text_area(
        "Write your solution",
        height=190,
        key=f"challenge_code_{current}",
        placeholder="Write your Python solution here...",
        label_visibility="collapsed",
    )

    challenge_run_col, challenge_clear_col = st.columns(
        [1, 1],
        gap="small",
    )

    with challenge_run_col:

        challenge_run = st.button(
            "▶ Run Challenge",
            key=f"challenge_run_{current}",
            use_container_width=True,
            type="primary",
        )

    with challenge_clear_col:

        challenge_clear = st.button(
            "↻ Clear",
            key=f"challenge_clear_{current}",
            use_container_width=True,
        )

    # -----------------------------------------------------
    # CLEAR
    # -----------------------------------------------------

    if challenge_clear:

        st.session_state[
            f"challenge_result_{current}"
        ] = ""

        st.session_state[
            f"challenge_status_{current}"
        ] = ""

        st.rerun()

    # -----------------------------------------------------
    # RUN CHALLENGE
    # -----------------------------------------------------

    if challenge_run:

        if not challenge_code.strip():

            st.warning(
                "Please write your solution first."
            )

        else:

            challenge_temp_path = None

            try:

                with tempfile.NamedTemporaryFile(
                    mode="w",
                    suffix=".py",
                    delete=False,
                    encoding="utf-8",
                ) as file:

                    file.write(challenge_code)
                    challenge_temp_path = file.name

                challenge_result = subprocess.run(
                    [
                        sys.executable,
                        challenge_temp_path,
                    ],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )

                if challenge_result.returncode == 0:

                    challenge_output = (
                        challenge_result.stdout.strip()
                        or "Code executed successfully."
                    )

                    st.session_state[
                        f"challenge_result_{current}"
                    ] = challenge_output

                    # -------------------------------------
                    # CHECK ANSWER
                    # -------------------------------------

                    expected_output = challenge.get(
                        "expected_output"
                    )

                    if expected_output is not None:

                        actual = challenge_output.strip()
                        expected = expected_output.strip()

                        if actual == expected:

                            st.session_state[
                                f"challenge_status_{current}"
                            ] = "correct"

                        else:

                            st.session_state[
                                f"challenge_status_{current}"
                            ] = "incorrect"

                    else:

                        # Some challenges need flexible
                        # answers, so we only confirm that
                        # the code executed successfully.
                        st.session_state[
                            f"challenge_status_{current}"
                        ] = "executed"

                else:

                    st.session_state[
                        f"challenge_result_{current}"
                    ] = challenge_result.stderr.strip()

                    st.session_state[
                        f"challenge_status_{current}"
                    ] = "error"

            except subprocess.TimeoutExpired:

                st.session_state[
                    f"challenge_result_{current}"
                ] = (
                    "Execution stopped: code took too long."
                )

                st.session_state[
                    f"challenge_status_{current}"
                ] = "error"

            except Exception as error:

                st.session_state[
                    f"challenge_result_{current}"
                ] = f"Error: {error}"

                st.session_state[
                    f"challenge_status_{current}"
                ] = "error"

            finally:

                if (
                    challenge_temp_path
                    and os.path.exists(challenge_temp_path)
                ):

                    os.remove(challenge_temp_path)

    # -----------------------------------------------------
    # RESULT
    # -----------------------------------------------------

    challenge_result = st.session_state.get(
        f"challenge_result_{current}",
        "",
    )

    challenge_status = st.session_state.get(
        f"challenge_status_{current}",
        "",
    )

    if challenge_result:

        st.markdown(
            "#### 📤 Challenge Output"
        )

        st.code(
            challenge_result,
            language="text",
        )

        # ---------------------------------------------
        # CORRECT
        # ---------------------------------------------

        if challenge_status == "correct":

            st.success(
                "🎉 Correct! Challenge completed successfully."
            )

        # ---------------------------------------------
        # INCORRECT
        # ---------------------------------------------

        elif challenge_status == "incorrect":

            st.warning(
                "❌ Not quite. Your code ran successfully, "
                "but the output does not match the expected answer. "
                "Try again!"
            )

        # ---------------------------------------------
        # FLEXIBLE ANSWER
        # ---------------------------------------------

        elif challenge_status == "executed":

            st.info(
                "✓ Your code executed successfully. "
                "Check the output and compare it with the task."
            )

        # ---------------------------------------------
        # ERROR
        # ---------------------------------------------

        elif challenge_status == "error":

            st.error(
                "❌ There is an error in your code. "
                "Read the output above and try again."
            )

    # =====================================================
# NOTES
# =====================================================

with tab_notes:

    st.markdown(
        "### 📝 Notes"
    )

    st.caption(
        "Write and save your personal notes for this topic."
    )

    # -------------------------------------------------
    # NOTE STORAGE
    # -------------------------------------------------

    note_key = f"notes_{current}"

    if note_key not in st.session_state:

        st.session_state[note_key] = ""

    # -------------------------------------------------
    # CURRENT TOPIC
    # -------------------------------------------------

    st.info(
        f"📚 **Current Topic:** {current}"
    )

    # -------------------------------------------------
    # NOTE EDITOR
    # -------------------------------------------------

    notes = st.text_area(
        "Your Notes",
        value=st.session_state[note_key],
        height=230,
        key=f"notes_editor_{current}",
        placeholder=(
            "Write your notes here...\n\n"
            "Example:\n"
            "• A variable stores a value.\n"
            "• Variables can store different data types.\n"
            "• Use print() to display a value."
        ),
        label_visibility="collapsed",
    )

    # -------------------------------------------------
    # NOTE ACTIONS
    # -------------------------------------------------

    save_note_col, clear_note_col = st.columns(
        [1, 1],
        gap="small",
    )

    with save_note_col:

        if st.button(
            "💾 Save Note",
            key=f"save_note_{current}",
            use_container_width=True,
            type="primary",
        ):

            st.session_state[note_key] = notes

            st.success(
                "✓ Note saved for this topic."
            )

    with clear_note_col:

        if st.button(
            "↻ Clear Note",
            key=f"clear_note_{current}",
            use_container_width=True,
        ):

            st.session_state[note_key] = ""

            st.rerun()

    # -------------------------------------------------
    # SAVED NOTE STATUS
    # -------------------------------------------------

    if st.session_state[note_key].strip():

        st.caption(
            "✓ You have a saved note for this topic."
        )

    else:

        st.caption(
            "No note saved yet."
        )

# =========================================================
# BOOKMARK TAB
# =========================================================

with tab_bookmark:

    # =====================================================
    # BOOKMARK DATABASE HELPERS
    # =====================================================

    def bookmark_get_user_id():

        connection = None
        cursor = None

        try:

            connection = get_connection()
            cursor = connection.cursor()

            user_email = st.session_state.get(
                "user_email",
                "priyanka@codepractice.local",
            )

            cursor.execute(
                """
                SELECT id
                FROM users
                WHERE email = %s
                LIMIT 1;
                """,
                (user_email,),
            )

            row = cursor.fetchone()

            if row:
                return row[0]

            return None

        except Exception as error:

            print(
                f"BOOKMARK USER ERROR: {error}"
            )

            return None

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()


    def bookmark_is_saved(topic_name):

        connection = None
        cursor = None

        try:

            connection = get_connection()
            cursor = connection.cursor()

            user_email = st.session_state.get(
                "user_email",
                "priyanka@codepractice.local",
            )

            cursor.execute(
                """
                SELECT b.id
                FROM bookmarks b

                JOIN users u
                    ON u.id = b.user_id

                JOIN lessons l
                    ON l.id = b.lesson_id

                WHERE u.email = %s
                  AND l.subject = %s
                  AND l.title = %s

                LIMIT 1;
                """,
                (
                    user_email,
                    "Python",
                    topic_name,
                ),
            )

            return cursor.fetchone() is not None

        except Exception as error:

            print(
                f"BOOKMARK CHECK ERROR: {error}"
            )

            return False

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()


    def bookmark_save(topic_name):

        connection = None
        cursor = None

        try:

            connection = get_connection()
            cursor = connection.cursor()

            user_email = st.session_state.get(
                "user_email",
                "priyanka@codepractice.local",
            )

            # -------------------------------------------------
            # USER
            # -------------------------------------------------

            cursor.execute(
                """
                SELECT id
                FROM users
                WHERE email = %s
                LIMIT 1;
                """,
                (user_email,),
            )

            user_row = cursor.fetchone()

            if not user_row:

                raise Exception(
                    f"User not found: {user_email}"
                )

            user_id = user_row[0]

            # -------------------------------------------------
            # LESSON
            # -------------------------------------------------

            cursor.execute(
                """
                SELECT id
                FROM lessons
                WHERE subject = %s
                  AND title = %s
                LIMIT 1;
                """,
                (
                    "Python",
                    topic_name,
                ),
            )

            lesson_row = cursor.fetchone()

            # -------------------------------------------------
            # CREATE LESSON IF MISSING
            # -------------------------------------------------

            if not lesson_row:

                cursor.execute(
                    """
                    SELECT COALESCE(
                        MAX(lesson_order),
                        0
                    ) + 1
                    FROM lessons
                    WHERE subject = %s;
                    """,
                    ("Python",),
                )

                order_row = cursor.fetchone()

                next_order = (
                    order_row[0]
                    if order_row
                    else 1
                )

                cursor.execute(
                    """
                    INSERT INTO lessons (
                        subject,
                        title,
                        description,
                        lesson_order
                    )
                    VALUES (
                        %s,
                        %s,
                        %s,
                        %s
                    )
                    RETURNING id;
                    """,
                    (
                        "Python",
                        topic_name,
                        f"Python lesson: {topic_name}",
                        next_order,
                    ),
                )

                lesson_row = cursor.fetchone()

            lesson_id = lesson_row[0]

            # -------------------------------------------------
            # CREATE BOOKMARK
            # -------------------------------------------------

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
                )
                ON CONFLICT (
                    user_id,
                    lesson_id
                )
                DO UPDATE SET
                    topic_name = EXCLUDED.topic_name;
                """,
                (
                    user_id,
                    lesson_id,
                    topic_name,
                ),
            )

            connection.commit()

            return True

        except Exception as error:

            if connection:
                connection.rollback()

            print(
                f"BOOKMARK SAVE ERROR: {error}"
            )

            return False

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()


    def bookmark_remove(topic_name):

        connection = None
        cursor = None

        try:

            connection = get_connection()
            cursor = connection.cursor()

            user_email = st.session_state.get(
                "user_email",
                "priyanka@codepractice.local",
            )

            cursor.execute(
                """
                DELETE FROM bookmarks b
                USING users u, lessons l
                WHERE b.user_id = u.id
                  AND b.lesson_id = l.id
                  AND u.email = %s
                  AND l.subject = %s
                  AND l.title = %s;
                """,
                (
                    user_email,
                    "Python",
                    topic_name,
                ),
            )

            deleted = cursor.rowcount

            connection.commit()

            return deleted > 0

        except Exception as error:

            if connection:
                connection.rollback()

            print(
                f"BOOKMARK REMOVE ERROR: {error}"
            )

            return False

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()


    # =====================================================
    # BOOKMARK HEADER
    # =====================================================

    st.markdown(
        "## 🔖 Bookmark"
    )

    st.caption(
        "Save this topic to your Bookmarks so you can find it later."
    )


    # =====================================================
    # CURRENT TOPIC
    # =====================================================

    st.info(
        f"📚 Current Topic: {current}"
    )


    # =====================================================
    # DATABASE STATUS
    # =====================================================

    bookmarked = bookmark_is_saved(current)


    # =====================================================
    # SAVED STATUS
    # =====================================================

    if bookmarked:

        st.success(
            f"✓ **{current}** is saved in your Bookmarks."
        )

        st.caption(
            "This bookmark is stored in PostgreSQL and linked to your account."
        )

    else:

        st.warning(
            f"**{current}** is not saved yet."
        )


    # =====================================================
    # SAVE / REMOVE BUTTONS
    # =====================================================

    save_col, remove_col = st.columns(
        [1, 1],
        gap="small",
    )


    # =====================================================
    # SAVE
    # =====================================================

    with save_col:

        save_clicked = st.button(
            "🔖 Save Bookmark",
            key=f"save_bookmark_{current}",
            use_container_width=True,
            type="primary",
            disabled=bookmarked,
        )

        if save_clicked:

            saved = bookmark_save(current)

            if saved:

                st.success(
                    f"✓ {current} has been saved to your Bookmarks."
                )

                st.rerun()

            else:

                st.error(
                    "Could not save the bookmark."
                )

                st.caption(
                    "Open the VS Code Terminal and check "
                    "the BOOKMARK SAVE ERROR message."
                )


    # =====================================================
    # REMOVE
    # =====================================================

    with remove_col:

        remove_clicked = st.button(
            "🗑 Remove Bookmark",
            key=f"remove_bookmark_{current}",
            use_container_width=True,
            disabled=not bookmarked,
        )

        if remove_clicked:

            removed = bookmark_remove(current)

            if removed:

                st.success(
                    f"✓ {current} has been removed from your Bookmarks."
                )

                st.rerun()

            else:

                st.error(
                    "Could not remove the bookmark."
                )


    # =====================================================
    # DATABASE INFORMATION
    # =====================================================

    st.divider()

    st.caption(
        "🔗 PostgreSQL • Your bookmarks are saved to your account."
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
        CodePractice AI • Learn → Practice → Grow
    </div>
    """,
    unsafe_allow_html=True,
)

from fastapi import FastAPI

from database.database import get_connection


app = FastAPI(
    title="CodePractice AI API",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "CodePractice AI API is running"
    }


@app.get("/database-status")
def database_status():

    try:
        connection = get_connection()
        connection.close()

        return {
            "database": "PostgreSQL",
            "status": "connected"
        }

    except Exception as error:

        return {
            "database": "PostgreSQL",
            "status": "error",
            "message": str(error)
        }
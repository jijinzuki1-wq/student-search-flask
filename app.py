from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)

# Allow Android app to communicate with Flask
CORS(app)

# CSV file
CSV_FILE = "students_cleaned.csv"


# ==========================================
# LOAD STUDENT DATA
# ==========================================

try:
    df = pd.read_csv(CSV_FILE)

    # Clean Student ID
    df["student_id"] = (
        df["student_id"]
        .astype(str)
        .str.strip()
    )

    print("Student data loaded successfully.")
    print("Total students:", len(df))

except Exception as e:

    print("Error loading student data:", e)

    df = pd.DataFrame()


# ==========================================
# HOME / API STATUS
# ==========================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "success": True,
        "message": "Student Search System API is running",
        "total_students": len(df)
    })


# ==========================================
# SEARCH ANY STUDENT BY ID
# ==========================================

@app.route("/students/<student_id>", methods=["GET"])
def search_student(student_id):

    # Clean entered ID
    student_id = str(student_id).strip()

    # Check database
    if df.empty:

        return jsonify({
            "success": False,
            "message": "Student database is unavailable."
        }), 500

    # Search Student ID
    result = df[
        df["student_id"].str.lower()
        == student_id.lower()
    ]

    # Student not found
    if result.empty:

        return jsonify({
            "success": False,
            "message": "Student ID not found."
        }), 404

    # Get student
    student = result.iloc[0]

    # Create student response
    student_data = {

        "student_id": str(
            student["student_id"]
        ),

        "full_name": str(
            student["full_name"]
        ),

        "gender": str(
            student["gender"]
        ),

        "region": str(
            student["region"]
        ),

        "course": str(
            student["course"]
        ),

        "age": int(
            student["age"]
        ),

        "score_math": float(
            student["score_math"]
        ),

        "score_programming": float(
            student["score_programming"]
        ),

        "score_networking": float(
            student["score_networking"]
        ),

        "attendance_percent":
            f'{student["attendance_percent"]}%',

        "registration_date": str(
            student["registration_date"]
        ),

        "phone": str(
            student["phone"]
        )
    }

    return jsonify({

        "success": True,

        "message": "Student found!",

        "student": student_data
    })


# ==========================================
# RUN FLASK SERVER
# ==========================================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )
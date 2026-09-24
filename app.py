import os
import json
from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev_default_secret")

# MongoDB Atlas Connection
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["devops_assignment"]
collection = db["submissions"]

# --- Task 1: JSON API Route ---
@app.route("/api/data", methods=["GET"])
def get_api_data():
    """Reads data from a backend file and returns it as a JSON list."""
    try:
        data_file_path = os.path.join(os.path.dirname(__file__), "data.json")
        with open(data_file_path, "r") as f:
            data = json.load(f)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": f"Failed to read data: {str(e)}"}), 500


# --- Task 2: Frontend Form with MongoDB Atlas ---
@app.route("/", methods=["GET", "POST"])
def index():
    error_message = None
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        feedback = request.form.get("feedback", "").strip()

        # Input validation
        if not name or not email:
            error_message = "Name and Email are required fields."
            return render_template("form.html", error=error_message)

        try:
            # Insert document into MongoDB Atlas
            doc = {
                "name": name,
                "email": email,
                "feedback": feedback
            }
            collection.insert_one(doc)
            # Redirect on success
            return redirect(url_for("success"))
        except PyMongoError as err:
            # Display error on the same page without redirection
            error_message = f"Database insertion failed: {str(err)}"
            return render_template("form.html", error=error_message)
        except Exception as err:
            error_message = f"An unexpected error occurred: {str(err)}"
            return render_template("form.html", error=error_message)

    return render_template("form.html", error=None)


@app.route("/success", methods=["GET"])
def success():
    """Renders the success page after form submission."""
    return render_template("success.html")

@app.route("/todo", methods=["GET"])
def todo_page():
    return render_template("todo.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
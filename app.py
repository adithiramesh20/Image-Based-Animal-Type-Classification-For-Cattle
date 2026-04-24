from flask import Flask, render_template, request, redirect
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# USER STORAGE
users = {}

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login")
def login():
    return render_template("login.html")


# LOGIN / REGISTER LOGIC
@app.route("/welcome", methods=["POST"])
def welcome():
    email = request.form["email"]
    password = request.form["password"]

    # EXISTING USER
    if email in users:
        return render_template("welcome.html",
                               email=email,
                               message="Already registered")

    # NEW USER
    users[email] = password
    return render_template("welcome.html",
                           email=email,
                           message="Successfully logged in")


@app.route("/analysis")
def analysis():
    return render_template("analysis.html")


@app.route("/predict", methods=["POST"])
def predict():
    file = request.files["image"]

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        return render_template("result.html",
                               prediction="Ringworm Detected",
                               solution="Apply antifungal medication",
                               prevention="Maintain hygiene and isolate infected cattle",
                               image_path=filepath)

    return redirect("/analysis")


if __name__ == "__main__":
    app.run(debug=True)
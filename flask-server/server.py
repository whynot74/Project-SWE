from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configure MSSQL database
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mssql+pyodbc://Zeyadk:12341234@localhost/EventSystem?driver=ODBC+Driver+17+for+SQL+Server"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Models
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


class UserPreference(db.Model):
    __tablename__ = 'user_preference'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_name = db.Column(db.String(100), nullable=False)


# Initialize the database
with app.app_context():
    db.create_all()


# Routes
@app.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        if not name or not email or not password:
            return jsonify({"message": "All fields are required"}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({"message": "Email is already registered"}), 400

        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "Registration successful!"}), 201

    except Exception as e:
        print(f"Error during registration: {type(e).__name__} - {e}")
        return jsonify({"message": "An internal error occurred during registration."}), 500


@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"message": "Email and password are required"}), 400

        user = User.query.filter_by(email=email, password=password).first()
        if not user:
            return jsonify({"message": "Invalid email or password"}), 401

        return jsonify({"message": "Login successful!", "user_id": user.id}), 200

    except Exception as e:
        print(f"Error during login: {type(e).__name__} - {e}")
        return jsonify({"message": "An internal error occurred during login."}), 500


@app.route("/save_preferences", methods=["POST"])
def save_preferences():
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        preferences = data.get("preferences")  # List of category names

        print(f"Data received: user_id={user_id}, preferences={preferences}")

        # Validate input
        if not user_id or not isinstance(preferences, list) or len(preferences) == 0:
            return jsonify({"message": "Invalid input! `user_id` and `preferences` are required."}), 400

        # Check if the user exists
        user = db.session.get(User, user_id)
        if not user:
            print(f"User with ID {user_id} not found in the database.")
            return jsonify({"message": f"User with ID {user_id} does not exist."}), 404

        # Clear existing preferences for the user
        UserPreference.query.filter_by(user_id=user_id).delete()

        # Save new preferences
        for category_name in preferences:
            print(f"Adding preference: {category_name}")
            new_preference = UserPreference(user_id=user_id, category_name=category_name)
            db.session.add(new_preference)

        db.session.commit()
        print("Preferences saved successfully!")
        return jsonify({"message": "Preferences saved successfully!"}), 200

    except Exception as e:
        print(f"Error saving preferences: {type(e).__name__} - {e}")
        return jsonify({"message": "Failed to save preferences due to an internal error."}), 500


@app.route("/get_preferences/<int:user_id>", methods=["GET"])
def get_preferences(user_id):
    try:
        user = db.session.get(User, user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        preferences = (
            db.session.query(UserPreference.category_name)
            .filter(UserPreference.user_id == user_id)
            .all()
        )

        return jsonify({"preferences": [p[0] for p in preferences]}), 200

    except Exception as e:
        print(f"Error fetching preferences: {type(e).__name__} - {e}")
        return jsonify({"message": "Failed to fetch preferences due to an internal error."}), 500


if __name__ == "__main__":
    app.run(debug=True)

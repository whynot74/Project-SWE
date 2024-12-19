from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from functools import wraps

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
    bookmarks = db.relationship('Bookmark', backref='user')
    tickets = db.relationship('Ticket', backref='user')


class UserPreference(db.Model):
    __tablename__ = 'user_preference'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_name = db.Column(db.String(100), nullable=False)

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    ticket_price = db.Column(db.Float, nullable=False)

class UniversityClub(db.Model):
    __tablename__ = 'clubs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(300))

class Bookmark(db.Model):
    __tablename__ = 'bookmarks'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(300))

class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    message = db.Column(db.String(300), nullable=False)
    read_status = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    purchase_date = db.Column(db.DateTime, server_default=db.func.now())
    price = db.Column(db.Float, nullable=False)
    seat_number=db.Column(db.String(10))



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
@app.route('/events', methods=['GET'])
def get_all_events():
    events = Event.query.all()
    result = [
        {
            "id": event.id,
            "title": event.title,
            "location": event.location,
            "date": event.date,
            "time": event.time,
            "category": event.category,
            "ticket_price": event.ticket_price
        }
        for event in events
    ]
    return jsonify({"events": result}), 200
@app.route('/event/<int:event_id>', methods=['GET'])
def get_event_details(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    return jsonify({
        "id": event.id,
        "title": event.title,
        "location": event.location,
        "date": event.date,
        "time": event.time,
        "category": event.category,
        "ticket_price": event.ticket_price
    }), 200
@app.route('/send_notification', methods=['POST'])
def send_notification():
    data = request.json
    user_id = data.get('user_id')
    message = data.get('message')

    if not User.query.get(user_id):
        return jsonify({"error": "User not found"}), 404

    new_notification = Notification(user_id=user_id, message=message, read_status=False)
    db.session.add(new_notification)
    db.session.commit()

    return jsonify({"message": "Notification sent successfully"}), 201
@app.route('/notifications/<int:user_id>', methods=['GET'])
def get_notifications(user_id):
    notifications = Notification.query.filter_by(user_id=user_id).all()
    result = [
        {"id": notification.id, "message": notification.message, "read_status": notification.read_status}
        for notification in notifications
    ]
    return jsonify({"notifications": result}), 200
@app.route('/notification/read/<int:notification_id>', methods=['POST'])
def mark_notification_as_read(notification_id):
    notification = Notification.query.get(notification_id)
    if not notification:
        return jsonify({"error": "Notification not found"}), 404

    notification.read_status = True
    db.session.commit()

    return jsonify({"message": "Notification marked as read"}), 200
@app.route('/add_bookmark', methods=['POST'])
def add_bookmark():
    data = request.json
    user_id = data.get('user_id')
    event_id = data.get('event_id')

    if not Event.query.get(event_id):
        return jsonify({"error": "Event not found"}), 404

    bookmark = Bookmark.query.filter_by(user_id=user_id, event_id=event_id).first()
    if bookmark:
        return jsonify({"message": "Bookmark already exists"}), 409

    new_bookmark = Bookmark(user_id=user_id, event_id=event_id)
    db.session.add(new_bookmark)
    db.session.commit()

    return jsonify({"message": "Bookmark added successfully"}), 201
@app.route('/remove_bookmark', methods=['POST'])
def remove_bookmark():
    data = request.json
    user_id = data.get('user_id')
    event_id = data.get('event_id')

    bookmark = Bookmark.query.filter_by(user_id=user_id, event_id=event_id).first()
    if not bookmark:
        return jsonify({"error": "Bookmark not found"}), 404

    db.session.delete(bookmark)
    db.session.commit()

    return jsonify({"message": "Bookmark removed successfully"}), 200
@app.route('/bookmarks/<int:user_id>', methods=['GET'])
def get_bookmarks(user_id):
    bookmarks = Bookmark.query.filter_by(user_id=user_id).all()
    result = [{"event_id": bookmark.event_id} for bookmark in bookmarks]

    return jsonify({"bookmarked_events": result}), 200
# Admin-only route decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = request.json.get("user_id")  # Ensure it's passed in the body
        if not user_id:
            user_id = request.args.get("user_id")  # Alternatively, from query params
        user = User.query.get(user_id)
        if not user or not user.is_admin:
            return jsonify({"error": "Admin access required"}), 403
        return f(*args, **kwargs)
    return decorated_function

# Admin Routes

@app.route("/admin/events/update/<int:event_id>", methods=["PUT"])
@admin_required
def admin_update_event(event_id):
    data = request.json
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    # Update fields
    event.title = data.get("title", event.title)
    event.category = data.get("category", event.category)
    event.location = data.get("location", event.location)
    event.date = data.get("date", event.date)
    event.time = data.get("time", event.time)
    event.ticket_price = data.get("ticket_price", event.ticket_price)

    db.session.commit()
    return jsonify({"message": "Event updated successfully"}), 200


@app.route("/admin/events/delete/<int:event_id>", methods=["DELETE"])
@admin_required
def admin_delete_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    db.session.delete(event)
    db.session.commit()
    return jsonify({"message": "Event deleted successfully"}), 200


@app.route("/admin/reviews/delete/<int:review_id>", methods=["DELETE"])
@admin_required
def admin_delete_review(review_id):
    review = Review.query.get(review_id)
    if not review:
        return jsonify({"error": "Review not found"}), 404

    db.session.delete(review)
    db.session.commit()
    return jsonify({"message": "Review deleted successfully"}), 200


@app.route("/admin/send_notification", methods=["POST"])
@admin_required
def admin_send_notification():
    data = request.json
    message = data.get("message")

    if not message:
        return jsonify({"error": "Message cannot be empty"}), 400

    # Send to all users
    users = User.query.all()
    for user in users:
        new_notification = Notification(user_id=user.id, message=message, read_status=False)
        db.session.add(new_notification)

    db.session.commit()
    return jsonify({"message": "Notification sent to all users"}), 201

@app.route("/profile/<int:user_id>", methods=["GET"])
def get_user_profile(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"id": user.id, "name": user.name, "email": user.email}), 200

@app.route("/profile/update", methods=["POST"])
def update_profile():
    data = request.json
    user = User.query.get(data["user_id"])
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.name = data.get("name", user.name)
    user.email = data.get("email", user.email)
    db.session.commit()

    return jsonify({"message": "Profile updated successfully!"}), 200


@app.route("/tickets/purchase", methods=["POST"])
def purchase_ticket():
    data = request.json
    user_id = data.get("user_id")
    event_id = data.get("event_id")

    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    new_ticket = Ticket(user_id=user_id, event_id=event_id, price=event.ticket_price)
    db.session.add(new_ticket)
    db.session.commit()

    return jsonify({"message": "Ticket purchased successfully", "price": event.ticket_price}), 201

@app.route("/tickets/<int:user_id>", methods=["GET"])
def get_user_tickets(user_id):
    tickets = Ticket.query.filter_by(user_id=user_id).all()
    result = [
        {"ticket_id": ticket.id, "event_id": ticket.event_id, "purchase_date": ticket.purchase_date}
        for ticket in tickets
    ]
    return jsonify({"tickets": result}), 200
@app.route("/events/search", methods=["GET"])
def search_events():
    category = request.args.get("category")
    location = request.args.get("location")
    date = request.args.get("date")  # Optional

    query = Event.query
    if category:
        query = query.filter_by(category=category)
    if location:
        query = query.filter_by(location=location)
    if date:
        query = query.filter_by(date=date)

    results = query.all()
    return jsonify({
        "events": [{"id": e.id, "title": e.title, "location": e.location, "date": e.date} for e in results]
    }), 200
@app.route("/reviews/create", methods=["POST"])
def create_review():
    data = request.json
    user_id = data.get("user_id")
    event_id = data.get("event_id")
    rating = data.get("rating")
    comment = data.get("comment")

    new_review = Review(user_id=user_id, event_id=event_id, rating=rating, comment=comment)
    db.session.add(new_review)
    db.session.commit()
    return jsonify({"message": "Review submitted successfully!"}), 201

@app.route("/reviews/event/<int:event_id>", methods=["GET"])
def get_event_reviews(event_id):
    reviews = Review.query.filter_by(event_id=event_id).all()
    result = [
        {"user_id": r.user_id, "rating": r.rating, "comment": r.comment}
        for r in reviews
    ]
    return jsonify({"reviews": result}), 200
@app.route('/events', methods=['GET'])
def get_events_paginated():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)  # Default 10 items per page
    events = Event.query.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        "events": [{"id": e.id, "title": e.title} for e in events.items],
        "total": events.total,
        "pages": events.pages,
        "current_page": events.page
    }), 200
# University Club Routes

@app.route('/clubs', methods=['GET'])
def get_all_clubs():
    clubs = UniversityClub.query.all()
    result = [{"id": club.id, "name": club.name, "description": club.description} for club in clubs]
    return jsonify({"clubs": result}), 200


@app.route('/clubs/<int:club_id>/events', methods=['GET'])
def get_club_events(club_id):
    club = UniversityClub.query.get(club_id)
    if not club:
        return jsonify({"error": "Club not found"}), 404

    events = Event.query.filter_by(club_id=club_id).all()
    result = [
        {"id": event.id, "title": event.title, "location": event.location, "date": event.date, "time": event.time}
        for event in events
    ]
    return jsonify({"club": {"id": club.id, "name": club.name}, "events": result}), 200


@app.route('/clubs', methods=['POST'])
@admin_required
def create_club():
    data = request.json
    name = data.get("name")
    description = data.get("description", "")

    if not name:
        return jsonify({"error": "Club name is required"}), 400

    new_club = UniversityClub(name=name, description=description)
    db.session.add(new_club)
    db.session.commit()

    return jsonify({"message": "University club created successfully!"}), 201
@app.route('/recommendations/<int:user_id>', methods=['GET'])
def recommend_events(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    preferences = db.session.query(UserPreference.category_name).filter_by(user_id=user_id).all()
    preferred_categories = [p[0] for p in preferences]

    if not preferred_categories:
        return jsonify({"message": "No preferences found for this user"}), 200

    # Find events matching preferences
    recommended_events = Event.query.filter(Event.category.in_(preferred_categories)).all()
    result = [
        {
            "id": event.id,
            "title": event.title,
            "location": event.location,
            "date": event.date,
            "time": event.time,
            "category": event.category,
        }
        for event in recommended_events
    ]

    return jsonify({"recommended_events": result}), 200
@app.route('/tickets/reserve_seat', methods=['POST'])
def reserve_seat():
    data = request.json
    user_id = data.get("user_id")
    event_id = data.get("event_id")
    seat_number = data.get("seat_number")

    # Check if event exists
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    # Check if seat is already reserved
    if Ticket.query.filter_by(event_id=event_id, seat_number=seat_number).first():
        return jsonify({"error": "Seat already reserved"}), 409

    # Reserve the ticket
    new_ticket = Ticket(user_id=user_id, event_id=event_id, seat_number=seat_number, price=event.ticket_price)
    db.session.add(new_ticket)
    db.session.commit()

    return jsonify({"message": "Seat reserved successfully!", "seat_number": seat_number, "price": event.ticket_price}), 201
@app.route('/events/<int:event_id>/seating', methods=['GET'])
def get_seating_plan(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    # Example seating plan: rows A-E, seats 1-10
    seating_plan = {f"{row}{seat}": "available" for row in "ABCDE" for seat in range(1, 11)}

    # Mark reserved seats
    reserved_seats = Ticket.query.filter_by(event_id=event_id).with_entities(Ticket.seat_number).all()
    for seat in reserved_seats:
        seating_plan[seat[0]] = "reserved"

    return jsonify({"seating_plan": seating_plan}), 200
@app.route("/events/create", methods=["POST"])
def create_event():
    data = request.get_json()
    title = data.get("title")
    category = data.get("category")
    location = data.get("location")
    date = data.get("date")  # Should be in YYYY-MM-DD format
    time = data.get("time")  # Should be in HH:MM:SS format
    ticket_price = data.get("ticket_price")

    if not (title and category and location and date and time and ticket_price):
        return jsonify({"error": "All fields are required"}), 400

    try:
        new_event = Event(
            title=title,
            category=category,
            location=location,
            date=date,
            time=time,
            ticket_price=ticket_price
        )
        db.session.add(new_event)
        db.session.commit()

        return jsonify({"message": "Event created successfully!", "event_id": new_event.id}), 201
    except Exception as e:
        print(f"Error creating event: {type(e).__name__} - {e}")
        return jsonify({"error": "Failed to create event due to an internal error."}), 500
@app.route("/tickets/cancel", methods=["POST"])
def cancel_ticket():
    data = request.get_json()
    ticket_id = data.get("ticket_id")

    if not ticket_id:
        return jsonify({"error": "Ticket ID is required"}), 400

    try:
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            return jsonify({"error": "Ticket not found"}), 404

        db.session.delete(ticket)
        db.session.commit()

        return jsonify({"message": "Ticket canceled successfully"}), 200
    except Exception as e:
        print(f"Error canceling ticket: {type(e).__name__} - {e}")
        return jsonify({"error": "Failed to cancel ticket due to an internal error."}), 500

if __name__ == "__main__":
    app.run(debug=True)
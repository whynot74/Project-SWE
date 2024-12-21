import pytest
from app import app, db, User, Event, Bookmark, Notification, Ticket, Review, UserPreference, Club, TicketReservation, SeatingPlan, Admin, TicketPurchase, TicketCancellation, TicketUpdate, NotificationRead, TicketCancel, EventUpdate, ClubEvent, Recommendation

DATABASE_URI = "mssql+pyodbc://Zeyadk:12341234@localhost/EventSystem?driver=ODBC+Driver+17+for+SQL+Server"

@pytest.fixture(scope="module")
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

        with app.app_context():
            db.session.remove()
            db.drop_all()


@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
    with app.app_context():
        db.session.query(Notification).delete()
        db.session.query(Ticket).delete()
        db.session.query(Bookmark).delete()
        db.session.query(Review).delete()
        db.session.query(Event).delete()
        db.session.query(UserPreference).delete()
        db.session.query(User).delete()
        db.session.commit()


# Test User Registration and Login
def test_register_user(client):
    response = client.post('/register', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 201
    assert response.get_json()['message'] == 'Registration successful!'


def test_register_user_duplicate(client):
    client.post('/register', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123'
    })
    response = client.post('/register', json={
        'name': 'Another User',
        'email': 'test@example.com',
        'password': 'password456'
    })
    assert response.status_code == 400
    assert response.get_json()['message'] == 'Email is already registered'


def test_login_user(client):
    client.post('/register', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123'
    })
    response = client.post('/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Login successful!'


# Test User Preferences
def test_save_preferences(client):
    client.post('/register', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123'
    })
    response = client.post('/save_preferences', json={
        'user_id': 1,
        'preferences': ['Music', 'Sports']
    })
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Preferences saved successfully!'


def test_get_preferences(client):
    client.post('/register', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123'
    })
    client.post('/save_preferences', json={
        'user_id': 1,
        'preferences': ['Music', 'Sports']
    })
    response = client.get('/get_preferences/1')
    assert response.status_code == 200
    assert response.get_json()['preferences'] == ['Music', 'Sports']


# Test Events
def test_create_event(client):
    response = client.post('/events/create', json={
        'title': 'Concert',
        'category': 'Music',
        'location': 'New York',
        'date': '2024-12-25',
        'time': '19:00:00',
        'ticket_price': 50.0
    })
    assert response.status_code == 201
    assert response.get_json()['message'] == 'Event created successfully!'


def test_get_all_events(client):
    client.post('/events/create', json={
        'title': 'Concert',
        'category': 'Music',
        'location': 'New York',
        'date': '2024-12-25',
        'time': '19:00:00',
        'ticket_price': 50.0
    })
    response = client.get('/events')
    assert response.status_code == 200
    assert len(response.get_json()['events']) > 0


def test_get_event_details(client):
    client.post('/events/create', json={
        'title': 'Concert',
        'category': 'Music',
        'location': 'New York',
        'date': '2024-12-25',
        'time': '19:00:00',
        'ticket_price': 50.0
    })
    response = client.get('/event/1')
    assert response.status_code == 200
    assert response.get_json()['title'] == 'Concert'


# Test Notifications
def test_send_notification(client):
    client.post('/register', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123'
    })
    response = client.post('/send_notification', json={
        'user_id': 1,
        'message': 'Test Notification'
    })
    assert response.status_code == 201
    assert response.get_json()['message'] == 'Notification sent successfully'


def test_get_notifications(client):
    client.post('/register', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123'
    })
    client.post('/send_notification', json={
        'user_id': 1,
        'message': 'Test Notification'
    })
    response = client.get('/notifications/1')
    assert response.status_code == 200
    assert len(response.get_json()['notifications']) > 0


# Test Bookmarks
def test_add_bookmark(client):
    client.post('/register', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123'
    })
    client.post('/events/create', json={
        'title': 'Concert',
        'category': 'Music',
        'location': 'New York',
        'date': '2024-12-25',
        'time': '19:00:00',
        'ticket_price': 50.0
    })
    response = client.post('/add_bookmark', json={
        'user_id': 1,
        'event_id': 1
    })
    assert response.status_code == 201
    assert response.get_json()['message'] == 'Bookmark added successfully'


def test_remove_bookmark(client):
    client.post('/register', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123'
    })
    client.post('/events/create', json={
        'title': 'Concert',
        'category': 'Music',
        'location': 'New York',
        'date': '2024-12-25',
        'time': '19:00:00',
        'ticket_price': 50.0
    })
    client.post('/add_bookmark', json={
        'user_id': 1,
        'event_id': 1
    })
    response = client.post('/remove_bookmark', json={
        'user_id': 1,
        'event_id': 1
    })
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Bookmark removed successfully'
# Profile Management
def test_get_user_profile(client):
    client.post('/register', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123'
    })
    response = client.get('/profile/1')
    assert response.status_code == 200
    assert response.get_json()['name'] == 'Test User'

def test_update_profile(client):
    client.post('/register', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123'
    })
    response = client.post('/profile/update', json={
        'user_id': 1,
        'name': 'Updated User',
        'email': 'updated@example.com'
    })
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Profile updated successfully!'

# Notifications
def test_mark_notification_as_read(client):
    client.post('/register', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123'
    })
    client.post('/send_notification', json={
        'user_id': 1,
        'message': 'Test Notification'
    })
    response = client.post('/notification/read/1')
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Notification marked as read'

# Events Pagination
def test_get_paginated_events(client):
    client.post('/events/create', json={
        'title': 'Event 1',
        'category': 'Category',
        'location': 'Location',
        'date': '2024-12-25',
        'time': '19:00:00',
        'ticket_price': 100
    })
    client.post('/events/create', json={
        'title': 'Event 2',
        'category': 'Category',
        'location': 'Location',
        'date': '2024-12-26',
        'time': '20:00:00',
        'ticket_price': 200
    })
    response = client.get('/events?page=1&per_page=1')
    assert response.status_code == 200
    assert len(response.get_json()['events']) == 1

# Tickets
def test_cancel_ticket(client):
    client.post('/register', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123'
    })
    client.post('/events/create', json={
        'title': 'Concert',
        'category': 'Music',
        'location': 'New York',
        'date': '2024-12-25',
        'time': '19:00:00',
        'ticket_price': 50.0
    })
    client.post('/tickets/purchase', json={
        'user_id': 1,
        'event_id': 1
    })
    response = client.post('/tickets/cancel', json={
        'ticket_id': 1
    })
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Ticket canceled successfully'

# Admin Functionality
def test_admin_update_event(client):
    client.post('/register', json={
        'name': 'Admin',
        'email': 'admin@example.com',
        'password': 'admin123',
        'is_admin': True  # Assuming `is_admin` is a column in `User`
    })
    client.post('/events/create', json={
        'title': 'Old Event',
        'category': 'Old Category',
        'location': 'Old Location',
        'date': '2024-12-25',
        'time': '19:00:00',
        'ticket_price': 50.0
    })
    response = client.put('/admin/events/update/1', json={
        'user_id': 1,  # Admin User ID
        'title': 'Updated Event',
        'category': 'Updated Category',
        'location': 'Updated Location'
    })
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Event updated successfully'
# Recommendations
def test_recommend_events(client):
    # Register a user
    client.post('/register', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123'
    })

    # Save user preferences
    client.post('/save_preferences', json={
        'user_id': 1,
        'preferences': ['Music', 'Sports']
    })

    # Create matching and non-matching events
    client.post('/events/create', json={
        'title': 'Music Concert',
        'category': 'Music',
        'location': 'New York',
        'date': '2024-12-25',
        'time': '19:00:00',
        'ticket_price': 50.0
    })
    client.post('/events/create', json={
        'title': 'Sports Tournament',
        'category': 'Sports',
        'location': 'Los Angeles',
        'date': '2024-12-30',
        'time': '15:00:00',
        'ticket_price': 30.0
    })
    client.post('/events/create', json={
        'title': 'Cooking Class',
        'category': 'Cooking',
        'location': 'Chicago',
        'date': '2024-12-15',
        'time': '12:00:00',
        'ticket_price': 20.0
    })

    # Fetch recommendations
    response = client.get('/recommendations/1')
    assert response.status_code == 200

    # Verify only matching events are returned
    recommendations = response.get_json()['recommended_events']
    assert len(recommendations) == 2
    assert recommendations[0]['category'] in ['Music', 'Sports']
    assert recommendations[1]['category'] in ['Music', 'Sports']
# Test Ticket Reservation
def test_reserve_seat(client):
    client.post('/register', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123'
    })
    client.post('/events/create', json={
        'title': 'Concert',
        'category': 'Music',
        'location': 'New York',
        'date': '2024-12-25',
        'time': '19:00:00',
        'ticket_price': 50.0
    })
    response = client.post('/tickets/reserve_seat', json={
        'user_id': 1,
        'event_id': 1,
        'seat_number': 'A1'
    })
    assert response.status_code == 201
    assert response.get_json()['message'] == 'Seat reserved successfully!'


def test_get_seating_plan(client):
    client.post('/events/create', json={
        'title': 'Concert',
        'category': 'Music',
        'location': 'New York',
        'date': '2024-12-25',
        'time': '19:00:00',
        'ticket_price': 50.0
    })
    client.post('/tickets/reserve_seat', json={
        'user_id': 1,
        'event_id': 1,
        'seat_number': 'A1'
    })
    response = client.get('/events/1/seating')
    assert response.status_code == 200
    seating_plan = response.get_json()['seating_plan']
    assert seating_plan['A1'] == 'reserved'

# Test Admin Event Deletion
def test_admin_delete_event(client):
    client.post('/register', json={
        'name': 'Admin',
        'email': 'admin@example.com',
        'password': 'admin123',
        'is_admin': True
    })
    client.post('/events/create', json={
        'title': 'Concert',
        'category': 'Music',
        'location': 'New York',
        'date': '2024-12-25',
        'time': '19:00:00',
        'ticket_price': 50.0
    })
    response = client.delete('/admin/events/delete/1', json={'user_id': 1})
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Event deleted successfully'

# Test Clubs
def test_create_club(client):
    client.post('/register', json={
        'name': 'Admin',
        'email': 'admin@example.com',
        'password': 'admin123',
        'is_admin': True
    })
    response = client.post('/clubs', json={
        'user_id': 1,
        'name': 'Art Club',
        'description': 'A club for art enthusiasts'
    })
    assert response.status_code == 201
    assert response.get_json()['message'] == 'University club created successfully!'


def test_get_all_clubs(client):
    client.post('/clubs', json={
        'user_id': 1,
        'name': 'Art Club',
        'description': 'A club for art enthusiasts'
    })
    response = client.get('/clubs')
    assert response.status_code == 200
    assert len(response.get_json()['clubs']) > 0


def test_get_club_events(client):
    client.post('/clubs', json={
        'user_id': 1,
        'name': 'Art Club',
        'description': 'A club for art enthusiasts'
    })
    client.post('/events/create', json={
        'title': 'Art Exhibition',
        'category': 'Art',
        'location': 'Museum',
        'date': '2024-12-10',
        'time': '10:00:00',
        'ticket_price': 10.0
    })
    response = client.get('/clubs/1/events')
    assert response.status_code == 200
    assert len(response.get_json()['events']) > 0

# Test Reviews
def test_create_review(client):
    client.post('/register', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123'
    })
    client.post('/events/create', json={
        'title': 'Concert',
        'category': 'Music',
        'location': 'New York',
        'date': '2024-12-25',
        'time': '19:00:00',
        'ticket_price': 50.0
    })
    response = client.post('/reviews/create', json={
        'user_id': 1,
        'event_id': 1,
        'rating': 5,
        'comment': 'Amazing event!'
    })
    assert response.status_code == 201
    assert response.get_json()['message'] == 'Review submitted successfully!'


def test_get_event_reviews(client):
    client.post('/reviews/create', json={
        'user_id': 1,
        'event_id': 1,
        'rating': 5,
        'comment': 'Amazing event!'
    })
    response = client.get('/reviews/event/1')
    assert response.status_code == 200
    reviews = response.get_json()['reviews']
    assert len(reviews) > 0
    assert reviews[0]['rating'] == 5
    assert reviews[0]['comment'] == 'Amazing event!'

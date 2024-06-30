from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
from pymongo import MongoClient, errors
import bcrypt
import os
from bson.objectid import ObjectId
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import datetime
import openai

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# MongoDB connection
try:
    client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
    db = client['EP']
    log_collection = db['log']
    print("MongoDB connected successfully.")
except errors.ServerSelectionTimeoutError as err:
    print("Failed to connect to MongoDB server:", err)

# Google Calendar API configuration
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
flow = Flow.from_client_secrets_file(
    'client_secret.json',
    scopes=['https://www.googleapis.com/auth/calendar.readonly'],
    redirect_uri='http://127.0.0.1:5000/oauth2callback'
)

def get_calendar_service():
    credentials = Credentials(**session['credentials'])
    service = build('calendar', 'v3', credentials=credentials)
    return service

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('ecolife'))
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        if log_collection.find_one({"email": email}):
            return render_template('login.html', signup_error="Email already registered")

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            user_id = log_collection.insert_one({
                "name": name,
                "email": email,
                "password": hashed_password,
                "points": 0
            }).inserted_id

            session['user_id'] = str(user_id)
            session['name'] = name
            session['points'] = 0

            return redirect(url_for('ecolife'))
        except errors.PyMongoError as e:
            return render_template('login.html', signup_error="Internal server error")

    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = log_collection.find_one({"email": email})

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            session['user_id'] = str(user['_id'])
            session['name'] = user['name']
            session['points'] = user['points']
            return redirect(url_for('ecolife'))
        else:
            return render_template('login.html', login_error="Invalid email or password")

    return render_template('login.html')

@app.route('/ecolife')
def ecolife():
    if 'user_id' not in session:
        return redirect(url_for('home'))

    # Check if we have already authenticated with Google
    if 'credentials' not in session:
        return redirect(url_for('authorize'))

    service = get_calendar_service()

    now = datetime.datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    # Create an events dictionary with hours as keys
    events_dict = {}
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        start_hour = int(start.split('T')[1].split(':')[0])
        events_dict[start_hour] = event['summary']

    meal_times = get_optimal_meal_times(events_dict)

    return render_template('ecolife.html', name=session['name'], points=session['points'], meal_times=meal_times, events=events_dict)

def get_optimal_meal_times(events):
    openai.api_key = "sk-proj-vp7yzLWGvsYVWqG9hpO9T3BlbkFJHRMRIHYxsmf2bQrTzLvM"

    prompt = f"Based on the following schedule, suggest optimal and healthiest times for breakfast, lunch, and dinner. Only provide the hour in 24-hour format and the food in each line: {events}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that suggests meal times based on a schedule."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )

    meal_times_text = response['choices'][0]['message']['content'].strip()
    meal_times = {"breakfast": {}, "lunch": {}, "dinner": {}}
    
    example_meals = {
        "breakfast": "Oatmeal with fresh berries and a glass of orange juice.",
        "lunch": "Grilled chicken salad with a variety of fresh vegetables.",
        "dinner": "Baked salmon with quinoa and steamed broccoli."
    }

    for line in meal_times_text.split('\n'):
        try:
            if "Breakfast:" in line:
                meal_times["breakfast"] = {"hour": int(line.split(":")[1].split()[0]), "food": example_meals["breakfast"]}
            elif "Lunch:" in line:
                meal_times["lunch"] = {"hour": int(line.split(":")[1].split()[0]), "food": example_meals["lunch"]}
            elif "Dinner:" in line:
                meal_times["dinner"] = {"hour": int(line.split(":")[1].split()[0]), "food": example_meals["dinner"]}
        except ValueError:
            continue

    return meal_times

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/increase_points', methods=['POST'])
def increase_points():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    user_id = session['user_id']
    user = log_collection.find_one({"_id": ObjectId(user_id)})

    if user:
        new_points = user['points'] + 1
        log_collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"points": new_points}})
        session['points'] = new_points
        return jsonify({"points": new_points})
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/authorize')
def authorize():
    authorization_url, state = flow.authorization_url()
    session['state'] = state
    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    flow.fetch_token(authorization_response=request.url)

    if not session['state'] == request.args['state']:
        flash('State mismatch. Possible CSRF attack.')
        return redirect(url_for('home'))  # Prevent CSRF

    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)

    return redirect(url_for('ecolife'))

def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}

if __name__ == '__main__':
    app.run(debug=True)

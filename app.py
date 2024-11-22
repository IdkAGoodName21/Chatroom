from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
import uuid
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Configure Database (using SQLite for simplicity)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatroom.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Set up file upload settings
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'webm'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Define User and Chatroom models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))

class Chatroom(db.Model):
    id = db.Column(db.String(100), primary_key=True, default=str(uuid.uuid4()))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_messages = db.relationship('Message', backref='chatroom', lazy=True)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    chatroom_id = db.Column(db.String(100), db.ForeignKey('chatroom.id'))

# Helper function to check file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Home page (Login/Sign-up)
@app.route('/')
def home():
    return render_template('login.html')

# Register page (Optional: can be combined with login)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.')
        return redirect(url_for('home'))
    return render_template('register.html')

# Login page
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        return redirect(url_for('chatroom', chatroom_id="default"))
    else:
        flash('Login failed. Check your username and/or password.')
        return redirect(url_for('home'))

# Chatroom page
@app.route('/chat/<chatroom_id>', methods=['GET', 'POST'])
def chatroom(chatroom_id):
    chat = Chatroom.query.filter_by(id=chatroom_id).first()
    if not chat:
        flash("Chatroom doesn't exist.")
        return redirect(url_for('home'))

    if request.method == 'POST':
        content = request.form['message']
        user_id = 1  # Example, you need to associate this with the logged-in user
        new_message = Message(content=content, sender_id=user_id, chatroom_id=chatroom_id)
        db.session.add(new_message)
        db.session.commit()

    messages = Message.query.filter_by(chatroom_id=chatroom_id).all()
    return render_template('chatroom.html', chatroom=chat, messages=messages)

# Create a new chatroom
@app.route('/create', methods=['GET', 'POST'])
def create_chatroom():
    if request.method == 'POST':
        chatroom_id = str(uuid.uuid4())
        new_chatroom = Chatroom(id=chatroom_id)
        db.session.add(new_chatroom)
        db.session.commit()
        flash('Chatroom created successfully!')
        return redirect(url_for('chatroom', chatroom_id=chatroom_id))
    return render_template('create_chatroom.html')

# Upload media (images, videos, GIFs)
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('File uploaded successfully!')
        return redirect(url_for('chatroom', chatroom_id="default"))
    else:
        flash('Invalid file type!')
        return redirect(request.url)

# Run the Flask app
if __name__ == "__main__":
    db.create_all()  # Create tables if not already created
    app.run(host='0.0.0.0', port=5000, debug=True)

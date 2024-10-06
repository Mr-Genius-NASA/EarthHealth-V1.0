from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='forum/static')
CORS(app)  # Enable CORS for all routes
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forum.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '09684663955'  # Set the secret key for session management
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    filename = db.Column(db.String(200), nullable=True)
    file_url = db.Column(db.String(300), nullable=True)

with app.app_context():
    db.create_all()  # Create tables if they don't exist

@app.route('/forum')
def index_forum():
    posts = Post.query.all()
    return render_template('forum.html', posts=posts)

@app.route('/upload', methods=['GET', 'POST'])
def upload_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        file = request.files.get('file')

        # Ensure the uploads directory exists
        upload_folder = 'static/uploads'
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)  # Create the directory if it doesn't exist

        if file:
            filename = file.filename
            file.save(os.path.join(upload_folder, filename))  # Save the file in the uploads directory
            
            # Construct the file URL
            file_url = f'http://127.0.0.1:5000/static/uploads/{filename}'
            print(f'File uploaded: {filename}')  # Debugging print statement
        else:
            filename = None
            file_url = None

        new_post = Post(title=title, content=content, filename=filename, file_url=file_url)
        db.session.add(new_post)
        db.session.commit()
        flash('Post uploaded successfully!')
        return redirect(url_for('index_forum'))

    return render_template('post.html')
if __name__ == "__main__":
    app.run('0.0.0.0', debug=True)
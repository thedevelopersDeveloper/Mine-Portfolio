from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-unique-secret-key-12345'

db = SQLAlchemy(app)

# Define the Data model
class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

# Create tables after model definition
with app.app_context():
    db.create_all()

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        new_message = Data(name=name, email=email, message=message)
        db.session.add(new_message)
        db.session.commit()

        flash('Your message has been sent successfully!', 'success')
        return redirect('/contact')
    except Exception as e:
        db.session.rollback()
        flash(f'An error occurred: {e}', 'error')
        return redirect('/contact')


if __name__ == '__main__':
    app.run(debug=True)
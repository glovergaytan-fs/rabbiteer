from flask import Flask, render_template, request, redirect, url_for, session
import json
import os
from dotenv import load_dotenv

load_dotenv()
my_secret_key = os.getenv("S_KEY")
app = Flask(__name__)
app.secret_key = my_secret_key  # Important for sessions 

# Data storage (we'll use a JSON file for simplicity)
DATA_FILE = 'suggestions.json'

# Load suggestions from JSON or initialize an empty list
def load_suggestions():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Save suggestions to JSON
def save_suggestions(suggestions):
    with open(DATA_FILE, 'w') as f:
        json.dump(suggestions, f)

@app.route('/')
def index():
    suggestions = load_suggestions()
    # Sort suggestions by net votes (upvotes - downvotes)
    suggestions.sort(key=lambda x: x['upvotes'] - x['downvotes'], reverse=True) 
    return render_template('index.html', suggestions=suggestions)

@app.route('/upvote/<int:index>')
def upvote(index):
    suggestions = load_suggestions()
    if 0 <= index < len(suggestions):
        if f'voted_{index}' not in session:
            suggestions[index]['upvotes'] += 1
            session[f'voted_{index}'] = 'up'
            save_suggestions(suggestions)
        elif session[f'voted_{index}'] == 'down':  # Change vote
            suggestions[index]['upvotes'] += 1
            suggestions[index]['downvotes'] -= 1
            session[f'voted_{index}'] = 'up'
            save_suggestions(suggestions) 
    return redirect(url_for('index'))

@app.route('/downvote/<int:index>')
def downvote(index):
    suggestions = load_suggestions()
    if 0 <= index < len(suggestions):
        if f'voted_{index}' not in session:
            suggestions[index]['downvotes'] += 1
            session[f'voted_{index}'] = 'down'
            save_suggestions(suggestions)
        elif session[f'voted_{index}'] == 'up': # Change vote
            suggestions[index]['downvotes'] += 1
            suggestions[index]['upvotes'] -= 1
            session[f'voted_{index}'] = 'down'
            save_suggestions(suggestions)
    return redirect(url_for('index'))

@app.route('/suggest', methods=['POST'])
def suggest():
    new_suggestion = request.form['suggestion']
    suggestions = load_suggestions()
    suggestions.append({'text': new_suggestion, 'upvotes': 0, 'downvotes': 0})
    save_suggestions(suggestions)
    return redirect(url_for('index'))

@app.route('/build')
def build():
    # This is just a placeholder build function to demonstrate
    # the GitHub Actions workflow. 
    # Replace this with your actual build logic if needed.
    print("Building website...")
    return "Build complete!"

if __name__ == '__main__':
    app.run(debug=True) 
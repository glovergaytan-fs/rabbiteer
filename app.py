from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

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
        suggestions[index]['upvotes'] += 1
        save_suggestions(suggestions)
    return redirect(url_for('index'))

@app.route('/downvote/<int:index>')
def downvote(index):
    suggestions = load_suggestions()
    if 0 <= index < len(suggestions):
        suggestions[index]['downvotes'] += 1
        save_suggestions(suggestions)
    return redirect(url_for('index'))

@app.route('/suggest', methods=['POST'])
def suggest():
    new_suggestion = request.form['suggestion']
    suggestions = load_suggestions()
    suggestions.append({'text': new_suggestion, 'upvotes': 0, 'downvotes': 0})
    save_suggestions(suggestions)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
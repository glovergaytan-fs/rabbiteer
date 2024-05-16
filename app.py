from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Important for session management

DATA_FILE = 'suggestions.json'

def load_suggestions():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_suggestions(suggestions):
    with open(DATA_FILE, 'w') as f:
        json.dump(suggestions, f)

@app.route('/')
def index():
    suggestions = load_suggestions()
    suggestions.sort(key=lambda x: x['upvotes'] - x['downvotes'], reverse=True) 
    return render_template('index.html', suggestions=suggestions)

@app.route('/upvote/<int:index>', methods=['POST'])
def upvote(index):
    if 'voted_suggestions' not in session:
        session['voted_suggestions'] = []

    if index not in session['voted_suggestions']:
        suggestions = load_suggestions()
        if 0 <= index < len(suggestions):
            suggestions[index]['upvotes'] += 1
            session['voted_suggestions'].append(index)
            save_suggestions(suggestions)
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'already_voted'})

@app.route('/downvote/<int:index>', methods=['POST'])
def downvote(index):
    if 'voted_suggestions' not in session:
        session['voted_suggestions'] = []

    if index not in session['voted_suggestions']:
        suggestions = load_suggestions()
        if 0 <= index < len(suggestions):
            suggestions[index]['downvotes'] += 1
            session['voted_suggestions'].append(index)
            save_suggestions(suggestions)
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'already_voted'})

@app.route('/suggest', methods=['POST'])
def suggest():
    new_suggestion = request.form['suggestion']
    suggestions = load_suggestions()
    suggestions.append({'text': new_suggestion, 'upvotes': 0, 'downvotes': 0})
    save_suggestions(suggestions)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
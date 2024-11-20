from flask import Flask, request, redirect, jsonify
from flask_cors import CORS
import random
import string
import json
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

url_map = {}
file_path = "urls.json"  # The file where the URL mappings will be stored

# Helper function to generate a short ID
def generate_short_id(num_chars):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=num_chars))

# Function to load existing URL mappings from the file
def load_url_map():
    global url_map
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            url_map = json.load(file)

# Function to save URL mappings to the file
def save_url_map():
    with open(file_path, "w") as file:
        json.dump(url_map, file, indent=4)

# Load the URL mappings when the server starts
load_url_map()

@app.route('/shorten', methods=['POST'])
def shorten_url():
    original_url = request.json['url']
    print(f"Received URL: {original_url}")  # Log the incoming URL

    # Check if the URL already exists in the URL map
    for short_id, url in url_map.items():
        if url == original_url:
            print(f"URL already shortened: {url}")
            return jsonify(shortened_url=f'http://127.0.0.1:5000/{short_id}')

    # Generate a new short ID
    short_id = generate_short_id(6)
    url_map[short_id] = original_url
    save_url_map()  # Save the updated mappings to the file

    print(f"Shortened URL: http://127.0.0.1:5000/{short_id}")  # Log the shortened URL
    return jsonify(shortened_url=f'http://127.0.0.1:5000/{short_id}')


@app.route('/<short_id>')
def redirect_url(short_id):
    original_url = url_map.get(short_id)
    if original_url:
        return redirect(original_url)
    return 'URL not found', 404

if __name__ == '__main__':
    app.run(debug=True)

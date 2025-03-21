import json

from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)

posts = {
    1: {
        "id": 1,
        "upvote": 3,
        "title": "My cat is the cutest!",
        "link": "https://i.imgur.com/jseZqNK.jpg",
        "username": "alicia98"
    },
    2: {
        "id": 1,
        "upvote": 3,
        "title": "Cat loaf",
        "link": "https://i.imgur.com/TJ46wX4.jpg",
        "username": "alicia98"
    }
}

@app.route("/tasks/")

# Get all posts 
def get_posts():
    response = {"posts": list(posts.values())}
    return json.dumps(response), 200

# Create a post

# Get a specific post

# Delete a specific post

# Get comments for a specific post

# Post a comment for a specific post

# Edit a comment for a specific post


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

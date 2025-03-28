import json

from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)

def success_response(body, code=200):
    return json.dumps(body), code

def failure_response(message, code=404):
    return json.dumps({'error': message}), code

posts = {
    1: {
        "id": 0,
        "upvotes": 3,
        "title": "My cat is the cutest!",
        "link": "https://i.imgur.com/jseZqNK.jpg",
        "username": "alicia98"
    },
    2: {
        "id": 1,
        "upvotes": 3,
        "title": "Cat loaf",
        "link": "https://i.imgur.com/TJ46wX4.jpg",
        "username": "alicia98"
    }
}

post_id_counter = 2

comments = {
    1: [
        {
            "id": 0,
            "upvotes": 8,
            "text": "Wow, my first Reddit gold!",
            "username": "alicia98"
        }
    ],
    2: [
        {
            "id": 1,
            "upvotes": 8,
            "text": "Wow, my first Reddit gold!",
            "username": "alicia98"
        }
    ],
}

comment_id_counter = 2

# Get all posts 
@app.route("/api/posts/")
def get_posts():
    response = {"posts": list(posts.values())}
    return success_response(response)

# Create a post
@app.route("/api/posts/", methods=["POST"])
def create_post():
    global post_id_counter
    body = json.loads(request.data)
    post = {
        "id": post_id_counter,
        "upvotes": 1,
        "title": body["title"],
        "link": body["link"],
        "username": body["username"]
    }
    posts[post_id_counter] = post
    comments[post_id_counter] = []
    post_id_counter += 1
    if post is None:
        return failure_response("Something went wrong while creating post!", 500)
    return success_response(post, 201)

# Get a specific post
@app.route("/api/posts/<int:pid>/")
def get_post(pid):
    post = posts.get(pid)
    if post is None:
        return failure_response("Post not found!")
    return success_response(post)

# Delete a specific post
@app.route("/api/posts/<int:pid>/", methods=["DELETE"])
def delete_post(pid):
    post = posts.get(pid)
    if post is None:
        return failure_response("Post not found!")
    del posts[pid]
    del comments[pid]
    return success_response(post)

# Get comments for a specific post
@app.route("/api/posts/<int:pid>/comments/")
def get_comments(pid):
    comment_list = comments.get(pid)
    if comment_list is None:
        return failure_response("Comments not found!")
    response = {"comments": comment_list}
    return success_response(response)

# Post a comment for a specific post
@app.route("/api/posts/<int:pid>/comments/", methods=["POST"])
def create_comment(pid):
    global comment_id_counter
    body = json.loads(request.data)
    # Checks to see if the post referenced exists
    if posts.get(pid) is None:
        return failure_response("Post not found!")
    comment = {
        "id": comment_id_counter,
        "upvotes": 1,
        "text": body["text"],
        "username": body["username"]
    }
    if comment is None:
        return failure_response("Something went wrong while creating comment!", 500)
    # Checks to see if there is already comments for the post
    if comments.get(pid) is None:
        comments[pid] = [comment]
    else:
        comments[pid].append(comment)
    comment_id_counter += 1
    return success_response(comment, 201)

# Edit a comment for a specific post
@app.route("/api/posts/<int:pid>/comments/<int:cid>/", methods=["PUT"])
def edit_comment(pid, cid):
    if pid not in comments:
        return failure_response("Post not found!")
    comment_list = comments[pid]
    target_comment = None
    # Parses through all the comments in the post's comment list until one matches the cid
    for comment in comment_list:
        if comment["id"] == cid:
            target_comment = comment
            break
    if target_comment is None:
        return failure_response("Comment not found!")
    body = json.loads(request.data)
    target_comment["text"] = body["text"]
    return success_response(target_comment)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

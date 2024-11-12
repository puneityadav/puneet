from flask import Flask, request, jsonify
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

# In-memory "database" for storing blog posts
blog_posts = {}

# This is my Blog Post Resource
class BlogPost(Resource):
    def get(self, post_id=None):
        if post_id is None:
            return jsonify(blog_posts)
        
        post = blog_posts.get(post_id)
        if post is not None:
            return jsonify(post)
        else:
            return {"message": "Post not found"}, 404

    def post(self):
        data = request.get_json()
        post_id = len(blog_posts) + 1
        blog_posts[post_id] = {
            "id": post_id,
            "title": data["title"],
            "content": data["content"]
        }
        return {"message": "Post created successfully", "post": blog_posts[post_id]}, 201

    def put(self, post_id):
        post = blog_posts.get(post_id)
        if post is None:
            return {"message": "Post not found"}, 404

        data = request.get_json()
        post["title"] = data.get("title", post["title"])
        post["content"] = data.get("content", post["content"])
        return {"message": "Post updated successfully", "post": post}, 200

    def delete(self, post_id):
        if post_id in blog_posts:
            deleted_post = blog_posts.pop(post_id)
            return {"message": "Post deleted successfully", "post": deleted_post}, 200
        else:
            return {"message": "Post not found"}, 404

# adding some resources to the API
api.add_resource(BlogPost, "/posts", "/posts/<int:post_id>")

# this will be our Root route for the API
@app.route('/')
def home():
    return "Welcome to the Blog API! " 

if __name__ == "__main__":
    app.run(debug=True)

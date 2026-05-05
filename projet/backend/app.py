from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)

# ---------------- MODELS ----------------

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(200))
    caption = db.Column(db.String(200))

# ---------------- ROUTES HTML ----------------

@app.route("/")
def home():
    posts = Post.query.all()
    return render_template("home.html", posts=posts)

# ---------------- API ----------------

@app.route("/api/posts", methods=["GET"])
def get_posts():
    posts = Post.query.all()
    return jsonify([
        {"id": p.id, "image": p.image, "caption": p.caption}
        for p in posts
    ])

@app.route("/api/posts", methods=["POST"])
def create_post():
    data = request.json

    if not data.get("image"):
        return {"error": "image required"}, 400

    post = Post(
        image=data["image"],
        caption=data.get("caption", "")
    )

    db.session.add(post)
    db.session.commit()

    return {"message": "post created"}

# ---------------- RUN ----------------

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
# from flask import Flask, render_template
app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "sqlite:///mydatabase.db"  # SQLite database file name
db = SQLAlchemy(app)


# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"


# Define Post model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    # user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"<Post {self.title}>"


@app.route("/")
def hello():
    return "Hello, World!"


def create_user_and_post():
    with app.app_context():  # Create an application context
        # Create a new user
        new_user = User(username="Sczaxzsdpppiswsal")
        print(new_user, " new user")
        db.session.add(new_user)
        db.session.commit()

        # Create a new post for the user
        new_post = Post(
            title="My First Post",
            content="This is the content of my first post.",
            # user_id=new_user.id,
        )
        db.session.add(new_post)
        db.session.commit()


@app.route("/posts")
def list_posts():
    # Query all posts from the database
    posts = Post.query.all()

    # Render a simple HTML page to display posts and their authors
    return render_template("posts.html", posts=posts)


if __name__ == "__main__":
    with app.app_context():  # Create an application context
        db.create_all()  # Create database tables

    # Call the function to create a new user and a post
    create_user_and_post()

    # Run the Flask app
    app.run()

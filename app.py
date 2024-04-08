"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import db, connect_db, User, Post
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Milagros@localhost:5432/blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = 'secret'
toolbar = DebugToolbarExtension(app)

connect_db(app)

# Create the User table if it doesn't exist
with app.app_context():
    db.drop_all()
    db.create_all()

with app.app_context():
    User.query.delete()

# Check if User table is empty before inserting dummy users
with app.app_context():
    if User.query.count() == 0:
        user1 = User(first_name='Sabina', last_name='Rasulova', image_url='https://images.unsplash.com/photo-1544005313-94ddf0286df2?q=80&w=1976&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D')
        user2 = User(first_name='Jane', last_name='Doe', image_url='https://images.unsplash.com/photo-1554151228-14d9def656e4?q=80&w=1972&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D')
        user3 = User(first_name='Michael', last_name='Johnson', image_url='https://images.unsplash.com/photo-1504593811423-6dd665756598?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D')
        user4 = User(first_name='Emily', last_name='Brown', image_url='https://images.unsplash.com/photo-1580489944761-15a19d654956?q=80&w=1961&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D')
        user5 = User(first_name='David', last_name='Williams', image_url='https://images.unsplash.com/photo-1500648767791-00dcc994a43e?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D')

        # Add users to the session
        db.session.add_all([user1, user2, user3, user4, user5])

        # Commit the session to persist changes to the database
        db.session.commit()


@app.route('/')
def home_page():
    users = User.query.all()
    return render_template("base.html", users=users)

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/addUser')
def add_user_page():
    return render_template("addUser.html")

@app.route('/addUser', methods=["POST"])
def add_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    user = User(first_name=first_name, last_name = last_name, image_url=image_url)

    db.session.add(user)
    db.session.commit()
    return redirect(f"/{user.id}")

@app.route("/<int:user_id>")
def show_user_detail(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("detail.html", user=user)

@app.route("/<int:user_id>/edit")
def edit_user_page(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("editUser.html", user = user)

@app.route("/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form["last_name"]
    user.image_url = request.form['image_url']
    db.session.commit()
    return redirect(f'/{user.id}')


@app.route("/<int:user_id>/delete")
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/")


@app.route("/users/<int:user_id>/posts/new", methods=["GET"])
def show_add_post_new(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('addPost.html', user=user)

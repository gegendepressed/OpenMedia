from flask import Flask, render_template, url_for, flash, redirect, request
from form import RegistrationForm, LoginForm, PostForm
from models import *
from datetime import datetime
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
import hashlib
import time


login_manager = LoginManager()
app = Flask(__name__)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)
login_manager.init_app(app)
with app.app_context():
    db.create_all()

salt = "mysalt"



@login_manager.user_loader
def load_user(user_id):
    return db.session.execute(db.select(User).where(User.username == user_id)).scalar_one_or_none()

@app.route("/")
def home():
    posts = db.session.scalars( select(Posts) ).all()

    return render_template('home.html', posts=posts, datetime=datetime)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = hashlib.sha256((form.password.data + salt).encode('utf-8')).hexdigest()
        user = User(
            username=form.username.data,
            fullname=form.fullname.data,
            email=form.email.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}! Go Login Now !', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.execute(db.select(User).where(User.username == form.username.data)).scalar_one_or_none()
        hashed_password = hashlib.sha256((form.password.data + salt).encode('utf-8')).hexdigest()
        if user and hashed_password == user.password:
            login_user(user)
            flash('You have been logged in!', 'success')
            next = request.args.get('next')
            return redirect(next or url_for('home'))
        else:
            flash("Login Unsuccessful, Please check Username and Passowrd", "danger")

    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect( url_for("home") )

@app.route("/account")
@login_required
def account():
    image_file = url_for('static', filename = current_user.profile_pic_url)
    return render_template('account.html', title='Your Account', profile_pic_url= image_file)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm() 
    if form.validate_on_submit():
        timestamp = int(time.time())
        post = Posts( 
                     title=form.title.data, 
                     text=form.content.data,
                     owner=current_user,
                     timestamp=timestamp
                     )
        db.session.add(post)
        db.session.commit()
        flash('Post Created!', 'success')
        return redirect(url_for('home'))
    return render_template('newpost.html', title='New Post', form=form, legend='New Post')



if __name__ == '__main__':
    app.run(debug=True)

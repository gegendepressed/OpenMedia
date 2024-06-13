from flask import Flask, render_template, url_for, flash, redirect, request
from form import RegistrationForm, LoginForm, PostForm, CommentForm, EditProfileForm, RequestResetForm, ResetPasswordForm
from models import *
from datetime import datetime
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_mail import Mail, Message
import hashlib
import time
from pytz import timezone
from itsdangerous.url_safe import URLSafeTimedSerializer
from itsdangerous.exc import SignatureExpired
import os
from fileupload import upload_image, delete_image
import secrets
from sqlalchemy import delete
from PIL import Image
from io import BytesIO

login_manager = LoginManager()
mail = Mail()
app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY") if os.environ.get("FLASK_SECRET_KEY") else '5791628bb0b13ce0c676dfde280ba245'
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URI") if os.environ.get("DB_URI") else "sqlite:///project.db"
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")

db.init_app(app)
login_manager.init_app(app)
mail.init_app(app)

with app.app_context():
    db.create_all()

salt = "mysalt"
salt = os.environ.get("FLASK_SALT") if os.environ.get("FLASK_SALT") else salt
itsd_secret_key = "SECRET-KEY"
itsd_secret_key = os.environ.get("ITSD_SECRET_KEY") if os.environ.get("ITSD_SECRET_KEY") else itsd_secret_key
itsd_salt = "MY-SALT"
itsd_salt = os.environ.get("ITSD_SALT") if os.environ.get("ITSD_SALT") else itsd_salt
reset_pass_serializer = URLSafeTimedSerializer(itsd_secret_key, salt=itsd_salt)
tz = timezone("Asia/Kolkata")


def send_reset_mail(recipient_email, signature):
    msg = Message("Openmedia: Reset Password")
    msg.body = (f"Use this URL to reset your password: {url_for('reset_password', token=signature, _external=True)} \n"
                f"Only Valid for 15 minutes.\n\n"
                f"Ignore if not requested")
    msg.add_recipient(recipient_email)
    mail.send(msg)


def check_moderator(user):
    if current_user.is_authenticated:
        if current_user.is_moderator():
            return True
    return False


@app.context_processor
def moderator_processor():
    return dict(check_moderator=check_moderator)


@login_manager.user_loader
def load_user(user_id):
    return db.session.execute(db.select(User).where(User.username == user_id)).scalar_one_or_none()


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))

@app.route("/")
def home():
    current_page = request.args.get('page', 1, type=int)
    query = db.select(Posts).order_by(Posts.timestamp.desc())
    posts = db.paginate(query, page = current_page, per_page=10)
    page_list = posts.iter_pages(left_edge=1,right_edge=1, left_current=2, right_current=2)
    return render_template('home.html', title='Home', current_page=current_page,
                           posts=posts,datetime=datetime,tz=tz, page_list=page_list)

@app.route("/profile/<string:username>")
def profile(username):
    user = db.session.execute( select(User).where(User.username == username ) ).scalar_one_or_none()
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for('home'))

    current_page = request.args.get('page', 1, type=int)
    query = db.select(Posts).where(Posts.owner_id == username).order_by(Posts.timestamp.desc())
    posts = db.paginate(query, page=current_page, per_page=5)
    page_list = posts.iter_pages(left_edge=1, right_edge=1, left_current=2, right_current=2)
    return render_template('profile.html',
                               user=user,
                               posts=posts,
                               current_page=current_page,
                               page_list=page_list,
                               datetime=datetime,
                               tz=tz
                           )


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
            login_user(user, remember=form.remember.data)
            flash('You have been logged in!', 'success')
            next = request.args.get('next')
            return redirect(next or url_for('home'))
        else:
            flash("Login Unsuccessful, Please check Username and Password", "danger")
    return render_template('login.html', title='Login', form=form)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = db.session.execute(db.select(User).where(User.username == form.username.data)).scalar_one_or_none()
        if user:
            token = reset_pass_serializer.dumps({"username": user.username})
            send_reset_mail(user.email, token)
        flash('If the user exists, an email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', legend='Reset Password', form=form)

@app.route("/reset_password/<string:token>", methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    try:
        user_dict = reset_pass_serializer.loads(token, max_age=900)
    except SignatureExpired:
        flash("Reset Token expired, please regenerate.", "danger")
        return redirect(url_for("reset_request"))
    except:
        flash("Invalid Password Reset Token.", "danger")
        return redirect(url_for("reset_request"))

    username = user_dict["username"]
    form = ResetPasswordForm()

    if form.validate_on_submit():
        user = db.session.execute(db.select(User).where(User.username == username)).scalar_one_or_none()
        user.password = hashlib.sha256((form.password.data + salt).encode('utf-8')).hexdigest()
        db.session.commit()
        flash("Password Reset Successfully!", "success")
        return redirect(url_for("home"))
    return render_template('reset_password.html', legend='Enter new password: ', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect( url_for("home") )

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    image_file = url_for('static', filename = current_user.profile_pic_url)
    user=current_user
    form = EditProfileForm()
    if form.validate_on_submit():
        file = form.photo.data
        if file:
            randomhex = secrets.token_hex(10)
            if user.profile_pic_url != "user.png":
                current_image_id = user.profile_pic_url.split("/")[-1]
                delete_image(current_image_id)

            image_id = upload_image(file, f"{current_user.username}_profile_{randomhex}")
            with Image.open(file) as im:
                size = 175, 175
                im.thumbnail(size, resample=Image.LANCZOS)
                final_image = BytesIO()
                im.save(final_image, format='png')
                final_image.seek(0)
            image_url = upload_image(final_image, image_id)
            user.profile_pic_url = image_url

        user.fullname = form.fullname.data if form.fullname.data else user.fullname
        user.email = form.email.data if form.email.data else user.email
        if form.password.data:
            user.password = hashlib.sha256((form.password.data + salt).encode('utf-8')).hexdigest()
        db.session.commit()
        flash('Profile has been updated!', 'success')

        return redirect(url_for('home'))
    return render_template('account.html', title='Your Account', form=form,user=user, profile_pic_url= image_file)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm() 
    if form.validate_on_submit():
        timestamp = int(time.time())
        file = form.photo.data
        if file:
            randomhex = secrets.token_hex(10)
            image_url = upload_image(file, f"{current_user.username}_post_{randomhex}")
            post = Posts(
                title=form.title.data,
                text=form.content.data,
                owner=current_user,
                timestamp=timestamp,
                image=image_url
            )
        else:
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

@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    post = db.session.execute(db.select(Posts).where(Posts.id == post_id)).scalar_one_or_none()
    comments_list = post.comments[::-1] if post.comments else []
    if current_user.is_authenticated:
        has_liked = db.session.execute(select(Likes)
                                       .where(Likes.liked_by_id == current_user.username)
                                       .where(Likes.liked_post_id == post_id)
                                       ).scalar_one_or_none()
        form = CommentForm(text="")
        if form.validate_on_submit() :
            comment = Comments( 
                        text=form.text.data,
                        created_by=current_user,
                        post_id = post_id,
                        )
            db.session.add(comment)
            post.comments.append(comment)
            comment.created_by = current_user
            db.session.commit()
            flash('Comment Created!', 'success')
            return redirect(url_for("post", post_id=post_id))

        return render_template('post.html', post=post,datetime=datetime,comments=comments_list,form=form,tz=tz, has_liked=has_liked)
    else:
        return render_template('post.html', post=post,datetime=datetime,comments=comments_list,form=None,tz=tz)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
        post = db.session.execute(db.select(Posts).where(Posts.id == post_id)).scalar_one_or_none()
        form = PostForm(title=post.title, content=post.text)
        if post.owner != current_user and not check_moderator(current_user):
            return redirect(url_for('post', post_id=post.id))
        if form.validate_on_submit():
                post.title = form.title.data
                post.text = form.content.data
                file = form.photo.data
                if file:
                    if post.image:
                        image_id = post.image.split("/")[-1]
                        delete_image(image_id)

                        randomhex = secrets.token_hex(10)
                        image_url = upload_image(file, f"{current_user.username}_post_{randomhex}")

                        post.image = image_url
                    else:
                        randomhex = secrets.token_hex(10)
                        image_url = upload_image(file, f"{current_user.username}_post_{randomhex}")
                        post.image = image_url
                db.session.commit()
                flash('Post has been updated!', 'success')
                return redirect(url_for('home'))
        return render_template('newpost.html', title='Update Post', form=form, legend='Update Post')

@app.route("/post/<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
        post = db.session.execute(db.select(Posts).where(Posts.id == post_id)).scalar_one_or_none()
        if post.owner != current_user and not check_moderator(current_user):
               return redirect(url_for('post', post_id=post.id))
        else:
            if post.image:
                image_id = post.image.split("/")[-1]
                delete_image(image_id)
            db.session.execute( delete(Comments).where(Comments.post_id == post_id) )
            db.session.execute( delete(Likes).where(Likes.liked_post_id == post_id) )
            db.session.delete(post)
            db.session.commit()
            flash('Post has been Deleted !', 'success')
            return redirect(url_for('home'))

@app.route("/post/<int:post_id>/like", methods=['GET', 'POST'])
@login_required
def like_post(post_id):
    post = db.session.get(Posts, post_id)
    has_liked = db.session.execute( select(Likes)
                                    .where(Likes.liked_by_id == current_user.username)
                                    .where(Likes.liked_post_id == post_id )
                                ).scalar_one_or_none()
    
    if not has_liked:
        like_object = Likes(
            liked_post_id=post_id,
            liked_by_id=current_user.username
        )
        db.session.add(like_object)
        post.likes.append(like_object)
        db.session.commit()
    else:
        post.likes.remove(has_liked)
        db.session.delete(has_liked)
        db.session.commit()
    return redirect(url_for('post', post_id=post_id))




if __name__ == '__main__':
    app.run(debug=True)

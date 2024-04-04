from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from sqlalchemy import select
from models import *


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2,max=19)])
    fullname = StringField('Full Name', validators=[DataRequired(), Length(min=2,max=19)])
    email = EmailField('Email Address', validators=[DataRequired(),Email()])
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField("Repeat the Password",validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        result = db.session.execute(select(User.username).where(User.username == username.data)).all()
        if result:
            raise ValidationError(f"The username {username.data} is taken, please choose a different one")

    def validate_email(self, email):
        result = db.session.execute(select(User.username).where(User.email == email.data)).all()
        if result:
            raise ValidationError(f"The email {email.data} is already used, please choose a different one")


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('New Password', validators=[DataRequired()] )
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")

class PostForm(FlaskForm):
    title = StringField('Add Post Title',validators=[DataRequired()])
    content = TextAreaField("Write down your thoughts !",validators=[DataRequired()])
    submit = SubmitField("Submit")

class CommentForm(FlaskForm):
    text = TextAreaField("Comment here!",validators=[DataRequired()])
    submit = SubmitField("Submit")
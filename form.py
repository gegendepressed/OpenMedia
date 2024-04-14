from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed, FileSize
from wtforms import StringField, PasswordField, EmailField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from wtforms import validators
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

class RequestResetForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField("Submit")

class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField("Repeat the Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Reset")

class PostForm(FlaskForm):
    title = StringField('Add Post Title',validators=[DataRequired()])
    content = TextAreaField("Write down your thoughts !",validators=[DataRequired()])
    photo = FileField("image", validators=[validators.Optional(),
                                        FileAllowed(['jpg', 'png'], 'Please choose jpg or png!'),
                                        FileSize(max_size=2*1024*1024, message="File must be under 2MB")
                                        ])
    submit = SubmitField("Submit")

class CommentForm(FlaskForm):
    text = TextAreaField("",validators=[DataRequired()])
    submit = SubmitField("Submit")

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[])
    fullname = StringField('Full Name', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')
    email = EmailField('Email Address', validators=[validators.Optional(),Email()])
    password = PasswordField('New Password', validators=[])
    confirm_password = PasswordField("Repeat the Password", validators=[EqualTo('password')])

    def validate_username(self, username):
        result = db.session.execute(select(User.username).where(User.username == username.data)).all()
        if result:
            raise ValidationError(f"The username {username.data} is taken, please choose a different one")

    def validate_email(self, email):
        result = db.session.execute(select(User.username).where(User.email == email.data)).all()
        if result:
            raise ValidationError(f"The email {email.data} is already used, please choose a different one")
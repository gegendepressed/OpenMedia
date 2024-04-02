from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2,max=19)])
    fullname = StringField('Full Name', validators=[DataRequired(), Length(min=2,max=19)])
    email = EmailField('Email Address', validators=[DataRequired(),Email()])
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField("Repeat the Password",validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Sign Up")

class LoginForm(FlaskForm):
    email = EmailField('Email Address', validators=[DataRequired(),Email()])
    password = PasswordField('New Password', validators=[DataRequired()] )
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")
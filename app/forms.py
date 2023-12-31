from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User #, Skis

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    location = StringField('location')
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
        
class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    location = StringField('location')
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    location = StringField('location')
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

class PostForm(FlaskForm):
    post = TextAreaField('Say something', validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Submit')

class SkiForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    length = TextAreaField('length', validators=[DataRequired()])
    make = TextAreaField('make', validators=[DataRequired()])
    model = TextAreaField('model', validators=[DataRequired()])
    binding = TextAreaField('binding')
    description = TextAreaField('Description', validators=[DataRequired()])
    image_url = StringField('Image URL')
    submit = SubmitField('Create Post')

class SurfForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    length = TextAreaField('length', validators=[DataRequired()])
    make = TextAreaField('make', validators=[DataRequired()])
    model = TextAreaField('model', validators=[DataRequired()])
    description= TextAreaField('Description', validators=[DataRequired()])
    image_url = StringField('Image URL')
    submit = SubmitField('Create Post')
from flask_wtf import FlaskForm
from models import User
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from passlib.hash import pbkdf2_sha512

def invalid_credentials(form, field):
    username_entered=form.username.data
    passord_entered=field.data

    user_object = User.query.filter_by(username=username_entered).first()
    if user_object is None:
        raise ValidationError("Username or password is incorrect.")
    elif not pbkdf2_sha512.verify(passord_entered, user_object.password):
        raise ValidationError("Username or password is incorrect.")

class RegistrationForm(FlaskForm):
    """Registration Form"""

    username = StringField('username_label',
        validators=[InputRequired(message="Username Required"),
        Length(min=4, max=25, message="Username must be between 4 and 25 characters")])
    password = PasswordField('password_label',
        validators=[InputRequired(message="Password Required"),
        Length(min=4, max=25, message="Password must be between 4 and 25 characters")])
    confirm_pswd = PasswordField('confirm_pswd',
        validators=[InputRequired(message="Confirm Password"),
        EqualTo('password', message="Passwords must match!")])
    
    submit_button=SubmitField('Create')
    
    def validate_username(self, username):
        user_object = User.query.filter_by(username=username.data).first()
        if user_object:
            raise ValidationError("Username already exists! Select a different username.")
            
            
class LoginForm(FlaskForm):
    username=StringField('username_label', validators=[InputRequired(message="username required")])
    password=PasswordField('password_label', validators=[InputRequired(message="password required"),
    invalid_credentials])
    
    submit_button=SubmitField('Login')
    


    
    
    
    
    
    
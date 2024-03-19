from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import Email, DataRequired

class SimpleFrom(FlaskForm):
    text = StringField("Login: ", validators=[DataRequired()])
    #email = StringField("Email: ", validators=[Email()])
    #gender = SelectField('Gender: ', choices=[('m', 'man'), ('w', 'woman')])

    password = PasswordField('Password: ', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password: ')

    accept_tos = BooleanField('I accept all. ', [validators.DataRequired()])
    submit = SubmitField("Log in!")
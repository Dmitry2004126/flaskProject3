from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import Email, DataRequired, Length


class SimpleFrom(FlaskForm):
    text = StringField("Login: ", validators=[DataRequired()])
    email = StringField("Email: ", validators=[Email()])

    password = PasswordField('Password: ', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password: ')

    accept_tos = BooleanField('You will get an email! ', [validators.DataRequired()])
    submit = SubmitField("Log in!")


class AddNewItemForm(FlaskForm):

    item_name = StringField('Name', validators=[DataRequired(), Length(1, 100)])
    item_photo = URLField('Photo', validators=[DataRequired()])
    cat_id = SelectField('Category', choices=[])
    item_price = DecimalField('Price', validators=[DataRequired()])
    submit = SubmitField("Add an item")


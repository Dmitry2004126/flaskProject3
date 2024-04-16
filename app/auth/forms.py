from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError


from app.models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me', validators=[DataRequired()])
    submit = SubmitField("Log in")


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1, 64),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_•]*$', 0,
                                                          'users must have only letters,number,dots and underscore')])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2',
                                                                             message="Password doesn't much")])
    password2 = PasswordField('ConfirmPassword', validators=[DataRequired()])
    submit = SubmitField("Reg in")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("email already reg")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Username already use")
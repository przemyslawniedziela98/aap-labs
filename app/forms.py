from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from .models.user import User
from .utils.logger import GlobalLogger


class LoginForm(FlaskForm):
    """
    Form for user login.
    """
    username: StringField = StringField('Username', validators=[DataRequired()])
    password: PasswordField = PasswordField('Password', validators=[DataRequired()])
    submit: SubmitField = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    """
    Form for user registration.
    """
    username: StringField = StringField(
        'Username',
        validators=[DataRequired(), Length(min=3, max=25)]
    )

    password: PasswordField = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=6, message="Password must be at least 6 characters long"),
        ]
    )

    confirm_password: PasswordField = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password', message="Passwords must match.")
        ]
    )

    submit: SubmitField = SubmitField('Register')

    def validate_username(self, username: StringField) -> None:
        """
        Custom validator to ensure the username is unique.

        Args:
            username (StringField): The username input field.
        """
        try:
            user = User.query.filter_by(username=username.data).first()
            if user:
                GlobalLogger.log_error(f"Attempted registration with existing username: {username.data}")
                raise ValidationError('Username already exists.')
        except Exception as e:
            GlobalLogger.log_error(f"Error validating username '{username.data}': {e}")
            raise ValidationError('An error occurred. Please try again.')

    def validate_password(self, field: PasswordField) -> None:
        """
        Custom validator to ensure the password meets complexity requirements.

        Args:
            field (PasswordField): The password input field.
        """
        password = field.data
        if not any(char.isdigit() for char in password):
            GlobalLogger.log_error("Password validation failed: Missing a number.")
            raise ValidationError("Password must contain at least one number.")
        if not any(char.isupper() for char in password):
            GlobalLogger.log_error("Password validation failed: Missing an uppercase letter.")
            raise ValidationError("Password must contain at least one uppercase letter.")

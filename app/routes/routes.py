from flask import Blueprint, render_template, redirect, url_for, flash
from ..models.user import User, db
from ..forms import LoginForm, RegistrationForm
from ..utils.logger import GlobalLogger

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/', methods=['GET', 'POST'])
def main():
    """
    Displays the home page.

    Returns:
        str: The rendered home.html template.
    """
    GlobalLogger.log_info("Accessed home page.")
    return render_template('home.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles user login.

    Returns:
        str: The rendered login.html template on GET or validation failure.
        Response: A redirect to the dashboard on successful login.
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            flash('Login successful!', 'success')
            GlobalLogger.log_info(f"User {form.username.data} logged in successfully.")
            return redirect(url_for('auth.dashboard'))
        else:
            flash('Invalid username or password', 'danger')
            GlobalLogger.log_warning(f"Failed login attempt for user {form.username.data}.")
    return render_template('login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handles user registration.

    Returns:
        str: The rendered register.html template on GET or validation failure.
        Response: A redirect to the login page on successful registration.
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = User(username=form.username.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            GlobalLogger.log_info(f"New user registered: {form.username.data}")
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'danger')
            GlobalLogger.log_error(f"Error registering user {form.username.data}: {e}")
    return render_template('register.html', form=form)

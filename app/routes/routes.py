import os 
from typing import Tuple, List
from flask import Blueprint, render_template, redirect, url_for, flash
from ..models.user import User, db
from ..forms import LoginForm, RegistrationForm
from ..utils.logger import GlobalLogger
from ..utils import const
from flask_login import login_required, current_user, login_user, logout_user

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
            login_user(user)
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

@auth_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    """
    Displays the dashboard.

    Returns:
        str: The rendered dashboard.html template.
    """
    return render_template('dashboard.html', user=current_user)

def generate_subject_page(directory: str) -> Tuple[List[str], List[str]]:
    """
    Generate file paths for subject pages by listing files from specific directories.

    Args:
        directory (str): The base directory path containing the subdirectories.

    Returns:
        Tuple[List[str], List[str]]: A tuple containing two lists:
    """
    base_static_path = os.path.join(os.getcwd(), 'app', 'static', 'class_files')
    course_materials_path = os.path.join(base_static_path, directory)
    additional_materials_path = os.path.join(base_static_path, directory + '_additional')

    def _list_files(directory_path: str) -> List[str]:
        return sorted([
            f for f in os.listdir(directory_path)
            if os.path.isfile(os.path.join(directory_path, f)) and not f.startswith('.')
        ])

    return _list_files(course_materials_path), _list_files(additional_materials_path)

@auth_bp.route('/zmsi', methods=['GET'])
@login_required
def zmsi():
    """
    Route to render the ZMSI page.
    """
    files, files_additional = generate_subject_page('zmsi')

    return render_template(
        'subject_page.html',
        prefix = 'zmsi',
        title = const.SUBJECT_CONTENT['zmsi']['title'],
        description = const.SUBJECT_CONTENT['zmsi']['description'],
        files=files,
        files_additional=files_additional
    )

@auth_bp.route('/app', methods=['GET'])
@login_required
def app():
    """
    Route to render the APP page.
    """
    files, files_additional = generate_subject_page('app')
   
    return render_template(
        'subject_page.html',
        prefix = 'app',
        title = const.SUBJECT_CONTENT['app']['title'],
        description = const.SUBJECT_CONTENT['app']['description'],
        files=files,
        files_additional=files_additional
    )

@auth_bp.route('/logout')
@login_required
def logout():
    """
    Logs the user out and redirects them to the login page.
    """
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('auth.login'))
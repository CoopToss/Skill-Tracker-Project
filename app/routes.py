from flask import redirect, url_for, render_template, request, flash, abort
from flask_login import login_user, logout_user, current_user, login_required
from . import db
from .models import User, Skill, Goal
from .forms import LoginForm, RegistrationForm
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def init_app(app):
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        return render_template('index.html')

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        form = RegistrationForm()
        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            password = form.password.data

            if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
                flash('Username or email already exists.')
                return redirect(url_for('signup'))

            new_user = User(username=username, email=email)
            new_user.set_password(password)

            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)
            return redirect(url_for('dashboard'))
        return render_template('register.html', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            logger.debug('Form validated successfully.')
            email = form.email.data
            password = form.password.data

            user = User.query.filter_by(email=email).first()

            if user and user.check_password(password):
                logger.debug('User authenticated successfully.')
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                logger.debug('Invalid email or password.')
                flash('Invalid email or password.')
        else:
            logger.debug('Form validation failed.')
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"Error in {getattr(form, field).label.text}: {error}")

        return render_template('login.html', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))

    @app.route('/dashboard')
    @login_required
    def dashboard():
        user_id = current_user.id
        user = User.query.get(user_id)
        skills = Skill.query.filter_by(user_id=user_id).all()
        goals = Goal.query.filter_by(user_id=user_id).all()
        return render_template('dashboard.html', user=user, skills=skills, goals=goals)

    @app.route('/add_skill', methods=['POST'])
    @login_required
    def add_skill():
        skill_name = request.form.get('skill_name')
        hours_logged_str = request.form.get('hours_logged')
        goal_details = request.form.get('goal_details')

        if hours_logged_str is None:
            return redirect(url_for('dashboard'))

        try:
            hours_logged = int(hours_logged_str)
            if hours_logged < 0:
                flash('Hours logged cannot be negative.')
                return redirect(url_for('dashboard'))
        except ValueError:
            return redirect(url_for('dashboard'))

        existing_skill = Skill.query.filter_by(name=skill_name, user_id=current_user.id).first()

        if existing_skill:
            existing_skill.hours_logged += hours_logged
            existing_skill.goal_details = goal_details
        else:
            new_skill = Skill(name=skill_name, hours_logged=hours_logged, goal_details=goal_details, user_id=current_user.id)
            db.session.add(new_skill)

        db.session.commit()
        return redirect(url_for('dashboard'))

    @app.route('/skill/<int:skill_id>')
    @login_required
    def skill_detail(skill_id):
        skill = Skill.query.get_or_404(skill_id)
        goal_details = [skill.goal_details] if skill.goal_details else []
        return render_template('skill_detail.html', skill=skill, goal_details=goal_details)

    @app.route('/delete_skill/<int:skill_id>', methods=['POST'])
    @login_required
    def delete_skill(skill_id):
        skill = Skill.query.get_or_404(skill_id)
        if skill.user != current_user:
            abort(403)
        db.session.delete(skill)
        db.session.commit()
        flash('Skill has been deleted!', 'success')
        return redirect(url_for('dashboard'))

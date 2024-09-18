from urllib.parse import urlsplit
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
import sqlalchemy as sa
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User

@app.route('/')
@app.route('/index')
@login_required
def index():
  user = {'username': 'Joe'}
  posts = [
    {
      'author': {'username': 'John'},
      'body': 'Beautify day in Amarillo today. Lorem ipsum dolor sit amet consectetur, adipisicing elit.'
    },
    {
      'author': {'username': 'Ande'},
      'body': 'I should have used a Blackwing.'
    },
    {
      'author': {'username': 'Ron'},
      'body': 'Platform 9 & 3/4!'
    },
    {
      'author': {'username': 'Gandalf'},
      'body': 'There are no safe paths in this part of the world, Bilbo.'
    }
  ]
  return render_template('index.html', title='Home', posts=posts)

@app.route('/about')
def about():
  return render_template('about.html', title="about")

@app.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = LoginForm()
  if form.validate_on_submit():
    user = db.session.scalar(
      sa.select(User).where(User.username == form.username.data))
    if user is None or not user.check_password(form.password.data):
      flash('Invalid username or password')
      return redirect(url_for('login'))
    login_user(user, remember=form.remember_me.data)
    next_page = request.args.get('next')
    if not next_page or urlsplit(next_page).netloc != '':
      next_page = url_for('index')
    return redirect(next_page)
  return render_template('login.html', title='Sign In', form=form)

  @app.route('/logout')
  def logout():
    logout_user()
    return redirect(url_for('index'))

  @app.route('/register', methods=['GET', 'POST'])
  def register():
    if current_user.is_authenticated:
      return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
      user = User(username=form.username.data, email=form.email.data)
      user.set_password(form.password.data)
      db.session.add(user)
      db.session.commit()
      flash('Congratulations, you are now a registered user!')
      return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
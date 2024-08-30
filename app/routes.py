from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
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
  return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/about')
def about():
  return render_template('about.html', title="about")

@app.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    flash('Login requested for user {}, remember_me={}'.format(
      form.username.data, form.remember_me.data
    ))
    return redirect(url_for('index'))
  return render_template('login.html', title='Sign In', form=form)
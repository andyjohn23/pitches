from flask import render_template, redirect, url_for
from . import main
from flask_login import login_required


@main.route('/')
def index():
	"""
	view root page function that returns the index page and its data
	"""

	return render_template('index.html')


@main.route('/category')
def category():
	"""
	view root page function that returns the category page and its data
	"""
    
	return render_template('category.html')



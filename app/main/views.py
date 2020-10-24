from flask import render_template, redirect, url_for
from . import main


@main.route('/')
def index():
	"""
	view root page function that returns the index page and its data
	"""

	return render_template('index.html')


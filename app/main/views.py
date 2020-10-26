from flask import render_template,request,redirect, url_for,abort,flash
from . import main
from flask_login import login_required,current_user
from ..models import User,pitch,likes,dislikes,comments
from .forms import UpdateProfile,CommentsForm,PitchForm
from .. import db,photos


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

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/new_pitch', methods = ['POST','GET'])
@login_required
def new_pitch():
    form = PitchForm()
    if form.validate_on_submit():
        title = form.title.data
        post = form.post.data
        category = form.category.data
        author = current_user
        new_pitch_object = pitch(title = title, post = post, category = category, author = author)
        new_pitch_object.save_pitch()

        flash('Your pitch has been created', 'success')
        return redirect(url_for('main.category'))
        
    return render_template('new_pitch.html', form = form)

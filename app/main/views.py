from flask import render_template, request, redirect, url_for, abort, flash
from . import main
from flask_login import login_required, current_user
from ..models import User, pitch, comment
from .forms import UpdateProfile, CommentsForm, PitchForm
from .. import db, photos


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

    pitches = pitch.query.all()
    sales = pitch.query.filter_by(category = 'sales').all() 
    interview = pitch.query.filter_by(category = 'interview').all()
    elevator = pitch.query.filter_by(category = 'elevator').all()
    promotion = pitch.query.filter_by(category = 'promotion').all()
    personal = pitch.query.filter_by(category = 'personal').all()
    pickuplines = pitch.query.filter_by(category = 'pickuplines').all()

    return render_template('category.html', pitches = pitches, sales = sales,interview = interview, 
    elevator = elevator,promotion = promotion, personal = personal, pickuplines = pickuplines)

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

@main.route('/pitch_new', methods = ['GET','POST'])
@login_required
def new_pitch():
    """
    create and save pitches
    """
    form = PitchForm()
    if form.validate_on_submit():
        pitches = pitch(title = form.title.data, content = form.content.data, category = form.category.data, user_id = current_user.id)
        pitches.save_pitch()

        return(redirect(url_for('main.category')))

    return render_template('pitch_new.html', form = form)

@main.route('/pitch/<category>')
def pitch_category(category):
    """
    displays various pitch categories
    """
    pitches = pitch.query.filter_by(category = category).all()
    return render_template('category.html', pitches = pitches)

@main.route('/pitch/view/<pitch_id>', methods = ['GET', 'POST'])
def view_pitch(pitch_id):
    """
    view pitches
    """
    pitches = pitch.query.filter_by(id = pitch_id).first()
    comments = comment.query.filter_by(pitch_id = pitch_id).all()
    
    return render_template('pitch/pitch.html', pitch = pitches, comments = comments)
    

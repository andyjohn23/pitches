from flask_wtf import FlaskForm
from wtforms import StringField,SelectField,TextAreaField,SubmitField
from wtforms.validators import Required

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')

class PitchForm(FlaskForm):
    """
    pitch form to create new pitch
    """
    title = StringField('Title', validators=[Required()])
    category = SelectField('Pitch Category', choices=[('Sales','Sales'),('Interview','Interview'),
    ('Elevator','Elevator'),('Promotion','Promotion'),('Personal','Personal'),
    ('Pickup-lines','Pickup-lines')],validators=[Required()])
    content = TextAreaField('Pitch', validators=[Required()])
    submit = SubmitField('Post Pitch')


class CommentsForm(FlaskForm):
    """
    comment form
    """
    content = TextAreaField('Comment', validators=[Required()])
    submit = SubmitField('Comment')
from flask import render_template,abort,redirect,url_for
from . import main
from flask_login import login_required
from ..models import User,Review,Comment,Upvote,Downvote
from .forms import UpdateProfile
from .. import db



@main.route('/')
@login_required
def index():
    pitches = Review.query.all()
    job = Review.query.filter_by(category = 'Clubs').all() 
    event = Review.query.filter_by(category = '').all()
    advertisement = Review.query.filter_by(category = 'Advertisement').all()
    return render_template('index.html', job = job,event = event, pitches = pitches,advertisement= advertisement)



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



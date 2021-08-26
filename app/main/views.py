from flask import render_template, redirect, url_for,abort,request
from . import main
from flask_login import login_required,current_user
from ..models import User,Review,Comment,Upvote,Downvote
from .forms import UpdateProfile,ReviewForm,CommentForm
from .. import db,photos

@main.route('/')
@login_required
def index():
    reviews= Review.query.all()
    clubs = Review.query.filter_by(category = 'Clubs').all() 
    hotel = Review.query.filter_by(category = 'Hotel').all()
    restaurant = Review.query.filter_by(category = 'Restaurant').all()
    return render_template('index.html', clubs = clubs,hotel = hotel, reviews = reviews,restaurant= restaurant)

@main.route('/home')
def home():
   
    return render_template('home.html')

@main.route('/create_new', methods = ['POST','GET'])
@login_required
def new_review():
    form = ReviewForm()
    if form.validate_on_submit():
        title = form.title.data
        post = form.post.data
        category = form.category.data
        location=form.location.data
        link=form.link.data
        user_id = current_user
        new_review_object = Review(post=post,user_id=current_user._get_current_object().id,category=category,title=title,location=location,link=link)
        new_review_object.save_p()
        return redirect(url_for('main.index'))
        
    return render_template('create_review.html', form = form)

@main.route('/comment/<int:review_id>', methods = ['POST','GET'])
@login_required
def comment(review_id):
    form = CommentForm()
    review = Review.query.get(review_id)
    all_comments = Comment.query.filter_by(review_id=review_id).all()
    if form.validate_on_submit():
        comment = form.comment.data 
        review_id = review_id
        user_id = current_user._get_current_object().id
        new_comment = Comment(comment = comment,user_id = user_id,review_id=review_id)
        new_comment.save_c()
        return redirect(url_for('.comment', review_id=review_id))
    return render_template('comment.html', form =form, review=review,all_comments=all_comments)


@main.route('/user/<name>')
def profile(name):
    user = User.query.filter_by(username = name).first()
    user_id = current_user._get_current_object().id
    posts = Review.query.filter_by(user_id = user_id).all()
    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user,posts=posts)

@main.route('/user/<name>/updateprofile', methods = ['POST','GET'])
@login_required
def updateprofile(name):
    form = UpdateProfile()
    user = User.query.filter_by(username = name).first()
    if user == None:
        abort(404)
    if form.validate_on_submit():
        user.bio = form.bio.data
        user.save_u()
        return redirect(url_for('.profile',name = name))
    return render_template('profile/update.html',form =form)


@main.route('/user/<name>/update/pic',methods= ['POST'])
@login_required
def update_pic(name):
    user = User.query.filter_by(username = name).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',name=name))

@main.route('/like/<int:id>',methods = ['POST','GET'])
@login_required
def like(id):
    get_reviews = Upvote.get_upvotes(id)
    valid_string = f'{current_user.id}:{id}'
    for review in get_reviews:
        to_str = f'{review}'
        print(valid_string+" "+to_str)
        if valid_string == to_str:
            return redirect(url_for('main.index',id=id))
        else:
            continue
    new_vote = Upvote(user = current_user, review_id=id)
    new_vote.save()
    return redirect(url_for('main.index',id=id))

@main.route('/dislike/<int:id>',methods = ['POST','GET'])
@login_required
def dislike(id):
    review = Downvote.get_downvotes(id)
    valid_string = f'{current_user.id}:{id}'
    for p in review:
        to_str = f'{p}'
        print(valid_string+" "+to_str)
        if valid_string == to_str:
            return redirect(url_for('main.index',id=id))
        else:
            continue
    new_downvote = Downvote(user = current_user, review_id=id)
    new_downvote.save()
    return redirect(url_for('main.index',id = id))
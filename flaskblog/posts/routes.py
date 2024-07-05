from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post, Comment, Like, Chat
from flaskblog.posts.forms import PostForm

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    user = current_user.username
    rooms = Chat.query.filter(Chat.rooms.like(f'%{user}%')).order_by(Chat.date_created.desc()).group_by(Chat.rooms)
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post', rooms=rooms)


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    user = current_user.username
    rooms = Chat.query.filter(Chat.rooms.like(f'%{user}%')).order_by(Chat.date_created.desc()).group_by(Chat.rooms)
    return render_template('post.html', title=post.title, post=post, rooms=rooms)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    user = current_user.username
    rooms = Chat.query.filter(Chat.rooms.like(f'%{user}%')).order_by(Chat.date_created.desc()).group_by(Chat.rooms)
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post', rooms=rooms)


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))

@posts.route("/create-comment/<post_id>", methods=['POST'])
@login_required
def create_comment(post_id):
    user = current_user.username
    rooms = Chat.query.filter(Chat.rooms.like(f'%{user}%')).order_by(Chat.date_created.desc()).group_by(Chat.rooms)
    text = request.form.get('text')

    if not text:
        flash('Comment cannot be empty.', category='error')
    else:
        post = Post.query.filter_by(id=post_id).first()
        if post:
            comment = Comment(
                text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
            return render_template('post.html', title=post.title, post=post, rooms=rooms)
        else:
            flash('Post does not exist.', category='error')
    

@posts.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash('Comment does not exist.', category='error')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('You do not have permission to delete this comment.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('main.home'))

@posts.route("/like-post/<post_id>", methods=['GET'])
@login_required
def like(post_id):
    user = current_user.username
    rooms = Chat.query.filter(Chat.rooms.like(f'%{user}%')).order_by(Chat.date_created.desc()).group_by(Chat.rooms)
    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(
        author=current_user.id, post_id=post_id).first()

    if not post:
        flash('Post does not exist.', category='error')
    elif like:
        db.session.delete(like)
        db.session.commit()
        return redirect(url_for("main.home"))
    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()
        return render_template('post.html', title=post.title, post=post, rooms=rooms)
    
    
   

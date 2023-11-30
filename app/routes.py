from app import app, db
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from .forms import LoginForm, EditProfileForm, PostForm, SkiForm, SurfForm, UserForm
from app.models import User, Post, Skis, Surf
# from werkzeug.urls import url_parse
from app.forms import RegistrationForm

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    posts = current_user.followed_posts().all()
    return render_template("index.html", title='Home Page', form=form, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # if user is None or not user.check_password(form.password.data):
        #     flash('Invalid username or password')
        #     return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

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

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user', methods=["GET", "POST"])
@login_required
def users():
    form = UserForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            location=form.location.data,
            about_me=form.about_me.data,
        )
@app.route('/user')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        current_user.location = form.location.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        form.location.data = current_user.location
        
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@app.route('/explore')
@login_required
def explore():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', title='Explore', posts=posts)

@app.route('/skis', methods=["GET", "POST"])
@login_required
def skis():
    form = SkiForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        ski = Skis(
            title=form.title.data,
            length=form.length.data,
            make=form.make.data,
            model=form.model.data,
            binding=form.binding.data,
            description=form.description.data,
            user_id=current_user.id,
            image_url=form.image_url.data 
        )
        try:
            db.session.add(ski)
            db.session.commit()
            flash(f"{ski.title} has been created")
            print("ski committed")
            return redirect(url_for('skis'))
        except Exception as e:
            print(f"Error adding surf to the database: {str(e)}")
            db.session.rollback()
    # skis = current_user.followed_posts().all()
    return render_template('skis.html', title="skis", form=form)

@app.route('/surf', methods=["GET", "POST"])
@login_required
def surf():
    form = SurfForm()
    if form.validate_on_submit():

        surf = Surf(
        title = form.title.data,
        length = form.length.data,
        make=form.make.data,
        model=form.model.data,
        description = form.description.data,
        user_id=current_user.id
        # image_url = form.image_url.data or None
        )
        db.session.add(surf)
        db.session.commit()

        # flash a success message
        flash(f"{surf.title} has been created")
        return redirect(url_for('surf'))
    
    return render_template('surf.html', title="Surfboards", form=form)

@app.route('/skis/<ski_id>')
def ski_view(ski_id):
    surf = db.session.get(Skis, ski_id)
    if not surf:
        flash('That post does not exist')
        return redirect(url_for('index'))
    return render_template('skis.html', surf=surf)

@app.route('/surf/<surf_id>')
def surf_view(surf_id):
    surf = db.session.get(Surf, surf_id)
    if not surf:
        flash('That post does not exist')
        return redirect(url_for('index'))
    return render_template('post.html', surf=surf)


# Editing only adds new Skis to DB - FIXED
@app.route('/skis/edit/<ski_id>', methods=["GET", "POST"])
@login_required
def edit_ski(ski_id):
    ski = db.session.get(Skis, ski_id)
    if not ski:
        flash('That post does not exist')
        return redirect(url_for('edit_skis'))
    if current_user != ski.user_id:
        flash('You can only edit skis you have authored!')
        # return redirect(url_for('edit_skis.html', ski_id=ski_id))
    # Create an instance of the SkiForm
    form = SkiForm()

    # If form submitted, update the post
    if form.validate_on_submit():
        # update the post with the for data
        ski.title = form.title.data
        ski.description = form.description.data
        ski.length=form.length.data,
        ski.make=form.make.data,
        ski.model=form.model.data,
        ski.description=form.description.data,
        ski.user_id=current_user.id
        # ski.image_url = form.image_url.data
        # Commit to the database
        db.session.commit()
        flash(f'{ski.title} has been edited.', 'success')
        return redirect(url_for('index'))

    # Pre-populate the form with the post's data
    form.title.data = ski.title
    form.description.data = ski.description
    form.length.data = ski.length
    form.make.data = ski.make
    form.model.data = ski.model

    # form.image_url.data = surf.image_url
    return render_template('edit_skis.html', ski=ski_id, form=form)

@app.route('/surf/edit/<surf_id>', methods=["GET", "POST"])
@login_required
def edit_surf(surf_id):
    surf = db.session.get(Surf, surf_id)
    if not surf:
        flash('That post does not exist')
        return redirect(url_for('edit_skis'))
    if current_user != surf.user_id:
        flash('You can only edit skis you have authored!')
        # return redirect(url_for('edit_skis.html', ski_id=ski_id))
    # Create an instance of the SkiForm
    form = SkiForm()

    # If form submitted, update the post
    if form.validate_on_submit():
        # update the post with the for data
        surf.title = form.title.data
        surf.description = form.description.data
        surf.length=form.length.data,
        surf.make=form.make.data,
        surf.model=form.model.data,
        surf.description=form.description.data,
        surf.user_id=current_user.id
        # surf.image_url = form.image_url.data
        # Commit to the database
        db.session.commit()
        flash(f'{surf.title} has been edited.', 'success')
        return redirect(url_for('surf'))

    # Pre-populate the form with the post's data
    form.title.data = surf.title
    form.description.data = surf.description
    form.length.data = surf.length
    form.make.data = surf.make
    form.model.data = surf.model
    
    # form.image_url.data = surf.image_url
    return render_template('edit_surf.html', surf=surf_id, form=form)


@app.route('/explore_skis')
@login_required
def explore_skis():
    skis = Skis.query.all()
    return render_template('explore_skis.html', title='Explore', skis=skis)

@app.route('/explore_surf')
@login_required
def explore_surf():
    surf = Surf.query.all()
    return render_template('explore_surf.html', title='Explore', surf=surf)
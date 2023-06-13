from flask import Flask, request, render_template, redirect, session, flash, url_for, jsonify  
from models import db, connect_db, User, Feedback
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from forms import RegisterUser, LoginUser, FeedbackForm
 
app = Flask(__name__)  

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'scamp'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

app.app_context().push()

connect_db(app)


@app.route('/')
def redirect_register():
    return redirect('/register')


@app.route('/register', methods = ['GET', 'POST'])
def register():
    """Register user."""
    if "user_id" in session:
        """Check if user is already logged in so they aren't shown the register page again."""
        flash(f"You're already signed in, why do you want to register again?", "primary")
        return redirect(url_for('user_page', username = session['user_id']))
    else:
        form = RegisterUser()
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            email = form.email.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            new_user = User.register(username, password, email, first_name, last_name)
            db.session.add(new_user)
            try: 
                db.session.commit()
            except IntegrityError:
                form.username.errors.append('Username taken. Please pick another.')
                form.email.errors.append('Account already with associated email. Already have an account?')
                return render_template('register-form.html', form=form)
            session['user_id'] = new_user.username
            flash('You have successfully created your account. Welcome aboard!', "success")
            return redirect(url_for('user_page', username = session['user_id']))

        return render_template('register-form.html', form=form)


@app.route('/users/<username>')
def user_page(username):
    """User's page."""
    if "user_id" not in session:
        flash(f"You don't have permission to view that page. Please register your account or login.", "danger")
        return redirect('/')
    
    else:
        user = User.query.filter_by(username = username).first_or_404()
        user_feedback = Feedback.query.filter_by(username = username).all()
        return render_template('index.html', user = user, feedback = user_feedback)
       
            
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login user."""
    form = LoginUser()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        """If user is already in the system, redirect to user page."""
        if user:
            flash(f"Welcome back, {user.first_name}!", "primary")
            session['user_id'] = user.username
            return redirect(url_for("user_page", username = user.username))
        
        else:
            form.username.errors = ['Invalid username/password.']
            
    return render_template('login-form.html', form = form)


@app.route('/logout')
def logout_user():
    """Logout the user."""
    session.pop('user_id')
    flash("Goodbye!", "info")
    return redirect('/')


@app.route('/users/<username>/feedback/add', methods=['POST', 'GET'])
def add_feedback(username):
    """Render template for adding feedback. Check if user has permission."""
    if "user_id" not in session:
        flash(f"You don't have permission to view that page. Please register your account or login.", "danger")
        return redirect('/')
    else:
        form = FeedbackForm()
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            name = username
            user_feedback = Feedback(title = title, content = content, username = name)
            
            db.session.add(user_feedback)
            db.session.commit()
            return redirect(url_for('user_page', username = username))

        else:
            return render_template('feedback-form.html', form=form)
    
    
@app.route('/feedback/<int:id>/update', methods=['GET', 'POST'])
def update_feedback(id):
    """Update feedback for a given user. Check if user has permission."""
    if "user_id" not in session:
        flash(f"You don't have permission to view that page. Please register your account or login.", "danger")
        return redirect('/')
    else:
        feedback = Feedback.query.get_or_404(id)
        form = FeedbackForm(obj=feedback)
        username = feedback.user.username

        if form.validate_on_submit():
            feedback.title = form.title.data
            feedback.content = form.content.data
            db.session.commit()
            return redirect(url_for("user_page", username = feedback.user.username))

        else:
            return render_template('edit-feedback.html', form=form, username = username, feedback = feedback)
        
    
@app.route('/feedback/<int:id>/delete', methods=['POST'])
def delete_feedback(id):
    """Delete a feedback post. Check for user permission."""
    if "user_id" not in session:
        flash(f"You don't have permission to view that page. Please register your account or login.", "danger")
        return redirect('/')
    else:
        feedback = Feedback.query.get_or_404(id)
        username = feedback.user.username
        db.session.delete(feedback)
        db.session.commit()
        return redirect(url_for('user_page', username = username))
    
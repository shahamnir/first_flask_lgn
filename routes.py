from flask import redirect, render_template, request, url_for, flash
from flask_login import logout_user, login_required,login_user
from flask_bcrypt import check_password_hash, generate_password_hash
from app import create_app,db,login_manager
from models import User
from forms import LoginForm,RegisterForm

app = create_app()


@app.route('/')
def index():
    return render_template("index.html")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login/', methods=('GET','POST'))
def login():
    if request.method == 'POST':
        form = LoginForm()
        if form.validate_on_submit():
            try:
                user = User.query.filter_by(email=form.email.data).first()
                if check_password_hash(user.password,form.pwd.data):
                    login_user(user)
                    return redirect(url_for('index'))
                else:
                    flash(f'Invalid user name or password', "danger" )
            except Exception as e:
                flash(e, "danger")
        return redirect(url_for('login'))
    else:
        form = LoginForm()
        return render_template("auth.html", form=form)
    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login.html'))
    


@app.route('/register/', methods=('GET','POST'))
def register():
    if request.method == 'POST':
        form = RegisterForm()
        if form.validate_on_submit():
            email = form.email.data
            username = form.username.data
            pwd = form.pwd.data

            newUser = User(
                username=username, 
                email=email,
                password=generate_password_hash(pwd)
                )
            db.session.add(newUser)
            db.session.commit()
            flash("Account created succesfully")
            return redirect(url_for('login'))

    else:
        form = RegisterForm()
        return render_template("auth.html", form=form)
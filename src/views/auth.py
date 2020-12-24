from flask import Blueprint, redirect, render_template, request, session

auth = Blueprint(__name__, 'auth')


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@auth.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # user = User.query.filter_by(username=username).first()
        # if not user:
        #     user = User(username=username)
        #     db.session.add(user)
        #     db.session.commit()
        session['id'] = username
        # if user is not just to log in, but need to head back to the auth page, then go for it
        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)
        return redirect('/')
    else:
        return render_template('authenticate.html')

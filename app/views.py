from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
#from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db
#from .forms import LoginForm
from models import User, Class, Group, Online
from forms import SigninForm, RegisterForm, NewGroupForm
import json
import time
import datetime

@app.before_request
def configure_session():
    session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=app.config['ONLINE_LAST_MINUTES'])

@app.route('/index', methods=['GET', 'POST'])
def index():
    online_users = get_online_users();
    return Response('Online: %s' % ', '.join(get_online_users()),
                                        mimetype='text/plain')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    #print request.method
    login = SigninForm()
    register = RegisterForm()
    if ('user' in session):
        print 'user already signed in : %r' % session['user']
        return redirect(url_for('user_profile')) 

    if login.validate_on_submit(): 
        logged_in_user = login.finduser()
        session['user'] = logged_in_user.user_id
        mark_active(logged_in_user.user_id)
        return redirect(url_for('user_profile'))
    elif register.validate_on_submit():
        print 'validating new user'
        new_user = register.getuser()
        session['user'] = new_user.user_id
        mark_active(new_user.user_id)
        flash('you have succesfully registered!')
        return redirect(url_for('user_profile'))

    flash('Incorrect login details. Please try again or register for a new account.')
    return render_template('signIn.html', login=login, register=register) 

#unused
@app.route('/newuser', methods=['GET', 'POST'])
def new_user():
    register = RegisterForm()
    if register.validate_on_submit():
        new_user = register.getuser()
        session['user'] = new_user.user_id
        mark_active(new_user.user_id)
        flash('you have succesfully registered!')
        return redirect(url_for('user_profile'))
        
    return render_template('newuser.html', register=register)

@app.route('/profile', methods=['GET','POST'])
def user_profile():
    group_form = NewGroupForm()

    if 'user' in session:
        curr_id = session['user']
        current_user = User.query.filter(User.user_id==curr_id).first()
        mark_active(curr_id)
        active_users = get_active_users()

        thisUser = ''.join(json.dumps(current_user.serialize))

        #returns set of online users
        usersJSON = [i.serialize for i in active_users]
        jsonString = ''.join(json.dumps(o) + ";" for o in usersJSON)

        #returns set of groups
        groupsJSON = [i.serialize for i in Group.query.all()]
        groupJsonString = ''.join(json.dumps(o) + ';' for o in groupsJSON)

        if group_form.validate_on_submit():
            group = Group(group_form.group_name.data)
            user = User.query.filter(User.user_id=curr_id).first()
            group.user.append(user)
            db.session.add(group)
            db.session.commit()

        print active_users
        #return render_template('profile_test.html', current_user=current_user, active_users=active_users)
        return render_template('profile.html', thisUser=thisUser, usersJSON=jsonString, 
                                groupForm=group_form, groupsJSON=groupsJsonString)

    return redirect(url_for('signin'))

@app.route('/filter')
def filter():
    if ('user' in session):
        filterOption = request.args.get("course")
        user = User.query.filter_by(user_id=session['user']).first()
        user.courseOpt = filterOption
        db.session.commit()
        return redirect(url_for('user_profile'))
    return redirect(url_for('signin'))

@app.route('/logout')
def signout():
    mark_inactive(session['user'])
    session.pop('user', None)
    return redirect(url_for('signin'))

@app.route('/group/create', methods=['GET', 'POST'])
def create_group():
    if not 'user' in session:
        return redirect(url_for('signin'))

    group_form = NewGroupForm()
    if group_form.validate_on_submit():
        user_id = session['user']
        group = Group(group_form.group_name.data)
        user = User.query.filter(User.user_id=user_id).first()
        group.user.append(user)
        db.session.add(group)
        db.session.commit()

@app.route('/group/join/<int:group_id>')
def join_group(group_id):
    user = User.query.filter(User.user_id=session['user'])
    user.group_id=group_id
    db.session.commit()
    return

##############HELPERS#################

def get_active_users():
    #all _users is an 'Online' object
    all_users = Online.query.all()
    print all_users
    active_users = []
    for user in all_users:
        if user.is_active():
            #appends active users id
            active_users.append(user.user)
    return set(active_users)

def is_active(user_id):
    active_users_set = get_active_users
    return user_id in active_users_set

def mark_active(user_id):
    user = Online.query.filter(Online.user_id == user_id).first()
    print 'marking as active %r' % (user_id)
    if user:
        user.last_active = datetime.datetime.utcnow()
        db.session.commit()
    else:
        print 'creating new online entity'
        user = Online(user_id)
        db.session.add(user)
        db.session.commit()

def mark_inactive(user_id):
    user = Online.query.filter(Online.user_id == user_id).first()
    print 'marking inactive %r' % user_id
    db.session.delete(user)
    db.session.commit()

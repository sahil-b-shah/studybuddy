from flask.ext.wtf import Form
from flask.ext.wtf.html5 import EmailField
from wtforms import validators, ValidationError, TextField, RadioField, TextAreaField, SubmitField, PasswordField, SelectMultipleField, FormField, SelectField
from flask import Flask, render_template, redirect, request
from app import db
from models import User, Class

class RegisterForm(Form):
    firstName = TextField("First name", [validators.Required("Please enter your first name.")])
    lastName = TextField("Last name", [validators.Required("Please enter your last name.")])
    email = TextField("Email", [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
    major = TextField("Major", [validators.Required("Please enter your email address.")])
    year = TextField("Year", [validators.Required("Please enter your year")])
    gender = RadioField('Gender', choices=[('male','Male'),('female','Female')])
    courses = TextField("Courses", [validators.Required("Please enter your classes separated by semicolons.")])
    bio = TextField("Description", [validators.Required("Please enter in a short bio.")])
    upLocation = TextField("Location", [validators.Required("Please submit your location")])
    submit = SubmitField("Let's Study!!")

    password = PasswordField('Password', [validators.Required("Please enter a password.")])
    pwdcheck = PasswordField('Password', [validators.Required("Please enter a password.")])

    def validate(self):
        print 'in register validate'
        self.printData()
        if not Form.validate(self):
            print "register form not valid"
            print self.errors
            return False
        if self.pwdcheck.data != self.password.data:
            self.password.errors.append("Please retype your password - they didn't match")
            return False
            
        #user = User.query.filter(User.email == self.email.data.lower()).first()
        user = self.getuser()
        if user:
            print 'email already taken %r' % user.email
            self.email.errors.append("That email is already taken")
            return False
        else:
            user = User(self.firstName.data, self.lastName.data, self.email.data, self.gender.data,
                self.year.data, self.major.data, self.bio.data, self.password.data)
            classes = self.get_classes()
            user.classes = classes
            db.session.add(user)
            db.session.commit()
            return True

    def get_classes(self):
        if not self.courses:
            return []
        tmp = self.courses.data.strip()
        classes_string = tmp.split(';')
        print classes_string
        classes = []
        for c in classes_string:
            class_to_add = Class.query.filter(Class.class_name==c).first()
            if not class_to_add:
                class_to_add = Class(c)
            classes.append(class_to_add)
        return classes

    def getuser(self):
        user = User.query.filter(User.email==self.email.data.lower()).first()
        return user

    def printData(self):
        print "validating register form"
        print self.firstName.data
        print self.lastName.data
        print self.email.data
        print self.major.data
        print self.year.data
        print self.gender.data
        print self.bio.data
        print self.password.data
        print self.pwdcheck.data
        print self.courses.data

class SigninForm(Form): 
    email = TextField("Email", [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
    password = PasswordField('Password', [validators.Required("Please enter a password.")])
    submit = SubmitField("Let's Study!")

    def finduser(self):
        user = User.query.filter(User.email==self.email.data.lower()).first()
        if user and user.check_password(self.password.data):
            return user
        return None

    def validate(self):
        print 'in login validate'
        if not Form.validate(self):
            print 'login not valid'
            print self.errors
            return False
        if self.finduser():
            print 'user exists'
            return True
        else:
            print 'user does not exist'
            self.email.errors.append("Invalid e-mail or password")
            return False

class UpdateForm(Form):
    curCourse = TextField("Course")
    curRoom = TextField("Room")
    curAssignment = TextField("Assignment")
    submit = SubmitField("Update")

    def validate(self):
        user = User.query.filter_by(user_id=session['user']).first()
        if user:
            user.curCourse = curCourse
            user.curRoom = curRoom
            user.curAssignment = curAssignment
            db.session.commit()
            return True
        return False

class NewGroupForm(Form):
    group_name = TextField("Group Name")
    submit = SubmitField("Create")

    def validate(self):
        if not Form.validate(self):
            print self.errors
            return False
        if self.findgroup(self):
            print 'group already exists'
            self.group_name.errors.append("That group already exists")
            return False
        else:

            return True

    def findgroup(self):
        group = Group.query.filter(Group.group_name = self.group_name.data.lower()).first()
        return group

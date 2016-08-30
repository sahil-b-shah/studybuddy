import tbFinder.db as db
import json
import random
from tbFinder import app
from flask import Flask, render_template, redirect, request
import re


#Homepage
@app.route('/', methods=['POST', 'GET'])
@app.route('/home', methods=['POST', 'GET'])
def home():
    return render_template('home.html')

#valiadate the email
@app.route('/valiadate', methods=['POST', 'GET'])
def valiadate(name = None):
    email = request.form['email'].encode('ascii','ignore')
    x = re.findall(r"upenn.edu", email)
    if x:
    	person = createUser()
        return render_template('valiadateSuccess.html', name = person.name)
    else:
        return render_template('valiadateFailure.html')

def createUser():
	x = request.form['email'].encode('ascii','ignore').split("@")[0]
	return User(x)


@app.route('/report', methods=['GET', 'POST'])
def report():
	return render_template('report.html')


@app.route('/allCourses')
def allCourses():
    all_courses = db.get_all_course_codes()
    return render_template('allcourses.html', all_courses=all_courses)


@app.route('/course/<dept>')
@app.route('/course/<dept>/<course_id>')
def course(dept, course_id=None, methods =['GET']):
    if (course_id is None):
        results = db.get_all_dept_links(dept)
        return render_template('dept_results.html', dept=dept, results=results)
    else:	
		results = db.get_all_course_links(dept, course_id)
		return render_template('courseid_results.html', dept=dept,
								course_id=course_id, results=json.loads(results))


@app.route('/add')
def add():
    return render_template('add.html')


@app.route('/addLink', methods=['POST'])
def addLink():
    db.add_tb_info(request.form)
    return redirect('/allCourses')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/explore')
def explore():
    results = db.get_all_course_codes()
    dept_list = list(results.keys())
    selected_dept = random.choice(dept_list)
    return redirect('/course/' + selected_dept)


@app.route('/search', methods=['POST', 'GET'])
def search():
    query = request.form.get('query')
    try:
        query = int(query)
        results = db.search(query)
        if len(results) == 0:
            return render_template('results.html', query=query, results="null")
        else:
            return render_template('results.html', query=query, results=results)
    except ValueError:
        return render_template('results.html', query=query, results="notanint")


class User():

	def __init__(self, name):
		self.name = str(name)

	def __repr__(self):
		return str(name)

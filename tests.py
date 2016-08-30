from app import app, db
from app.models import User, Class

def printTables():
	print "Students---------------------"
	students = User.query.filter()
	classes = Class.query.filter()

	for student in students:
		print '%p', student

	for class_ in classes:
		print '%p', class_

	# for student in students:
	# 	print '%s | %s | %s | %s | %s | %s | %s | %s | %s | %p', (student.firstname, student.lastname, 
	# 															student.username, student.email, student.gender, student.year
	# 															student.major, student.bio, student.classes)

	# print "Classes---------------------"
	# classes = Class.query.filter()
	# for class_ in classes:
	# 	print '%s | ', class_.class_name



db.drop_all()
db.create_all()

sahil = User('Sahil', 'Shah', 'deltaspin@gmail.com', 'male', '2016', 'CMPE', 'I love computer science', 'pwd1')
nickhil = User('Nickhil', 'Nabar', 'nick@gmail.com', 'male', '2017', 'CIS', 'I dont love computer science', 'pwd1')
murray = User('Eric', 'Murray','murr@gmail.com', 'male', '2016', 'CIS', 'I love CIS110', 'pwd3')
rachel = User('Rachel', 'Chan','rchan@gmail.com', 'female', '2017', 'CIS', 'eyo', 'pwd4')
matt = User('Matt', 'ICantSpell','matt@gmail.com', 'male', '2017', 'CIS', 'I love the shore but not fling', 'pwd3')


cis350 = Class('CIS 350')
cis455 = Class('CIS 455')
cis120 = Class('CIS 120')
cis121 = Class('CIS 121')
cis519 = Class('CIS 519')


#Add classes
db.session.add(cis350)
db.session.add(cis455)
db.session.add(cis120)
db.session.add(cis121)
db.session.add(cis519)
db.session.commit()

#Add users
db.session.add(sahil)
db.session.add(nickhil)
db.session.add(murray)
db.session.add(rachel)
db.session.add(matt)
db.session.commit()

#Check if updating a user and then committing again works
user = User.query.filter(User.firstname=='Sahil').first()
user.bio = 'I wanted to change my bio a little'
db.session.commit()

#Add 120 and 121 to murray
class_to_add = Class.query.filter(Class.class_name=='CIS 120').first()
class2_to_add = Class.query.filter(Class.class_name=='CIS 121').first()
user = User.query.filter(User.firstname=='Eric').filter(User.lastname=='Murray').first()
user.classes.append(class_to_add)
user.classes.append(class2_to_add)

#add 120 to nickhil
nics = User.query.filter(User.email=='nick@gmail.com').first()
nics.classes.append(class_to_add)
db.session.commit()

#add 350, 455, and 121 to rachel
user = User.query.filter(User.email=='rchan@gmail.com').first()
class_to_add = Class.query.filter(Class.class_name=='CIS 350').first()
class2_to_add = Class.query.filter(Class.class_name=='CIS 455').first()
class3_to_add = Class.query.filter(Class.class_name=='CIS 121').first()
user.classes.append(class_to_add)
user.classes.append(class2_to_add)
user.classes.append(class3_to_add)


#add 350 and 121 to matt
user = User.query.filter(User.email=='matt@gmail.com').first()
class_to_add = Class.query.filter(Class.class_name=='CIS 350').first()
class2_to_add = Class.query.filter(Class.class_name=='CIS 121').first()
user.classes.append(class_to_add)
user.classes.append(class2_to_add)
db.session.commit()

#filter by class
#users_in_121 = User.query.join(Class).filter(Class.class_name=='CIS 121').all()
class_121_obj = Class.query.filter(Class.class_name=='CIS 121').first()
print 'Users in 121--------------------'
print class_121_obj.users
print

#filter by year -- users in 2016
users = db.session.query(User).filter(User.year == '2016').all()
print 'Users in 2016--------------------'
print users
print

#no users in cis 519
users = Class.query.filter(Class.class_name=='CIS 519').first().users
print 'No users in 519--------------------'
print users
print


printTables()

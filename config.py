import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
#SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
ONLINE_LAST_MINUTES = 1
SECRET_KEY = '+p_+ Vc23A*b:>nG`{<L=QY7bN+|uM;IP]_<7BwHRP$b;qNwZsw]/yeIl*h?sGy&'

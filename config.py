import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False

ADMINS = frozenset(['dev@stratasan.com'])
SECRET_KEY = 'SecretKeyForSessionSigning'

SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
DATABASE_CONNECT_OPTIONS = {}

THREADS_PER_PAGE = 8

CSRF_ENABLED = True
CSRF_SESSION_KEY = 'somethingimpossibletoguess'

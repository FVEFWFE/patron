from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
import os
from os.path import abspath, join
import shelve
import json

basedir = abspath(os.path.dirname(__file__))

# Load persona configuration
with open(join(basedir, 'persona_config.json'), 'r') as f:
    PERSONA_CONFIG = json.load(f)


class Config(object):
    # Persona Configuration
    PERSONA = PERSONA_CONFIG['persona']
    THEME_CONFIG = PERSONA_CONFIG['theme']
    CONTENT_CONFIG = PERSONA_CONFIG['content']
    SEO_CONFIG = PERSONA_CONFIG['seo']
    
    BLOGGING_SITENAME = PERSONA['name']
    BLOGGING_SITEURL = os.environ.get('SITEURL') or 'https://example.com'
    BUTTON_MAP = {'submit': 'primary'}
    SERVER_NAME = os.environ.get('VIRTUAL_HOST')
    BLOGGING_URL_PREFIX = '/updates'
    BLOGGING_BRANDURL = os.environ.get('BRANDURL')
    BLOGGING_TWITTER_USERNAME = os.environ.get('TWITTER')
    # Google Analytics removed for privacy
    BLOGGING_GOOGLE_ANALYTICS = None
    BLOGGING_PERMISSIONS = True
    BLOGGING_PERMISSIONNAME = 'admin'
    BLOGGING_PLUGINS = None
    BLOGGING_ALLOW_FILE_UPLOAD = True
    BLOGGING_ESCAPE_MARKDOWN = False
    # Comments system completely disabled
    COMMENTS = False
    COMMENTS_URL = None
    PREFERRED_URL_SCHEME = 'https'
    if os.environ.get('SCHEDULER_HOUR') is not None:
        SCHEDULER_HOUR = int(os.environ.get('SCHEDULER_HOUR'))
    else:
        SCHEDULER_HOUR = 9
    if os.environ.get('SCHEDULER_MINUTE') is not None:
        SCHEDULER_MINUTE = int(os.environ.get('SCHEDULER_MINUTE'))
    else:
        SCHEDULER_MINUTE = None
    SECRET_KEY_LOCATION = os.environ.get('SECRET_KEY_LOCATION') or \
        join(basedir, 'key')
    with shelve.open(SECRET_KEY_LOCATION) as key:
        if key.get('key') is None:
            SECRET_KEY = os.urandom(24).hex()
            key['key'] = SECRET_KEY
        else:
            SECRET_KEY = key['key']
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + join(basedir, 'app.db')
    SCHEDULER_JOBSTORES = {
            'default': SQLAlchemyJobStore(url=SQLALCHEMY_DATABASE_URI)
        }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Custom dark theme
    THEME = 'custom-dark'

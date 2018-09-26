import os

class Config(object):
    DEBUG = False
    DEVELOPMENT = False
    TESTING = False

    # IMPORTANT: You should wrap this script and provide an:
    #
    # export SECRET_KEY='something-fixed-but-random'
    #
    # in the script where you run this code (for example, in wsgi_app.py).
    # This way, you will always have the same SECRET_KEY, and therefore 
    # the same session regardless server restarts.
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32)

    # You should also store these credentials somewhere safer, like in the
    # same script as in the SECRET_KEY (in wsgi_app.py, not here)
    WEBLAB_USERNAME = os.environ.get('WEBLAB_USERNAME') or 'weblabdeusto'
    WEBLAB_PASSWORD = os.environ.get('WEBLAB_PASSWORD') or 'password'

    # If an unauthorized user comes in, redirect him to this link
    WEBLAB_UNAUTHORIZED_LINK = 'https://docs.labsland.com/weblablib/'

    # Alternatively, you can establish a template that will be rendered
    # WEBLAB_UNAUTHORIZED_TEMPLATE = 'unauthorized.html'

    # These URLs should change to customize your lab:
    SESSION_COOKIE_NAME = 'complete-session'
    SESSION_COOKIE_PATH = '/'
    WEBLAB_SESSION_ID_NAME = 'wl-mylab'
    WEBLAB_REDIS_BASE = 'complete-example'

    # If you put this, for example, then you should configure
    # WebLab-Deusto to use http://<lab-server>/foo/weblab/
    WEBLAB_BASE_URL = '/foo'

    WEBLAB_NO_THREAD = True

    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    WEBLAB_REDIS_URL = os.environ.get('WEBLAB_REDIS_URL') or 'redis://localhost:6379/0'
    SOCKETIO_REDIS_URL = os.environ.get('SOCKETIO_REDIS_URL') or 'redis://localhost:6379/0'

    # Other parameters (and default values):
    #
    # WEBLAB_TIMEOUT = 15 # If the user doesn't reply in 15 seconds, consider expired
    # WEBLAB_REDIS_URL = 'redis://localhost:6379/0'
    # WEBLAB_TASK_EXPIRES = 3600 # Time to expire the session results
    # WEBLAB_AUTOPOLL = True # Every method calls poll()
    # WEBLAB_EXPIRED_USERS_TIMEOUT = 3600 # How long an expired user can be before kicked out


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'shared_secret_key'
    ASSETS_DEBUG = (os.environ.get('ASSETS_DEBUG') or '0') == '1'

    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    WEBLAB_REDIS_URL = os.environ.get('WEBLAB_REDIS_URL') or 'redis://localhost:6379/0'
    SOCKETIO_REDIS_URL = os.environ.get('SOCKETIO_REDIS_URL') or 'redis://localhost:6379/0'

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    # WEBLAB_SCHEME = 'https'
    pass

config = {
    'default': DevelopmentConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}

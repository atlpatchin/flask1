import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config:
    SECRET_KEY= os.environ.get('SECRET_KEY') or 'hard to guss string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN=True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER='Flasky Admin <atlpat@163.com>'
    FLASKY_ADMIN ='atlpat@163.com'# os.environ.get('FLASKY_ADMIN')
    MAIL_SERVER='smtp.163.com'
    MAIL_PORT=25
    MAIL_USERNAME='atlpat@163.com' #os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD='llh151'#os.environ.get('MAIL_PASSWORD')
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI=os.environ.get('DEV_DATABASE_URL') or 'sqlite:///'+os.path.join(basedir,'data-dev.sqlite')

class TestingConfig(Config):
    TESTING=True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DABASE_URL') or 'sqlite:///'+os.path.join(basedir,'data-test.sqlite')
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI =os.environ.get('DATABASE_URL') or 'sqlite:///  '+os.path.join(basedir,'data.sqlite')
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

























































































































































































































































































































































































































































































































































































































































































































































































































































































































































































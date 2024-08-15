import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI =  f'sqlite:///site.db' #os.environ.get('SQLALCHEMY_DATABASE_URI')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "ch.harit33@gmail.com" #os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = "gdxq nczj gkuv gggr" #os.environ.get('EMAIL_PASS')

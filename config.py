import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'meow_secret_key'
    DEBUG = True

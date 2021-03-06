# -*- coding: utf-8 -*-
# @Author: wsljc
# @Date:   2017-03-11 18:23:02
# @Last Modified by:   wsljc
# @Last Modified time: 2017-04-18 08:12:02
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	FLASKY_MAIL_SUBJECT_PREFIX = '[FLASKY]'
	FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
	FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
	
	UPLOAD_FOLDER = './weibo/static/images/touxiang'
	MAX_CONTENT_LENGTH = 16 * 1024 * 1024

	UPLOADED_PHOTOS_DEST = './weibo/static/images/touxiang'

	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS =True
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
	    'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
	    'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
	    'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
	'development':DevelopmentConfig, 
	'testing':TestingConfig, 
	'production':ProductionConfig, 
	'default':DevelopmentConfig
}
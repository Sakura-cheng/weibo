# -*- coding: utf-8 -*-
# @Author: wsljc
# @Date:   2017-03-11 18:22:12
# @Last Modified by:   wsljc
# @Last Modified time: 2017-04-18 08:13:56
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
from flask_uploads import UploadSet, configure_uploads, IMAGES

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'main.login'

photos = UploadSet('photos', IMAGES)

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)

	bootstrap.init_app(app)
	mail.init_app(app)
	moment.init_app(app)
	db.init_app(app)
	login_manager.init_app(app)

	configure_uploads(app, photos)

	#附加路由和自定义的错误页面


	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	return app
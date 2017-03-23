# -*- coding: utf-8 -*-
# @Author: wsljc
# @Date:   2017-03-14 16:38:08
# @Last Modified by:   wsljc
# @Last Modified time: 2017-03-14 16:39:17
from flask import render_template
from . import main

@main.app_errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@main.app_errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500
# -*- coding: utf-8 -*-
# @Author: wsljc
# @Date:   2017-03-14 16:37:57
# @Last Modified by:   wsljc
# @Last Modified time: 2017-03-14 16:38:35
from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors
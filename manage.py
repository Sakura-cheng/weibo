# -*- coding: utf-8 -*-
# @Author: wsljc
# @Date:   2017-03-11 18:22:53
# @Last Modified by:   Sakura-cheng
# @Last Modified time: 2017-03-23 21:19:03
import os
from weibo import create_app, db
from weibo.models import User, Article, Comment, Follow
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
	return dict(app=app, db=db, User=User, Article=Article, Comment=Comment)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
	manager.run()
	#app.run(debug=True)
	#app.run(host='0.0.0.0')
# -*- coding: utf-8 -*-
# @Author: wsljc
# @Date:   2017-03-14 16:38:15
# @Last Modified by:   wsljc
# @Last Modified time: 2017-05-07 19:58:54
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import Required, Length, Email, EqualTo, Regexp
from wtforms import ValidationError
from ..models import User, Comment, Article, Follow

class PublishForm(Form):
	content = TextAreaField('说点什么吧：', validators=[Required()])
	submit = SubmitField('发表')

class CommentForm(Form):
	content = TextAreaField('写评论：', validators=[Required()])
	submit = SubmitField('评论')

# class ModifyForm(Form):
# 	username = StringField(validators=[Required(), Length(1, 64)])
# 	content = TextAreaField()
# 	submit = SubmitField('保存')

class LoginForm(Form):
	email = StringField('邮箱：', validators=[Required(), Length(1, 64), Email()])
	#username = StringField('用户名：', validators=[Required()])
	password = PasswordField('密码：', validators=[Required()])
	remember_me = BooleanField('记住我')
	submit = SubmitField('登录')

class RegisterForm(Form):
	email = StringField('邮箱：', validators=[Required(), Length(1, 64), Email()])
	username = StringField('用户名：', validators=[
		Required(), Length(1, 64)
		])
	password =PasswordField('密码：', validators=[Required()])
	password2 = PasswordField('重复密码：', validators=[Required(), EqualTo('password', message='两次密码应一致')])
	submit = SubmitField('注册')

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('邮箱已被注册')

	def validate_username(self, field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('用户名已被注册')
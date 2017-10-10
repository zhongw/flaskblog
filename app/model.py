# _*_ coding: utf-8 _*_
#
# Copyright (C) 2017 钟伟 <zhong.wei@qq.com>
# All rights reserved.
#
# Author: 钟伟 <zhong.wei@qq.com>
#

from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, url_for
from datetime import datetime
import bleach
from markdown import markdown


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    email = db.Column(db.String(64), unique=True, index=True)
    email_confirmed = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    post = db.relationship('Post', backref='author', lazy='dynamic')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['ADMIN_EMAIL']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # 生成token
    def generate_token(self, expires_in=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in)
        return s.dumps({'id': self.id})

    # 验证token
    def confirm_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False

        if data.get('id') != self.id:
            return False

        self.email_confirmed = True
        db.session.add(self)
        return True

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def can(self, permissions):
        return self.role is not None and \
               (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def ping(self):
        """每次用户请求时更新最后访问时间"""
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def to_json(self):
        json_user = {
            #'url': url_for('api.get_post', id=self.id, _external=True),
            'username': self.display_name,
            'member_since': self.member_since,
            'last_seen': self.last_seen
            #'posts': url_for('api.get_user_posts', id=self.id, _external=True)
        }


class AnonymousUser(AnonymousUserMixin):
    def can(self, permission):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    # 只有一个角色的设置为True, 其他设置为False，用户注册时，其角色会被设置为默认角色
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    user = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles={
            'User': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.WRITE_ARTICLE, True),
            'Moderator': (Permission.FOLLOW |
                          Permission.COMMENT |
                          Permission.WRITE_ARTICLE |
                          Permission.MODERATE_COMMENTS, False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()


class Permission:
    FOLLOW = 0x01                    # 关注用户，关注其他用户
    COMMENT = 0x02                   # 在他人的文章中发表评论
    WRITE_ARTICLE = 0x04             # 写文章
    MODERATE_COMMENTS = 0x08         # 管理他人发表的评论
    ADMIN = 0x80                     # 管理员权限，管理网站


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    create_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body_html = db.Column(db.Text)

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        """Markdown文本转换为HTML，再将允许的HTML标签传给bleach.clean函数进行清理，
        再由bleach.linkify函数把URL转成<a>链接"""
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'hr',
                        'i', 'li', 'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'h4', 'p']
        target.body_html =  bleach.linkify(bleach.clean(markdown(value, output_format='html'),
                                                        tags=allowed_tags, strip=True))

    def to_json(self):
        json_post = {
            #'url': url_for('api.get_post', id=self.id, _external=True),
            'body': self.body,
            'body_html': self.body_html,
            'timestamp': self.update_date
            #'author': url_for('api.get_user', id=self.author_id, _external=True)
        }
        return json_post


db.event.listen(Post.body, 'set', Post.on_changed_body)
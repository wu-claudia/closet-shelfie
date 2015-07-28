#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import users
import logging

env=jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

class Clothes(ndb.Model):
    color=ndb.StringProperty(required=True)
    part=ndb.StringProperty(required=True)
    file_name=ndb.StringProperty(indexed=False)
    image=ndb.BlobProperty(required=True)

class User(ndb.Model):
    username=ndb.StringProperty(required=True)
    #email=ndb.EmailProperty(required=True)
    password=ndb.StringProperty(required=True)

# class Outfit(ndb.Model):
#     name=ndb.StringProperty()
#     reminder=ndb.BooleanProperty()
#     date=ndb.DateTimeProperty()
#     clothes_key=ndb.KeyProperty(kind=Outfit)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template=env.get_template('main.html')
        login_url = users.create_login_url('/')
        variables={'login_url':login_url}
        self.response.write(template.render(variables))
        if user:
            self.redirect('/home')

class HomeHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template=env.get_template('home.html')
        variables = {'user':user}
        self.response.write(template.render(variables))
        logout_url = users.create_logout_url('/home')
        self.response.write('<b><p><a href="%s" id="log">Log Out</a></p></b>' % logout_url)
        if user is None:
            self.redirect('/')
    #def post(self):
        # username=self.request.get("usernamesignup")
        # password=self.request.get("passwordsignup")
        # user = User(username=username,
        #             password=password)
        # user_key=ndb.Key(User, user).fetch()
        # button_val = self.request.get('Sign up')
        # logging.error("Button value: ", button_val)
        # if user_key:
        #     return self.redirect('/custom')
        #
        # return self.redirect('/')

class CustomizeHandler(webapp2.RequestHandler):
    def get(self):
        template=env.get_template('customize.html')
        self.response.write(template.render())

class UploadHandler(webapp2.RequestHandler):
    def get(self):
        template=env.get_template('upload.html')
        self.response.write(template.render())

    def post(self):
        imagedata = Clothes(color=self.request.get('color'),
                            file_name = str(self.request.get('name')),
                            part=self.request.get('part'),
                            image = self.request.get('image'))
        imagedata.put()
        return self.redirect('/upload')

class OutfitHandler(webapp2.RequestHandler):
    def get(self):
        template=env.get_template('outfit.html')
        self.response.write(template.render())

class CalendarHandler(webapp2.RequestHandler):
    def get(self):
        template=env.get_template('calendar.html')
        self.response.write(template.render())

class AboutHandler(webapp2.RequestHandler):
    def get(self):
        template=env.get_template('about.html')
        self.response.write(template.render())

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/home', HomeHandler),
    ('/custom', CustomizeHandler),
    ('/upload', UploadHandler),
    ('/outfit', OutfitHandler),
    ('/calendar', CalendarHandler),
    ('/about', AboutHandler),
], debug=True)

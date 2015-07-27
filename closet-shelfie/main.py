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

env=jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

class Clothes(ndb.Model):


class MainHandler(webapp2.RequestHandler):
    def get(self):
        template=env.get_template('home.html')
        self.response.write(template.render())

class CustomizeHandler(webapp2.RequestHandler):
    def get(self):
        template=env.get_template('customize.html')
        self.response.write(template.render())

class UploadHandler(webapp2.RequestHandler):
    def get(self):
        template=env.get_template('upload.html')
        self.response.write(template.render())

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
    ('/custom', CustomizeHandler),
    ('/upload', UploadHandler),
    ('/outfit', OutfitHandler),
    ('/calendar', CalendarHandler),
    ('/about', AboutHandler),
], debug=True)
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
from google.appengine.api import images
import logging

env=jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

class User(ndb.Model):
#     #email=ndb.EmailProperty(required=True)
     reminder=ndb.BooleanProperty()

class Clothes(ndb.Model):
    color=ndb.StringProperty(required=True)
    part=ndb.StringProperty(required=True)
    file_name=ndb.StringProperty(indexed=False)
    image=ndb.BlobProperty(required=True)
    user_key=ndb.KeyProperty(kind=User)

class Outfit(ndb.Model):
     name=ndb.StringProperty()
     user=ndb.UserProperty()
     clothes_key=ndb.KeyProperty(kind=Clothes, repeated=True)

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

class CustomizeHandler(webapp2.RequestHandler):
    def get(self):
        edit_outfit_urlsafe=self.request.get('outfit')
        if edit_outfit_urlsafe:
            edit_outfit_key=ndb.Key(urlsafe=edit_outfit_urlsafe)
            outfit=edit_outfit_key.get()
        else:
            outfit=None
        user=users.get_current_user()
        user_id = user.user_id()
        user_key = ndb.Key(User, user_id)
        user_clothes = Clothes.query(Clothes.user_key==user_key).fetch()

        tops=[]
        bottoms=[]
        outerwear=[]
        accessory=[]
        shoes=[]

        for x in user_clothes:
            if x.part == "aTop":
                tops.append(x)
            elif x.part == "cBottom":
                bottoms.append(x)
            elif x.part == "Accessory":
                accessory.append(x)
            elif x.part == "bOuterwear":
                outerwear.append(x)
            else:
                shoes.append(x)
        template=env.get_template('customize.html')
        variables={'tops':tops, 'bottoms':bottoms,'outerwear':outerwear,'accessory':accessory,'shoes':shoes, 'outfit':outfit}
        self.response.write(template.render(variables))

    def post(self):
        outfit_clothes=[]
        user=users.get_current_user()
        user_id = user.user_id()
        user_key = ndb.Key(User, user_id)
        user_clothes = Clothes.query(Clothes.user_key==user_key).fetch()
        for x in user_clothes:
            if self.request.get('checked' + x.key.urlsafe()) == "on":
                outfit_clothes.append(x.key)

        edit_outfit_urlsafe=self.request.get('outfit')
        if edit_outfit_urlsafe:
            edit_outfit_key=ndb.Key(urlsafe=edit_outfit_urlsafe)
            edit_outfit=edit_outfit_key.get()
            edit_outfit.clothes_key=outfit_clothes
            edit_outfit.put()
        else:
            logging.error("No value")
            complete_outfit = Outfit(name=self.request.get('name'),
                                     user=user,
                                     clothes_key=outfit_clothes)
            complete_outfit.put()
        self.redirect('/outfit')

class ImageHandler(webapp2.RequestHandler):
    def get(self):
        key_id=self.request.get('key')
        item=ndb.Key(urlsafe=key_id).get()
        if (item and key_id):
            self.response.headers['Content-Type'] = 'image/jpeg'
            self.response.out.write(item.image)
        else:
            self.redirect('/static/noimage.jpg')

class DeleteClothesHandler(webapp2.RequestHandler):
     def get(self):
        clothes_key_urlsafe=self.request.get('item')
        clothes_key=ndb.Key(urlsafe=clothes_key_urlsafe)
        clothes_obj=clothes_key.get()
        clothes_key.delete()

        outfits_with_clothes=Outfit.query(Outfit.clothes_key == clothes_key).fetch()
        for outfit in outfits_with_clothes:
            outfit.key.delete()

        self.redirect('/custom')

class UploadHandler(webapp2.RequestHandler):
    def get(self):
        template=env.get_template('upload.html')
        self.response.write(template.render())

    def post(self):
        user_id = users.get_current_user().user_id()
        color=self.request.get('color')
        file_name=str(self.request.get('name'))
        part=self.request.get('part')
        image=self.request.get('image')
        user_key=ndb.Key(User, user_id)
        imagedata = Clothes(color=color,
                            file_name=file_name,
                            part=part,
                            image=image,
                            user_key=user_key)
        imagedata.put()
        return self.redirect('/upload')

class OutfitHandler(webapp2.RequestHandler):
    def get(self):
        user=users.get_current_user()
        user_outfits = Outfit.query(Outfit.user==user).fetch()
        outfit_to_clothes = {
        #   "outfit1_key": ["clothes1", "clothes2"],
        #   "outfit2": ["clothes1", "clothes2"]
        }
        for outfit in user_outfits:
            outfit_to_clothes[outfit.key] = []
            for x in outfit.clothes_key:
                outfit_to_clothes[outfit.key].append(x.get())
        template=env.get_template('outfit.html')
        variables = {'outfit_to_clothes':outfit_to_clothes}
        self.response.write(template.render(variables))

class CalendarHandler(webapp2.RequestHandler):
    def get(self):
        user=users.get_current_user()
        variables={'user':user}
        template=env.get_template('calendar.html')
        self.response.write(template.render(variables))

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
    ('/images', ImageHandler),
    ('/delete', DeleteClothesHandler),
], debug=True)

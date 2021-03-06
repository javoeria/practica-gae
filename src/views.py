from datetime import datetime
import os
import webapp2
import jinja2
import time

from google.appengine.ext import db
from google.appengine.api import users

from models import Comic, Image, Comment

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = \
    jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR))


class BaseHandler(webapp2.RequestHandler):

    def render_template(
        self,
        filename,
        template_values,
        **template_args
        ):
        template = jinja_environment.get_template(filename)
        self.response.out.write(template.render(template_values))

class ShowComics(BaseHandler):
    
    def get(self):
        user = users.get_current_user()
        if user:
            comics = Comic.all()
            text = self.request.get('input')
            if users.is_current_user_admin():
                role = "Dibujante"
            else:
                role = "Lector"
            self.render_template('adds.html', {'comics': comics, 'input': text, 'user': user, 'role': role, 'logout': users.create_logout_url('/')})
        else:
            self.redirect(users.create_login_url(self.request.uri))
        
class NewComic(BaseHandler):

    def post(self):
        comic = Comic(name=self.request.get('inputName'),
                      description=self.request.get('inputDescription'),
                      cover=self.request.get('inputURL'))
        comic.put()
        return webapp2.redirect('/')

    def get(self):
        user = users.get_current_user()
        if users.is_current_user_admin():
            role = "Dibujante"
        else:
            role = "Lector"
        self.render_template('new.html', {'user': user, 'role': role, 'logout': users.create_logout_url('/')})
        
class NewImage(BaseHandler):

    def post(self, comic_id):
        iden = int(comic_id)
        comic = db.get(db.Key.from_path('Comic', iden))
        image = Image(comic = comic,
                      link=self.request.get('inputLink'),
                      text=self.request.get('inputText'))
        image.put()
        comic.update_date = datetime.now()
        comic.put()
        time.sleep(.1)
        return webapp2.redirect('/show/'+comic_id)

    def get(self, comic_id):
        user = users.get_current_user()
        if users.is_current_user_admin():
            role = "Dibujante"
        else:
            role = "Lector"
        iden = int(comic_id)
        comic = db.get(db.Key.from_path('Comic', iden))
        self.render_template('image.html', {'comic': comic, 'user': user, 'role': role, 'logout': users.create_logout_url('/')})


class ViewComic(BaseHandler):

    def post(self, comic_id):
        iden = int(comic_id)
        comic = db.get(db.Key.from_path('Comic', iden))
        comment = Comment(comic = comic,
                          mark = bool(self.request.get('inputMark')),
                          text = self.request.get('inputComment'))
        comment.put()
        time.sleep(.1)
        return webapp2.redirect('/show/'+comic_id)

    def get(self, comic_id):
        user = users.get_current_user()
        if users.is_current_user_admin():
            role = "Dibujante"
        else:
            role = "Lector"
        iden = int(comic_id)
        comic = db.get(db.Key.from_path('Comic', iden))
        self.render_template('show.html', {'comic': comic, 'user': user, 'role': role, 'logout': users.create_logout_url('/')})

class EditComic(BaseHandler):

    def post(self, comic_id):
        iden = int(comic_id)
        comic = db.get(db.Key.from_path('Comic', iden))
        comic.name = self.request.get('inputName')
        comic.description = self.request.get('inputDescription')
        comic.cover = self.request.get('inputURL')
        comic.update_date = datetime.now()
        comic.put()
        return webapp2.redirect('/')

    def get(self, comic_id):
        user = users.get_current_user()
        if users.is_current_user_admin():
            role = "Dibujante"
        else:
            role = "Lector"
        iden = int(comic_id)
        comic = db.get(db.Key.from_path('Comic', iden))
        self.render_template('edit.html', {'comic': comic, 'user': user, 'role': role, 'logout': users.create_logout_url('/')})


class DeleteComic(BaseHandler):

    def get(self, comic_id):
        iden = int(comic_id)
        comic = db.get(db.Key.from_path('Comic', iden))
        db.delete(comic)
        return webapp2.redirect('/')
    
class DeleteComment(BaseHandler):

    def get(self):
        comic_id = self.request.GET.get('id')
        comment_id = self.request.GET.get('c')
        iden = int(comment_id)
        comment = db.get(db.Key.from_path('Comment', iden))
        db.delete(comment)
        time.sleep(.1)
        return webapp2.redirect('/show/'+comic_id)

class DeleteImage(BaseHandler):

    def get(self):
        comic_id = self.request.GET.get('id')
        image_id = self.request.GET.get('i')
        iden = int(image_id)
        image = db.get(db.Key.from_path('Image', iden))
        db.delete(image)
        time.sleep(.1)
        return webapp2.redirect('/show/'+comic_id)

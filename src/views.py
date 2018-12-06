from datetime import datetime
import os
import webapp2
import jinja2

from google.appengine.ext import db
from google.appengine.api import users

from models import Comic, Imagen, Comentario

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

class MainPage(webapp2.RequestHandler):
    
    def get(self):
        user = users.get_current_user()
        if user:
            comics = Comic.all()
            self.response.out.write(
                "%s <a href='%s'>Salir</a>" % 
                (user.nickname(), users.create_logout_url('/'))
            )
            self.render_template('adds.html', {'adds': comics}) #CHANGE:ADDS
        else:
            self.redirect(users.create_login_url(self.request.uri)) 


##################################

class ShowAdds(BaseHandler):
    
    def get(self):
        user = users.get_current_user()
        if user:
            adds = Adds.all()
            self.response.out.write(
                "%s <a href='%s'>Salir</a>" % 
                (user.nickname(), users.create_logout_url('/'))
            )
            self.render_template('adds.html', {'adds': adds})
        else:
            self.redirect(users.create_login_url(self.request.uri))   
        
class NewAdd(BaseHandler):

    def post(self):
        add = Adds(author=self.request.get('inputAuthor'),
                  text=self.request.get('inputText'),
                  priority=int(self.request.get('inputPriority')))
        add.put()
        return webapp2.redirect('/')

    def get(self):
        self.render_template('new.html', {})


class EditAdd(BaseHandler):

    def post(self, add_id):
        iden = int(add_id)
        add = db.get(db.Key.from_path('Adds', iden))
        add.author = self.request.get('inputAuthor')
        add.text = self.request.get('inputText')
        add.priority = int(self.request.get('inputPriority'))
        add.date = datetime.now()
        add.put()
        return webapp2.redirect('/')

    def get(self, add_id):
        iden = int(add_id)
        add = db.get(db.Key.from_path('Adds', iden))
        self.render_template('edit.html', {'add': add})


class DeleteAdd(BaseHandler):

    def get(self, add_id):
        iden = int(add_id)
        add = db.get(db.Key.from_path('Adds', iden))
        db.delete(add)
        return webapp2.redirect('/')



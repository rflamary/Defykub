
import webapp2
import jinja2
import os
import defykub
from google.appengine.api import users


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)+'/template'))
    
    

class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            
            login = users.create_logout_url(self.request.uri)
            login_text = 'Logout'
            
            template_values = {
            'title': 'Defykub Home',
            'login': login,
            'login_text': login_text,
            }   
            template = jinja_environment.get_template('main.html')
            self.response.out.write(template.render(template_values))
            
        else:
            self.redirect(users.create_login_url(self.request.uri))
            
            
class Play(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            
            login = users.create_logout_url(self.request.uri)
            login_text = 'Logout'
            
            defy=defykub.get_random_defykub()
            
            template_values = {
            'title': 'Defykub Play',
            'login': login,
            'login_text': login_text,
            'game': defy.get_svg()
            }   
            template = jinja_environment.get_template('play.html')
            self.response.out.write(template.render(template_values))
            
        else:
            self.redirect(users.create_login_url(self.request.uri))            

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/play',Play)],
                              debug=True)

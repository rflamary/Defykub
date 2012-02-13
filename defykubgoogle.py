
import webapp2
import jinja2
import os
import defykub
from google.appengine.api import users
from google.appengine.ext import db


svgw=20;

param_random={'sx':20,
              'sy':20,
              'nbwall':50,
              'nbtarg':3,
              'nbmob':5,
              'nbactions':20}  

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)+'/template'))
    
class PlayDB(db.Model):
    user = db.UserProperty()
    game = db.TextProperty()
    game0= db.TextProperty()
    selected = db.IntegerProperty()
    nbactions = db.IntegerProperty()
    date_start = db.DateTimeProperty(auto_now_add=True)  
    
def game_key(game_name=None):
  """Constructs a datastore key for a Guestbook entity with guestbook_name."""
  return db.Key.from_path('Game', game_name or 'default_game')

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
            
def play_action(defy,mob,d):
    if defy.nbmob:
        defy.play_action(mob,d)
        if mob>=defy.nbmob:
            mob=0
        return mob
            
class Play(webapp2.RequestHandler):
    
    def get(self):
        user = users.get_current_user()

        if user:
            
            action=self.request.get('action',default_value='show')
            
            game = db.GqlQuery("SELECT * "
                                "FROM PlayDB "
                                "WHERE user = :1",user)             
            if action=='show':
                
                     
                if game.count():
                    
                    game=game.get()
                    defy=defykub.defykub()
                    defy.from_string(game.game)
                        
                else:
                    defy=defykub.get_random_defykub(**param_random)
                        
                    game=PlayDB()
                    
                    game.user=user
                    game.nbactions=0
                    game.selected=0
                    game.game=defy.to_string()
                    game.game0=defy.to_string()
                    game.put()
                    
            elif action == 'new':
                
                if game.count():
                    
                    for g in game:
                        g.delete()
                 
                defy=defykub.get_random_defykub(**param_random)
                    
                game=PlayDB()
                
                game.user=user
                game.nbactions=0
                game.selected=0
                game.game=defy.to_string()
                game.game0=defy.to_string()
                game.put()                
                    
            defy.svgw=svgw    
                
            # preparing output                
            login = users.create_logout_url(self.request.uri)
            login_text = 'Logout'                           
            template_values = {
            'title': 'Defykub Play',
            'login': login,
            'login_text': login_text,
            'game': defy.get_svg(game.selected)
            }   
            template = jinja_environment.get_template('play.html')
            self.response.out.write(template.render(template_values))
            
        else:
            self.redirect(users.create_login_url(self.request.uri))     
            
    def post(self):
        user = users.get_current_user()

        if user:
            
            action=self.request.get('action',default_value='show')
            
            game = db.GqlQuery("SELECT * "
                                "FROM PlayDB "
                                "WHERE user = :1",user)             
            if action == 'new':
                
                if game.count():
                    
                    for g in game:
                        g.delete()
                 
                defy=defykub.get_random_defykub(**param_random)
                    
                game=PlayDB()
                
                game.user=user
                game.nbactions=0
                game.selected=0
                game.game=defy.to_string()
                game.game0=defy.to_string()
                game.put()     
                
            elif action=='switch':
                
                game=game.get()
                defy=defykub.defykub()
                defy.from_string(game.game)
                
                game.selected=(game.selected+1) % defy.nbmob
                
                game.put()
                
            elif action=='right':
                
                game=game.get()
                defy=defykub.defykub()
                defy.from_string(game.game)
                
                game.selected=play_action(defy,game.selected,defykub.d_right)
                    
                game.game=defy.to_string()
                game.nbactions+=1
                
                game.put()                
                
            elif action=='left':
                
                game=game.get()
                defy=defykub.defykub()
                defy.from_string(game.game)

                game.selected=play_action(defy,game.selected,defykub.d_left)
                    
                game.game=defy.to_string()
                game.nbactions+=1
                
                game.put() 
                   
            elif action=='up':
                
                game=game.get()
                defy=defykub.defykub()
                defy.from_string(game.game)
                
                game.selected=play_action(defy,game.selected,defykub.d_up)
                    
                game.game=defy.to_string()
                game.nbactions+=1
                
                game.put()       
                
            elif action=='down':
                
                game=game.get()
                defy=defykub.defykub()
                defy.from_string(game.game)
                
                game.selected=play_action(defy,game.selected,defykub.d_down)
                    
                game.game=defy.to_string()
                game.nbactions+=1
                
                game.put()                 
            elif action=='reset':
                
                game=game.get()
                defy=defykub.defykub()
                defy.from_string(game.game0)
                
                game.game=game.game0
   
                game.put()    
                
            else:
                    
                game=game.get()
                defy=defykub.defykub()
                defy.from_string(game.game)
                                      
                
            defy.svgw=svgw                    
            # preparing output                
            login = users.create_logout_url(self.request.uri)
            login_text = 'Logout'                           
            template_values = {
            'title': 'Defykub Play',
            'login': login,
            'login_text': login_text,
            'game': defy.get_svg(game.selected)
            }   
            template = jinja_environment.get_template('play.html')
            self.response.out.write(template.render(template_values))
            
        else:
            self.redirect(users.create_login_url(self.request.uri))               

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/play/',Play)],
                              debug=True)

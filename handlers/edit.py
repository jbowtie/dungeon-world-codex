import webapp2
import jinja2
from google.appengine.ext import db
from google.appengine.api import users
from monsterrules.common import Monster, Profile
import configuration.site


class EditHandler(webapp2.RequestHandler):
  """Edits a single monster
  
  Given the ID of a monster to edit, query for that monster and present it for
  editing iff it's owned by the current user.
  
  Templates used: edit.html"""
  
  def get(self, entity_id=None):
    """HTML GET handler.
    
    Check the query parameters for the ID of the monster to be edited.
    If found, display that monster for editing."""
    
    template_values = {
      'user' : users.get_current_user()
    }
    
    if entity_id:
      monster = Monster.get_by_id(int(entity_id))
      if monster:
        user = users.get_current_user()
        if monster.creator.account == user:
          template_values['monster'] = monster
        else:
          template_values['error'] = 401
      else:
        template_values['error'] = 404
    else:
      template_values['error'] = 404
    
    template = configuration.site.jinja_environment.get_template('edit.html')
    self.response.write(template.render(template_values))
    
  def post(self, entity_id=None):
    """HTML POST handler. 
    
    Save changes to the given monster."""
    
    template_values = {
      'user' : users.get_current_user()
    }
    
    if entity_id:
      monster = Monster.get_by_id(int(entity_id))
      if monster:
        user = users.get_current_user()
        if monster.creator.account == user:
          monster.name = self.request.get('name')
          monster.hp = self.request.get('hp')
          monster.armor = self.request.get('armor')
          monster.damage = self.request.get('damage')
          monster.instinct = self.request.get('instinct')
          monster.description = self.request.get('description')
          
          nextindex = 0
          monster.tags = []
          while self.request.get('tag-'+str(nextindex)):
            monster.tags.append(self.request.get('tag-'+str(nextindex)))
            nextindex += 1
          
          nextindex = 0
          monster.special_qualities = []
          while self.request.get('specialquality-'+str(nextindex)):
            monster.special_qualities.append(self.request.get('specialquality-'+str(nextindex)))
            nextindex += 1
          
          nextindex = 0
          monster.damage_tags = []
          while self.request.get('damagetag-'+str(nextindex)):
            monster.damage_tags.append(self.request.get('damagetag-'+str(nextindex)))
            nextindex += 1
            
          nextindex = 0
          monster.moves = []
          while self.request.get('move-'+str(nextindex)):
            monster.moves.append(self.request.get('move-'+str(nextindex)))
            nextindex += 1
          
          monster.edited = True
          monster.put()
          return self.redirect('/view/'+str(monster.key().id()))
        else:
          template_values['error'] = 401
      else:
        template_values['error'] = 404
    else:
      template_values['error'] = 404
      
    template = configuration.site.jinja_environment.get_template('edit.html')
    self.response.write(template.render(template_values))


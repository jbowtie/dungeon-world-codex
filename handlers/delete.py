import webapp2
import jinja2
from google.appengine.ext import db
from google.appengine.api import users
from monsterrules.common import Monster, Profile
import handlers.base
import configuration.site

class DeleteHandler(handlers.base.LoggedInRequestHandler):
  """Deletes a single monster
  
  Given the ID of a monster to delete, query for that monster and delete it
  iff it's owned by the current user.
  
  Templates used: delete.html"""
  
  def get(self, entity_id=None):
    """HTML GET handler.
    
    Check the query parameters for the ID of the monster to be displayed.
    If found, disply that monster using the standard template."""
    
    template_values = self.build_template_values()
    
    if entity_id:
      monster = Monster.get_by_id(int(entity_id))
      if monster:
        if monster.creator.account == template_values[handlers.base.USER_KEY]:
          monster.delete()
        else:
          template_values['error'] = 401
      else:
        template_values['error'] = 404
    else:
      template_values['error'] = 404
    
    template = configuration.site.jinja_environment.get_template('delete.html')
    self.response.write(template.render(template_values))

import webapp2
from google.appengine.api import users
from monsterrules.common import Profile
import configuration.site

USER_KEY = "user"
PROFILE_KEY = "profile"
LOGIN_URL_KEY = "login_url"

class LoggedInRequestHandler(webapp2.RequestHandler):
      
  def build_template_values(self):
    template_values = {}
    template_values[USER_KEY] = users.get_current_user()
    if not template_values[USER_KEY]:
      template_values[LOGIN_URL_KEY] = users.create_login_url(self.uri_for('login'))
    else:
      template_values[PROFILE_KEY] = Profile.all().filter("account = ", template_values[USER_KEY]).get()
    self.template_values = template_values
    return template_values
    
  def forbidden(self):
    self.response.set_status(403)
    template = configuration.site.jinja_environment.get_template('errors/forbidden.html')
    self.response.write(template.render(self.template_values))
    
  def not_found(self):
    self.response.set_status(404)
    template = configuration.site.jinja_environment.get_template('errors/not_found.html')
    self.response.write(template.render(self.template_values))
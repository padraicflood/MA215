import jinja2
import webapp2
import cgi
import os
from affine_needle import align

JINJA_ENVIRONMENT = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
        extensions=['jinja2.ext.autoescape'],
        autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        template_values = {
                'xout': [],
                'yout': [],
                'value': '',
                'x': '',
                'y': '',
                'o':'',
                'e':'',
                'match': '',
                'transition': '',
                'transversion': '',
                }
        template = JINJA_ENVIRONMENT.get_template('align.html')
        self.response.write(template.render(template_values))

class Align(webapp2.RequestHandler):
    def post(self):
        valid = True
        for n in self.request.get('x').upper():
            if n not in ('A', 'T', 'G', 'C'):
                valid = False
                break
        for n in self.request.get('y').upper():
            if n not in ('A', 'T', 'G', 'C'):
                valid = False
                break
        if valid:
            (value, xout, yout) = align(self.request.get('x').upper(),self.request.get('y').upper(),\
                    int(self.request.get('o')),int(self.request.get('e')),\
                    int(self.request.get('match')),int(self.request.get('transition')),\
                    int(self.request.get('transversion')))

            template_values = {
                    'xout': xout,
                    'yout': yout,
                    'value': value,
                    'x': self.request.get('x').upper(),
                    'y': self.request.get('y').upper(),
                    'o': self.request.get('o'),
                    'e': self.request.get('e'),
                    'match': self.request.get('match'),
                    'transition': self.request.get('transition'),
                    'transversion': self.request.get('transversion'),
                    }
            template = JINJA_ENVIRONMENT.get_template('align.html')
            self.response.write(template.render(template_values))
        else:
            self.response.write("<div class='error'>Error: sequence must contain only dna characters (A T G C)</div>")
            template_values = {
                    'xout': [],
                    'yout': [],
                    'value': '',
                    'x': self.request.get('x').upper(),
                    'y': self.request.get('y').upper(),
                    'o': self.request.get('o'),
                    'e': self.request.get('e'),
                    'match': self.request.get('match'),
                    'transition': self.request.get('transition'),
                    'transversion': self.request.get('transversion'),
                    }
            template = JINJA_ENVIRONMENT.get_template('align.html')
            self.response.write(template.render(template_values))
    def get(self):
        template_values = {
                'xout': [],
                'yout': [],
                'value': '',
                'x': '',
                'y': '',
                'o':'',
                'e':'',
                'match': '',
                'transition': '',
                'transversion': '',
                }
        template = JINJA_ENVIRONMENT.get_template('align.html')
        self.response.write(template.render(template_values))
    
application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/align', Align),
], debug=False)

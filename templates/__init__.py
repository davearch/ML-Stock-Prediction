from flask import Flask
app = Flask(__name__,
 	static_folder = './public',
 	template_folder="./static")

#from templates.api.views import api_blueprint
# register the blueprints

#app.register_blueprint(api_blueprint)

from templates.hello.views import hello_blueprint
app.register_blueprint(hello_blueprint)

from .api import api as api_blueprint
app.register_blueprint(api_blueprint, url_prefix='/api')

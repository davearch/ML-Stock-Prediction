from flask import Flask
app = Flask(__name__,
 	static_folder = './public',
 	template_folder="./static")

from templates.hello.views import hello_blueprint
from templates.api.views import api_blueprint
# register the blueprints
app.register_blueprint(hello_blueprint)
app.register_blueprint(api_blueprint)

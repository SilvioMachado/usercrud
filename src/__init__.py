from flask import Flask
from src.user.blueprint import blueprint as user_blueprint

app = Flask(__name__)
app.register_blueprint(user_blueprint, url_prefix='user/')

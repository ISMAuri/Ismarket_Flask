from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

# Secret key is used to protect the data from being tampered with
# It is used to create a signature for the data that is sent to the client
#Nothing will happen if we enter the register page without a secret key(we need it to ensure security)
#os.urandom(12).hex()
#'238da175c3940cee08dd798d'
app.config['SECRET_KEY'] = '238da175c3940cee08dd798d'

db = SQLAlchemy(app)

# bcrypt is used to hash the password before storing it in the database
bcrypt = Bcrypt(app)

# LoginManager is used to manage the user sessions
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

# So I dont need to "with app.app_context()" every time I want to interact with the database
app.app_context().push()

from market import routes
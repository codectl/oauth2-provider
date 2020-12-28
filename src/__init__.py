from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


# SQLite database
db = SQLAlchemy()

# Initialize session handler
login_manager = LoginManager()

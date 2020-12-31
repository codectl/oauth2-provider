from flask import Blueprint
from flask_restplus import Api

# Create API blueprint
restful_api = Blueprint('api', __name__)

# Initialize Flask Restplus root api
api = Api(restful_api,
          title='OAuth2 Provider Service API',
          version='1.0',
          description='an OAuth2 service implementation to manage authorization requests.'
          )

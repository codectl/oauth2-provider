from authlib.integrations.sqla_oauth2 import OAuth2AuthorizationCodeMixin

from src import db


class OAuth2AuthorizationCode(db.Model, OAuth2AuthorizationCodeMixin):
    __tablename__ = 'oauth2_authorization_code'

    id = db.Column(db.Integer, primary_key=True)
    resource_owner_id = db.Column(
        db.Integer, db.ForeignKey('oauth2_resource_owner.id', ondelete='CASCADE'))
    user = db.relationship('OAuth2ResourceOwner')

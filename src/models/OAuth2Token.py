import time

from authlib.integrations.sqla_oauth2 import OAuth2TokenMixin

from src import db


class OAuth2Token(db.Model, OAuth2TokenMixin):
    __tablename__ = 'oauth2_token'

    id = db.Column(db.Integer, primary_key=True)
    resource_owner_id = db.Column(
        db.Integer, db.ForeignKey('oauth2_resource_owner.id', ondelete='CASCADE'))
    resource_owner = db.relationship('OAuth2ResourceOwner')

    def is_refresh_token_active(self):
        if self.revoked:
            return False
        expires_at = self.issued_at + self.expires_in * 2
        return expires_at >= time.time()

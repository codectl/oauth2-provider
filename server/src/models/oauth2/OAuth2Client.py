from authlib.integrations.sqla_oauth2 import OAuth2ClientMixin

from server.src import db


class OAuth2Client(db.Model, OAuth2ClientMixin):
    __tablename__ = 'oauth2_client'

    id = db.Column(db.Integer, primary_key=True)
    resource_owner_id = db.Column(
        db.Integer, db.ForeignKey('oauth2_resource_owner.id', ondelete='CASCADE')
    )
    resource_owner = db.relationship('OAuth2ResourceOwner')

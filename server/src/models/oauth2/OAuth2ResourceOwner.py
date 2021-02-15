from server.src import db


class OAuth2ResourceOwner(db.Model):
    __tablename__ = 'oauth2_resource_owner'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20))

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'oauth2_resource_owner'
    }

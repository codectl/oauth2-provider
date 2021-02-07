from src import db


class Scope(db.Model):
    __tablename__ = 'scopes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return "<Scope '{0}'>".format(self.name)

from src import db


class Permission(db.Model):
    __tablename__ = 'permissions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(100), nullable=True)
    read_only = db.Column(db.Boolean, nullable=False, default=True)

    @property
    def scope(self):
        return ''.join(('read' if self.read_only else 'write', ':', self.name))

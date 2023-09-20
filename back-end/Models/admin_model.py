from . import db
class Admin(db.Model):
	__tablename__= 'admins'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(100), nullable=False)
	password = db.Column(db.String(100), nullable=False)
	name = db.Column(db.String(100), nullable=False)
	uuid = db.Column(db.String(32), nullable=False)

	def __repr__(self):
		return '<Admin %r>' % self.id

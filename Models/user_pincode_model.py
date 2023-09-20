from . import db
class User_pincode(db.Model):
	__tablename__= 'user_pincodes'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	pincode = db.Column(db.String(7), nullable=False)

	def __repr__(self):
		return '<User_pincode %r>' % self.id

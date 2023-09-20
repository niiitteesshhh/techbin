from . import db
class User(db.Model):
	__tablename__= 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(250), nullable=False)
	name = db.Column(db.String(250), nullable=False)
	password = db.Column(db.String(100), nullable=False)
	uuid = db.Column(db.String(32), nullable=False)
	records = db.relationship('Record', backref = db.backref("UserOfRecords"))
	user_pincodes = db.relationship('User_pincode', backref = db.backref("UserOfUser_pincodes"))

	def __repr__(self):
		return '<User %r>' % self.id

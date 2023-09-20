from . import db
class Record(db.Model):
	__tablename__= 'records'
	id = db.Column(db.Integer, primary_key=True)
	trashcan_id = db.Column(db.Integer, db.ForeignKey('trashcans.id'))
	lastPickup = db.Column(db.DateTime, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

	def __repr__(self):
		return '<Record %r>' % self.id

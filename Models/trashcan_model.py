from . import db
class Trashcan(db.Model):
	__tablename__= 'trashcans'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(250), nullable=False)
	longitude = db.Column(db.String(50), nullable=False)
	latitude = db.Column(db.String(50), nullable=False)
	pincode = db.Column(db.String(7), nullable=False)
	status = db.Column(db.Enum('empty','half','full'), nullable=False)
	records = db.relationship('Record', backref = db.backref("TrashcanOfRecords"))

	def __repr__(self):
		return '<Trashcan %r>' % self.id

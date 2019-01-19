from app import db

class HawkerCentre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    address = db.Column(db.String(256))

    def __repr__(self):
        return '<HawkerCentre {}>'.format(self.id) 

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)

    def __repr__(self):
        return '<Food {}>'.format(self.id) 

class Vendor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    unit_no = db.Column(db.String(20))
    hawker_id = db.Column(db.Integer, index=True)

    def __repr__(self):
        return '<Vendor {}>'.format(self.id) 

class Cost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hawker_id = db.Column(db.Integer, index=True)
    food_id = db.Column(db.Integer, index=True)

    def __repr__(self):
        return '<Cost {}>'.format(self.id) 

class Discount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime)
    amount = db.Column(db.Float)
    cost_id = db.Column(db.Integer, index=True)

    def __repr__(self):
        return '<Discount {}>'.format(self.id) 
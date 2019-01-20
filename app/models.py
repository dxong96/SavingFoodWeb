from app import db

class BaseModel(db.Model):
    __abstract__ = True

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class HawkerCentre(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    address = db.Column(db.String(256))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    def __repr__(self):
        return '<HawkerCentre {}>'.format(self.id) 

class Food(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)

    def __repr__(self):
        return '<Food {}>'.format(self.id) 

class Vendor(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    unit_no = db.Column(db.String(20))
    hawker_id = db.Column(db.Integer, index=True)

    def __repr__(self):
        return '<Vendor {}>'.format(self.id) 

class Cost(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, index=True)
    food_id = db.Column(db.Integer, index=True)
    amount = db.Column(db.Float)

    def __repr__(self):
        return '<Cost {}>'.format(self.id) 

class Discount(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime)
    amount = db.Column(db.Float)
    cost_id = db.Column(db.Integer, index=True)
    qty = db.Column(db.Integer)

    def __repr__(self):
        return '<Discount {}>'.format(self.id) 
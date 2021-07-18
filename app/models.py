from app import db
import json


def serialize(obj):
    return dict(sorted({k: v for k, v in obj.__dict__.items() if k != '_sa_instance_state'}.items()))


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    SKU = db.Column(db.String(16), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('type.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Product %r>' % self.id


class Type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return '<Type %r>' % self.name

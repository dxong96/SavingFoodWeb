from app import app, db
from flask import render_template
from flask import jsonify
from flask import request
from app.models import HawkerCentre, Food, Vendor, Cost, Discount
from datetime import date
from app.latlong import distance


@app.route("/")
@app.route("/index")
def index():
    user = {"username": "dx"}
    return render_template("index.html", title="hello!", user= user)


@app.route("/foods.json")
def foods():
    foods = Food.query.all()
    return jsonify(list(map(Food.as_dict, foods)))


@app.route("/nearby.json")
def nearby():
    # for now list all hawkers, need to change the code to compare the latitude and longitude
    lat = request.args.get('lat')
    lon = request.args.get('long')
    centres = HawkerCentre.query.all()
    if lat != None and lon != None:
        lat = float(lat)
        lon = float(lon)
        new_centres = []
        for centre in centres: 
            if distance(lat, lon, centre.latitude, centre.longitude) < 0.5:
                new_centres.append(centre)

        centres = new_centres
    return jsonify(list(map(HawkerCentre.as_dict, centres)))

@app.route("/foods/<int:food_id>/vendors.json")
def food_vendors(food_id):
    costs = Cost.query.filter_by(food_id=food_id).all()
    vendor_ids = map(lambda c: c.vendor_id, costs)
    vendors = db.session.query(Vendor).filter(Vendor.id.in_(vendor_ids)).all()

    return jsonify(list(map(Vendor.as_dict, vendors)))


@app.route("/centres/<int:centre_id>/vendors.json")
def centre_vendors(centre_id):
    vendors = Vendor.query.filter_by(hawker_id=centre_id).all()
    return jsonify(list(map(Vendor.as_dict, vendors)))


@app.route("/vendors/<int:vendor_id>.json")
def vendor(vendor_id):
    vendor = Vendor.query.get(vendor_id)
    ret = vendor.as_dict()
    if vendor != None:
        costs = Cost.query.filter_by(vendor_id=vendor_id).all()
        cost_ids = []
        food_id_cost = {}
        for cost in costs:
            cost_ids.append(cost.id)
            food_id_cost[cost.food_id] = cost

        food_ids = list(map(lambda c: c.food_id, costs))
        foods = db.session.query(Food).filter(Food.id.in_(food_ids)).all()


        ret["foods"] = []
        for food in foods:
            item = food.as_dict()
            cost = food_id_cost[food.id]
            item["cost"] = cost.amount
            discount = Discount.query.filter_by(cost_id=cost.id).first()
            item["discount"] = 0
            if discount != None and discount.start_time.date() == date.today():
                item["discount"] = discount.amount
            ret["foods"].append(item)
    return jsonify(ret)

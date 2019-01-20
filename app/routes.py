
from app import app, db
from flask import render_template
from flask import jsonify
from flask import request
from app.models import HawkerCentre, Food, Vendor, Cost, Discount
from datetime import date
from app.latlong import distance
from flask import Flask, render_template, flash, request, redirect, url_for
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, SelectField


app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'



class ReusableForm(Form):
    hawker_name = TextField('Name:', validators=[validators.required()])
    unit_no = TextField('Unit No', validators=[validators.required(), validators.Length(max=20)])
    hawker_centre = SelectField('Hawker Centres', choices=[(1, 'Ayer Rajah Hawker Centre'), (2,'Holland Village Hawker Centre')])
    food = TextField("Food Name", validators=[validators.required()])
    food_cost = TextField("Food Price", validators=[validators.required()])


@app.route("/", methods = ['GET', 'POST'])
def index():

    form = ReusableForm(request.form)

    print (form.errors)

    if request.method == 'POST':
        form = request.form
        hawker_name=form['hawker_name']
        unit_no=form['unit_no']
        hawker_centre=form['hawker_centre']

        vendor = Vendor(name = hawker_name, unit_no = unit_no, hawker_id = hawker_centre)
        db.session.add(vendor)
        db.session.commit()

        return redirect(url_for('addFood'))

        # return render_template("addFood.html")
    return render_template("index.html", title="hello!", form = form)

@app.route("/vendors")
def list_vendors():
    return render_template("vendors.html", vendors = Vendor.query.all())

@app.route("/addFood/<int:vendor_id>")
def addFood(vendor_id):
    return render_template("food.html", foods = Food.query.all(), vendor_id=vendor_id)

@app.route("/addFoods", methods = ['POST'])
def addFoods():
    food_ids = request.form.getlist('food_id[]')
    costs = request.form.getlist('cost[]')
    vendor_id = request.form.get('vendor_id')

    length = len(food_ids)
    for i in range(length):
        c = Cost(food_id=food_ids[i], vendor_id=vendor_id, amount=float(costs[i]))
        db.session.add(c)
    db.session.commit()
    return redirect('/vendors')

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

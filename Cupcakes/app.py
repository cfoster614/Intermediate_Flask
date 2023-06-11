from flask import Flask, request, render_template, redirect, url_for, jsonify  
from models import db, connect_db, Cupcake
import logging


logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
app = Flask(__name__)  
app.config['SECRET_KEY'] = "scamp" 
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

@app.route('/api/cupcakes')
def list_all_cupcakes():
    """Return JSON {'cupcakes': [{id, flavor, size, rating, image}]}"""
    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(all_cupcakes=all_cupcakes)


@app.route('/api/cupcakes/<int:cupcake_id>')
def cupcake_details(cupcake_id):
    """Return JSON { 'cupcake': {id, flavor, size, rating, image}}"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake = cupcake.serialize())

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    
    data = request.json
    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']
    image = request.json['image']
    
    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
    db.session.add(new_cupcake)
    db.session.commit()
    
    return jsonify(cupcake = new_cupcake.serialize())

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    request.json
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)
    db.session.commit()
    
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message='deleted')
    

@app.route('/')
def homepage():
    cupcakes = Cupcake.query.all()
    last_cupcake = Cupcake.query.order_by(Cupcake.id.desc()).first()
    return render_template('index.html', cupcakes = cupcakes, last_cupcake = last_cupcake)


    
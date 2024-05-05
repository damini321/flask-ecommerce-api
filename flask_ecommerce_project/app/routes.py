from flask import request, jsonify
from app import app, db
from app.models import Product, User
import json
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash


# GET endpoint to retrieve all products
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    # Serialize products into dictionaries
    serialized_products = [{"id": product.id, "title": product.title, "description": product.description, "price": product.price} for product in products]
    # Convert list of dictionaries to JSON string with sorted keys
    response_data = json.dumps(serialized_products, sort_keys=False)
    return app.response_class(response=response_data, status=200, mimetype='application/json')

# GET endpoint to retrieve a specific product by ID
@app.route('/products/<int:id>', methods=['GET'])
@jwt_required()
def get_product(id):
    product = Product.query.get(id)
    if product:
        # Serialize product into a dictionary
        serialized_product = {"id": product.id, "title": product.title, "description": product.description, "price": product.price}
        # Convert dictionary to JSON string with sorted keys
        response_data = json.dumps(serialized_product, sort_keys=False)
        return app.response_class(response=response_data, status=200, mimetype='application/json')
    else:
        response_data = json.dumps({"error": "Product not found"})
        return app.response_class(response=response_data, status=404, mimetype='application/json')

# POST endpoint to create a new product
@app.route('/products', methods=['POST'])
@jwt_required()
def create_product():
    current_user_id = get_jwt_identity()
    data = request.json
    new_product = Product(title=data['title'], description=data['description'], price=data['price'])
    db.session.add(new_product)
    db.session.commit()
    # Serialize the new product into a dictionary
    serialized_new_product = {"id": new_product.id, "title": new_product.title, "description": new_product.description, "price": new_product.price}
    # Convert dictionary to JSON string with sorted keys
    response_data = json.dumps(serialized_new_product, sort_keys=False)
    return app.response_class(response=response_data, status=201, mimetype='application/json')

# PUT endpoint to update an existing product by ID
@app.route('/products/<int:id>', methods=['PUT'])
@jwt_required()
def update_product(id):
    current_user_id = get_jwt_identity()
    product = Product.query.get(id)
    if product:
        data = request.json
        product.title = data.get('title', product.title)
        product.description = data.get('description', product.description)
        product.price = data.get('price', product.price)
        db.session.commit()
        # Serialize the updated product into a dictionary
        serialized_updated_product = {"id": product.id, "title": product.title, "description": product.description, "price": product.price}
        # Convert dictionary to JSON string with sorted keys
        response_data = json.dumps(serialized_updated_product, sort_keys=False)
        return app.response_class(response=response_data, status=200, mimetype='application/json')
    else:
        response_data = json.dumps({"error": "Product not found"})
        return app.response_class(response=response_data, status=404, mimetype='application/json')

# DELETE endpoint to delete a product by ID
@app.route('/products/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    product = Product.query.get(id)
    if product:
        db.session.delete(product)
        db.session.commit()
        response_data = json.dumps({"message": f"Product with ID {id} deleted successfully"})
        return app.response_class(response=response_data, status=200, mimetype='application/json')
    else:
        response_data = json.dumps({"error": "Product not found"})
        return app.response_class(response=response_data, status=404, mimetype='application/json')

jwt = JWTManager(app)

# User registration endpoint
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400
    
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 400
    
    # Hash the password before storing it
    hashed_password = generate_password_hash(password)

    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

# User login endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid username or password'}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token}), 200

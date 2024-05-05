from flask import request
from app import app, db
from app.models import Product
import json

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
def create_product():
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
def update_product(id):
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

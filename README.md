# Flask Product Management API

## Overview

This Flask application provides a RESTful API for managing products. It allows users to perform CRUD (Create, Read, Update, Delete) operations on products, as well as user registration and authentication using JWT (JSON Web Tokens).

Follow the steps below to set up the Flask-Ecommerce project and run it:

## 1. Installation
- Clone the repository:

``` bash
git clone <repository_url>
```

- Navigate to the project directory:

```bash
cd flask-product-management-api
```

- Create a virtual environment (optional but recommended):
```bash
python -m venv venv
```

- Activate the virtual environment:
Windows:

```bash
venv\Scripts\activate
```

- Install the required packages:
```bash
pip install -r requirements.txt
```

- Create a .env file in the project root directory and add the following environment variables:
```bash
JWT_SECRET_KEY=<your_secret_key>
```

- Run the Flask application:
```bash
python run.py
```

## Endpoints

### Products

GET /products: Retrieve all products.
GET /products/<id>: Retrieve a specific product by ID.
POST /products: Create a new product (requires authentication).
PUT /products/<id>: Update an existing product by ID (requires authentication).
DELETE /products/<id>: Delete a product by ID (requires authentication).

### User Authentication

POST /register: Register a new user.
POST /login: Log in with existing credentials to obtain an access token.

## Authentication

User authentication is implemented using JWT (JSON Web Tokens). To access protected endpoints (e.g., create, update, delete products), clients need to include a valid JWT token in the request headers.

- Example:

```
Authorization: Bearer <access_token>
```

## Database

This application uses SQLite as the default database. You can find the database file (products.db) in the project root directory.


## Contributing
Contributions are welcome! Please feel free to open issues or pull requests.

## License
This project is licensed under the MIT License.

from functools import wraps
from flask import request, jsonify
from config import Config
from models import db, Product


def require_gateway_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("X-Gateway-Token")

        if not token:
            return jsonify({"message": "Token no proporcionado."}), 401

        if token != Config.GATEWAY_SERVICE_TOKEN:
            return jsonify({"message": "Token inválido."}), 403

        return f(*args, **kwargs)

    return decorated


def register_routes(app):
    @app.route("/api/products", methods=["GET"])
    @require_gateway_token
    def get_products():
        products = Product.query.all()
        return jsonify([product.to_dict() for product in products]), 200

    @app.route("/api/products/<int:id>", methods=["GET"])
    @require_gateway_token
    def get_product(id):
        product = Product.query.get_or_404(id)
        return jsonify(product.to_dict()), 200

    @app.route("/api/products", methods=["POST"])
    @require_gateway_token
    def create_product():
        data = request.get_json()

        if not data:
            return jsonify({"message": "No se enviaron datos."}), 400

        required_fields = ["name", "description", "price", "stock"]

        for field in required_fields:
            if field not in data:
                return jsonify({"message": f"El campo '{field}' es obligatorio."}), 400

        product = Product(
            name=data["name"],
            description=data["description"],
            price=float(data["price"]),
            stock=int(data["stock"]),
        )

        db.session.add(product)
        db.session.commit()

        return jsonify({
            "message": "Producto creado correctamente.",
            "product": product.to_dict()
        }), 201

    @app.route("/api/products/<int:id>", methods=["PUT"])
    @require_gateway_token
    def update_product(id):
        product = Product.query.get_or_404(id)
        data = request.get_json()

        if not data:
            return jsonify({"message": "No se enviaron datos."}), 400

        product.name = data.get("name", product.name)
        product.description = data.get("description", product.description)
        product.price = float(data.get("price", product.price))
        product.stock = int(data.get("stock", product.stock))

        db.session.commit()

        return jsonify({
            "message": "Producto actualizado correctamente.",
            "product": product.to_dict()
        }), 200

    @app.route("/api/products/<int:id>", methods=["DELETE"])
    @require_gateway_token
    def delete_product(id):
        product = Product.query.get_or_404(id)

        db.session.delete(product)
        db.session.commit()

        return jsonify({
            "message": "Producto eliminado correctamente."
        }), 200

    @app.route("/api/products/<int:id>/stock", methods=["GET"])
    @require_gateway_token
    def get_stock(id):
        product = Product.query.get_or_404(id)

        return jsonify({
            "id": product.id,
            "name": product.name,
            "stock": product.stock
        }), 200

    @app.route("/api/products/<int:id>/stock/decrease", methods=["PATCH"])
    @require_gateway_token
    def decrease_stock(id):
        product = Product.query.get_or_404(id)
        data = request.get_json()

        if not data or "quantity" not in data:
            return jsonify({"message": "El campo 'quantity' es obligatorio."}), 400

        quantity = int(data["quantity"])

        if quantity <= 0:
            return jsonify({"message": "La cantidad debe ser mayor que cero."}), 400

        if product.stock < quantity:
            return jsonify({"message": "Stock insuficiente."}), 400

        previous_stock = product.stock
        product.stock -= quantity
        db.session.commit()

        return jsonify({
            "message": "Stock actualizado correctamente.",
            "product": {
                "id": product.id,
                "name": product.name,
                "previous_stock": previous_stock,
                "discounted_quantity": quantity,
                "current_stock": product.stock
            }
        }), 200
    

    @app.route("/api/products/<int:id>/stock/increase", methods=["PATCH"])
    @require_gateway_token
    def increase_stock(id):
        product = Product.query.get_or_404(id)
        data = request.get_json()

        if not data or "quantity" not in data:
            return jsonify({"message": "El campo 'quantity' es obligatorio."}), 400

        quantity = int(data["quantity"])

        if quantity <= 0:
            return jsonify({"message": "La cantidad debe ser mayor que cero."}), 400

        previous_stock = product.stock
        product.stock += quantity
        db.session.commit()

        return jsonify({
            "message": "Stock aumentado correctamente.",
            "product": {
                "id": product.id,
                "name": product.name,
                "previous_stock": previous_stock,
                "added_quantity": quantity,
                "current_stock": product.stock
            }
        }), 200

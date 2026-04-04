from flask import jsonify, request, current_app
from models import db, Store


def validate_token():
    token = request.headers.get("X-Gateway-Token")

    if not token:
        return False, ("Token requerido", 401)

    if token != current_app.config["GATEWAY_SERVICE_TOKEN"]:
        return False, ("Token inválido", 403)

    return True, None


def register_routes(app):
    @app.route("/api/stores/health", methods=["GET"])
    def health():
        is_valid, error = validate_token()
        if not is_valid:
            return jsonify({"error": error[0]}), error[1]

        return jsonify({
            "message": "Stores service is running."
        })
    
    @app.route("/api/stores", methods=["POST"])
    def create_store():
        is_valid, error = validate_token()
        if not is_valid:
            return jsonify({"error": error[0]}), error[1]

        data = request.get_json()

        name = data.get("name")
        address = data.get("address")
        city = data.get("city")
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        product_ids = data.get("productIds", [])

        if not name or not address or not city:
            return jsonify({"error": "Campos obligatorios faltantes"}), 400

        if not isinstance(product_ids, list):
            return jsonify({"error": "productIds debe ser una lista"}), 400

        store = Store(
            name=name,
            address=address,
            city=city,
            latitude=latitude,
            longitude=longitude,
            product_ids=product_ids
        )

        db.session.add(store)
        db.session.commit()

        return jsonify({
            "message": "Tienda creada correctamente",
            "store": {
                "id": store.id,
                "name": store.name
            }
        }), 201

    @app.route("/api/stores", methods=["GET"])
    def get_stores():
        is_valid, error = validate_token()
        if not is_valid:
            return jsonify({"error": error[0]}), error[1]

        stores = Store.query.all()

        result = []

        for store in stores:
            result.append({
                "id": store.id,
                "name": store.name,
                "address": store.address,
                "city": store.city,
                "latitude": store.latitude,
                "longitude": store.longitude,
                "isActive": store.is_active,
                "productIds": store.product_ids
            })

        return jsonify({
            "stores": result
        }), 200        
    
    @app.route("/api/stores/<int:store_id>", methods=["GET"])
    def get_store_by_id(store_id):
        is_valid, error = validate_token()
        if not is_valid:
            return jsonify({"error": error[0]}), error[1]

        store = Store.query.get(store_id)

        if not store:
            return jsonify({"error": "Tienda no encontrada"}), 404

        return jsonify({
            "store": {
                "id": store.id,
                "name": store.name,
                "address": store.address,
                "city": store.city,
                "latitude": store.latitude,
                "longitude": store.longitude,
                "isActive": store.is_active,
                "productIds": store.product_ids
            }
        }), 200

    @app.route("/api/stores/city/<string:city>", methods=["GET"])
    def get_stores_by_city(city):
        is_valid, error = validate_token()
        if not is_valid:
            return jsonify({"error": error[0]}), error[1]

        stores = Store.query.filter_by(city=city).all()

        result = []

        for store in stores:
            result.append({
                "id": store.id,
                "name": store.name,
                "address": store.address,
                "city": store.city,
                "latitude": store.latitude,
                "longitude": store.longitude,
                "isActive": store.is_active,
                "productIds": store.product_ids
            })

        return jsonify({
            "stores": result
        }), 200

    @app.route("/api/stores/product/<int:product_id>", methods=["GET"])
    def get_stores_by_product(product_id):
        is_valid, error = validate_token()
        if not is_valid:
            return jsonify({"error": error[0]}), error[1]

        stores = Store.query.all()

        result = []

        for store in stores:
            if store.product_ids and product_id in store.product_ids:
                result.append({
                    "id": store.id,
                    "name": store.name,
                    "address": store.address,
                    "city": store.city,
                    "latitude": store.latitude,
                    "longitude": store.longitude,
                    "isActive": store.is_active,
                    "productIds": store.product_ids
                })

        return jsonify({
            "stores": result
        }), 200
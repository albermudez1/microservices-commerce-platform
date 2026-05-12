import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv

load_dotenv()

# para ejecutar en local
#BASE_URL = os.getenv("GATEWAY_BASE_URL", "http://127.0.0.1:8000/api").rstrip("/")

# para ejecutar con docker
BASE_URL = "http://gateway:8000/api"

TEST_USER_NAME = os.getenv("TEST_USER_NAME", "Usuario Testing")
TEST_USER_EMAIL = os.getenv("TEST_USER_EMAIL", "testing@example.com")
TEST_USER_PASSWORD = os.getenv("TEST_USER_PASSWORD", "Password123*")
TEST_USER_QUESTION = os.getenv("TEST_USER_QUESTION", "Color favorito")
TEST_USER_ANSWER = os.getenv("TEST_USER_ANSWER", "Azul")

TEST_PRODUCT_NAME = os.getenv("TEST_PRODUCT_NAME", "Producto Testing")
TEST_PRODUCT_DESCRIPTION = os.getenv(
    "TEST_PRODUCT_DESCRIPTION",
    "Producto creado para pruebas de rendimiento",
)
TEST_PRODUCT_PRICE = float(os.getenv("TEST_PRODUCT_PRICE", "99.9"))
TEST_PRODUCT_STOCK = int(os.getenv("TEST_PRODUCT_STOCK", "50"))

TEST_STORE_NAME = os.getenv("TEST_STORE_NAME", "Tienda Testing")
TEST_STORE_ADDRESS = os.getenv("TEST_STORE_ADDRESS", "Calle 1 # 1-01")
TEST_STORE_CITY = os.getenv("TEST_STORE_CITY", "Bogota")
TEST_STORE_LATITUDE = float(os.getenv("TEST_STORE_LATITUDE", "4.6097"))
TEST_STORE_LONGITUDE = float(os.getenv("TEST_STORE_LONGITUDE", "-74.0817"))

TEST_SALE_QUANTITY = int(os.getenv("TEST_SALE_QUANTITY", "2"))


def print_step(message: str) -> None:
    print(f"\n=== {message} ===")


def save_test_data(data: dict) -> None:
    output_path = Path(__file__).parent / "test_data.json"
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def safe_json(response: requests.Response) -> Any:
    try:
        return response.json()
    except Exception:
        return response.text


def extract_token(payload: Any) -> Optional[str]:
    if not isinstance(payload, dict):
        return None

    direct_keys = ["token", "access_token", "plainTextToken"]
    for key in direct_keys:
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value

    data = payload.get("data")
    if isinstance(data, dict):
        for key in direct_keys:
            value = data.get(key)
            if isinstance(value, str) and value.strip():
                return value

    auth = payload.get("authorization")
    if isinstance(auth, dict):
        for key in direct_keys:
            value = auth.get(key)
            if isinstance(value, str) and value.strip():
                return value

    return None


def register_user(session: requests.Session) -> None:
    print_step("Registering user")

    payload = {
        "name": TEST_USER_NAME,
        "email": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD,
        "password_confirmation": TEST_USER_PASSWORD,
        "question": TEST_USER_QUESTION,
        "answer": TEST_USER_ANSWER,
    }

    response = session.post(
        f"{BASE_URL}/register",
        json=payload,
        headers={"Accept": "application/json"},
        timeout=20,
    )

    body = safe_json(response)
    print(f"Status: {response.status_code}")
    print(body)

    if response.status_code not in (200, 201, 409, 422):
        raise RuntimeError("User registration failed.")


def login_user(session: requests.Session) -> Dict[str, Any]:
    print_step("Logging in user")

    payload = {
        "email": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD,
    }

    response = session.post(
        f"{BASE_URL}/login",
        json=payload,
        headers={"Accept": "application/json"},
        timeout=20,
    )

    body = safe_json(response)
    print(f"Status: {response.status_code}")
    print(body)

    if response.status_code != 200:
        raise RuntimeError("User login failed.")

    token = extract_token(body)
    if not token:
        raise RuntimeError("Could not extract auth token from login response.")

    if not isinstance(body, dict) or "user" not in body or not isinstance(body["user"], dict):
        raise RuntimeError("Could not extract user data from login response.")

    return {
        "token": token,
        "user": body["user"],
    }


def create_product(session: requests.Session, auth_headers: Dict[str, str]) -> int:
    print_step("Creating product")

    payload = {
        "name": TEST_PRODUCT_NAME,
        "description": TEST_PRODUCT_DESCRIPTION,
        "price": TEST_PRODUCT_PRICE,
        "stock": TEST_PRODUCT_STOCK,
    }

    response = session.post(
        f"{BASE_URL}/products",
        json=payload,
        headers=auth_headers,
        timeout=20,
    )

    body = safe_json(response)
    print(f"Status: {response.status_code}")
    print(body)

    if response.status_code not in (200, 201):
        raise RuntimeError("Product creation failed.")

    if isinstance(body, dict):
        product = body.get("product", body)
        if isinstance(product, dict) and "id" in product:
            return int(product["id"])

    raise RuntimeError("Could not extract product id.")


def create_store(
    session: requests.Session,
    auth_headers: Dict[str, str],
    product_id: int,
) -> int:
    print_step("Creating store")

    payload = {
        "name": TEST_STORE_NAME,
        "address": TEST_STORE_ADDRESS,
        "city": TEST_STORE_CITY,
        "latitude": TEST_STORE_LATITUDE,
        "longitude": TEST_STORE_LONGITUDE,
        "productIds": [product_id],
    }

    response = session.post(
        f"{BASE_URL}/stores",
        json=payload,
        headers=auth_headers,
        timeout=20,
    )

    body = safe_json(response)
    print(f"Status: {response.status_code}")
    print(body)

    if response.status_code not in (200, 201):
        raise RuntimeError("Store creation failed.")

    if isinstance(body, dict):
        store = body.get("store", body)
        if isinstance(store, dict) and "id" in store:
            return int(store["id"])

    raise RuntimeError("Could not extract store id.")


def process_sale(
    session: requests.Session,
    auth_headers: Dict[str, str],
    product_id: int,
) -> Dict[str, Any]:
    print_step("Processing sale")

    payload = {
        "productId": product_id,
        "quantity": TEST_SALE_QUANTITY,
    }

    response = session.post(
        f"{BASE_URL}/sales/process",
        json=payload,
        headers=auth_headers,
        timeout=20,
    )

    body = safe_json(response)
    print(f"Status: {response.status_code}")
    print(body)

    if response.status_code not in (200, 201):
        raise RuntimeError("Sales process failed.")

    if isinstance(body, dict):
        sale = body.get("sale")
        if isinstance(sale, dict):
            return sale

    raise RuntimeError("Could not extract sale data.")


def main() -> None:
    session = requests.Session()

    register_user(session)
    login_result = login_user(session)

    token = login_result["token"]
    user = login_result["user"]

    auth_headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    product_id = create_product(session, auth_headers)
    store_id = create_store(session, auth_headers, product_id)
    sale = process_sale(session, auth_headers, product_id)

    test_data = {
        "user_email": TEST_USER_EMAIL,
        "user_id": int(user["id"]),
        "product_id": product_id,
        "store_id": store_id,
        "sale_id": sale["_id"],
        "token": token,
    }

    save_test_data(test_data)

    print_step("Test data ready")
    print(test_data)


if __name__ == "__main__":
    main()
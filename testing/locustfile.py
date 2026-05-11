import json
import os
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv
from locust import HttpUser, between, task

load_dotenv()

API_BASE_URL = os.getenv("GATEWAY_BASE_URL", "http://127.0.0.1:8000/api").rstrip("/")

parsed_url = urlparse(API_BASE_URL)
HOST = f"{parsed_url.scheme}://{parsed_url.netloc}"
API_PREFIX = parsed_url.path.rstrip("/")

TEST_DATA_PATH = Path(__file__).parent / "test_data.json"

if not TEST_DATA_PATH.exists():
    raise FileNotFoundError(
        "No se encontró testing/test_data.json. "
        "Ejecuta primero setup_test_data.py."
    )

with open(TEST_DATA_PATH, "r", encoding="utf-8") as file:
    TEST_DATA = json.load(file)

TOKEN = TEST_DATA.get("token")
PRODUCT_ID = TEST_DATA.get("product_id")
USER_ID = TEST_DATA.get("user_id")

if not TOKEN:
    raise ValueError("No se encontró 'token' en test_data.json.")

if not PRODUCT_ID:
    raise ValueError("No se encontró 'product_id' en test_data.json.")

if not USER_ID:
    raise ValueError("No se encontró 'user_id' en test_data.json.")


class CommercePlatformUser(HttpUser):
    host = HOST
    wait_time = between(1, 2)

    def on_start(self):
        self.headers = {
            "Authorization": f"Bearer {TOKEN}",
            "Accept": "application/json",
        }
        self.product_id = PRODUCT_ID
        self.user_id = USER_ID

    @task(1)
    def get_products(self):
        self.client.get(
            f"{API_PREFIX}/products",
            headers=self.headers,
            name="/api/products",
        )

    @task(1)
    def get_product_by_id(self):
        self.client.get(
            f"{API_PREFIX}/products/{self.product_id}",
            headers=self.headers,
            name="/api/products/{product_id}",
        )

    @task(1)
    def get_product_stock(self):
        self.client.get(
            f"{API_PREFIX}/products/{self.product_id}/stock",
            headers=self.headers,
            name="/api/products/{product_id}/stock",
        )

    @task(1)
    def get_sales(self):
        self.client.get(
            f"{API_PREFIX}/sales",
            headers=self.headers,
            name="/api/sales",
        )

    @task(1)
    def get_sales_by_user(self):
        self.client.get(
            f"{API_PREFIX}/sales/user/{self.user_id}",
            headers=self.headers,
            name="/api/sales/user/{user_id}",
        )

    @task(1)
    def get_top_selling_recommendations(self):
        self.client.get(
            f"{API_PREFIX}/recommendations/top-selling",
            headers=self.headers,
            name="/api/recommendations/top-selling",
        )

    @task(1)
    def get_user_recommendations(self):
        self.client.get(
            f"{API_PREFIX}/recommendations/user",
            headers=self.headers,
            name="/api/recommendations/user",
        )

    @task(1)
    def get_total_sales_report(self):
        self.client.get(
            f"{API_PREFIX}/reports/total-sales",
            headers=self.headers,
            name="/api/reports/total-sales",
        )

    @task(1)
    def get_sales_by_product_report(self):
        self.client.get(
            f"{API_PREFIX}/reports/sales-by-product",
            headers=self.headers,
            name="/api/reports/sales-by-product",
        )

    @task(1)
    def get_stores(self):
        self.client.get(
            f"{API_PREFIX}/stores",
            headers=self.headers,
            name="/api/stores",
        )
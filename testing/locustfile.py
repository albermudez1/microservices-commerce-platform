from locust import HttpUser, task, between


class SalesProcessUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        login_payload = {
            "email": "test@example.com",
            "password": "password123"
        }

        response = self.client.post(
            "/api/login",
            json=login_payload,
            headers={"Accept": "application/json"},
            name="Login"
        )

        if response.status_code == 200:
            data = response.json()
            self.token = data.get("token")
        else:
            self.token = None

    @task
    def process_sale(self):
        if not self.token:
            return

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        payload = {
            "productId": 1,
            "quantity": 1
        }

        self.client.post(
            "/api/sales/process",
            json=payload,
            headers=headers,
            name="Process Sale"
        )
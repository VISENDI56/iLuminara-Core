from locust import HttpUser, task, between
import random

class iLuminaraSovereignUser(HttpUser):
    """
    Simulates high-concurrency traffic on the iLuminara-Core stack.
    """
    wait_time = between(1, 3)  # Realistic human delay

    @task(5)  # 5x more likely: Standard Health Queries
    def health_query(self):
        self.client.get("/", name="Home_Dashboard_Load")

    @task(2)  # Medium likelihood: Biosecurity Verification
    def rsa_verification(self):
        payload = {
            "query_id": f"TEST-{random.randint(1000,9999)}",
            "context": "Dadaab_Sector_4_Check"
        }
        # Simulating a call to the RSA/Nebius Bridge
        self.client.post("/?page=Technical_Specs", json=payload, name="RSA_Oracle_Bridge")

    @task(1)  # Rare: CLO Audit (Heavy Snowflake Query)
    def clo_audit(self):
        self.client.get("/?page=Legal_Fortress", name="Snowflake_Audit_Sync")
import snowflake.connector
import os
import json
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class SnowflakeSovereignFortress:
    """
    Invention #16: The Sovereign Data Fortress.
    Centralizes all 47-Law compliance data into a Time-Travel enabled warehouse.
    """
    def __init__(self):
        self.account = os.getenv("SNOWFLAKE_ACCOUNT")
        self.user = os.getenv("SNOWFLAKE_USER")
        self.password = os.getenv("SNOWFLAKE_PASSWORD")
        self.database = "ILUMINARA_SOVEREIGN_DB"
        self.schema = "GOVERNANCE_AUDIT"
        
        self.enabled = all([self.account, self.user, self.password])

    def get_connection(self):
        return snowflake.connector.connect(
            account=self.account,
            user=self.user,
            password=self.password,
            warehouse="COMPLIANCE_WH",
            database=self.database,
            schema=self.schema
        )

    def archive_sovereign_trace(self, receipt):
        """
        Pipes STBK (Invention #2) receipts into Snowflake.
        Ensures 100% auditability for Sheila Jelimo (CLO).
        """
        if not self.enabled:
            return "LOCAL_STORAGE_ONLY"

        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Create Audit Table if not exists (Sovereign Schema)
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.schema}.STBK_LEDGER (
                    TIMESTAMP TIMESTAMP_NTZ,
                    RECEIPT_ID STRING,
                    DECISION_TYPE STRING,
                    LEGAL_STATUTE STRING,
                    Z3_PROOF_ID STRING,
                    GEOSPATIAL_CELL STRING,
                    CLO_SIGNATURE STRING
                )
            """)

            # Insert the Receipt
            query = f"INSERT INTO {self.schema}.STBK_LEDGER VALUES (%s, %s, %s, %s, %s, %s, %s)"
            data = (
                datetime.now(),
                receipt['receipt_id'],
                receipt['packet']['decision'],
                receipt['packet']['legal_authority']['statute'],
                receipt['packet']['legal_authority']['proof_id'],
                receipt['packet']['origin_coordinate'],
                os.getenv("CLO_IDENTITY")
            )
        
            cursor.execute(query, data)
            conn.close()
            return "SUCCESS: ARCHIVED_IN_FORTRESS"
        except Exception as e:
            return f"ERROR: {str(e)}"

    def execute_sovereign_kill_switch(self):
        """
        The CLO's ultimate authority: Severs all cloud synchronization 
        if a jurisdictional breach is detected.
        """
        if not self.enabled: return False
        
        conn = self.get_connection()
        # Revokes all access to the Data Clean Rooms
        conn.cursor().execute("ALTER NETWORK POLICY SOVEREIGN_LOCK SET ALLOWED_IP_LIST = ('127.0.0.1')")
        conn.close()
        return "NETWORK_SEVERED_BY_CLO"

snowflake_fortress = SnowflakeSovereignFortress()
import os
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col

class UnistoreControlPlane:
    """
    Invention #17: The Unistore Control Plane.
    Using Hybrid Tables for sub-second Transactional Sovereignty.
    """
    def __init__(self):
        self.conn_params = {
            "account": os.getenv("SNOWFLAKE_ACCOUNT"),
            "user": os.getenv("SNOWFLAKE_USER"),
            "password": os.getenv("SNOWFLAKE_PASSWORD"),
            "warehouse": "COMPUTE_WH",
            "database": "ILUMINARA_SOVEREIGN_DB",
            "schema": "KERNEL_STATE"
        }

    def sync_node_state(self, node_id, status, pwr_consumption):
        """
        Transactional update of Node State using Hybrid Tables.
        Ensures strict referential integrity for the Ghost-Mesh.
        """
        session = Session.builder.configs(self.conn_params).create()
        
        # SQL for Hybrid Table (Unistore)
        # Note: HYBRID tables require a Primary Key for row-level locking
        session.sql(f"""
            CREATE HYBRID TABLE IF NOT EXISTS KERNEL_STATE.NODE_REGISTRY (
                NODE_ID STRING PRIMARY KEY,
                STATUS STRING,
                WATTAGE FLOAT,
                LAST_HEARTBEAT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
            )
        """).collect()

        # Upsert logic (Atomic Transaction)
        session.sql(f"""
            INSERT INTO KERNEL_STATE.NODE_REGISTRY (NODE_ID, STATUS, WATTAGE)
            VALUES ('{node_id}', '{status}', {pwr_consumption})
            ON CONFLICT (NODE_ID) DO UPDATE SET 
                STATUS = EXCLUDED.STATUS, 
                WATTAGE = EXCLUDED.WATTAGE,
                LAST_HEARTBEAT = CURRENT_TIMESTAMP()
        """).collect()
        
        session.close()
        return "NODE_STATE_SYNCHRONIZED_AT_EDGE"

unistore_kernel = UnistoreControlPlane()
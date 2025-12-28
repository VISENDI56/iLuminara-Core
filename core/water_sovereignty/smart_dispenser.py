class WaterATM:
    """
    IoT-triggered smart contract for equitable water distribution.
    """
    def dispense_water(self, user_zkp, liters):
        print(f"   [Water-ATM] Verifying ZKP for {liters}L dispense...")
        # Triggers ReFi payment to maintenance fund
        return {"valve_status": "OPEN", "transaction_hash": "H2O_TX_9982"}
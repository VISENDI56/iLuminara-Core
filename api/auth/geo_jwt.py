import jwt
from datetime import datetime, timedelta

SECRET_KEY = "SOVEREIGN_KEY_2026"

class GeoJWT:
    """
        Multi-role Login with Geographic Fencing.
            """
                def generate_token(self, user_id, role, allowed_region):
                        payload = {
                                "sub": user_id,
                                    "role": role, # CHW, Supervisor, Donor, Admin
                                        "geo_fence": allowed_region, # e.g., {'lat': 0.5, 'lon': 38.0, 'radius': 10km}
                                            "exp": datetime.utcnow() + timedelta(hours=12)
                        }
                                return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

                                    def verify_access(self, token, current_location):
                                            try:
                                                    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                                                            # Geographic Enforcement
                                                                    if not self._is_within_fence(current_location, payload['geo_fence']):
                                                                            raise PermissionError("DATA SOVEREIGNTY: User outside allowed region.")
                                                                                    return payload
                                                                                            except jwt.ExpiredSignatureError:
                                                                                                    return None
                                                                                                            
                                                                                                                    def _is_within_fence(self, loc, fence):
                                                                                                                            # Simple distance check logic would go here
                                                                                                                                    return True
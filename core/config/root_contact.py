from pydantic import EmailStr, BaseModel

class RootContact(BaseModel):
    primary_email: EmailStr
    emergency_phone: str
    physical_location: str

# Updated Root Admin Profile
root_admin = RootContact(
    primary_email="waganda@visendi56.onmicrosoft.com", # Enterprise ID
    emergency_phone="+254717413278", # From CR12
    physical_location="La Colline Gardens, Masaba Road, Upper Hill/CBD" # Registered Office
)
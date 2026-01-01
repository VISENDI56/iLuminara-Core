from core.config.corporate_identity import visendi_identity, get_legal_footer

def test_usa_identity():
    usa = visendi_identity.usa_entity
    assert usa.legal_name == "VISENDI56 LLC"
    assert usa.registration_number == "1387664800024"
    assert usa.tax_id == "92-3622772"
    print("✅ USA Corporate Identity Verified")

def test_kenya_identity():
    ke = visendi_identity.kenya_entity
    assert ke.legal_name == "VISENDI56 INVESTMENT LIMITED"
    assert ke.registration_number == "PVT-MKUMQYEX"
    assert ke.tax_id == "P052221589C"
    assert "The Billows" in ke.address.street
    print("✅ Kenya Corporate Identity Verified")

if __name__ == "__main__":
    test_usa_identity()
    test_kenya_identity()
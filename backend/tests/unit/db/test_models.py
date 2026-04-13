from db.models import Ecran, OfficeLicence, Ordinateur, User


class TestModelsCreation:
    def test_create_user(self, db_session):
        user = User(name="Test User", email="test@example.com")
        db_session.add(user)
        db_session.commit()

        retrieved = db_session.query(User).first()
        assert retrieved is not None
        assert retrieved.name == "Test User"

    def test_create_ordinateur(self, db_session):
        ordinateur = Ordinateur(type_pc="Desktop", marque="Dell")
        db_session.add(ordinateur)
        db_session.commit()

        retrieved = db_session.query(Ordinateur).first()
        assert retrieved is not None
        assert retrieved.type_pc == "Desktop"

    def test_create_ecran(self, db_session):
        ecran = Ecran(tag="ECRAN001", marque="LG")
        db_session.add(ecran)
        db_session.commit()

        retrieved = db_session.query(Ecran).first()
        assert retrieved is not None
        assert retrieved.tag == "ECRAN001"

    def test_create_office_license(self, db_session):
        license = OfficeLicence(version="Office 2021", type_license="Pro")
        db_session.add(license)
        db_session.commit()

        retrieved = db_session.query(OfficeLicence).first()
        assert retrieved is not None
        assert retrieved.version == "Office 2021"

from employee_management import db
from employee_management.asset.models import Asset


def setup():
    a1 = Asset(
        name="laptop"
    )
    a2 = Asset(
        name="mouse"
    )
    a3 = Asset(
        name="keyboard"
    )
    db.session.add_all([a1, a2, a3])
    db.session.commit()
    print("data entered in assets table")


if __name__ == '__main__':
    setup()

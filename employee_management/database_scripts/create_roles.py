from employee_management import db
from employee_management.employee.models import Role


def setup():
    r1 = Role(
        name="hr"
    )
    r2 = Role(
        name="ceo"
    )
    r3 = Role(
        name="developer"
    )
    db.session.add_all([r1, r2, r3])
    db.session.commit()
    print("data entered in roles table")


if __name__ == '__main__':
    setup()

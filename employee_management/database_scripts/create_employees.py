from employee_management import db
from employee_management.employee.models import Employee


def setup():
    emp1 = Employee(
        name="Paul John", email="pj@gmail.com"
    )
    emp2 = Employee(
        name="John Doe", email="JD@gmail.com"
    )
    emp3 = Employee(
        name="John Pop", email="JP@gmail.com"
    )
    db.session.add_all([emp1, emp2, emp3])
    db.session.commit()
    print("data entered in employees table")


if __name__ == '__main__':
    setup()

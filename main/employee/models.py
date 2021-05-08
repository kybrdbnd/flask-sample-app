from main import db, ma

# clear db metadata object
db.metadata.clear()


class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    email = db.Column(db.String())


class EmployeeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email')


employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)

if __name__ == "__main__":
    db.create_all()
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

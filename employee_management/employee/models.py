from employee_management import db, ma

# clear db metadata object
db.metadata.clear()


class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    email = db.Column(db.String())
    nameSlug = db.Column(db.String())

    def __init__(self, name, email):
        self.name = name
        self.email = email
        nameObjs = self.name.split(' ')
        nameObjs = list(map(lambda x: x.lower(), nameObjs))
        self.nameSlug = '-'.join(nameObjs)

    def __repr__(self):
        return f'<Employee> {self.name}'


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)

    def __repr__(self):
        return f'<Role> {self.name}'


if __name__ == "__main__":
    db.create_all()

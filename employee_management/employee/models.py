from employee_management import db

# clear db metadata object

db.metadata.clear()

employee_assets = db.Table('employee_assets',
                           db.Column('assetId', db.Integer, db.ForeignKey('assets.id'), primary_key=True),
                           db.Column('employeeId', db.Integer, db.ForeignKey('employees.id'), primary_key=True)
                           )

from employee_management.asset.models import Asset
from employee_management.role.models import Role


class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    email = db.Column(db.String())
    nameSlug = db.Column(db.String())
    roleId = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=True)
    assets = db.relationship('Asset', secondary=employee_assets, lazy='subquery',
                             backref=db.backref('employees', lazy=True))
    role = db.relationship('Role', backref=db.backref('employees', lazy=True))
    tempPassword = db.Column(db.String())

    def __init__(self, **kwargs):
        super(Employee, self).__init__(**kwargs)
        nameObjs = self.name.split(' ')
        nameObjs = list(map(lambda x: x.lower(), nameObjs))
        self.nameSlug = '-'.join(nameObjs)


def __repr__(self):
    return f'<Employee> {self.name}'


if __name__ == "__main__":
    db.create_all()

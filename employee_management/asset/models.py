from employee_management import db


class Asset(db.Model):
    __tablename__ = 'assets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)

    def __repr__(self):
        return self.name


if __name__ == "__main__":
    db.create_all()

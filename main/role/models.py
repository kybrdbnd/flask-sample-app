from main import db, ma

# clear db metadata object
db.metadata.clear()


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)

    def __repr__(self):
        return f'<Role> {self.name}'


class RoleSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')


role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)

if __name__ == "__main__":
    db.create_all()
    r1 = Role(name='HR')
    r2 = Role(name='CEO')
    r3 = Role(name='developer')
    db.session.add_all([r1, r2, r3])
    db.session.commit()

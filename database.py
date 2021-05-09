from flask_script import Manager, prompt_bool

from employee_management import db

manager = Manager(usage="Perform database operations")


@manager.command
def drop():
    "Drops database tables"
    if prompt_bool("Are you sure you want to lose all your data"):
        db.drop_all()


@manager.command
def create():
    "Creates database tables from sqlalchemy models"
    db.create_all()
    print("all database tables created successfully")
    populate()


@manager.command
def recreate():
    "Recreates database tables (same as issuing 'drop' and then 'create')"
    drop()
    create()


@manager.command
def populate(default_data=False, sample_data=False):
    "Populate database with default data"
    from employee_management.database_scripts import create_employees, create_roles
    create_employees.setup()
    create_roles.setup()

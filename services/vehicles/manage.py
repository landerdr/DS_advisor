from flask.cli import FlaskGroup
from project import create_app, db

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()

    # create standard types
    from project.api.models import VehicleType
    db.session.add(VehicleType(vehicle_type="Bus"))
    db.session.add(VehicleType(vehicle_type="Metro"))

    db.session.commit()


if __name__ == "__main__":
    cli()

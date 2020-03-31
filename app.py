from mobilXpertenApp import create_app, db
from mobilXpertenApp.models import User, Device, Repair


def repopulate_db(app):
    with app.app_context():
        db.create_all()
        print("Deleting all old devices")
        Device.query.delete()
        print("Deleting all old repairs")
        Repair.query.delete()
        print("Deleting all old Users")
        User.query.delete()

        print("Initalizing new data...")
        u = User(username="Jimmie", email="jimmie@sd.se")
        db.session.add(u)

        for m in ['5', '5s', '6', '6+' , '6s', '7' , '7+', '8', '8+', 'X' , 'Xs', 'Xr', '11']:
            d = Device(brand="Apple", model="iPhone "+m)
            db.session.add(d)
            for r in ['Screen', 'Battery', 'Backside', 'Charge port']:
                r = Repair(name=r+" Replacement", price=695, estimated_time=3, device=d)
                db.session.add(r)

        # Samsung
        for m in ['s6', 's7', 's7 edge', 's8' , 's9', 's10' , 's20']:
            d = Device(brand="Samsung", model="Galaxy "+m)
            db.session.add(d)
            for r in ['Screen', 'Battery', 'Backside', 'Charge port']:
                r = Repair(name=r+" Replacement", price=695, estimated_time=24, device=d)
                db.session.add(r)

        print("User", User.query.all())
        for d in Device.query.all():
            print(d)
            for r in d.repairs:
                print("    ", r)
        
        print("Data Initalized.")
        # Save changes
        db.session.commit()


app = create_app()
repopulate_db(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Device': Device, 'Repair': Repair}

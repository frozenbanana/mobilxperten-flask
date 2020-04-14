from mobilXpertenApp import create_app, db
from mobilXpertenApp.models import User, Device, Repair
from random import randrange

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
        u.set_password("123")
        db.session.add(u)

        for m in ['5', '5s', '6', '6+' , '6s', '7' , '7+', '8', '8+', 'X' , 'Xs', 'Xr', '11']:
            d = Device(brand="Apple", model="iPhone "+m, type="smartphone")
            db.session.add(d)
            for r in ['Screen', 'Battery', 'Backside', 'Charge port']:
                r = Repair(name=r+" Replacement", price=randrange(695,1995, 100), estimated_time=3, device=d)
                db.session.add(r)

        for m in ['Pro', 'Mini', 'Air', 'Air 2']:
            d = Device(brand="Apple", model="iPad "+m, type="tablet")
            for r in ['Screen', 'Battery', 'Backside', 'Charge port']:
                r = Repair(name=r+" Replacement", price=randrange(695,1995, 100), estimated_time=72, device=d)
                db.session.add(r)
        
        # Samsung
        for m in ['S6', 'S7', 'S7 edge', 'S8' , 'S9', 'S10' , 'S20']:
            d = Device(brand="Samsung", model="Galaxy "+m, type="smartphone")
            db.session.add(d)
            for r in ['Screen', 'Battery', 'Backside', 'Charge port']:
                r = Repair(name=r+" Replacement", price=randrange(695,1995, 100), estimated_time=24, device=d)
                db.session.add(r)
        
        for m in ['S4', 'S5e', 'S6']:
            d = Device(brand="Samsung", model="Galaxy Tab "+m, type="tablet")
            db.session.add(d)
            for r in ['Screen', 'Battery', 'Backside', 'Charge port']:
                r = Repair(name=r+" Replacement", price=randrange(695,1995, 100), estimated_time=72, device=d)
                db.session.add(r)

        print("Data Initalized.")
        # Save changes
        db.session.commit()


app = create_app()
repopulate_db(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Device': Device, 'Repair': Repair}

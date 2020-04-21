from mobilXpertenApp import create_app, db
from mobilXpertenApp.models import User, RepairDevice, Repair, SaleDevice, SaleInfo
from random import randrange, choice

def repopulate_db(app):
    with app.app_context():
        db.create_all()
        print("Deleting all old RepairDevices")
        RepairDevice.query.delete()
        print("Deleting all old repairs")
        Repair.query.delete()
        print("Deleting all old SaleDevices")
        SaleDevice.query.delete()
        print("Deleting all old SaleInfo")
        SaleInfo.query.delete()
        print("Deleting all old Users")
        User.query.delete()

        print("Initalizing new data...")
        u = User(username="Jimmie", email="jimmie@sd.se")
        u.set_password("123")
        db.session.add(u)

        # Sales Items
        sale_repairs = []
        for i in range(3):
            models = ['6s', '7' , '7+']
            si = SaleInfo(memory_capacity=randrange(16,64, 16), imei_number=123123678678, grade=randrange(0,4), color=choice(['black', 'white']), price_in=randrange(800, 1800, 100), price_out=randrange(1600, 2800, 100))
            # add repairs done to sales info
            for r in ['Screen', 'Battery']:
                Repair(name=r+" Replacement", price=randrange(695,1995, 100), estimated_time=72, sale_info=si)     
            # add sales info to device being sold  
            d = SaleDevice(brand="Apple", model="iPhone "+models[i], typeOf="smartphone", sale_info=si)
            db.session.add(d)

        for m in ['5', '5s', '6', '6+' , '6s', '7' , '7+', '8', '8+', 'X' , 'Xs', 'Xr', '11']:
            d = RepairDevice(brand="Apple", model="iPhone "+m, typeOf="smartphone")
            db.session.add(d)
            for r in ['Screen', 'Battery', 'Backside', 'Charge port']:
                r = Repair(name=r+" Replacement", price=randrange(695,1995, 100), estimated_time=3, device=d)
                db.session.add(r)

        for m in ['Pro', 'Mini', 'Air', 'Air 2']:
            d = RepairDevice(brand="Apple", model="iPad "+m, typeOf="tablet")
            for r in ['Screen', 'Battery', 'Backside', 'Charge port']:
                r = Repair(name=r+" Replacement", price=randrange(695,1995, 100), estimated_time=72, device=d)
                db.session.add(r)
        
        # Samsung
        for m in ['S6', 'S7', 'S7 edge', 'S8' , 'S9', 'S10' , 'S20']:
            d = RepairDevice(brand="Samsung", model="Galaxy "+m, typeOf="smartphone")
            db.session.add(d)
            for r in ['Screen', 'Battery', 'Backside', 'Charge port']:
                r = Repair(name=r+" Replacement", price=randrange(695,1995, 100), estimated_time=24, device=d)
                db.session.add(r)
        
        for m in ['S4', 'S5e', 'S6']:
            d = RepairDevice(brand="Samsung", model="Galaxy Tab "+m, typeOf="tablet")
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
    return {'es': app.elasticsearch, 'app': app, 'repopulate_db': repopulate_db,'db': db, 'User': User, 'RepairDevice': RepairDevice, 'Repair': Repair, 'SaleDevice': SaleDevice,'SaleInfo': SaleInfo}

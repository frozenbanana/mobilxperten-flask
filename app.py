from mobilXpertenApp import app, db
from mobilXpertenApp.models import Device, Repair
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Device': Device, 'Repair': Repair}


def populate_db():
    # Apple
    for m in ['5', '5s', '6', '6+' , '6s', '7' , '7+', '8', '8+', 'X' , 'Xs', 'Xr', '11']:
        device = Device(brand="Apple", model="iPhone "+m)
        db.session.add(device)
        for r in ['Screen', 'Battery', 'Backside', 'Charge port']:
            r = Repair(name=r+" Replacement", price=695, estimated_time=3, device=device)
            db.session.add(r)

    # Samsung
    for m in ['s6', 's7', 's7 edge', 's8' , 's9', 's10' , 's20']:
        device = Device(brand="Samsung", model="Galaxy "+m)
        db.session.add(device)
        for r in ['Screen', 'Battery', 'Backside', 'Charge port']:
            r = Repair(name=r+" Replacement", price=695, estimated_time=24, device=device)
            db.session.add(r)

    # Save changes
    db.session.commit()

def reset_db():
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print 'Clear table %s' % table
        db.session.execute(table.delete())
    db.session.commit()
reset_db()
populate_db()
from mobilXpertenApp.api import bp
from mobilXpertenApp.api.errors import bad_request
from mobilXpertenApp.models import Device, Repair
from flask import request, jsonify



@bp.route('/devices/<int:id>', methods=['GET'])
def get_device(id):
    device = Device.query.get_or_404(id, description='There is no data with id {}'.format(id))
    response = device.to_dict()
    return jsonify(response)


@bp.route('/devices', methods=['GET'])
def get_devices():
    devices = Device.query.limit(100).all()
    response = [d.to_dict() for d in devices]
    return jsonify(response)

@bp.route('/devices/<int:id>/repairs', methods=['GET'])
def get_device_repairs(id):
    device = Device.query.get_or_404(id, description='There is no data with id {}'.format(id))
    repairs = device.repairs
    response = [r.to_dict() for r in repairs]
    return jsonify(response)

@bp.route('/devices', methods=['POST'])
def create_device():
    data = request.get_json() or {}
    if 'model' not in data or 'brand' not in data:
        return bad_request('must include model and brand fields')
    if Device.query.filter_by(username=data['model']).first():
        return bad_request('modelplease use a different username')
    device = Device()
    device.from_dict(data, new_device=True)
    db.session.add(device)
    db.session.commit()
    response = device.to_dict()
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_device', id=device.id)
    return jsonify(response)


@bp.route('/devices/<int:id>', methods=['PUT'])
def update_device(id):
    device = Device.query.get_or_404(id)
    data = request.get_json() or {}
    if 'model' in data and data['model'] != device.model and \
            Device.query.filter_by(model=data['model']).first():
        return bad_request('please use a different model')

    device.from_dict(data, new_device=False)
    db.session.commit()
    response = device.to_dict()
    return jsonify(response)

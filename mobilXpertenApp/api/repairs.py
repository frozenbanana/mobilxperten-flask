from mobilXpertenApp.api import bp
from mobilXpertenApp.models import RepairDevice, Repair
from flask import request, jsonify


@bp.route('/repairs', methods=['GET'])
def get_repairs():
    repairs = Repair.query.limit(100).all()
    response = [r.to_dict() for r in repairs]
    return jsonify(response)

@bp.route('/repairs/<int:id>', methods=['GET'])
def get_repair(id):
    repair = Repair.query.get_or_404(id, description='There is no data with id {}'.format(id))
    response = repair.to_dict()
    return jsonify(response)

@bp.route('/repairs', methods=['POST'])
def create_repair():
    data = request.get_json() or {}
    if 'name' not in data or  \
       'price' not in data or \
       'estimated_time' not in data:
        return bad_request('must include name, price and estimated_time fields')
    repair = repair()
    repair.from_dict(data, new_repair=True)
    db.session.add(repair)
    db.session.commit()
    response = repair.to_dict()
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_repair', id=repair.id)
    return jsonify(response)


@bp.route('/repairs', methods=['PUT'])
def update_repair(id):
    repair = RepairDevice.query.get_or_404(id)
    data = request.get_json() or {}
    repair.from_dict(data, new_device=False)
    db.session.commit()
    response = repair.to_dict()
    return jsonify(response)

from flask import jsonify, request, url_for, session
from flask_login import login_required
from volunteercore import db
from datetime import datetime
from volunteercore.api import bp
from volunteercore.volops.models import Hours
from volunteercore.api.errors import bad_request
from volunteercore.decorators import requires_roles

# API GET endpoint returns individuals total hours
@bp.route('/api/admin/hours/total/<int:id>', methods=['GET'])
@login_required
@requires_roles('Admin')
def admin_get_total_hours_api(id):
    #TODO dont have this be a oneliner
    data = [x.month_hours for x in Hours.query.filter_by(user_id = id).all() if x.month_hours != None]
    dic = {"hours":sum(data),"user_id":id}
    return jsonify(dic), 200

# API GET endpoint returns individuals hours for a given month
@bp.route('/api/admin/hours/<string:month>/<int:id>',methods=['GET'])
@login_required
@requires_roles('Admin')
def admin_get_month_hours_api(id,month):
    data = Hours.query.filter_by(user_id = id, datetime = month).first()
    if data == None:
        return bad_request('this entry does not exist')
    return jsonify(data.to_dict()),200

# API PUT endpoint to manually modify an individuals hours
#TODO this needs work
@bp.route('/api/admin/hours/put', methods=['PUT'])
@login_required
@requires_roles('Admin')
def admin_create_hours_api():
    hours = Hours()
    data = request.get_json() or {}
    if data == {}:
        return bad_request('please supply valid json')
    hours.from_dict(data)
    db.session.add(hours)
    db.session.commit()
    return jsonify(hours.to_dict())

# API DELETE endpoint to delete an individual hours by id and month
@bp.route('/api/admin/hours/<string:month>/<int:id>', methods=['DELETE'])
@login_required
@requires_roles('Admin')
def admin_delete_hours_api(id, month):
    data = Hours.query.filter_by(user_id = id, datetime = month).first()
    if data == None:
        return bad_request("this entry does not exist")
    hours = Hours.query.get_or_404(id)
    db.session.delete(hours)
    db.session.commit()
    return 'deleted',204

# API POST endpoint to add to an individuals hours
# for the current month and current logged in user
# TODO add some verification that the user actually
# put in the hours
@bp.route('/api/hours/month/<float:hours>',methods=['POST'])
@login_required
def update_month_hours_api(hours):
    #This should be fine, cookies are secure in flask presumably with HMAC or signing.
    #should probably verify this though.
    id = session['user_id']
    month = datetime.now().strftime("%Y-%m")
    data = Hours.query.filter_by(user_id = id, datetime = month).first()
    #If our entry does not exist, create one
    if data == None:
        data = Hours(user_id = id, datetime = month, month_hours = 0)
        db.session.add(data)
    # TODO race contidion? 
    data.month_hours += hours
    db.session.commit()
    return jsonify(data.to_dict()),200

# API GET endpoint returns individuals total hours
@bp.route('/api/hours/total', methods=['GET'])
@login_required
def get_total_hours_api():
    id = session['user_id']
    #TODO dont have this be a oneliner
    data = [x.month_hours for x in Hours.query.filter_by(user_id = id).all() if x.month_hours != None]
    if data == None:
        return bad_request("this entry does not exist")
    dic = {"month_hours":sum(data),"user_id":id}
    return jsonify(dic), 200

# API GET endpoint returns individuals current month hours
@bp.route('/api/hours/month', methods=['GET'])
@login_required
def get_month_hours_api():
    id = session['user_id']
    month = datetime.now().strftime("%Y-%m")
    data = Hours.query.filter_by(user_id = id, datetime= month).first()
    if data == None:
        return bad_request("this entry does not exist")
    dic = {"month_hours":data.month_hours,"user_id":id, "datetime":month}
    return jsonify(dic), 200

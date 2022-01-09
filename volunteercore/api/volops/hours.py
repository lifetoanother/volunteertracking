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
    data = [x.hours for x in Hours.query.filter_by(user_id = id).all() if x.hours != None]
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

# API POST endpoint to add to an individuals hours
# for the current month and current logged in user
@bp.route('/api/hours/month',methods=['POST'])
@login_required
def update_month_hours_api():
    #TODO handle if bad data is sent
    data = request.get_json() or {}
    if data == {}:
        return bad_request('please supply valid json')
    id = session['user_id']
    month = datetime.now().strftime("%Y-%m")
    hours = data['hours']
    description = data['description']
    entry = Hours(user_id = id, datetime = month, hours = hours, description = description)
    db.session.add(entry)
    db.session.commit()
    return jsonify(entry.to_dict()),200

# API GET endpoint returns individuals total hours
@bp.route('/api/hours/total', methods=['GET'])
@login_required
def get_total_hours_api():
    id = session['user_id']
    #TODO dont have this be a oneliner
    data = [x.hours for x in Hours.query.filter_by(user_id = id).all() if x.hours != None]
    if data == None:
        return bad_request("this entry does not exist")
    dic = {"month_hours":sum(data),"user_id":id}
    return jsonify(dic), 200

# API GET endpoint returns individuals current month hours
# TODO add a way to check past months
@bp.route('/api/hours/month', methods=['GET'])
@login_required
def get_month_hours_api():
    id = session['user_id']
    month = datetime.now().strftime("%Y-%m")
    data = Hours.query.filter_by(user_id = id, datetime = month).all()
    if data == None:
        return bad_request("this entry does not exist")
    data = [x.hours for x in data if x.hours != None]
    dic = {"month_hours":sum(data),"user_id":id, "datetime":month}
    return jsonify(dic), 200

from flask import jsonify, request, url_for
from flask_login import login_required
from volunteercore import db
from volunteercore.api import bp
from volunteercore.volops.models import Opportunity
from volunteercore.api.errors import bad_request
from flask_whooshalchemyplus import index_one_record

# API GET endpoint returns individual opportunity from given id
@bp.route('/api/opportunities/<int:id>', methods=['GET'])
@login_required
def get_opportunity_api(id):
    return jsonify(Opportunity.query.get_or_404(id).to_dict())

# API GET endpoint returns all opportunities, paginated with given page and
# quantity per page. Accepts search argument to filter with Whoosh search.
@bp.route('/api/opportunities', methods=['GET'])
@login_required
def get_opportunities_api():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    search = request.args.get('search')

    if search:
        data = Opportunity.query.whoosh_search(search, or_=True)
    else:
        data = Opportunity.query
    data = Opportunity.to_colletion_dict(
            data, page, per_page, 'api.get_opportunities_api')
    return jsonify(data)

# API PUT endpoint to update an opportunity
@bp.route('/api/opportunities/<int:id>', methods=['PUT'])
@login_required
def update_opportunity_api(id):
    opportunity = Opportunity.query.get_or_404(id)
    data = request.get_json() or {}
    opportunity.from_dict(data, new_opportunity=False)
    opportunity.update_tag_strings()
    db.session.add(opportunity)
    db.session.commit()
    index_one_record(opportunity)
    return jsonify(opportunity.to_dict())

# API POST endpoint to create a new opportunity
@bp.route('/api/opportunities', methods=['POST'])
@login_required
def create_opportunity_api():
    data = request.get_json() or {}
    if 'name' not in data:
        return bad_request('must include opportunity name field')
    opportunity = Opportunity()
    opportunity.from_dict(data, new_opportunity=True)
    db.session.add(opportunity)
    db.session.commit()
    index_one_record(opportunity)
    response = jsonify(opportunity.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for(
        'api.get_opportunity_api', id=opportunity.id)
    return response

# API DELETE endpoint to delete an opportunity
@bp.route('/api/opportunities/<int:id>', methods=['DELETE'])
@login_required
def delete_opportunity_api(id):
    if not Opportunity.query.filter_by(id=id).first():
        return bad_request('this opportunity does not exist')
    opportunity = Opportunity.query.get_or_404(id)
    db.session.delete(opportunity)
    db.session.commit()
    index_one_record(opportunity, delete=True)
    return '', 204

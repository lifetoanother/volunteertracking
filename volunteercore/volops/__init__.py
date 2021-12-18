from flask import Blueprint

bp = Blueprint('volops', __name__)

from volunteercore.volops.models import Opportunity, \
    TagCategory, Tag, Hours

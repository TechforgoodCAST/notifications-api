from flask import Blueprint, jsonify

from app.dao.organisation_dao import dao_count_organisations_with_live_services
from app.dao.services_dao import dao_count_live_services

status = Blueprint('status', __name__)


@status.route('/', methods=['GET'])
@status.route('/_status', methods=['GET', 'POST'])
def show_status():
    return jsonify(status="ok"), 200


@status.route('/_status/live-service-and-organisation-counts')
def live_service_and_organisation_counts():
    return jsonify(
        organisations=dao_count_organisations_with_live_services(),
        services=dao_count_live_services(),
    ), 200

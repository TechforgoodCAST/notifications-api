from flask import Blueprint, current_app, jsonify, request

from app.config import QueueNames
from app.dao.templates_dao import dao_get_template_by_id
from app.errors import register_errors
from app.models import EMAIL_TYPE, KEY_TYPE_NORMAL
from app.notifications.process_notifications import (
    persist_notification,
    send_notification_to_queue,
)
from app.utils import get_or_build_support_email_address

feedbacks_blueprint = Blueprint('feedbacks', __name__, url_prefix='/feedbacks')
register_errors(feedbacks_blueprint)


@feedbacks_blueprint.route('', methods=['POST'])
def create_feedback():
    data = request.get_json()
    template = dao_get_template_by_id(current_app.config['NEW_SUPPORT_REQUEST'])

    saved_notification = persist_notification(
        template_id=template.id,
        template_version=template.version,
        recipient=get_or_build_support_email_address(),
        service=template.service,
        personalisation={
            'message': data['message'],
            'name': data['name'],
            'email': data['email']
        },
        notification_type=EMAIL_TYPE,
        api_key_id=None,
        key_type=KEY_TYPE_NORMAL,
        reply_to_text=get_or_build_support_email_address()
    )
    send_notification_to_queue(saved_notification, research_mode=False, queue=QueueNames.NOTIFY)

    return jsonify(data={'id': saved_notification.id}), 201

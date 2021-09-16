import uuid

import pytest
from flask import current_app, json
from freezegun import freeze_time
from notifications_utils.url_safe_token import generate_token

from tests import create_authorization_header


@pytest.mark.parametrize('invitation_type', ['service', 'organisation'])
def test_validate_invitation_token_for_expired_token_returns_400(client, invitation_type):
    with freeze_time('2016-01-01T12:00:00'):
        token = generate_token(str(uuid.uuid4()), current_app.config['SECRET_KEY'],
                               current_app.config['DANGEROUS_SALT'])
    url = '/invite/{}/{}'.format(invitation_type, token)
    auth_header = create_authorization_header()
    response = client.get(url, headers=[('Content-Type', 'application/json'), auth_header])

    assert response.status_code == 400
    json_resp = json.loads(response.get_data(as_text=True))
    assert json_resp['result'] == 'error'
    assert json_resp['message'] == {
        'invitation': 'Your invitation to Catalyst Notify has expired. '
                      'Please ask the person that invited you to send you another one'}


@pytest.mark.parametrize('invitation_type', ['service', 'organisation'])
def test_validate_invitation_token_returns_200_when_token_valid(
        client, invitation_type, sample_invited_user, sample_invited_org_user
):
    invited_user = sample_invited_user if invitation_type == 'service' else sample_invited_org_user

    token = generate_token(str(invited_user.id), current_app.config['SECRET_KEY'],
                           current_app.config['DANGEROUS_SALT'])
    url = '/invite/{}/{}'.format(invitation_type, token)
    auth_header = create_authorization_header()
    response = client.get(url, headers=[('Content-Type', 'application/json'), auth_header])

    assert response.status_code == 200
    json_resp = json.loads(response.get_data(as_text=True))
    if invitation_type == 'service':
        assert json_resp['data']['id'] == str(sample_invited_user.id)
        assert json_resp['data']['email_address'] == sample_invited_user.email_address
        assert json_resp['data']['from_user'] == str(sample_invited_user.user_id)
        assert json_resp['data']['service'] == str(sample_invited_user.service_id)
        assert json_resp['data']['status'] == sample_invited_user.status
        assert json_resp['data']['permissions'] == sample_invited_user.permissions
        assert json_resp['data']['folder_permissions'] == sample_invited_user.folder_permissions
    if invitation_type == 'organisation':
        assert json_resp['data'] == sample_invited_org_user.serialize()


@pytest.mark.parametrize('invitation_type', ['service', 'organisation'])
def test_validate_invitation_token_returns_400_when_invited_user_does_not_exist(client, invitation_type):
    token = generate_token(str(uuid.uuid4()), current_app.config['SECRET_KEY'],
                           current_app.config['DANGEROUS_SALT'])
    url = '/invite/{}/{}'.format(invitation_type, token)
    auth_header = create_authorization_header()
    response = client.get(url, headers=[('Content-Type', 'application/json'), auth_header])

    assert response.status_code == 404
    json_resp = json.loads(response.get_data(as_text=True))
    assert json_resp['result'] == 'error'
    assert json_resp['message'] == 'No result found'


@pytest.mark.parametrize('invitation_type', ['service', 'organisation'])
def test_validate_invitation_token_returns_400_when_token_is_malformed(client, invitation_type):
    token = generate_token(
        str(uuid.uuid4()),
        current_app.config['SECRET_KEY'],
        current_app.config['DANGEROUS_SALT']
    )[:-2]

    url = '/invite/{}/{}'.format(invitation_type, token)
    auth_header = create_authorization_header()
    response = client.get(url, headers=[('Content-Type', 'application/json'), auth_header])

    assert response.status_code == 400
    json_resp = json.loads(response.get_data(as_text=True))
    assert json_resp['result'] == 'error'
    assert json_resp['message'] == {
        'invitation': 'Something’s wrong with this link. Make sure you’ve copied the whole thing.'
    }


def test_get_invited_user(admin_request, sample_invited_user):
    json_resp = admin_request.get(
        'global_invite.get_invited_user',
        invited_user_id=sample_invited_user.id
    )
    assert json_resp['data']['id'] == str(sample_invited_user.id)
    assert json_resp['data']['email_address'] == sample_invited_user.email_address
    assert json_resp['data']['service'] == str(sample_invited_user.service_id)
    assert json_resp['data']['permissions'] == sample_invited_user.permissions


def test_get_invited_user_404s_if_invite_doesnt_exist(admin_request, sample_invited_user, fake_uuid):
    json_resp = admin_request.get(
        'global_invite.get_invited_user',
        invited_user_id=fake_uuid,
        _expected_status=404
    )
    assert json_resp['result'] == 'error'


def test_get_invited_org_user(admin_request, sample_invited_org_user):
    json_resp = admin_request.get(
        'global_invite.get_invited_org_user',
        invited_org_user_id=sample_invited_org_user.id
    )
    assert json_resp['data']['id'] == str(sample_invited_org_user.id)
    assert json_resp['data']['email_address'] == sample_invited_org_user.email_address
    assert json_resp['data']['organisation'] == str(sample_invited_org_user.organisation_id)


def test_get_invited_org_user_404s_if_invite_doesnt_exist(admin_request, sample_invited_org_user, fake_uuid):
    json_resp = admin_request.get(
        'global_invite.get_invited_org_user',
        invited_org_user_id=fake_uuid,
        _expected_status=404
    )
    assert json_resp['result'] == 'error'

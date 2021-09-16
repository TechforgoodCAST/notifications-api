import json
from time import monotonic
from urllib.parse import urljoin

from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

from app.clients.sms import SmsClient, SmsClientResponseException


def get_twilio_responses(status, detailed_status_code=None):
    # Twilio send meaningful strings in their callbacks so there's no translation required
    return status, None


class TwilioUtils:

    @staticmethod
    def get_error_from_code(error_code):
        with open('app/clients/sms/twilio_error_codes.json') as f:
            error_mappings = json.load(f)
            return error_mappings.get(str(error_code), None)

    @staticmethod
    def format_number_for_twilio(number):
        return '+' + number


class TwilioClientResponseException(SmsClientResponseException):
    def __init__(self, response, exception):
        response_json = json.loads(response.content)
        error_code = response_json.get('code', None)
        error = TwilioUtils.get_error_from_code(error_code)

        self.status_code = response.status_code
        self.text = error.get('message')
        self.exception = exception

    def __str__(self):
        return "Code {} text {} exception {}".format(self.status_code, self.text, str(self.exception))


class TwilioClient(SmsClient):
    """
    Twilio SMS client.
    """

    def init_app(self, current_app, statsd_client, *args, **kwargs):
        super(SmsClient, self).__init__(*args, **kwargs)
        self.current_app = current_app
        self.twilio_sid = current_app.config.get('TWILIO_SID')
        self.twilio_auth_token = current_app.config.get('TWILIO_AUTH_TOKEN')
        self.from_number = current_app.config.get('FROM_NUMBER')
        self.hostname = current_app.config.get('API_HOST_NAME')
        self.name = 'twilio'
        self.statsd_client = statsd_client

    def get_name(self):
        return self.name

    def record_outcome(self, response):
        response_json = json.loads(response.content)
        status_code = response.status_code
        error_code = response_json.get('code', None)

        if error_code:
            error = TwilioUtils.get_error_from_code(error_code)
            self.statsd_client.incr("clients.twilio.error")
            log_message = "Received {} response from Twilio. Error {} ({})".format(status_code,
                                                                                   error_code,
                                                                                   error.get('message'))
        else:
            self.statsd_client.incr("clients.twilio.success")
            log_message = "Received {} from Twilio API.".format(status_code)

        self.current_app.logger.info(log_message)

    def send_sms(self, to, content, reference=None, sender=None):
        client = Client(self.twilio_sid, self.twilio_auth_token)
        start_time = monotonic()

        try:
            client.messages.create(
                to=TwilioUtils.format_number_for_twilio(to),
                from_=self.from_number if sender is None else sender,
                body=content,
                status_callback=urljoin(self.hostname, 'notifications/sms/twilio')
            )
        except TwilioRestException as exception:
            response = client.http_client.last_response
            raise TwilioClientResponseException(response=response, exception=exception)
        finally:
            response = client.http_client.last_response
            self.record_outcome(response)

            elapsed_time = monotonic() - start_time
            self.current_app.logger.info("Twilio request finished in {}".format(elapsed_time))
            self.statsd_client.timing("clients.twilio.request-time", elapsed_time)
            twilio_request_duration = response.headers.get('Twilio-Request-Duration')
            self.statsd_client.timing("clients.twilio.raw-request-time", twilio_request_duration)

        return response

import glob
import json
from jsonschema import validate
import os
import requests
from requests.auth import HTTPBasicAuth


schema_files = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'json_schemas/*.schema.json')
# [:-12] to remove .schema.json
name_to_schema = {
    os.path.basename(schema_file)[:-12]: json.load(open(schema_file))
    for schema_file in glob.glob(schema_files)}


class TangoAPIClient(object):

    def __init__(self, user, password):
        self.endpoint = 'https://sandbox.tangocard.com'
        self.auth = HTTPBasicAuth(user, password)

    def _handle_errors(self, uri, response_json, data=None):
        if not response_json['success']:
            msg = ("Tango API Error: uri=%s, data=%s, response=%s"
                   % (uri, data, response_json))
            raise Exception(msg)

    def _request_get_json(self, uri):
        response = requests.get(self.endpoint + uri, auth=self.auth)
        response_json = response.json()
        self._handle_errors(uri, response_json)
        return response_json

    def _request_post_json(self, uri, data=None):
        response = requests.post(self.endpoint + uri,
                                 auth=self.auth,
                                 data=json.dumps(data))
        response_json = response.json()
        self._handle_errors(uri, response_json, data=data)
        return response_json

    def create_account(self, customer, identifier, email):
        data = {
            'customer': customer,
            'identifier': identifier,
            'email': email,
        }
        schema = name_to_schema['account_create']
        validate(data, schema)
        return self._request_post_json('/raas/v1/accounts', data=data)

    def get_account(self, customer, identifier):
        return self._request_get_json(
            '/raas/v1/accounts/%s/%s' % (customer, identifier))

    def get_rewards(self):
        return self._request_get_json('/raas/v1/rewards')

    def register_credit_card(self, customer, identifier, client_ip, card_data):
        data = {
            'customer': customer,
            'account_identifier': identifier,
            'client_ip': client_ip,
            'credit_card': card_data,
        }
        schema = name_to_schema['cc_register']
        validate(data, schema)
        return self._request_post_json('/raas/v1/cc_register', data=data)

    def fund_account(self, customer, identifier, amount, client_ip,
                     security_code, cc_token):
        data = {
            'customer': customer,
            'account_identifier': identifier,
            'client_ip': client_ip,
            'amount': amount,
            'client_ip': client_ip,
            'security_code': security_code,
            'cc_token': cc_token,
        }
        schema = name_to_schema['cc_fund']
        validate(data, schema)
        return self._request_post_json('/raas/v1/cc_fund', data=data)

    def place_order(self, customer, identifier,
                    recipient_name, recipient_email, sku, amount,
                    reward_message, reward_subject, reward_from):
        data = {
            'customer': customer,
            'account_identifier': identifier,
            'recipient': {
                'name': recipient_name,
                'email': recipient_email,
            },
            'sku': sku,
            'amount': amount,
            'reward_message': reward_message,
            'reward_subject': reward_subject,
            'reward_from': reward_from,
        }
        schema = name_to_schema['order_create']
        validate(data, schema)
        return self._request_post_json('/raas/v1/orders', data=data)

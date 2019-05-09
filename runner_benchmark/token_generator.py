import os
import time
from uuid import uuid4

from sdc.crypto.encrypter import encrypt
from sdc.crypto.key_store import KeyStore

KEY_PURPOSE_AUTHENTICATION = 'authentication'


EQ_USER_AUTHENTICATION_RRM_PRIVATE_KEY_KID = '709eb42cfee5570058ce0711f730bfbb7d4c8ade'
SR_USER_AUTHENTICATION_PUBLIC_KEY_KID = 'e19091072f920cbf3ca9f436ceba309e7d814a62'

KEYS_FOLDER = './jwt-test-keys'


def get_file_contents(filename, trim=False):
    with open(os.path.join(KEYS_FOLDER, filename), 'r') as f:
        data = f.read()
        if trim:
            data = data.rstrip('\r\n')
    return data


_key_store = KeyStore({
    'keys': {
        EQ_USER_AUTHENTICATION_RRM_PRIVATE_KEY_KID: {
            'purpose': KEY_PURPOSE_AUTHENTICATION,
            'type': 'private',
            'value': get_file_contents('sdc-user-authentication-signing-rrm-private-key.pem')},
        SR_USER_AUTHENTICATION_PUBLIC_KEY_KID: {
            'purpose': KEY_PURPOSE_AUTHENTICATION,
            'type': 'public',
            'value': get_file_contents('sdc-user-authentication-encryption-sr-public-key.pem')},
    }
})


def _get_payload_with_params(form_type_id, eq_id, survey_url=None, **extra_payload):
    payload_vars = {
        'user_id': 'integration-test',
        'period_str': 'April 2016',
        'period_id': '201604',
        'collection_exercise_sid': str(uuid4()),
        'ru_ref': '123456789012A',
        'response_id': str(uuid4()),
        'case_id': str(uuid4()),
        'ru_name': 'Integration Testing',
        'ref_p_start_date': '2016-04-01',
        'ref_p_end_date': '2016-04-30',
        'return_by': '2016-05-06',
        'trad_as': 'Integration Tests',
        'employment_date': '1983-06-02',
        'variant_flags': None,
        'region_code': 'GB-ENG',
        'language_code': 'en',
        'sexual_identity': False,
        'roles': [],
        'tx_id': str(uuid4()),
        'eq_id': eq_id,
        'form_type': form_type_id,
        'iat': time.time(),
        'exp': time.time() + float(3600),  # one hour from now
        'jti': str(uuid4())
    }

    if survey_url:
        payload_vars['survey_url'] = survey_url

    for key, value in extra_payload.items():
        payload_vars[key] = value

    return payload_vars


def create_token(form_type_id, eq_id, **extra_payload):
    payload_vars = _get_payload_with_params(form_type_id, eq_id, None, **extra_payload)

    return generate_token(payload_vars)


def generate_token(payload):
    return encrypt(payload, _key_store, KEY_PURPOSE_AUTHENTICATION)

import os
import time
from uuid import uuid4

from sdc.crypto.encrypter import encrypt
from sdc.crypto.key_store import KeyStore

KEY_PURPOSE_AUTHENTICATION = 'authentication'

EQ_USER_AUTHENTICATION_RRM_PRIVATE_KEY_KID = '709eb42cfee5570058ce0711f730bfbb7d4c8ade'
SR_USER_AUTHENTICATION_PUBLIC_KEY_KID = 'e19091072f920cbf3ca9f436ceba309e7d814a62'

KEYS_FOLDER = './jwt-test-keys'

PAYLOAD = {
    'user_id': 'benchmark-user',
    'period_str': 'July 2019',
    'period_id': '201907',
    'collection_exercise_sid': str(uuid4()),
    'case_id': str(uuid4()),
    'case_type': 'HI',
    'display_address': '68 Abingdon Road, Goathill',
    'ru_ref': '123456789012A',
    'ru_name': 'Integration Testing',
    'ref_p_start_date': '2019-04-01',
    'ref_p_end_date': '2019-11-30',
    'return_by': '2019-12-06',
    'trad_as': 'Benchmark Tests',
    'employment_date': '1983-06-02',
    'region_code': 'GB-ENG',
    'language_code': 'en',
    'roles': [],
    'account_service_url': 'http://upstream.url',
    'variant_flags': {'sexual_identity': 'false'},
}


def get_file_contents(filename, trim=False):
    with open(os.path.join(KEYS_FOLDER, filename), 'r') as f:
        data = f.read()
        if trim:
            data = data.rstrip('\r\n')
    return data


_key_store = KeyStore(
    {
        'keys': {
            EQ_USER_AUTHENTICATION_RRM_PRIVATE_KEY_KID: {
                'purpose': KEY_PURPOSE_AUTHENTICATION,
                'type': 'private',
                'value': get_file_contents(
                    'sdc-user-authentication-signing-rrm-private-key.pem'
                ),
            },
            SR_USER_AUTHENTICATION_PUBLIC_KEY_KID: {
                'purpose': KEY_PURPOSE_AUTHENTICATION,
                'type': 'public',
                'value': get_file_contents(
                    'sdc-user-authentication-encryption-sr-public-key.pem'
                ),
            },
        }
    }
)


def _get_payload_with_params(schema_name, schema_url=None, **extra_payload):
    payload_vars = PAYLOAD.copy()
    payload_vars['tx_id'] = str(uuid4())
    payload_vars['response_id'] = str(uuid4())
    payload_vars['schema_name'] = schema_name
    if schema_url:
        payload_vars['schema_url'] = schema_url

    payload_vars['iat'] = time.time()
    payload_vars['exp'] = payload_vars['iat'] + float(3600)  # one hour from now
    payload_vars['jti'] = str(uuid4())
    payload_vars['response_expires_at'] =  payload_vars['iat'] + float(10080) # 7 days from now which is the default expiry time
    for key, value in extra_payload.items():
        payload_vars[key] = value

    return payload_vars


def create_token(schema_name, **extra_payload):
    payload_vars = _get_payload_with_params(schema_name, **extra_payload)

    return generate_token(payload_vars)


def generate_token(payload):
    return encrypt(payload, _key_store, KEY_PURPOSE_AUTHENTICATION)

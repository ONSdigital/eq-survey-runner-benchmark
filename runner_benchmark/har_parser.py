import json
from urllib.parse import unquote_plus
from pathlib import Path
from operator import itemgetter

import dateutil.parser
from haralyzer import HarParser

def parse_har_file(har_file_path):
    """
    Parse a HAR file into a list of request objects
    This currently filters requests by content_type (text/html)
    """
    with har_file_path.open() as f:
        har_parser = HarParser(json.loads(f.read()))

    requests = []

    for page in har_parser.pages:
        document_requests = page.filter_entries(content_type='text/html')
        for entry in document_requests:
            request = entry['request']

            keys_to_get = [('method', 'method'), ('url', 'url'), ('postData', 'data')]

            request_data = {k[1]: request.get(k[0]) for k in keys_to_get}

            if request_data['data']:
                request_data['data'] = {item['name']: item['value'] for item in request_data['data']['params']}

            request_data['datetime'] = dateutil.parser.parse(entry['startedDateTime'])

            if request_data['data']:
                request_data['data'] = decode_post_data(request_data['data'])

            requests.append(request_data)

    requests.sort(key=itemgetter('datetime'))

    for request in requests:
        request.pop('datetime', None)

    return requests

def decode_post_data(url_encoded_data):
    return {unquote_plus(k): unquote_plus(v) for k, v in url_encoded_data.items()}

def generate_har_benchmark(filename):
    filepath = Path(filename)
    absolute_path = filepath.absolute()
    requests = parse_har_file(absolute_path)

    print("Processing request data:")
    for r in requests:
        print(f"{r['method']}: {r['url']}")

if __name__ == '__main__':
    generate_har_benchmark('requests.har')

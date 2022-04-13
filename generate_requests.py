import json
from operator import itemgetter
from urllib.parse import unquote_plus, urlsplit

import click
import dateutil.parser
from haralyzer import HarParser


def parse_har_file(har_file):
    """
    Parse a HAR file into a list of request objects
    This currently filters requests by content_type (text/html)
    """
    har_parser = HarParser(json.load(har_file))

    requests = []

    for page in har_parser.pages:
        entries = page.filter_entries(content_type=r'(text/html|application/pdf)')
        for entry in entries:
            entry_request = entry['request']

            request_base_url = "{0.scheme}://{0.netloc}".format(
                urlsplit(entry_request['url'])
            )

            request = {
                'method': entry_request['method'],
                'url': entry_request['url'].replace(request_base_url, ""),
                'datetime': dateutil.parser.parse(entry['startedDateTime']),
            }

            if entry_request['method'] == 'POST':
                request['data'] = {
                    unquote_plus(item['name']): unquote_plus(item['value'])
                    for item in entry_request['postData']['params']
                }
                request['data'].pop('csrf_token', None)

            requests.append(request)

    requests.sort(key=itemgetter('datetime'))

    for request in requests:
        request.pop('datetime', None)

    return {'requests': requests}


@click.command()
@click.argument('har_file', type=click.File('r'))
@click.argument('requests_file', type=click.File('w'))
@click.argument('schema_name')
def generate_requests(har_file, requests_file, schema_name):
    requests = parse_har_file(har_file)
    requests['schema_name'] = schema_name
    requests['survey_url'] = f"https://storage.googleapis.com/eq-questionnaire-schemas/{schema_name}.json"
    json.dump(requests, requests_file, indent=4)


if __name__ == '__main__':
    generate_requests()

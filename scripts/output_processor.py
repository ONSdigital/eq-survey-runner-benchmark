#!/usr/bin/env python3

import csv
import re

input_filename = 'output_requests.csv'
output_filename = 'output_requests_processed.csv'

ce_id_regex = re.compile('\/[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}\/', re.I)

def mean_requests(key, first, second):
    """
    Takes a weighted mean of a certain key in each request set.
    """
    return (first[key] * first['num_requests'] + second[key] * second['num_requests']) / (first['num_requests'] + second['num_requests'])

def merge_requests(first, second):
    output = {}

    operators = {
        'num_requests': sum,
        'min_response_time': min,
        'max_response_time': max,
    }

    for k, op in operators.items():
        output[k] = op((first[k], second[k]))


    output['requests_per_second'] = mean_requests('requests_per_second', first, second)
    output['mean_response_time'] = mean_requests('mean_response_time', first, second)
    output['average_content_size'] = mean_requests('average_content_size', first, second)

    return output


if __name__ == '__main__':
    requests = {}

    with open(input_filename) as csv_requests:
        reader = csv.DictReader(csv_requests)
        for row in reader:

            stripped_url = ce_id_regex.sub('/[ID]/', row['Name'])

            request_key = (row['Method'], stripped_url)

            if int(row['# failures']) and not row['Name'] == 'Total':
                # Ignore any failed requests
                continue

            this_request = {
                'num_requests': int(row['# requests']),
                'mean_response_time': float(row['Average response time']),
                'min_response_time': float(row['Min response time']),
                'max_response_time': float(row['Max response time']),
                'average_content_size': float(row['Average Content Size']),
                'requests_per_second': float(row['Requests/s'])
            }

            if request_key in requests:
                requests[request_key] = merge_requests(requests[request_key], this_request)
            else:
                requests[request_key] = this_request

    with open(output_filename, 'w') as output_file:
        fieldnames = ['url', 'method', 'num_requests', 'mean_response_time', 'min_response_time',
                      'max_response_time', 'average_content_size', 'requests_per_second']

        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()

        for request_key in requests:
            output_dict = requests[request_key]
            output_dict['method'] = request_key[0]
            output_dict['url'] = request_key[1]

            writer.writerow(output_dict)

    print(f'Wrote output to file: {output_filename}')

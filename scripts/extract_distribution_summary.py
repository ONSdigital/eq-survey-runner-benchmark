#!/usr/bin/env python3

import sys

get_values = []
post_values = []
total = 0

for line in sys.stdin:
    if 'Name' in line:
        continue

    values = line.split(',')
    percentile_99th = int(values[9])

    if 'GET /questionnaire' in line:
        get_values.append(percentile_99th)
    if 'POST /questionnaire' in line:
        post_values.append(percentile_99th)
    if 'Total' in line:
        total = percentile_99th
  
get_average = int(sum(get_values) / len(get_values))
post_average = int(sum(post_values) / len(post_values))

print(f'Questionnaire GETs average: {get_average}ms')
print(f'Questionnaire POSTs average: {post_average}ms')
print(f'All requests average: {total}ms')

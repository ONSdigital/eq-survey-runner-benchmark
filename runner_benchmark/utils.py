from urllib.parse import urlparse, parse_qs


def parse_params_from_location(url, route):
    route_path = urlparse(route).path
    url_path = urlparse(url).path

    params = {}

    fields = [
        (i, element[1:-1])
        for i, element in enumerate(route_path.split("/"))
        if element.startswith('{') and element.endswith('}')
    ]

    for value_pos, value in enumerate(url_path.split("/")):
        for field_pos, field_name in fields:
            if field_pos == value_pos:
                params[field_name] = value

    if urlparse(route).query:
        query_result = parse_qs(urlparse(route).query)
        url_result = parse_qs(urlparse(url).query)

        query_result.update((key, url_result[key]) for key in query_result)

        for key, value in query_result.items():
            params[key] = value[0]

    return params

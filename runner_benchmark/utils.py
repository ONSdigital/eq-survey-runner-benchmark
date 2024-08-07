from urllib.parse import parse_qs, urlparse


def parse_params_from_location(url, route):
    parsed_route = urlparse(route)
    parsed_url = urlparse(url)

    params = {}

    fields = [
        (i, element[1:-1])
        for i, element in enumerate(parsed_route.path.split("/"))
        if element.startswith("{") and element.endswith("}")
    ]

    for value_pos, value in enumerate(parsed_url.path.split("/")):
        for field_pos, field_name in fields:
            if field_pos == value_pos:
                params[field_name] = value

    if parsed_route.query:
        query_result = parse_qs(parsed_route.query)
        url_result = parse_qs(parsed_url.query)

        params.update((key, url_result[key][0]) for key in query_result)

    return params

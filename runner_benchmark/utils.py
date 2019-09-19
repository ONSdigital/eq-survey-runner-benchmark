from urllib.parse import urlparse


def has_params(string):
    return '{' in string and '}' in string


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

    return params


if __name__ == "__main__":
    print(
        parse_params_from_location(
            'http://localhost:5000/questionnaire/household/riyjtl/add-or-edit-primary-person/',
            'http://localhost:5000/questionnaire/household/{person_1_list_id}/add-or-edit-primary-person/',
        )
    )

    print(
        parse_params_from_location(
            'http://localhost:5000/questionnaire/relationships/riyjtl/to/fgt56f/',
            'http://localhost:5000/questionnaire/relationships/{person_1_list_id}/to/{person_2_list_id}/',
        )
    )

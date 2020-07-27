from glob import glob


def get_stats(folder):
    stats = {
        "get": [],
        "post": [],
        "average_get": None,
        "average_post": None,
        "average_total": None,
        "total_requests": 0,
        "total_failures": 0,
        "error_percentage": 0
    }

    for file in glob(folder + '/*stats.csv'):

        with open(file) as f:
            data = f.read()

        for line in data.split('\n'):
            if 'Name' in line:
                continue

            values = line.split(',')

            percentile_99th = int(values[18])
            if values[1].startswith('"/questionnaire'):
                if values[0] == '"GET"':
                    stats["get"].append(percentile_99th)
                elif values[0] == '"POST"':
                    stats["post"].append(percentile_99th)

        if 'Aggregated' in line:
            stats["total_requests"] = stats["total_requests"] + int(values[2])
            stats["total_failures"] = stats["total_failures"] + int(values[3])

    return stats
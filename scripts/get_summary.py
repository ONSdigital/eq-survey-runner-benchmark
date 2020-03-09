import sys
from glob import glob

from scripts.visualise_results import get_stats

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print(
            "Provide the benchmark outputs directory as a parameter e.g. outputs/daily-test and the current run date"
        )
    else:
        output_folder = sys.argv[1]
        current_date = sys.argv[2] if len(sys.argv) > 2 else None
        filter_after = sys.argv[3] if len(sys.argv) > 3 else None

        test_run_folders = sorted(glob(f"{output_folder}/*"))

        stats = get_stats(test_run_folders, filter_after=filter_after)

        for stat in stats:
            if stat[0] == current_date:
                print(f'Questionnaire GETs average: {int(stat[1])}ms')
                print(f'Questionnaire POSTs average: {int(stat[2])}ms')
                print(f'All requests average: {int(stat[3])}ms')

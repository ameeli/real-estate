# TODO
# Work with Excel
# Deploy app with frontend
import argparse
import csv
import json
import requests

census_url = 'https://api.census.gov/data/{year}/acs/acs1/profile?get=group({group}),NAME&for=place:{place}&in=state:{state}'
groups = ['DP02', 'DP03', 'DP04', 'DP05']


def make_csv(start_year, end_year, place, state):
    years_to_check = range(int(start_year), int(end_year) + 1)

    for year in years_to_check:
        with open('{}_{}_{}.csv'.format(year, place, state), mode='w') as f:
            census_writer = csv.writer(f)

            for group in groups:
                url = census_url.format(year=year,
                                        group=group,
                                        place=place,
                                        state=state)
                try:
                    r = requests.get(url)
                except requests.exceptions.RequestException as e:
                    raise SystemExit(e)

                census_data = json.loads(r.text)
                census_data.writerow([year])
                census_writer.writerow(census_data[0])
                census_writer.writerow(census_data[1])


def parse_census_info():
    pass


if __name__ == '__main__':
    print('Collecting data from census...')
    parser = argparse.ArgumentParser()
    parser.add_argument('--begin', '-b')
    parser.add_argument('--end', '-e')
    parser.add_argument('--place', '-p')
    parser.add_argument('--state', '-s')
    args = parser.parse_args()

    print(make_csv(args.begin, args.end, args.place, args.state))

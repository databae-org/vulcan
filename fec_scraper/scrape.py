"""
Take a list of CONTRIBUTORS and a list of YEARS and fetch FEC filings from
FEC API
"""
from __future__ import absolute_import, unicode_literals, print_function

import os
from time import sleep

import arrow
import requests

URL = 'https://api.open.fec.gov/v1/download/schedules/schedule_a/'

CONTRIBUTORS = ['Robert Mercer', 'Diana Mercer', 'Rebekah Mercer']
YEARS = range(2007, 2017)

def build_params(contributor, year):
    """
    Generate URL paramaters passed to fec.gov API
    """
    params = {
        'api_key': os.environ['FEC_API_KEY'],  # generated by beta.fec.gov
        'sort_hide_null': True,
        'contributor_name': contributor,
        'contributor_state': 'NY',
        'two_year_transaction_period': year,
        'min_date': arrow.get('{}-01-01'.format(year - 1)).format('MM/DD/YYYY'),
        'max_date': arrow.get('{}-12-31'.format(year)).format('MM/DD/YYYY'),
        'sort': '-contribution_receipt_date',
        'is_individual': True
    }

    return params

def download_file(url, extension='', filename=None):
    """
    Download file from URL
    Modified from http://stackoverflow.com/a/16696317/868724
    """
    local_filename = filename or '{name}.{extension}'.format(name=url.split('/')[-1], extension=extension)
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    return local_filename

if __name__ == '__main__':
    slugify = lambda x: x.lower().replace(' ', '-')
    for year in YEARS:
        # the fec API request a filename payload the usual is the request time
        data = {
            'filename': '{}.zip'.format(str(arrow.get()).split('.')[0])
        }
        for contributor in CONTRIBUTORS:
            params = build_params(contributor, year)
            r = requests.post(URL, params=params, data=data)
            response = r.json()

            if response['status'] != 'complete':
                # sometimes the API needs to build the dataset and issues a 'queued' status
                # so, we're gonna sleep the script and then resend the request until
                # we receive a complete status
                sleep(5)
                r = requests.post(URL, params=params, data=data)

            download_file(r.json()['url'], filename='{}-{}-{}.zip'.format(
                year-1, year, slugify(contributor)))
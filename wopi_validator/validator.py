# coding=utf-8
from urlparse import urlparse, parse_qs

import requests

from argh import arg, CommandError, dispatch_command, ArghParser, add_commands
from termcolor import colored


__author__ = 'Tyler Butler <tyler@tylerbutler.com>'

TEST_STATUS = {
    0: 'Skipped',
    1: 'Passed',
    2: 'Failed',
}

TEST_STATUS_COLOR = {
    0: 'yellow',
    1: 'green',
    2: 'red',
}


# @click.command()
# @click.option('--getinfo_url', '-u', default='https://onenote.officeapps-df.live.com/hosting/GetWopiTestInfo.ashx')
# @click.option('--wopisrc', '-w', prompt=True)
# @click.option('--access_token', '-t', prompt=True)
# @click.option('--access_token_ttl', '-e', prompt=True)
# @arg('--getinfo_url', '-u', default='https://onenote.officeapps-df.live.com/hosting/GetWopiTestInfo.ashx')
@arg('--wopisrc', '-w')
@arg('--access_token', '-t')
@arg('-e', '--access_token_ttl')
def run(getinfo_url='https://onenote.officeapps-df.live.com/hosting/GetWopiTestInfo.ashx', wopisrc=None,
        access_token=None, access_token_ttl=None):
    parameters = {
        'wopisrc': wopisrc,
        'access_token': access_token,
        'access_token_ttl': access_token_ttl
    }
    resp = requests.get(getinfo_url, params=parameters)

    if resp.status_code != 200:
        # raise click.ClickException("WOPI validator URL returned HTTP code %s" % resp.status_code)
        raise CommandError("WOPI validator URL returned HTTP code %s" % resp.status_code)
    try:
        test_urls = resp.json()
    except ValueError as error:
        # raise click.ClickException("Response is not valid JSON.")
        raise CommandError(error)

    for test in test_urls:
        execute_test(test)

    print "Done."


def execute_test(test_url):
    print "Running test: %s" % get_test_name_from_query_string(test_url)
    resp = requests.get(test_url)

    try:
        result = resp.json()
    except ValueError:
        # raise click.ClickException("Response is not valid JSON.")
        raise CommandError("Response is not valid JSON.")

    test_name = result['Name']
    status = result['Status']
    print "%s: %s" % (test_name, colored(TEST_STATUS[status], TEST_STATUS_COLOR[status]))


def get_test_name_from_query_string(url):
    u = urlparse(url)
    qs = parse_qs(u.query)
    return qs['test'][0]


def discover_getinfo_url(discovery_url):
    pass


def cli():
    parser = ArghParser()
    parser.add_commands([run, discover_getinfo_url])
    parser.dispatch()


if __name__ == '__main__':
    cli()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ssh.alfredworkflow, v4.0
# Robin Breathe, 2013-2023

import json
import re
import sys
import os

from collections import defaultdict

DEFAULT_MAX_RESULTS = 36


class Hosts(defaultdict):
    def __init__(self, query, user=None):
        super(Hosts, self).__init__(list)
        self[query].append('input')
        self.query = query
        self.user = user

    def merge(self, source, hosts=()):
        for host in hosts:
            self[host].append(source)

    def _alfred_item(self, host, source):
        _arg = self.user and '@'.join([self.user, host]) or host
        _uri = 'ssh://{}'.format(_arg)
        _sub = 'source: {}'.format(', '.join(source))
        return {
            "uid": _uri,
            "title": _uri,
            "subtitle": _sub,
            "arg": _arg,
            "icon": {"path": "icon.png"},
            "autocomplete": _arg
        }

    def alfred_json(self, _filter=(lambda x: True), maxresults=DEFAULT_MAX_RESULTS):
        items = [
            self._alfred_item(host, self[host]) for host in self.keys()
            if _filter(host)
        ]
        return json.dumps({"items": items[:maxresults]})


def cache_file(filename, volatile=True):
    parent = os.path.expanduser(
        (
            os.getenv('alfred_workflow_data'),
            os.getenv('alfred_workflow_cache')
        )[bool(volatile)] or os.getenv('TMPDIR')
    )
    if not os.path.isdir(parent):
        os.mkdir(parent)
    if not os.access(parent, os.W_OK):
        raise IOError('No write access: %s' % parent)
    return os.path.join(parent, filename)


def fetch_file(file_path, cache_prefix, parser, env_flag):
    """
    Parse and cache a file with the named parser
    """
    # Allow default sources to be disabled
    if env_flag is not None and int(os.getenv('alfredssh_{}'.format(env_flag), 1)) != 1:
        return (file_path, ())

    # Expand the specified file path
    master = os.path.expanduser(file_path)

    # Skip a missing file
    if not os.path.isfile(master):
        return (file_path, ())

    # Read from JSON cache if it's up-to-date
    if cache_prefix is not None:
        cache = cache_file('{}.1.json'.format(cache_prefix))
        if os.path.isfile(cache) and os.path.getmtime(cache) > os.path.getmtime(master):
            return (file_path, json.load(open(cache, 'r')))

    # Open and parse the file
    try:
        with open(master, 'r') as f:
            results = parse_file(f, parser)
    except IOError:
        pass
    else:
        # Update the JSON cache
        if cache_prefix is not None:
            json.dump(list(results), open(cache, 'w'))
        # Return results
        return (file_path, results)


def parse_file(open_file, parser):
    parsers = {
        'ssh_config':
            (
                host for line in open_file
                if line[:5].lower() == 'host '
                for host in line.split()[1:]
                if not ('*' in host or '?' in host or '!' in host)
            ),
        'known_hosts':
            (
                host for line in open_file
                if line.strip() and not line.startswith('|')
                for host in line.split()[0].split(',')
            ),
        'hosts':
            (
                host for line in open_file
                if not line.startswith('#') and not line.startswith("127.0.0.1")
                for host in line.split()[1:]
                if host != 'broadcasthost'
            ),
        'extra_file':
            (
                host for line in open_file
                if not line.startswith('#')
                for host in line.split()
            )
    }
    return set(parsers[parser])


def complete():
    query = ''.join(sys.argv[1:])
    maxresults = int(os.getenv('alfredssh_max_results', DEFAULT_MAX_RESULTS))

    if '@' in query:
        (user, host) = query.split('@', 1)
    else:
        (user, host) = (None, query)

    host_chars = (('\\.' if x == '.' else x) for x in list(host))
    pattern = re.compile('.*?\b?'.join(host_chars), flags=re.IGNORECASE)

    hosts = Hosts(query=host, user=user)

    for results in (
        fetch_file('~/.ssh/config', 'ssh_config', 'ssh_config', 'ssh_config'),
        fetch_file('~/.ssh/known_hosts', 'known_hosts', 'known_hosts', 'known_hosts'),
        fetch_file('/etc/ssh/ssh_known_hosts', 'systemwide_known_hosts', 'known_hosts', 'known_hosts'),
        fetch_file('/usr/local/etc/ssh/ssh_known_hosts', 'localetc_known_hosts', 'known_hosts', 'known_hosts'),
        fetch_file('/etc/hosts', 'hosts', 'hosts', 'hosts'),
    ):
        hosts.merge(*results)

    extra_files = os.getenv('alfredssh_extra_files')
    if extra_files:
        for file_path in extra_files.split():
            file_prefix = os.path.basename(file_path)
            hosts.merge(*fetch_file(file_path, file_prefix, 'extra_file', None))

    return hosts.alfred_json(pattern.search, maxresults=maxresults)


if __name__ == '__main__':
    print(complete())

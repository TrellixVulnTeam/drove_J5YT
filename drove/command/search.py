#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import sys
import json
import contextlib
from . import Command
from . import CommandError

from six.moves import urllib


class SearchCommand(Command):
    """Search plugins in online repository"""
    def print_item(self, item):
        sys.stdout.write("%(id)-20s %(description)s\n" % item)
        sys.stdout.write("    %s\n" % (", ".join([x["id"]
                                       for x in item["version"]])))

    def execute(self):
        plugin_url = self.config.get("plugin_url",
                                     "https://plugins.drove.io").strip("/")
        request = ("%s/api/1/plugin/search?%s" %
                   (plugin_url,
                    urllib.parse.urlencode({"q": self.args.plugin})))

        try:
            with contextlib.closing(urllib.request.urlopen(request)) as resp:
                obj = json.loads(resp.read().decode("utf-8"))
                if "results" not in obj or \
                   not isinstance(obj["results"], list):
                    raise CommandError("Malformed response from '%s'" %
                                       (plugin_url,))
                else:
                    if len(obj["results"]) == 0:
                        self.log.warning("None plugin found")
                    else:
                        for result in obj["results"]:
                            self.print_item(result)
        except BaseException as e:
            raise CommandError(str(e))

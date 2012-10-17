# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

# Copyright (c) 2012 dput authors
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
"""
dput-ng native configuration file implementation.
"""

from dput.util import load_config, get_configs
from dput.core import logger
from dput.config import AbstractConfig
from dput.exceptions import DputConfigurationError


def get_sections():
    """
    Get all profiles we know about.
    """
    return get_configs('profiles')


class DputProfileConfig(AbstractConfig):
    """
    dput-ng native config file implementation. Subclass of a
    :class:`dput.config.AbstractConfig`.
    """

    def preload(self, replacements, configs):
        """
        See :meth:`dput.config.AbstractConfig.preload`
        """
        self.configs = {}
        self.replacements = replacements
        for section in get_sections():
            self.configs[section] = self.load_config(section,
                                                     configs=configs)

    def get_config_blocks(self):
        """
        See :meth:`dput.config.AbstractConfig.get_config_blocks`
        """
        return self.configs.keys()

    def get_defaults(self):
        """
        See :meth:`dput.config.AbstractConfig.get_defaults`
        """
        if "DEFAULT" in self.configs:
            return self.configs['DEFAULT']
        return {}

    def set_defaults(self, defaults):
        """
        See :meth:`dput.config.AbstractConfig.set_defaults`
        """
        self.configs['DEFAULT'] = defaults

    def get_config(self, name):
        """
        See :meth:`dput.config.AbstractConfig.get_config`
        """
        logger.debug("Getting %s" % (name))
        default = self.configs['DEFAULT'].copy()
        if name in self.configs:
            default.update(self.configs[name])
            default['name'] = name
            for key in default:
                val = default[key]
                if isinstance(val, basestring):
                    if "%(" in val and ")s" in val:
                        logger.debug("error with %s -> %s" % (
                            key,
                            val
                        ))
                        raise DputConfigurationError(
                            "Not converted values in key `%s' - %s" % (
                                key,
                                val
                            )
                        )
            return default
        return {}

    def load_config(self, name, configs=None):
        """
        See :meth:`dput.config.AbstractConfig.load_config`
        """
        kwargs = {
            "default": {},
            "schema": "config"
        }
        if configs is not None:
            kwargs['configs'] = configs

        profile = load_config(
            'profiles',
            name,
            **kwargs
        )
        repls = self.replacements
        for thing in profile:
            val = profile[thing]
            if not isinstance(val, basestring):
                continue
            for repl in repls:
                if repl in val:
                    val = val.replace("%%(%s)s" % (repl), repls[repl])
            profile[thing] = val
        return profile

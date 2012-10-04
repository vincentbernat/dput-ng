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


class DputError(BaseException):
    pass


class DputConfigurationError(DputError):
    pass


class NoSuchConfigError(DputError):
    pass


class ChangesFileException(DputError):
        pass


class UploadException(DputError):
    pass


class FtpUploadException(UploadException):
    pass


class SftpUploadException(UploadException):
    pass


class CheckerException(DputError):
    pass

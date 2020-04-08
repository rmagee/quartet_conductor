# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2019 SerialLab Corp.  All rights reserved.

import binascii


def convert_command_value(command_value: str) -> str:
    """
    Converts command strings for the scanners into the ascii hex the scanner
    expects
    :param command: The command value to convert.
    :return: A converted command value.
    """
    return str(binascii.hexlify(command_value.encode('ascii')))[2:].replace("'", "")

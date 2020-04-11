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
# Copyright 2020 SerialLab Corp.  All rights reserved.

from revpy_dio.inputs import InputMonitor as IM
from quartet_conductor.session import start_session
from quartet_conductor.microscan.utils import convert_command_value as ccv
from abc import abstractmethod
from telnetlib import Telnet

class InputMonitor(IM):
    """
    Monitors the inputs on a RevPi DIO and uses input 1 to start a session
    and input 2 to send a label.
    """

    def __init__(self, host: str, port: int, sleep_interval: float = .10):
        super().__init__(sleep_interval)
        self.session = None
        self.host = host
        self.port = port

    def handle_input(self, input_number: int):
        """
        Will look for an input 1 to start a session and input 2 to send
        the the label information.
        :param input_number: The input that was triggered
        :return: None
        """
        if input_number == 1:
            lot, expiry = self.get_session_data()
            self.session = start_session(lot, expiry)
        if input_number == 2:
            self.send_label(input_number)

    @abstractmethod
    def get_session_data(self):
        pass

    @abstractmethod
    def send_label(self, input_number: int):
        pass

    def get_match_string(self):
        return '*%s*%s*' % (self.session.expiry, self.session.lot)

    def intialize_scanner(self):
        with Telnet(self.host, self.port) as client:
            client.write('<K705,1,0,0>'.encode('ascii')) # only output matches
            match_string = '<K231h,1,%s>' % ccv(self.get_match_string())
            client.write(match_string.encode('ascii'))
            #client.write('< >'.encode('ascii'))
            client.close()

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
from typing import Optional, Callable, Any, Iterable, Mapping

from revpy_dio.inputs import InputMonitor as IM
from quartet_conductor.session import start_session
from django.conf import settings
from quartet_conductor.microscan.utils import convert_command_value as ccv
from abc import abstractmethod
from quartet_capture.tasks import create_and_queue_task
from quartet_capture.models import Rule
from quartet_capture.rules import Rule as CRule
from quartet_conductor.models import InputMap
from logging import getLogger
from telnetlib import Telnet
from threading import Thread

logger = getLogger()


class ThreadedInputMonitor(IM):
    """
    Monitors the inputs on a RevPi DIO and uses input 1 to start a session
    and input 2 to send a label.
    """

    def __init__(self, host: str, port: int, sleep_interval: float = .10):
        super().__init__(sleep_interval)
        self.session = None
        self.host = host
        self.port = port
        self.input_maps = {}

    def handle_input(self, input_number: int):
        """
        Will look for an input 1 to start a session and input 2 to send
        the the label information.
        :param input_number: The input that was triggered
        :return: None
        """
        # get the IO map if it is not already loaded and execute it's rule
        input_map = self.input_maps.get(input_number)
        if not input_map:
            try:
                input_map = InputMap.objects.select_related('rule').get(
                    input_number=input_number
                )
                self.input_maps[input_number] = input_map
                self.execute_task(input_map, input_number)
            except InputMap.DoesNotExist:
                logger.exception('There was no input map for input %s',
                                 input_number)

    def execute_task(self, input_map, input_number):
        create_and_queue_task(str(input_number),
                              rule_name=input_map.rule.name,
                              run_immediately=False,
                              initial_status='RUNNING',
                              rule=input_map.rule
                              )

    @abstractmethod
    def get_session_data(self):
        pass

    @abstractmethod
    def send_label(self, input_number: int):
        pass


class TaskThread(Thread):
    """
    Will run a task outside of celery to improve performance.
    """
    def __init__(self, group: None = ...,
                 target: Optional[Callable[..., Any]] = ...,
                 name: Optional[str] = ..., args: Iterable[Any] = ...,
                 kwargs: Mapping[str, Any] = ..., *,
                 daemon: Optional[bool] = ...) -> None:
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self.rule = None
        self.input_map = None
        self.input = None

    def execute_task(self, rule: Rule, input_map: InputMap, input: int):
        self.rule = rule
        self.input_map = input_map
        self.input = input
        self.start()

    def run(self) -> None:
        try:
            create_and_queue_task(str(self.input),
                                  rule_name=self.input_map.rule.name,
                                  run_immediately=True,
                                  initial_status='RUNNING',
                                  rule=self.input_map.rule
                                  )
        except:
            logger.exception('Could not execute the rule.')
            raise


# class RuleLoader:
#
#     def load_rules(self):
#         dummy_task = Task
#         maps = InputMap.objects.select_related('rule').all()
#         for map in maps:
#             CRule(Rule, )

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

from django.core.management.base import BaseCommand
from django.utils.translation import gettext as _
from quartet_capture.models import Rule
from quartet_conductor.models import InputMap


class Command(BaseCommand):
    help = _('Will create the rule, steps and logic necessary to initialize '
             'a microscan reader.')

    def add_arguments(self, parser):
        parser.add_argument(
            '--delete',
            action='store_true',
            help='Delete any maps and overwrite.'
        )
        parser.add_argument(
            '-i',
            '--print_input',
            action='store',
            help='The input number for this rule to listen on.',
            default='4'
        )
        parser.add_argument(
            '-r',
            '--start_input',
            action='store',
            help='The input number for this rule to listen on.',
            default='2'
        )

    def handle(self, *args, **options):
        answer = options['delete']
        print_input = int(options['print_input'])
        start_input = int(options['start_input'])
        try:
            print_rule = Rule.objects.get(name='VideoJet Print')
            init_rule = Rule.objects.get(name='Initialize Microscan')
            if answer:
                InputMap.objects.filter(
                    rule__in=[print_rule, init_rule]).delete()
            InputMap.objects.create(
                rule=print_rule,
                input_number=print_input,
                related_session_input=start_input
            )
            InputMap.objects.create(
                rule=init_rule,
                input_number=start_input
            )
        except Rule.DoesNotExist:
            print(
                'Make sure you have run the create_initialize_microscan_rule '
                'and the create_print_rule commands before running this '
                'command.')

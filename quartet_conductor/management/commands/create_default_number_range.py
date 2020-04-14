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
# .
from quartet_capture.models import Rule
from quartet_conductor.models import InputMap
from serialbox.models import Pool, SequentialRegion

class Command(BaseCommand):
    help = _('Will create the rule, steps and logic necessary to initialize '
             'a microscan reader.')

    def add_arguments(self, parser):
        parser.add_argument(
            '--delete',
            action='store_true',
            help='Delete any existing ranges and overwrites.'
        )

    def handle(self, *args, **options):
        answer = options['delete']
        try:
            if answer:
                Pool.objects.filter(machine_name='DEFAULT')
            pool = Pool.objects.create(
                readable_name='Default Range',
                machine_name='DEFAULT',
                active=True
            )
            sequential_region = SequentialRegion.objects.create(
                machine_name=pool.machine_name,
                readable_name=pool.readable_name,
                start=777000000000,
                end=999999999999,
                pool=pool
            )
        except Rule.DoesNotExist:
            print('Make sure you have run the create_initialize_microscan_rule '
                  'and the create_print_rule commands before running this '
                  'command.')



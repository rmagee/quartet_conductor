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
from quartet_capture import models
from quartet_templates.models import Template
from django.core.management.base import BaseCommand
from django.utils.translation import gettext as _
import os

class Command(BaseCommand):
    help = _('Will create the rule, steps and logic necessary to initialize '
             'a microscan reader.')

    def add_arguments(self, parser):
        parser.add_argument(
            '--delete',
            help='Delete any existing rule and overwrite it.'
        )

    def handle(self, *args, **options):
        answer = options['delete']
        if answer:
            rules = models.Rule.objects.filter(name='Initialize Microscan')
            print('Deleting %s rules' % rules.count())
            rules.delete()
        rule = models.Rule.objects.create(
            name='Initialize Microscan',
            description='Sends intialization data to a microscan reader.'
        )
        # ask the printer for details
        printer_query_step = models.Step.objects.create(
            name='Get Job Fields',
            description='Pulls the job fields from the printer.',
            step_class='quartet_conductor.videojet.steps.JobFieldsStep',
            order=1,
            rule=rule
        )
        # place the serial identifier on the context
        serial_id_step = models.Step.objects.create(
            name='Get Serial Identifier',
            description='Pulls the GTIN or SSCC value out of the job fields '
                        'and puts onto the context.',
            step_class='quartet_conductor.videojet.steps.GetSerialIdentifierStep',
            order=5,
            rule=rule
        )
        # formulate the match string command for the scanner
        command_step = models.Step.objects.create(
            name='Create match string command.',
            description='Creates the match string command for the reader.',
            step_class='quartet_conductor.microscan.steps.MatchStringCommandStep',
            order=10,
            rule=rule
        )
        # use the template to render the scanner commands format
        template_step = models.Step.objects.create(
            name='Render Initialization Commands',
            description='Renders the microscan template.',
            step_class='quartet_conductor.steps.TemplateStep',
            order=15,
            rule=rule
        )
        template_parameter = models.StepParameter.objects.create(
            name="Template Name",
            value='Initialize Microscan',
            step=template_step
        )
        # send the data to the scanner
        tcp_step = models.Step.objects.create(
            name = 'Telnet Data',
            description='Uses telnet session to send data to a TCP endpoint',
            step_class='quartet_conductor.steps.TelnetStep',
            rule = rule,
            order=20
        )
        models.StepParameter.objects.create(
            name='Host',
            value='scanner',
            description='The host to connect to. Microscan scanner.',
            step=tcp_step
        )
        models.StepParameter.objects.create(
            name='Port',
            value='2001',
            description='The port to connect to. Microscan scanner 2001.',
            step=tcp_step
        )
        create_session_step = models.Step.objects.create(
            name='Start Session',
            description='Creates a session object for input maps to access',
            step_class='quartet_conductor.videojet.steps.StartSessionStep',
            rule=rule,
            order=25
        )
        Template.objects.create(
            name='Initialize Microscan',
            description='Contains the data to send to the scanner to initialize'
                        ' it for operations.',
            content=self._get_template_data()
        )

    def _get_template_data(self):
        '''
        Loads the XML file and passes its data back as a string.
        '''
        curpath = os.path.dirname(__file__)
        data_path = os.path.join(curpath, '../../templates/scanner_init.txt')
        with open(data_path) as data_file:
            return data_file.read()

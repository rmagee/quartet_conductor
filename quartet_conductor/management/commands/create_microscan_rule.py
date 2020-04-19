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
import os
from django.core.management.base import BaseCommand
from django.utils.translation import gettext as _

from quartet_capture import models
from quartet_templates.models import Template


class Command(BaseCommand):
    help = _('Will create the rule, steps and logic necessary to initialize '
             'a microscan reader.')

    def add_arguments(self, parser):
        parser.add_argument(
            '-d',
            '--delete',
            action='store_true',
            help='Delete any existing rule and overwrite it.'
        )
        parser.add_argument(
            '-o',
            '--clearOutputs',
            action='store',
            help='A comma delimited list of numbers to clear when the rule '
                 'is executed.',
            default='6,8'
        )
        parser.add_argument(
            '-s',
            '--scannerHost',
            type=str,
            action='store',
            help='The IP or hostname of the scanner.',
            required=True
        )
        parser.add_argument(
            '-p',
            '--printerHost',
            type=str,
            action='store',
            help='The IP or hostname of the printer.',
            required=True
        )

    def handle(self, *args, **options):
        answer = options['delete']
        cleared_outputs = options['clearOutputs']
        if answer == True:
            print('******************************************')
            rules = models.Rule.objects.filter(name='Initialize Microscan')
            Template.objects.filter(name='Initialize Microscan').delete()
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
        printer_host_step_param = models.StepParameter.objects.create(
            name='Host',
            description='The IP or host name of the printer.',
            value=options['printerHost'],
            step=printer_query_step
        )
        models.StepParameter.objects.create(
            name='Port',
            value='777',
            description='The port to connect to for videojet text communications.',
            step=printer_query_step
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
            name='Create Match String',
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
            name='Telnet Data',
            description='Uses telnet session to send data to a TCP endpoint',
            step_class='quartet_conductor.steps.TelnetStep',
            rule=rule,
            order=20
        )
        models.StepParameter.objects.create(
            name='Host',
            value=options['scannerHost'],
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
        clear_outputs_step = models.Step.objects.create(
            name='Clear Outputs',
            description='Clears out the outputs in the step parameter.',
            step_class='quartet_conductor.steps.SetOutputsStep',
            rule=rule,
            order=30
        )
        outputs = models.StepParameter.objects.create(
            name='Output List',
            description='The outputs to set.',
            value=cleared_outputs,
            step=clear_outputs_step
        )
        direction = models.StepParameter.objects.create(
            name='On',
            description='Whether or not to turn on or off the outputs.',
            value='False',
            step=clear_outputs_step
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

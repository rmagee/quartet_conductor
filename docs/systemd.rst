Setting up systemd
------------------

Adjust the paths below if necessary and add to your /etc/systemd/system folder as
:code:`conductor.service`

.. code-block:: text

    [Unit]
    Description=QU4RTET Conductor
    After=network.target
    StartLimitIntervalSec=0

    [Service]
    Type=simple
    Restart=always
    RestartSec=1
    ExecStart=/home/pi/.virtualenvs/qu4rtet/bin/python /home/pi/quartet_conductor/quartet_conductor/microscan/inputs.py

    [Install]
    WantedBy=multi-user.target

Then issue a :code:`sudo systemctl daemon-reload && sudo systemctl start conductor.service` command.


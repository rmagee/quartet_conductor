-----------------
quartet_conductor
-----------------
Python module for machine and IoT interfaces.


=====
Hosts
=====

For testing and deployment using this in general, the host names that are used
in the unit tests and default configurations are as follows:

* scanner
* printer
* revpi

You can add these host names to your hosts file with the appropriate
IP addresses and you should be good to go.

=================
VideoJet Port 777
=================NO

The videojet printer needs to have it's text communications port
set to a non-zero value.  For conductor, it assumes you have set
the port to 777.  Please use this port to avoid any confusiont

Label Fields
============

The default label fields are as follows:

* LOT - The lot number
* EXPIRY - The expiration date
* GTIN - The GTIN field.
* SERIAL_NUMBER - The serial number field.

Any other fields are fine but will be ignored.

Settings
========
The following django settings are available.

This is the print rule used by the Input Monitor
DEFAULT_PRINT_RULE="VideoJet Print"

The number of seconds before a telnet connection will timeout.
TELNET_TIMEOUT=3

Whether or not to roll over to a default serial range if an explicit
GTIN range is not defined in serialbox.

USE_DEFAULT_RANGE=True

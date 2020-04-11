=====
Usage
=====

To use quartet_conductor in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'quartet_conductor.apps.QuartetConductorConfig',
        ...
    )

Add quartet_conductor's URL patterns:

.. code-block:: python

    from quartet_conductor import urls as quartet_conductor_urls


    urlpatterns = [
        ...
        url(r'^', include(quartet_conductor_urls)),
        ...
    ]

=====
Hosts
=====

For testing and using this in general, the hosts that are used
are as follows:

scanner
printer
revpi

You can add these host names to your hosts file with the appropriate
IP addresses and you should be good to go.

================
Printer Port 777
================

The videojet printer needs to have it's text communications port
set to a non-zero value.  For conductor, it assumes you have set
the port to 777.  Please use this port to avoid any confusiont

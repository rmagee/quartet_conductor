=============================
quartet_conductor
=============================

.. image:: https://gitlab.com/serial-lab/quartet_conductor/badges/master/coverage.svg
   :target: https://gitlab.com/serial-lab/quartet_conductor/pipelines
.. image:: https://gitlab.com/serial-lab/quartet_conductor/badges/master/build.svg
   :target: https://gitlab.com/serial-lab/quartet_conductor/commits/master
.. image:: https://badge.fury.io/py/quartet_conductor.svg
    :target: https://badge.fury.io/py/quartet_conductor

Python module for machine and IoT interfaces.

Documentation
-------------

The full documentation is at https://serial-lab.gitlab.io/quartet_conductor/

Quickstart
----------

Install quartet_conductor::

    pip install quartet_conductor

Add it to your `INSTALLED_APPS`:

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

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox


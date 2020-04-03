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

=============================
verification
=============================

.. image:: https://badge.fury.io/py/django-user-verification.png
    :target: https://badge.fury.io/py/django-user-verification

.. image:: https://travis-ci.org/Fueled/django-user-verification.png?branch=master
    :target: https://travis-ci.org/Fueled/django-user-verification

Package to help out with verifying new users.

Documentation
-------------

The full documentation is at https://django-user-verification.readthedocs.org.

Quickstart
----------

Install verification::

    pip install django-user-verification

Then use it in a project::

    import verification

Usage
--------

Defining Environment Variables for Backend
-----------------

In your settings file (e.g. common.py), define your credentials and any environment variables required for your backend service (e.g. Sendgrid, Twilio). This is how django-user-verification will actually send its verification link to whichever clients.

Also, add "verification" in your **INSTALLED_APPS** that's in your settings file.

For example, we define backend env variables in our settings file for Phone (Twilio) and Email:

.. code-block:: python

    USER_VERIFICATION = {
        'phone': {
            'BACKEND': 'verification.backends.base.TwilioBackend',
            'OPTIONS': {
                'SID': os.getenv('TWILIO_API_SID', default='fake'),
                'SECRET': os.getenv('TWILIO_API_SECRET', default='fake'),
                'FROM': os.getenv('TWILIO_FROM', default='+14755292729'),
                'MESSAGE': "Welcome, continue with this link: {link}"
            },
            'APP_URL': 'app://'
        },
        'email': {
            'BACKEND': 'verification.backends.base.EmailBackend',
            'OPTIONS': {
                'FROM': os.getenv('FROM_EMAIL', default='dummy@fueled.com')
            },
            'APP_URL': 'app://'
        },

    }

Then, go to your `urls.py` file and insert the following in your `urlpatterns`:

.. code-block:: python

    url(r'^api/', include("verification.urls")),


An example `POST` request for sending to a phone number:

`/verify/send/phone/`

and the payload being:

`{ "phone": "+15555555555" }`


Another example request for sending to an email is:

`/verify/send/email/`

with the payload being:

`{ "email": "joe@doe.com" }`



Running Tests
--------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install -r requirements-test.txt
    (myenv) $ python runtests.py

Credits
---------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-pypackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage

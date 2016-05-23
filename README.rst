=============================
verification
=============================

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
===========================================

In your settings file (e.g. common.py), define your credentials and any environment variables required for your backend service (e.g. Sendgrid, Twilio). This is how django-user-verification will actually send its verification link to whichever clients.

Also, add "verification" in your **INSTALLED_APPS** that's in your settings file.

For example, we define backend env variables in our settings file for Phone (Twilio) and Email:

.. code-block:: python

    USER_VERIFICATION = {
        'phone': {
            'BACKEND': 'verification.backends.twilio.TwilioBackend',
            'OPTIONS': {
                'SID': os.getenv('TWILIO_API_SID'),
                'SECRET': os.getenv('TWILIO_API_SECRET'),
                'FROM': os.getenv('TWILIO_FROM'),
                'MESSAGE': "Welcome, continue with this link: {link}"
            },
            'APP_URL': 'app://'
        },
        'email': {
            'BACKEND': 'verification.backends.email.EmailBackend',
            'OPTIONS': {
                'FROM': os.getenv('FROM_EMAIL', default='dummy@fueled.com')
            },
            'APP_URL': 'app://'
        },

    }

Then, go to your `urls.py` file and insert the following in your `urlpatterns`:

.. code-block:: python

    url(r'^verification/', include("verification.urls")),


An example `POST` request for sending to a phone number:

``/verify/send/phone/``

and the payload being:

    {
        "email": "joe@doe.com" 
    }


Another example request for sending to an email is:

``/verify/send/email/``

with the payload being:

    {
        "email": "joe@doe.com" 
    }


Configuration
--------------
You can user multiple verification backends, such as a `phone` or `email` backend. Inside these verification types we can set multiple `OPTIONS`, for example we could set up the `phone` verification type:

.. code::
    USER_VERIFICATION = {
        'phone': {
            'BACKEND': 'verification.backends.twilio.TwilioBackend',
            'OPTIONS': {
                'SID': os.getenv('TWILIO_API_SID'),
                'SECRET': os.getenv('TWILIO_API_SECRET'),
                'FROM': os.getenv('TWILIO_FROM'),
                'MESSAGE': "Welcome, continue with this link: {link}"
            },
            'APP_URL': 'app://',
            'GENERATOR': 'verification.generators.NumberGenerator'
        }
    }


**BACKEND**: The import path of a verification type. There are multiple verification backends available:
- `verification.backends.twilio.TwilioBackend`: Twilio backend for sending SMS, needs `SID`, `SECRET`, `FROM` and optionally `MESSAGE`
- `verification.backends.email.EmailBackend`: Email backend, uses Django default email handler, no options needed

**OPTIONS**: These are options specific for the backend

**APP_URL**: The App URL to redirect to, currently iOS Only

**GENERATOR**: The generator of the keys that are stored in the cache, default it is a 5 digit number

Verification
-----------------
This package solely creates a way to verify a phone number or email, but we decided we wanted to be able to add additional resources to the verification process, such as registration when pin number is correct. For that we made a serializer for you to use, which handles the validation of the pin for you.

To use the serializer we just have to extend the `verification.serializers.VerificationSerializer`, like so:

.. code-block:: python
    class MyOwnVerificationSerializer(VerificationSerializer):
        email = serializers.CharField()
        token = serializers.CharField()

        class Meta:
            verification_type = 'email'
            token_field = 'token'

**NOTE**: We have to add `verification_type` as minimum so that we know which flow we are using (e.g. `email` or `phone`)



Running Tests
--------------

Does the code actually work?

.. code-block:: bash

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install -r requirements-test.txt
    (myenv) $ python runtests.py

Contributing
--------------
Feel free to create issues or open pull requests, we would love to see your contributions coming in!

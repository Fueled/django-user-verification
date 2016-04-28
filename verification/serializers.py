# -*- coding: utf-8 -*-

# Third Party Stuff
from rest_framework import serializers, exceptions
from phonenumber_field.validators import validate_international_phonenumber


# smash Stuff
from .services import PhoneVerificationService


class PhoneVerificationSerializer(serializers.Serializer):
    phone_number = serializers.CharField(validators=[validate_international_phonenumber])

    def send(self):
        service = PhoneVerificationService()
        service.send_verification(self.validated_data['phone_number'], self.context['request'])


class PinNumberVerificationSerializer(serializers.Serializer):
    pin = serializers.CharField(required=True)
    phone_number = serializers.CharField(validators=[validate_international_phonenumber],
                                         required=True)

    class Meta:
        fields = ('pin', 'phone_number')

    def validate(self, data):
        data = super(PinNumberVerificationSerializer, self).validate(data)

        service = PhoneVerificationService()
        if not service.check_pin(data.get('pin'), data.get('phone_number')):
            raise exceptions.ValidationError('Invalid combination of pin and password')
        return data

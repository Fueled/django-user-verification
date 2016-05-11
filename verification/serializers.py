# Third Party Stuff
from rest_framework import serializers

# Local Stuff
from verification.services import get_service


class VerificationSerializer(serializers.Serializer):
    class Meta:
        verification_type = None
        token_field = 'token'

    def validate(self, data):
        meta = self.Meta
        value = data.get(meta.verification_type)
        token = data.get(meta.token_field)

        if not all([token, value]):
            raise serializers.ValidationError(
                "{} and {} are required.".format(meta.verification_type,
                                                 meta.token_field))
        service = get_service(meta.verification_type)
        if not service.validate_token(token, value):
            raise ValueError(
                "{} and {} combination is invalid".format(meta.token_field,
                                                          meta.verification_type))
        return data

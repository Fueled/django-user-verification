# Third Party Stuff
from rest_framework import serializers

# Local Stuff
from verification.services import get_service


class VerificationSerializer(serializers.Serializer):
    """
    The verification serializer that can be used inside other serializers
    so that these can intercept requests for pin verifications.

    This is done by changing the Meta object on that particular serializer,
    adding verification_type and token_field

    :example:
        class OtherSerializer(VerificationSerializer):
            class Meta:
                verification_type = "email"
                token_field = "pin"

    This way we know that we have to look for an `email` field and an `pin`
    field to validate the user.
    """

    class Meta:
        """
        Defaults for the Meta class.
        """
        token_field = 'token'

    def validate(self, data):
        """
        We override the validate method to do our check on the verification
        type and token field.

        :param data: dict object to be validated.
        """
        meta = self.Meta

        if not hasattr(meta, 'verification_type'):
            raise ValueError("Need an 'verification_type' inside the {} Meta object "
                             "to be fully functioning.".format(type(self)))

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

from rest_framework import serializers
from .models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework import status
from rest_framework.response import Response


# Change password serializer
class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


# register serializer
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            'name', 'email', 'password', 'password2', 'education', 'the_outcome_of_forensic_science', 'birth_date',
            'country', 'amount_of_quran', 'quran_number', 'sex', 'hobby'
        )

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            name=validated_data['name'],
            email=validated_data['email'],
            country=validated_data['country'],
            the_outcome_of_forensic_science=validated_data['the_outcome_of_forensic_science'],
        )
        if 'education' in validated_data:
            user.education = validated_data['education']
        if 'birth_date' in validated_data:
            user.birth_date = validated_data['birth_date']
        if 'amount_of_quran' in validated_data:
            user.amount_of_quran = validated_data['amount_of_quran']
        if 'birth_date' in validated_data:
            user.quran_number = validated_data['quran_number']
        if 'sex' in validated_data:
            user.quran_number = validated_data['sex']
        if 'hobby' in validated_data:
            user.quran_number = validated_data['hobby']
        user.set_password(validated_data['password'])
        user.save()

        return user

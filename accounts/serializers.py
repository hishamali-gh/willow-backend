from django.contrib.auth import authenticate, get_user_model
from django.db.models import Q
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from orders.serializers import OrderSerializer

User = get_user_model()

class RegistrationModelSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, error_messages={'blank': '*Confirm the password'})

    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password', 'confirm_password']
        extra_kwargs = {
            'name': {'error_messages': {
                'blank': '*Name is required'
            }},
            'username': {'error_messages': {
                'blank': '*Username is required'
            }},
            'email': {'error_messages': {
                'blank': '*Email is required'
            }},
            'password': {
                'write_only': True,
                'error_messages': {
                    'blank': '*Password is required'
                }
            }
        }

    def validate_password(self, value):
        try:
            validate_password(value)
        except DjangoValidationError as e:
            errors = []

            for err in e.error_list:
                if err.code == 'password_too_short':
                    errors.append('*Password must be at least 8 characters long')
                else:
                    errors.append(err.message)

            raise serializers.ValidationError(errors)

        return value

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError({'confirm_password':'*Your password inputs do not match'})
        
        attrs.pop('confirm_password')

        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField(max_length=30)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        identifier = attrs.get('identifier')
        password = attrs.get('password')

        user_obj = User.objects.filter(
            Q(username=identifier) | Q(email=identifier)
        ).first()

        if not user_obj:
            raise serializers.ValidationError('Invalid credentials')

        user = authenticate(
            username=user_obj.username,
            password=password
        )

        if not user:
            raise serializers.ValidationError('Invalid credentials')

        if not user.is_active:
            raise serializers.ValidationError('User account is disabled')

        attrs['user'] = user
        
        return attrs
    
class UserModelSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(read_only=True, many=True)
    
    class Meta:
        model = User
        fields = '__all__'
    
class MeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'username', 'email', 'is_superuser']

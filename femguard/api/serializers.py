from rest_framework import serializers
from .models import ChatHistory, UploadedFile, User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},  # Ensure the password is write-only
            'email': {'required': True}  # Email is mandatory
        }

    def create(self, validated_data):
        """
        Create a new user with a hashed password.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class ChatHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for the ChatHistory model.
    """
    user = serializers.StringRelatedField(read_only=True)  # Display user's username instead of ID
    created_at = serializers.DateTimeField(read_only=True)  # Ensure read-only for timestamps
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = ChatHistory
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'user']  # Prevent user from being overridden


class UploadedFileSerializer(serializers.ModelSerializer):
    """
    Serializer for the UploadedFile model.
    """
    user = serializers.StringRelatedField(read_only=True)  # Display user's username instead of ID
    uploaded_at = serializers.DateTimeField(read_only=True)  # Ensure read-only for timestamp

    class Meta:
        model = UploadedFile
        fields = '__all__'
        read_only_fields = ['uploaded_at', 'user']  # Prevent user from being overridden

    def validate_file_path(self, value):
        """
        Custom validation for the file_path field.
        """
        if not value.name.endswith(('.txt', '.pdf', '.docx')):
            raise serializers.ValidationError("Only .txt, .pdf, and .docx files are allowed.")
        return value

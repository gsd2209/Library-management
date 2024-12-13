from rest_framework import serializers
from .models import User, Book, BorrowRequest

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_librarian', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

# Book Serializer
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'available']

# Borrow Request Serializer
class BorrowRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRequest
        fields = ['id', 'user', 'book', 'start_date', 'end_date', 'status']
        read_only_fields = ['status']

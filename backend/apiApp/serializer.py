from rest_framework import serializers
from apiApp.models import *

#creating serializer
#serializer for users
class UserAccountSerializer (serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = '__all__'

#serializer for todos
class TodoSerializer (serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'


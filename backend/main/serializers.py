from rest_framework import serializers
from .models import *

# Conversor python <---> json
class DeadLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deadline
        fields = '__all__'
        many = True

from rest_framework import serializers
from .models import Paitent

class PaitentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paitent
        fields = '__all__'
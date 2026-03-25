"""
Serializers for screening app
"""

from rest_framework import serializers
from .models import ScreeningResult, ScreeningHistory, PHCLocation
from apps.users.serializers import UserSerializer


class ScreeningResultSerializer(serializers.ModelSerializer):
    """Serializer for screening results"""
    user_email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = ScreeningResult
        fields = [
            'id', 'user_email', 'assessment_type', 'audio_transcript',
            'symptoms', 'risk_score', 'risk_level', 'prediction_result',
            'confidence_score', 'notes', 'recommendations', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class ScreeningHistorySerializer(serializers.ModelSerializer):
    """Serializer for screening history"""
    screening_result = ScreeningResultSerializer()
    
    class Meta:
        model = ScreeningHistory
        fields = ['id', 'screening_result', 'status', 'review_notes', 'created_at']
        read_only_fields = ['id', 'created_at']


class PHCLocationSerializer(serializers.ModelSerializer):
    """Serializer for PHC locations"""
    class Meta:
        model = PHCLocation
        fields = ['id', 'name', 'address', 'phone', 'latitude', 'longitude', 'distance_km']
        read_only_fields = ['id']

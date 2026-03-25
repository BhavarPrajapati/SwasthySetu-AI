"""
Models for screening app
"""

import uuid
from django.db import models
from django.conf import settings


class ScreeningResult(models.Model):
    """Store Alzheimer's screening results"""
    id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='screening_results')
    
    # Assessment details
    assessment_type = models.CharField(
        max_length=50,
        choices=[
            ('memory', 'Memory Assessment'),
            ('cognitive', 'Cognitive Assessment'),
            ('behavioral', 'Behavioral Assessment'),
            ('xray', 'X-Ray Analysis'),
            ('voice', 'Voice Analysis')
        ]
    )
    
    # Audio transcription
    audio_transcript = models.TextField(blank=True, null=True)
    audio_file_url = models.URLField(blank=True, null=True)
    
    # Assessment results
    symptoms = models.JSONField(default=dict)  # Stores detected symptoms
    risk_score = models.FloatField(default=0.0)  # Risk score 0-100
    risk_level = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Low Risk'),
            ('medium', 'Medium Risk'),
            ('high', 'High Risk'),
            ('critical', 'Critical Risk')
        ],
        default='low'
    )
    
    # Predictions
    prediction_result = models.JSONField(default=dict)  # ML model predictions
    confidence_score = models.FloatField(default=0.0)
    
    # Metadata
    notes = models.TextField(blank=True, null=True)
    recommendations = models.JSONField(default=list)  # List of medical recommendations
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'screening_results'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.assessment_type} - {self.created_at}"


class ScreeningHistory(models.Model):
    """Store user screening history"""
    id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='screening_history')
    screening_result = models.ForeignKey(ScreeningResult, on_delete=models.CASCADE)
    
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('completed', 'Completed'),
            ('reviewed', 'Reviewed'),
        ],
        default='pending'
    )
    
    review_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'screening_history'
        ordering = ['-created_at']


class PHCLocation(models.Model):
    """Store Primary Health Centers locations"""
    id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    latitude = models.FloatField()
    longitude = models.FloatField()
    distance_km = models.FloatField(null=True, blank=True)  # Distance from user
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'phc_locations'

    def __str__(self):
        return self.name

"""
URLs for screening app
"""

from django.urls import path
from .views import (
    MemoryAssessmentView,
    VoiceTranscriptionView,
    AlzheimerPredictionView,
    ScreeningHistoryView,
    PHCFinderView,
    SaveAssessmentView,
    ScreeningResultDetailView
)

urlpatterns = [
    path('memory/', MemoryAssessmentView.as_view(), name='memory-assessment'),
    path('voice/', VoiceTranscriptionView.as_view(), name='voice-transcription'),
    path('prediction/', AlzheimerPredictionView.as_view(), name='prediction'),
    path('history/', ScreeningHistoryView.as_view(), name='screening-history'),
    path('phc-finder/', PHCFinderView.as_view(), name='phc-finder'),
    path('save/', SaveAssessmentView.as_view(), name='save-assessment'),
    path('result/<str:result_id>/', ScreeningResultDetailView.as_view(), name='result-detail'),
]

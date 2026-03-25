"""
Views for screening app
"""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import ScreeningResult, ScreeningHistory, PHCLocation
from .serializers import ScreeningResultSerializer, ScreeningHistorySerializer, PHCLocationSerializer


class MemoryAssessmentView(APIView):
    """Handle memory assessment"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            data = request.data
            symptoms = data.get('symptoms', {})
            
            # Create screening result
            screening_result = ScreeningResult.objects.create(
                user=request.user,
                assessment_type='memory',
                symptoms=symptoms,
                risk_score=data.get('risk_score', 0),
                risk_level=self._calculate_risk_level(data.get('risk_score', 0))
            )
            
            # Add to history
            ScreeningHistory.objects.create(
                user=request.user,
                screening_result=screening_result,
                status='completed'
            )
            
            return Response(
                ScreeningResultSerializer(screening_result).data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def _calculate_risk_level(score):
        """Calculate risk level based on score"""
        if score < 25:
            return 'low'
        elif score < 50:
            return 'medium'
        elif score < 75:
            return 'high'
        else:
            return 'critical'


class VoiceTranscriptionView(APIView):
    """Handle voice transcription and analysis"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            file = request.FILES.get('audio')
            if not file:
                return Response({'error': 'No audio file provided'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Process audio and transcribe
            # This would integrate with a speech-to-text service
            transcript = "Voice analysis - placeholder for actual transcription"
            
            screening_result = ScreeningResult.objects.create(
                user=request.user,
                assessment_type='voice',
                audio_transcript=transcript,
                audio_file_url=str(file)  # In production, upload to cloud storage
            )
            
            ScreeningHistory.objects.create(
                user=request.user,
                screening_result=screening_result,
                status='completed'
            )
            
            return Response(
                ScreeningResultSerializer(screening_result).data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AlzheimerPredictionView(APIView):
    """Handle Alzheimer's prediction"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            features = data.get('features', [[]])[0] if data.get('features') else []

            # Calculate risk score from features using weighted heuristic
            # Features order matches FEATURE_SCHEMA in frontend
            risk_score = 0
            if len(features) >= 32:
                age = features[0]
                mmse = features[22]           # lower = worse
                memory_complaints = features[24]
                behavioral_problems = features[25]
                confusion = features[27]
                disorientation = features[28]
                personality_changes = features[29]
                difficulty_tasks = features[30]
                forgetfulness = features[31]
                family_history = features[10]
                depression = features[13]
                head_injury = features[14]

                # Age factor
                if age > 80: risk_score += 25
                elif age > 70: risk_score += 15
                elif age > 60: risk_score += 8

                # MMSE (0-30, lower is worse)
                if mmse < 10: risk_score += 30
                elif mmse < 20: risk_score += 20
                elif mmse < 25: risk_score += 10

                # Symptoms
                risk_score += memory_complaints * 10
                risk_score += behavioral_problems * 8
                risk_score += confusion * 10
                risk_score += disorientation * 10
                risk_score += personality_changes * 7
                risk_score += difficulty_tasks * 7
                risk_score += forgetfulness * 8
                risk_score += family_history * 10
                risk_score += depression * 5
                risk_score += head_injury * 5

            probability = min(risk_score / 100, 1.0)

            if probability > 0.6:
                prediction = 1
                risk_classification = 'High'
            elif probability > 0.3:
                prediction = 2
                risk_classification = 'Medium'
            else:
                prediction = 0
                risk_classification = 'Low'

            prediction_result = {
                'prediction': prediction,
                'probability': probability,
                'probability_score': probability,
                'risk_classification': risk_classification,
                'confidence': probability,
                'result': f"Alzheimer's risk: {risk_classification}",
                'features': features
            }

            screening_result = ScreeningResult.objects.create(
                user=request.user,
                assessment_type='cognitive',
                symptoms=data.get('symptoms', {}),
                prediction_result=prediction_result,
                confidence_score=probability,
                risk_score=probability * 100,
                risk_level=risk_classification.lower(),
                notes=data.get('notes', '')
            )

            ScreeningHistory.objects.create(
                user=request.user,
                screening_result=screening_result,
                status='completed'
            )

            return Response(prediction_result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SaveAssessmentView(APIView):
    """Save assessment results - for compatibility with frontend"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            data = request.data
            
            # Extract data from frontend payload
            prediction_text = data.get('prediction', 'Low')
            probability = float(data.get('probability', 0))
            features = data.get('features', [])
            other_data = data.get('otherData', {})
            
            # Map prediction text to risk level
            risk_level_map = {
                'Low': 'low',
                'Medium': 'medium',
                'High': 'high',
                'Critical': 'critical'
            }
            risk_level = risk_level_map.get(prediction_text, 'low')
            
            screening_result = ScreeningResult.objects.create(
                user=request.user,
                assessment_type='cognitive',
                symptoms=other_data,
                prediction_result={
                    'prediction': prediction_text,
                    'probability': probability,
                    'features': features
                },
                confidence_score=probability,
                risk_score=probability * 100,
                risk_level=risk_level,
                notes=f"Assessment saved at {data.get('timestamp', 'unknown time')}"
            )
            
            ScreeningHistory.objects.create(
                user=request.user,
                screening_result=screening_result,
                status='completed'
            )
            
            return Response({
                'message': 'Assessment saved successfully',
                'result': ScreeningResultSerializer(screening_result).data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e), 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ScreeningHistoryView(APIView):
    """Get user's screening history"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            history = ScreeningHistory.objects.filter(
                user=request.user
            ).select_related('screening_result').order_by('-created_at')

            assessments = []
            for h in history:
                r = h.screening_result
                pr = r.prediction_result or {}
                assessments.append({
                    'timestamp': r.created_at.isoformat(),
                    'prediction': pr.get('prediction', 0),
                    'probability': pr.get('probability', r.risk_score / 100),
                    'riskLevel': r.risk_level.capitalize(),
                    'features': pr.get('features', []),
                    'otherData': r.notes or '',
                    'assessmentType': r.assessment_type,
                    'id': str(r.id),
                })

            return Response({'assessments': assessments}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PHCFinderView(APIView):
    """Find nearby Primary Health Centers"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            lat = request.data.get('latitude')
            lon = request.data.get('longitude')
            
            if not lat or not lon:
                return Response(
                    {'error': 'Latitude and longitude required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Get PHCs from database
            phcs = PHCLocation.objects.all()[:10]  # Get nearest 10
            serializer = PHCLocationSerializer(phcs, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ScreeningResultDetailView(APIView):
    """Get detailed screening result"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, result_id):
        try:
            result = ScreeningResult.objects.get(id=result_id, user=request.user)
            return Response(
                ScreeningResultSerializer(result).data,
                status=status.HTTP_200_OK
            )
        except ScreeningResult.DoesNotExist:
            return Response(
                {'error': 'Screening result not found'},
                status=status.HTTP_404_NOT_FOUND
            )

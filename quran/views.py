from django.shortcuts import render
from .models import (
    Surah,
    Verse,

)
import pandas as pd
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import (
    Explanation,
    Verse,
)
from .serializers import (
    ExplanationSerializer,
)


# Create your views here.
class VerseExplanation(APIView):
    def get(self, request, *args, **kwargs):
        verse = Verse.objects.filter(number=request.data['number'], surah=request.data['surah']).first()
        ex = Explanation.objects.filter(verse=verse)
        return Response(
            data={
                "length": len(ex),
                "details": ExplanationSerializer(ex, many=True).data,
            }
        )

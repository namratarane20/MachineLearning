from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from vuenote.models import Note
from vuenote.serializers import NoteSerializer
# Create your views here.
class NoteViewSet(viewsets.ModelViewSet):
    permission_classes = {
        IsAuthenticated,
    }
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    lookup_field = 'id'
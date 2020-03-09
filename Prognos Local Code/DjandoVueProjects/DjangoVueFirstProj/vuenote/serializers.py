from rest_framework import  serializers
from vuenote.models import Note
class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = "_all_"

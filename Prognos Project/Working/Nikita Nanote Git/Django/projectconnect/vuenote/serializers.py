from rest_framework import serializers
from vuenote.models import Note

class NoteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"

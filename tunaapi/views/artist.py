from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Artist

class ArtistView(ViewSet):
    """Artist Views"""
    def create(self, request):
        """CREATE Artist"""
        artist = Artist.objects.create(
            name=request.data["name"],
            age=request.data["age"],
            bio=request.data["bio"],
        )
    
        serializer = ArtistSerializer(artist)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk):
        """GET Single Artist"""
        artist = Artist.objects.get(pk=pk)
        serializer = ArtistSerializer(artist)
        return Response(serializer.data)
        
    def list(self, request):
        """GET All Artists"""
        artists = Artist.objects.all()
        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data)
      
    def update(self, request, pk):
        """UPDATE Artist"""
        artist = Artist.objects.get(pk=pk)
        artist.name = request.data["name"]
        artist.age = request.data["age"]
        artist.bio = request.data["bio"]
        artist.save()
        
        return Response('Artist edited', status=status.HTTP_204_NO_CONTENT)
      
    def destroy(self, request, pk):
        """DELETE Artist"""
        artist = Artist.objects.get(pk=pk)
        artist.delete()
        return Response('Artist deleted', status=status.HTTP_204_NO_CONTENT)
      
class ArtistSerializer(serializers.ModelSerializer):
    """JSON serializer for artists"""
    class Meta:
        model = Artist
        fields = ('id', 'name', 'age', 'bio')
    

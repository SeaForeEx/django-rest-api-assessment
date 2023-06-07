from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.db.models import Count, Q
from tunaapi.models import Artist, Song

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
        artist_id = Artist.objects.get(pk=pk)
        artist_songs = Song.objects.annotate(song_count=Count('artist_id', filter=Q(artist_id=artist_id)))
        serializer = ArtistSerializer(artist_songs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # def retrieve(self, request, pk):
    #     """GET Single Artist"""
    #     artist_id = Artist.objects.get(pk=pk)
    #     artist_songs = Song.objects.annotate(song_count=Count('songs', filter=Q(songs__artist=artist_id)))
    #     serializer = ArtistSerializer(artist_songs)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    
        
    def list(self, request):
        """GET All Artists"""
        artists = Artist.objects.all()
        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
      
    def update(self, request, pk):
        """UPDATE Artist"""
        artist = Artist.objects.get(pk=pk)
        artist.name = request.data["name"]
        artist.age = request.data["age"]
        artist.bio = request.data["bio"]
        artist.save()     
        return Response('Artist edited', status=status.HTTP_200_OK)
      
    def destroy(self, request, pk):
        """DELETE Artist"""
        artist = Artist.objects.get(pk=pk)
        artist.delete()
        return Response('Artist deleted', status=status.HTTP_204_NO_CONTENT)
      
class ArtistSerializer(serializers.ModelSerializer):
    """JSON serializer for artists"""
    song_count = serializers.IntegerField(default=None)
    class Meta:
        model = Artist
        fields = ('id', 'name', 'age', 'bio', 'song_count')
        depth = 2
    

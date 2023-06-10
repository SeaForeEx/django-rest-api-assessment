# from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Song, Artist

class SongView(ViewSet):
    """Song Views"""
    def create(self, request):
        """CREATE Song"""
        artist_id = Artist.objects.get(pk=request.data["artist_id"])
        song = Song.objects.create(
            title=request.data["title"],
            artist_id=artist_id,
            album=request.data["album"],
            length=request.data["length"],
        )
        
        serializer = SongSerializer(song)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
      
    def retrieve(self, request, pk):
        """GET Single Song"""
        song = Song.objects.prefetch_related('genres').get(pk=pk)
        
        serializer = SongSerializer(song)
        return Response(serializer.data, status=status.HTTP_200_OK)
      
    def list(self, request):
        """GET All Songs"""
        songs = Song.objects.all()
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
      
    def update(self, request, pk):
        """UPDATE Song"""
        song = Song.objects.get(pk=pk)
        song.title = request.data["title"]
        song.artist_id = Artist.objects.get(pk=request.data["artist_id"])
        song.album = request.data["album"]
        song.length = request.data["length"]
        song.save()
        return Response('Song updated', status=status.HTTP_200_OK)
      
    def destroy(self, request, pk):
        """DELETE Song"""
        song = Song.objects.get(pk=pk)
        song.delete()
        return Response('Song deleted', status=status.HTTP_204_NO_CONTENT)

class SongSerializer(serializers.ModelSerializer):
    """JSON serializer for songs"""

    artist = serializers.SerializerMethodField()
    genres = serializers.SerializerMethodField()

    class Meta:
        model = Song
        fields = ('id', 'title', 'artist', 'album', 'length', 'genres')
        
    def get_genres(self, obj):
        """Get Them Genres"""
        genres = obj.genres.all()
        return [{'id': genre.genre_id.id, 'description': genre.genre_id.description} for genre in genres]
    def get_artist(self, obj):
        """Get Them Artists"""
        artist = obj.artist_id
        return [{'id': artist.id, 'name': artist.name,'age': artist.age, 'bio': artist.bio}]

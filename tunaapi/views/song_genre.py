from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import SongGenre

class SongGenreView(ViewSet):
    """Song Genre Views"""
    def create(self, request):
        """CREATE Song Genre"""
        song_genre = SongGenre.objects.create(
            song_id=request.data["song_id"],
            genre_id=request.data["genre_id"],
        )
        
        serializer = SongGenreSerializer(song_genre)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
      
    def retrieve(self, request, pk):
        """GET Single Song Genre"""
        song_genre = SongGenre.objects.get(pk=pk)
        serializer = SongGenreSerializer(song_genre)
        return Response(serializer.data, status=status.HTTP_200_OK)
      
    def list(self, request):
        """GET All Song Genres"""
        songs = SongGenre.objects.all()
        serializer = SongGenreSerializer(songs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
      
class SongGenreSerializer(serializers.ModelSerializer):
    """JSON serializer for song genres"""
    model = SongGenre
    fields = ('id', 'song_id', 'genre_id')

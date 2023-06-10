# from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Genre, SongGenre

class GenreView(ViewSet):
    """Genre CRUD"""
    def create(self, request):
        """CREATE Genre"""
        genre = Genre.objects.create(
            description=request.data["description"],
        )
        
        serializer = GenreSerializer(genre)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
      
    def retrieve(self, request, pk):
        """GET Single Genre"""
        genre = Genre.objects.prefetch_related('songs').get(pk=pk)
        serializer = GenreSerializer(genre)
        return Response(serializer.data, status=status.HTTP_200_OK)
      
    def list(self, request):
        """GET All Genres"""
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
      
    def update(self, request, pk):
        """UPDATE Genre"""
        genre = Genre.objects.get(pk=pk)
        genre.description = request.data["description"]
        genre.save()
        return Response('Genre edited', status=status.HTTP_200_OK)
      
    def destroy(self, request, pk):
        """DELETE Genre"""
        genre = Genre.objects.get(pk=pk)
        genre.delete()
        return Response('Genre deleted', status=status.HTTP_204_NO_CONTENT)       

# SongGenreSerializer is a custom serializer for the SongGenre model
class SongGenreSerializer(serializers.ModelSerializer):
    """
    JSON serializer for song genres
    """
    # This serializer inherits from the ModelSerializer class
    id = serializers.SerializerMethodField()  # A custom field to get the id of the SongGenre instance
    title = serializers.SerializerMethodField()  # A custom field to get the title of the associated song
    artist_id = serializers.SerializerMethodField()  # A custom field to get the artist_id of the associated song
    album = serializers.SerializerMethodField()  # A custom field to get the album of the associated song
    length = serializers.SerializerMethodField()  # A custom field to get the length of the associated song

    # The Meta class specifies the model and the fields to be serialized
    class Meta:
        model = SongGenre  # The model associated with this serializer
        fields = ('id', 'title', 'artist_id', 'album', 'length')  # The fields to be serialized

    # The get_id, get_title, get_artist_id, get_album, and get_length methods are custom methods
    # that retrieve the related song information for each SongGenre instance
    def get_id(self, obj):
        """Get that id"""
        return obj.song_id.id

    def get_title(self, obj):
        """Get that title"""
        return obj.song_id.title

    def get_artist_id(self, obj):
        """Get that artist"""
        return obj.song_id.artist_id.id

    def get_album(self, obj):
        """Get that album"""
        return obj.song_id.album

    def get_length(self, obj):
        """Get that length"""
        return obj.song_id.length

# GenreSerializer is a custom serializer for the Genre model
class GenreSerializer(serializers.ModelSerializer):
    """
    JSON serializer for genres
    """
    # This serializer inherits from the ModelSerializer class
    songs = SongGenreSerializer(many=True, read_only=True)  # A nested serializer for the songs field, which is read-only and accepts multiple instances
    class Meta:
        model = Genre  # The model associated with this serializer
        fields = ('id', 'description', 'songs')  # The fields to be serialized
        depth = 1  # This line sets the serialization depth to 1, meaning that only one level of related objects (in this case, the SongGenre objects) will be serialized.

# from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.db.models import Count
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
        # Retrieve the artist object with the specified primary key (pk)
        artist = Artist.objects.annotate(
            # Annotate the queryset with the song_count, which is the count of songs for each artist
            song_count=Count('songs')
        ).get(pk=pk)

        # Create a serialized representation of the artist object using the ArtistSerializer
        serializer = ArtistSerializer(artist)

        # Return the serialized artist object as a JSON response with a 200 OK status code
        return Response(serializer.data, status=status.HTTP_200_OK) 
        
    def list(self, request):
        """GET All Artists"""
        artists = Artist.objects.annotate(song_count=Count('songs')).all()
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
      
# SongSerializer is a custom serializer for the Song model
class SongSerializer(serializers.ModelSerializer):
    """
    JSON serializer for songs
    """
    class Meta:
        model = Song  # Specifies the model that this serializer is working with (Song)
        fields = ('id', 'title', 'album', 'length')  # List of fields to be serialized in the output

# ArtistSerializer is a custom serializer for the Artist model
class ArtistSerializer(serializers.ModelSerializer):
    """
    JSON serializer for artists
    """
    song_count = serializers.IntegerField(default=None)  # A field to store the number of songs associated with the artist
    songs = serializers.SerializerMethodField()  # A custom field to get the list of songs associated with the artist

    class Meta:
        model = Artist  # Specifies the model that this serializer is working with (Artist)
        fields = ('id', 'name', 'age', 'bio', 'song_count', 'songs')  # List of fields to be serialized in the output
        depth = 1  # Specifies the depth of nested relationships to be serialized

    # The get_songs method is a custom method to retrieve the list of songs associated with the artist
    def get_songs(self, obj):
        """Get them songs"""
        songs = obj.songs.all()  # Get all the related songs for the given artist
        serializer = SongSerializer(songs, many=True)  # Create a new SongSerializer instance for serializing the list of songs
        return serializer.data  # Return the serialized data of the list of songs

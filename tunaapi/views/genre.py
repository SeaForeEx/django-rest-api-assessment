# from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Genre

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
        genre = Genre.objects.get(pk=pk)
        serializer = GenreSerializer(genre)
        return Response(serializer.data)
      
    def list(self, request):
        """GET All Genres"""
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data)
      
    def update(self, request, pk):
        """UPDATE Genre"""
        genre = Genre.objects.get(pk=pk)
        genre.description = request.data["description"]
        genre.save()
        return Response('Genre edited', status=status.HTTP_204_NO_CONTENT)
      
    def destroy(self, request, pk):
        """DELETE Genre"""
        genre = Genre.objects.get(pk=pk)
        genre.delete()
        return Response('Genre deleted', status=status.HTTP_204_NO_CONTENT)       
    
class GenreSerializer(serializers.ModelSerializer):
    """JSON serializer for genres"""
    class Meta:
        model = Genre
        fields = ('id', 'description')

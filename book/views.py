import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Book
from .serializers import BookSerializer
from .util import verifying_token


class BooksView(APIView):
    @verifying_token
    def post(self, request):
        try:
            serializer = BookSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': 'Book Added', 'status': 201, 'data': serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.exception(e)
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @verifying_token
    def get(self, request):

        try:
            books = Book.objects.filter(user_id=request.data.get('user_id'))
            # books = Book.objects.all()
            serializer = BookSerializer(books, many=True)
            return Response({'message': 'Retrieved Books', 'data': serializer.data})
        except Exception as e:
            logging.exception(e)
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @verifying_token
    def put(self, request):

        try:
            book = Book.objects.get(id=request.data.get('id'))
            serializer = BookSerializer(book, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': 'Book Updated successfully', 'data': serializer.data})
        except Exception as e:
            logging.exception(e)
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @verifying_token
    def delete(self, request):
        try:
            book = Book.objects.get(id=request.data.get("id"))
            book.delete()
            return Response(
                {
                    "message": "Data deleted"
                },
                status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logging.error(e)
            return Response(
                {
                    "message": "Data not deleted"
                },
                status=status.HTTP_400_BAD_REQUEST)


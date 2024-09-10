from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from .serializers import TodoSerializer
from .models import Todo


def validate_data(data):

    if (not isinstance(data.get('title'), str) and
            not isinstance(data.get('description'), str)):
        raise ValidationError([
            {"title": "Title must be a String"},
            {"description": "Description must be a String"}
        ])

    if not isinstance(data.get('title'), str):
        raise ValidationError({"title": "Title must be a String."})

    if not isinstance(data.get('description'), str):
        raise ValidationError(
            {"description": "Description must be a String."}
        )

    return data


class TodoListCreateAPIView(APIView):

    def get(self, request):

        todos = Todo.objects.all()
        serializer = TodoSerializer(todos, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = validate_data(data=request.data)

        serializer = TodoSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodoDetailAPIView(APIView):

    def get_object(self, pk):
        try:
            obj = Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            raise ValidationError(
                {"error": "Provided Todo Id does not exists."}
            )

        return obj

    def get(self, request, pk):

        todo = self.get_object(pk=pk)

        serializer = TodoSerializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):

        todo = self.get_object(pk=pk)
        data = validate_data(data=request.data)
        serializer = TodoSerializer(todo, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        todo = self.get_object(pk=pk)
        todo.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

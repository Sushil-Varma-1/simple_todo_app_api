from django.urls import path
from .views import TodoListCreateAPIView, TodoDetailAPIView

urlpatterns = [
    path('todos', TodoListCreateAPIView.as_view(), name='todo'),
    path('todos/<int:pk>', TodoDetailAPIView.as_view(), name='todo_detail')
]

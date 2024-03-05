from django.urls import path

from . import views 
from .views import home, menu, UpdateQuestion, CreateQuestion, DeleteQuestion, UpdateChoice, CreateChoice, DeleteChoice #, editors_home

app_name = "polls"
urlpatterns = [
    path("", views.QuestionListView.as_view(), name="questionlist"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path('update_question/<int:pk>/', UpdateQuestion.as_view(), name='UpdateQuestion'),
    path('agregar/', CreateQuestion.as_view(), name='CreateQuestion'),
    path('delete_question/<int:pk>/', DeleteQuestion.as_view(), name='DeleteQuestion'),
    path('updatechoice/<int:pk>/', UpdateChoice.as_view(), name = "UpdateChoice"),
    path('addchoice/<int:pk>/', CreateChoice.as_view(), name = "CreateChoice"),
    path('deletechoice/<int:pk>/', DeleteChoice.as_view(), name = "DeleteChoice"),
    path('menu/', views.MenuView.as_view() , name = 'menu'),
    #path('editor/', editors_home , name = 'EditorHome'),
    path('', home, name='home'),
]

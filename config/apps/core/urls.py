from django.urls import path

from . import views

app_name = 'core'
urlpatterns = [
    path('movies/', views.MovieListView.as_view(), name='movie_list'),
    path('movie/<int:pk>/',
         views.MovieDetailView.as_view(), name='movie_detail'),
    path('persons/<int:pk>/',
         views.PersonDetail.as_view(), name='person_detail'),
    path('movie/<int:movie_id>/vote/',
         views.CreateVote.as_view(), name='vote_create'),
    path('movie/<int:movie_id>/vote/<int:pk>/',
         views.UpdateVote.as_view(), name='vote_update'),
    path('movie/<int:movie_id>/image/upload/',
         views.MovieImageUpload.as_view(), name='movie_imageupload'),
]

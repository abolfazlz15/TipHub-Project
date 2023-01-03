from django.urls import path, re_path
from . import views

app_name = 'videos'
urlpatterns = [
    # video URL
    path('', views.HomeView.as_view(), name='home'),
    path('videos/', views.VideoListView.as_view(), name='all-video'),
    path('videos/favorite', views.FavoriteVideoList.as_view(), name='favorite-video'),
    path('videos/category/<int:id>', views.CategoryList.as_view(), name='category-video'),
    re_path(r'videos/(?P<slug>[-\w]+)/', views.VideoDetailView.as_view(), name='video-detail'),
    path('search/', views.SearchVideoView.as_view(), name='search-video'),

    # like URL
    # re_path(r'like/(?P<slug>[-\w]+)/', views.LikeView.as_view(), name='like'),
    path('like/<int:pk>', views.LikeView.as_view(), name='like'),

    # notification URL
    path('deletenotif/<int:id>', views.DeleteNotificationView.as_view(), name='delete-notification'),

    # path('comments/<int:video_id>', views.comment_view, name='comment'),
]


# old urlpatterns
# urlpatterns = [
#     # video URL
#     path('', views.HomeView.as_view(), name='home'),
#     path('videos/', views.VideoListView.as_view(), name='all-video'),
#     path('videos/favorite', views.FavoriteVideoList.as_view(), name='favorite-video'),
#     path('videos/category/<int:id>', views.CategoryList.as_view(), name='category-video'),
#     path('videos/<int:pk>/<slug:slug>/', views.VideoDetailView.as_view(), name='video-detail'),
#     path('search/', views.SearchVideoView.as_view(), name='search-video'),

#     # like URL
#    path('like/<int:id>/<slug:slug>', views.LikeView.as_view(), name='like'),

#     # notification URL
#     path('deletenotif/<int:id>', views.DeleteNotificationView.as_view(), name='delete-notification'),

#     # path('comments/<int:video_id>', views.comment_view, name='comment'),
# ]

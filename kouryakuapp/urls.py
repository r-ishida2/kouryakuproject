from django.urls import path
from . import views
from .views import CommentCreateView,KouryakuPostDetailView,CommentDeleteView,PostDeleteView,PostSearchView,AdminUpdateListView

app_name = 'kouryakuapp'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    path('post/',views.CreateKouryakuView.as_view(), name='post'),

    path('post_done/',views.PostSuccessView.as_view(),name='post_done'),
    
    path('comment_done/',views.CommentSuccessView.as_view(),name="comment_done"),

    path('post/<int:pk>/comment/', CommentCreateView.as_view(), name='comment_create'),
    
    path('post/<int:pk>/', KouryakuPostDetailView.as_view(), name='detail'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('mypage/', views.MypageView.as_view(), name = 'mypage'),
    path('user-list/<int:user>', views.UserView.as_view(), name = 'user_list'),
    path('kouryakus/<int:category>', views.CategoryView.as_view(), name = 'kouryakus_cat'),
    path('search/', PostSearchView.as_view(), name='post_search'),
    path('updates/', AdminUpdateListView.as_view(), name='admin_update_list'),
]

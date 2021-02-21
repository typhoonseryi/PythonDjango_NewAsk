from django.urls import path, re_path, include
from .views import (QuestionListView, QuestionDetailsView, UserCreateView, QuestionCreateView, ProfileLookView)

urlpatterns = [
    path('', QuestionListView.as_view(), name='main_page'),
    re_path(r'^question/(?P<id>\d+)/$', QuestionDetailsView.as_view(), name='question_details'),
    path('accounts/create/', UserCreateView.as_view(), name='create_account'),
    path('accounts/<slug:slug>/card/', ProfileLookView.as_view(), name='look_account'),
    path('question/create/', QuestionCreateView.as_view(), name='create_question'),
]
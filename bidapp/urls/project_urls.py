from django.urls import path
from ..apis.project import projects_list, project_detail, today_update_count

urlpatterns = [
    path('projects/', projects_list, name='projects_list'),
    path('projects/<str:project_id>/', project_detail, name='project_detail'),
    path('today_update_count/', today_update_count, name='today_update_count'),
]

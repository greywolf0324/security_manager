from django.urls import path
from . import views

app_name = 'security'

urlpatterns = [
  path('', views.home, name='home'),
  path('parse-upload', views.parseUpload, name='parse-upload'),
  path('required-items', views.requiredItems, name='required-items'),
  path('history', views.history, name='history'),
  path('history_view/<str:creation_date>/', views.history_viewer, name='history_view'),
  path('download-file/<id>', views.downloadFile, name='download-file'),
  path('POconversion', views.POconversion, name='POconversion'),
  path('dbchange', views.auto_matching_DB_changer, name='dbchange'),
  path('viewer', views.viewer, name='viewer'),
  path('export-doubleIgnore', views.live_doubleIgnore, name='export-file'),
  path('export-doubleUpdate', views.live_doubleUpdate, name='export-file'),
  path('history-delete', views.history_deletion, name='history-delete')
]
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views, detect, delete

app_name = 'detect'
urlpatterns = [
	path('', views.detect, name='index'),
	path('showall/', views.show_all, name='showall'),
	path('delete/', delete.delete_all, name='delete'),
	path('detect/', detect.detect, name='detect'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

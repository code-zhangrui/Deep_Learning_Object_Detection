from django.urls import include, path
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from detect import views

urlpatterns = [
	path('', views.show_all),
	path('admin/', admin.site.urls),
	path('detect/', include('detect.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('uiai2018/jet/', include('jet.urls', 'jet')),
    path('uiai2018/jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('uiai2018/captcha/', include('captcha.urls')),
    path('uiai2018/admin/', admin.site.urls),
    path('uiai2018/summernote/', include('django_summernote.urls')),
    path('uiai2018/', include('main.urls')),
    path('uiai2018/blog/', include('blog.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

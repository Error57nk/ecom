
from django.contrib import admin
from django.urls import include, path

from django.conf.urls.static import static
from django.conf import settings
from Vuser import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Store.urls')),
    path('registration/', user_views.regPage, name='registration'),
    path('login/', user_views.loginPage, name='login'),
    path('logout/', user_views.logoutUser, name='logout'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

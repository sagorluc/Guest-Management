
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rosetta/', include('rosetta.urls')),
    path('event/', include('event.urls')),
    path('accounts/', include('authentication.urls')),
    path('api/', include('API.urls'), name='api'),
    path('api_auth/', include('API_authentication.urls')),
    # path('social_accounts/', include('allauth.urls')),
      
    # prefix_default_language= False
]

urlpatterns += staticfiles_urlpatterns()


# urlpatterns = i18n_patterns(
#     path('admin/', admin.site.urls),
#     path('rosetta/', include('rosetta.urls')),
#     path('event/', include('event.urls')),
#     path('accounts/', include('authentication.urls')),
#     path('api/', include('API.urls'), name='api'),
#     path('api_auth/', include('API_authentication.urls')),
#     # path('/', include('googleauthentication.urls')),
#     # path('social_accounts/', include('allauth.urls')),
    
    
#     # prefix_default_language= False
# )


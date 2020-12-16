"""Demacia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
import DemaciaApp.views
from django.conf.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',DemaciaApp.views.main, name='main'),
    # path('main/',DemaciaApp.views.main, name='main'),
    path('login/',DemaciaApp.views.login, name='login'),
    # path('login_user/',DemaciaApp.views.login_user, name='login_user'),
    # path('login_admin/',DemaciaApp.views.login_admin, name='login_admin'),
    path('user_regist/',DemaciaApp.views.user_regist, name='user_regist'),
    path('user_regist/user_id_check/',DemaciaApp.views.user_id_check, name='user_id_check'),
    path('mypage/',DemaciaApp.views.mypage,name='mypage'),
    path('logout/',DemaciaApp.views.logout,name='logout'),
    path('video_analysis/',DemaciaApp.views.video_analysis, name='video_analysis'),
    # path('file_upload/', DemaciaApp.views.file_upload, name='file_upload'),
    path('video_analysis/file_upload/', DemaciaApp.views.file_upload, name='file_upload'),
    path('traffic_volume_research/', DemaciaApp.views.traffic_volume_research, name='traffic_volume_research'),
    path('traffic_volumne_research_data/',DemaciaApp.views.traffic_volumne_research_data, name='traffic_volumne_research_data'),
    path('traffic_volumne_research_chart_data/',DemaciaApp.views.traffic_volumne_research_chart_data, name='traffic_volumne_research_chart_data'),
    path('request_list/', DemaciaApp.views.request_list, name='request_list'),
    path('admin_home/', DemaciaApp.views.admin_home, name='admin_home'),
    path('admin_video_list/', DemaciaApp.views.admin_video_list, name='admin_video_list'),
    path('image_popup/',DemaciaApp.views.image_popup, name='image_popup'),
    path('video_analysis_progress/',DemaciaApp.views.video_analysis_progress, name='video_analysis_progress'),
]
if settings.DEBUG:
    # import debug_toolbar
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += [path('__debug__/', include(debug_toolbar.urls)),]

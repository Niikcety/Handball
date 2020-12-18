"""src URL Configuration

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

from team.views import list_teams, team_detail
from match.views import list_matches, match_create, match_detail, direct_matches, index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('teams/', list_teams, name='list_teams'),
    path('matches/', list_matches, name='list_matches'),
    path('create/', match_create, name='match_create'),
    path('matches/<int:match_id>', match_detail, name='match_detail'),
    path('matches/<int:home_team_id>/<int:away_team_id>', direct_matches, name='direct_matches'),
    path('teams/<int:team_id>', team_detail, name='team_detail'),
    path('', index, name='index')
]

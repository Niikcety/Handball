from django.shortcuts import render

from match.views import match_create

from .models import Team
from match.models import Match
# Create your views here.
def list_teams(request):
    teams = Team.objects.order_by('-wins', 'name')
    context = {
        'teams_list': teams
    }
    return render(request, "teams/teams_list.html", context)


def get_opponents(matches_home, matches_away):
    opponents = []
    for match in matches_home:
        opponents.append(match.away_team.name)
    for match in matches_away:
        opponents.append(match.home_team.name)
    return opponents

def team_detail(request, team_id):
    matches_home = Match.objects.filter(home_team=team_id).all()
    matches_away = Match.objects.filter(away_team=team_id).all()
    team_name = Team.objects.filter(id=team_id).first().name
    team_wins = Team.objects.filter(id=team_id).first().wins
    opponents = set(get_opponents(matches_home, matches_away))
    opponents_list = sorted(list(opponents), key=lambda opponent: opponent)
    opponents_dict = []
    for opponent in opponents_list:
        opponent_id = Team.objects.filter(name=opponent).first().id
        opponents_dict.append({'name': opponent, 'away_team_id':opponent_id})
    context = {
        'opponents': opponents_dict,
        'team_name': team_name,
        'home_team_id': team_id,
        'wins': team_wins
    }
    return render(request, 'teams/teams_detail.html', context)
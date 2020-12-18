from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from django.contrib import messages

from team.models import Team

from .models import Match
from .forms import CreateForm

# Create your views here.
def list_matches(request):
    matches = Match.objects.all()
    context = {
        'matches_list': matches
    }
    return render(request, "match/matches_list.html", context)


def save_matches(tokens):
    if Team.objects.filter(name=tokens['home_team']).count() == 0:
        Team(name=tokens['home_team'], wins=0).save()
    if Team.objects.filter(name=tokens['away_team']).count() == 0:
        Team(name=tokens['away_team'], wins=0).save()

    team1_id = Team.objects.filter(name=tokens['home_team']).values('id')[0]['id']
    team2_id = Team.objects.filter(name=tokens['away_team']).values('id')[0]['id']
    team1 = Team.objects.filter(name=tokens['home_team'])[0]
    team2 = Team.objects.filter(name=tokens['away_team'])[0]
    if Match.objects.filter(Q(home_team=team1_id) & Q(away_team=team2_id)).count() == 0:
        Match(home_team=team1, away_team=team2, home_score=tokens['first_match_home'], away_score=tokens['first_match_away']).save()
    if Match.objects.filter(home_team=team2).filter(away_team=team1).count() == 0:
        Match(home_team=team2, away_team=team1, home_score=tokens['second_match_home'], away_score=tokens['second_match_away']).save()
    
    winner_name = Match.get_winner(tokens)
    winner_team = Team.objects.get(name=winner_name)
    winner_team.wins += 1
    winner_team.save()

def match_create(request):
    if request.method == 'POST':
        form = CreateForm(request.POST)
        match_info = request.POST.get('match_info')
        if match_info == 'stop':
            return render(request, 'match/index.html')
        if Match.is_valid(match_info):
            tokens = Match.tokenizer(match_info)
            save_matches(tokens)
            messages.info(request, 'Match added successfully!')
            return render(request, 'match/match_create.html', {'form': CreateForm()})
        else:
            messages.info(request, 'Wrong input data. Try again.')
            return render(request, 'match/match_create.html', {'form': CreateForm()})
    else:
        form = CreateForm()
    context = {
        'form': form
    }
    return render(request, 'match/match_create.html', context)

def match_detail(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    context = {
        'match': match
    }
    return render(request, 'match/match_detail.html', context)

def direct_matches(request, home_team_id, away_team_id):
    match1 = Match.objects.filter(Q(home_team=home_team_id) & Q(away_team=away_team_id)).first()
    match2 = Match.objects.filter(Q(home_team=away_team_id) & Q(away_team=home_team_id)).first()
    context = {
        'match1': match1,
        'match2': match2
    }
    context['winner'] = Match.get_winner_queries(match1, match2)
    return render(request, 'match/direct_matches.html', context)

def index(request):
    return render(request, 'match/index.html')


from django.db import models

from team.models import Team

# Create your models here.
class Match(models.Model):
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="home_team")
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="away_team")
    home_score = models.IntegerField()
    away_score = models.IntegerField()

    def __str__(self):
        return "Home Team: {}\n Away Team:{}\n Score: {} : {}".format(self.home_team.name, self.away_team.name, self.home_score, self.away_score)
    
    @staticmethod
    def is_valid(match_info):
        information = match_info.split(' | ')
        if len(information) != 4:
            return False

        s1, s2 = information[2].split(':')
        s3, s4 = information[3].split(':')

        if int(s1) >= 0 and int(s2) >= 0 and int(s3) >= 0 and int(s4) >= 0:
            return True
        return False

    @staticmethod
    def tokenizer(match_info):
        information = match_info.split(' | ')
        tokens = {}
        score1 = information[2].split(':')
        score2 = information[3].split(':')
        tokens['home_team'] = information[0]
        tokens['away_team'] = information[1]
        tokens['first_match_home'] = int(score1[0])
        tokens['first_match_away'] = int(score1[1])
        tokens['second_match_home'] = int(score2[0])
        tokens['second_match_away'] = int(score2[1])
        return tokens

    @staticmethod
    def get_winner(tokens):
        first_team_score = tokens['first_match_home'] + tokens['second_match_away']
        second_team_score = tokens['first_match_away'] + tokens['second_match_home']
        if first_team_score > second_team_score:
            return tokens['home_team']
        elif second_team_score > first_team_score:
            return tokens['away_team']
        elif tokens['first_match_away'] > tokens['second_match_home']:
            return tokens['away_team']
        else:
            return tokens['home_team']

    @staticmethod
    def get_winner_queries(match1, match2):
        m1_h = match1.home_score
        m1_a = match1.away_score
        m2_h = match2.home_score
        m2_a = match2.away_score

        if m1_h + m2_a > m1_a + m2_h:
            return match1.home_team.name
        if m1_h + m2_a < m1_a + m2_h:
            return match1.away_team.name
        if m1_a > m2_a:
            return match1.away_team.name
        return match1.home_team.name

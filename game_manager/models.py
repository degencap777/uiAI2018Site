from user_panel.models import *
from django.db import models


class GameRequest(models.Model):
    PENDING = 'PENDING'
    ACCEPTED = 'ACCEPTED'
    REJECTED = 'REJECTED'
    STATUS_OPTIONS = (
        (PENDING, 'در انتظار'),
        (ACCEPTED, 'پذیرفته شده'),
        (REJECTED, 'رد شده'),
    )

    sender = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='sent_game_requests')
    receiver = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='received_game_requests')
    status = models.CharField(max_length=8, choices=STATUS_OPTIONS, default=PENDING)

    def __str__(self):
        return 'REQ: {} vs {} - {}'.format(self.sender.name, self.receiver.name, self.status)


class Game(models.Model):
    WAITING = 'WAITING'
    PLAYING = 'PLAYING'
    FINISHED = 'FINISHED'
    STATUS_OPTIONS = (
        (WAITING, 'در صف انتظار'),
        (PLAYING, 'در حال اجرا'),
        (FINISHED, 'پایان یافته'),
    )
    request = models.OneToOneField(GameRequest, on_delete=models.CASCADE)
    status = models.CharField(max_length=8, choices=STATUS_OPTIONS, default=WAITING)
    logged_team1_name = models.CharField(max_length=16, blank=True, null=True)
    logged_team2_name = models.CharField(max_length=16, blank=True, null=True)
    logged_team1_goals = models.IntegerField(blank=True, null=True)
    logged_team2_goals = models.IntegerField(blank=True, null=True)
    log_file = models.FileField(upload_to='logs', blank=True, null=True)

    def __str__(self):
        return 'GAME: {} vs {} - {}'.format(self.request.sender.name, self.request.receiver.name, self.status)

    def get_result_string(self):
        return '{} {} - {} {}'.format(self.logged_team1_name, self.logged_team1_goals,
                                      self.logged_team2_name, self.logged_team2_goals)

    def get_request_sender_team(self):
        return self.request.sender

    def get_request_receiver_team(self):
        return self.request.receiver

    def add_to_queue(self):
        pass  # todo

    def run_game(self):
        pass  # todo

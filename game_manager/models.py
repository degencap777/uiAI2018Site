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

    sender = models.ForeignKey('user_panel.Team', on_delete=models.CASCADE, related_name='sent_game_requests')
    receiver = models.ForeignKey('user_panel.Team', on_delete=models.CASCADE, related_name='received_game_requests')
    status = models.CharField(max_length=8, choices=STATUS_OPTIONS, default=PENDING)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'REQ: {} vs {} - {}'.format(self.sender.name, self.receiver.name, self.status)

    def get_dict(self):
        return {
            'id': self.pk,
            'sender_id': self.sender.pk,
            'receiver_id': self.receiver.pk,
            'status': self.status,
            'date': self.date,
        }


class Game(models.Model):
    WAITING = 'WAITING'
    PLAYING = 'PLAYING'
    FINISHED = 'FINISHED'
    ERROR = 'ERROR'
    STATUS_OPTIONS = (
        (WAITING, 'در صف انتظار'),
        (PLAYING, 'در حال اجرا'),
        (FINISHED, 'پایان یافته'),
        (ERROR, 'خطا در اجرای بازی')
    )
    request = models.OneToOneField(GameRequest, on_delete=models.CASCADE)
    status = models.CharField(max_length=8, choices=STATUS_OPTIONS, default=WAITING)
    status_text = models.TextField(max_length=8192, blank=True, null=True)
    logged_team1_name = models.CharField(max_length=16, blank=True, null=True)
    logged_team2_name = models.CharField(max_length=16, blank=True, null=True)
    logged_team1_goals = models.IntegerField(blank=True, null=True)
    logged_team2_goals = models.IntegerField(blank=True, null=True)
    log_file = models.FileField(upload_to='logs', blank=True, null=True)
    token = models.CharField(max_length=64)

    def __str__(self):
        return 'GAME: {} vs {} - {}'.format(self.request.sender.name, self.request.receiver.name, self.status)

    def get_dict(self):
        return {
            'id': self.pk,
            'status': self.get_status_display(),
            'team1_name': self.logged_team1_name,
            'team1_goals': self.logged_team1_goals,
            'team2_name': self.logged_team2_name,
            'team2_goals': self.logged_team2_goals,
            'log_file': self.log_file.url if self.log_file is not None else '',
        }

    def get_result_string(self):
        return '{} {} - {} {}'.format(self.logged_team1_name, self.logged_team1_goals,
                                      self.logged_team2_name, self.logged_team2_goals)

    def get_request_sender_team(self):
        return self.request.sender

    def get_request_receiver_team(self):
        return self.request.receiver

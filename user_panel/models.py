import json
import os
import zipfile
import requests

from django.contrib.auth.password_validation import validate_password
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError

from uiai2018_site.settings import BASE_DIR
from user_panel import upload_filenames, validators
from game_manager import models as game_manager_models
from game_manager.server_api import get_best_server


class UserManager(BaseUserManager):
    def create_user(self, email, password, first_name, last_name, english_full_name, phone, institute):
        try:
            validate_password(password)
        except ValidationError:
            raise ValidationError('گذرواژه انتخاب شده به اندازه کافی امن نیست.')
        if User.objects.filter(email=email).count() == 1:
            raise ValidationError('کاربری با این ایمیل قبلاً ثبت‌نام کرده است.')
        validators.phone_number_validator(phone)
        validators.english_string_validator(english_full_name)
        validators.persian_name_validator(first_name)
        validators.persian_name_validator(last_name)
        user = self.model(
            email=str(email).lower(),
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            institute=institute,
            english_full_name=english_full_name,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, first_name, last_name, english_full_name, phone, institute):
        if User.objects.filter(email=email).count() == 1:
            raise ValidationError('کاربری با این ایمیل قبلاً ثبت‌نام کرده است.')
        user = self.model(
            email=str(email).lower(),
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            institute=institute,
            english_full_name=english_full_name,
        )
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractUser):
    username = None
    first_name = models.CharField(max_length=16)
    last_name = models.CharField(max_length=16)
    english_full_name = models.CharField(max_length=32)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=16)
    institute = models.CharField(max_length=64)
    team = models.ForeignKey('Team', on_delete=models.DO_NOTHING, related_name='members', blank=True, null=True)
    wants_dorm = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', 'english_full_name', 'institute']

    def __str__(self):
        return self.get_full_name()

    def get_dict(self):
        return {
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'english_full_name': self.english_full_name,
            'institute': self.institute,
            'phone': self.phone,
            'sent_invitations': [invitation.get_dict() for invitation in self.sent_invitations.all()],
            'received_invitations': [invitation.get_dict() for invitation in self.received_invitations.all()],
            'wants_dorm': self.wants_dorm,
        }


class Team(models.Model):
    name = models.CharField(max_length=16, unique=True, validators=[validators.team_name_validator])
    logo = models.ImageField(upload_to=upload_filenames.team_logo, default='default_team_logo.png')
    qualified = models.BooleanField(default=False)
    payment_amount = models.IntegerField(default=0)
    transaction_id1 = models.CharField(max_length=255, blank=True, null=True)
    transaction_id2 = models.CharField(max_length=255, blank=True, null=True)
    factor_number = models.CharField(max_length=255, blank=True, null=True)
    card_number = models.CharField(max_length=255, blank=True, null=True)
    trace_number = models.CharField(max_length=255, blank=True, null=True)
    payment_message = models.TextField(max_length=1024, blank=True, null=True)
    payment_verified = models.BooleanField(default=False)

    def get_member1(self):
        return self.members.all()[0] if self.members.count() > 0 else None

    def get_member2(self):
        return self.members.all()[1] if self.members.count() > 1 else None

    def get_member3(self):
        return self.members.all()[2] if self.members.count() > 2 else None

    def get_final_code(self):
        try:
            return self.uploaded_codes.get(is_final=True)
        except Code.DoesNotExist or Code.MultipleObjectsReturned:
            return None

    def get_games(self):
        return game_manager_models.Game.objects.filter(request__sender=self) | \
               game_manager_models.Game.objects.filter(request__receiver=self)

    def __str__(self):
        return self.name

    def get_dict(self):
        return {
            'name': self.name,
            'members': [member.email for member in self.members.all()[:3]],
            'uploaded_codes': [code.get_dict() for code in self.uploaded_codes.all()],
            'received_game_requests': [r.get_dict() for r in self.received_game_requests.filter(is_hidden=False)],
            'sent_game_requests': [r.get_dict() for r in self.sent_game_requests.filter(is_hidden=False)],
            'games': [g.get_dict() for g in self.get_games()],
            'qualified': self.qualified,
            'payment': {
                'verified': self.payment_verified,
                'factor_number': self.factor_number,
                'trace_number': self.trace_number,
                'message': self.payment_message,
            }
        }


class TeamInvitation(models.Model):
    PENDING = 'PENDING'
    ACCEPTED = 'ACCEPTED'
    REJECTED = 'REJECTED'
    STATUS_OPTIONS = (
        (PENDING, 'در انتظار'),
        (ACCEPTED, 'پذیرفته شده'),
        (REJECTED, 'رد شده'),
    )

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_invitations')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='invitations')
    status = models.CharField(max_length=8, choices=STATUS_OPTIONS, default=PENDING)

    def __str__(self):
        return '{} for {}'.format(self.receiver, self.team)

    def get_dict(self):
        return {
            'id': self.pk,
            'sender': self.sender.email,
            'receiver': self.receiver.email,
            'team_name': self.team.name,
            'status': self.get_status_display(),
        }


class Settings(models.Model):
    key = models.CharField(max_length=32, primary_key=True)
    value = models.TextField(max_length=8192)

    def __str__(self):
        return self.key

    class Meta:
        verbose_name = 'Settings'
        verbose_name_plural = 'Settings'


class Code(models.Model):
    PYTHON, JAVA, CPP = 'PYTHON', 'JAVA', 'CPP'
    LANGUAGE_OPTIONS = (PYTHON, JAVA, CPP)

    WAITING = 'WAITING'
    COMPILING = 'COMPILING'
    COMPILATION_OK = 'COMPILATION_OK'
    COMPILATION_ERROR = 'COMPILATION_ERROR'
    STATUS_OPTIONS = (
        (WAITING, 'در انتظار'),
        (COMPILING, 'در حال کامپایل'),
        (COMPILATION_OK, 'کامپایل موفق'),
        (COMPILATION_ERROR, 'خطای کامپایل'),
    )

    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='uploaded_codes')
    is_final = models.BooleanField(default=False)
    compilation_status = models.CharField(max_length=18, choices=STATUS_OPTIONS, default=WAITING)
    compile_status_text = models.TextField(max_length=8192, blank=True, null=True)
    code_zip = models.FileField(upload_to=upload_filenames.code_filename)
    language = models.CharField(max_length=6, choices=((l, l) for l in LANGUAGE_OPTIONS))
    upload_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}, {} @{}'.format(self.team.name, self.language, self.upload_timestamp)

    def get_dict(self):
        return {
            'id': self.pk,
            'team_name': self.team.name,
            'is_final': self.is_final,
            'compile_status': self.get_compilation_status_display(),
            'compile_status_text': self.compile_status_text,
            'code_download_url': self.code_zip.url,
            'language': self.language,
            'upload_time': self.upload_timestamp,
        }

    def get_extraction_path(self):
        return os.path.join(BASE_DIR, 'temp', 'compile', str(self.team.pk), str(self.pk))

    def extract(self):
        with zipfile.ZipFile(self.code_zip.path, "r") as z:
            z.extractall(self.get_extraction_path())

    def compile(self):
        data = {'id': self.pk, 'language': self.language}
        file = {'code': open(self.code_zip.path, 'rb')}
        server = get_best_server(for_compile=True)
        r = requests.post('{}/api/compile/request/'.format(server), data=data, files=file)
        self.compilation_status = r.json()['status']
        self.compile_status_text = r.json()['message']
        self.save()
        return self.compilation_status

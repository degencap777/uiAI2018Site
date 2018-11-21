import glob
import os
import subprocess
import zipfile

from django.contrib.auth.password_validation import validate_password
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError

from uiai2018_site.settings import BASE_DIR
from user_panel import upload_filenames, validators
from game_manager import models as game_manager_models


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
        }


class Team(models.Model):
    name = models.CharField(max_length=16, unique=True, validators=[validators.team_name_validator])
    logo = models.ImageField(upload_to=upload_filenames.team_logo, default='default_team_logo.png')

    def get_member1(self):
        return self.members.all()[0] if self.members.count() > 0 else None

    def get_member2(self):
        return self.members.all()[1] if self.members.count() > 1 else None

    def get_member3(self):
        return self.members.all()[2] if self.members.count() > 2 else None

    def get_final_code(self):
        return self.uploaded_codes.get(is_final=True)

    def get_games(self):
        return game_manager_models.Game.objects.filter(request__sender=self) | \
               game_manager_models.Game.objects.filter(request__receiver=self)

    def __str__(self):
        return self.name

    def get_dict(self):
        return {
            'name': self.name,
            'logo': self.logo.url,
            'members': [member.email for member in self.members.all()[:3]],
            'uploaded_codes': [code.get_dict() for code in self.uploaded_codes.all()],
            'received_game_requests': [r.get_dict() for r in self.received_game_requests.all()],
            'sent_game_requests': [r.get_dict() for r in self.sent_game_requests.all()],
            'games': [g.get_dict() for g in self.get_games()],
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
    code_zip = models.FileField(upload_to='codes')
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
        return os.path.join(BASE_DIR, 'codes', str(self.team.pk), str(self.pk))

    def extract(self):
        with zipfile.ZipFile(self.code_zip.path, "r") as z:
            z.extractall(self.get_extraction_path())

    def compile(self):
        if self.language == Code.PYTHON:
            self.compile_status_text = 'بدون نیاز به کامپایل'
            self.compilation_status = Code.COMPILATION_OK
            self.save()
        elif self.language == Code.JAVA:
            self.compilation_status = Code.COMPILING
            self.save()
            client_files = glob.glob(os.path.join(self.get_extraction_path(), '*.java'))
            subprocess.run(['rm', '-r', 'out'], cwd=self.get_extraction_path())
            subprocess.run(['mkdir', 'out'], cwd=self.get_extraction_path())
            p = subprocess.run(['javac'] + client_files + ['-d', 'out'], cwd=self.get_extraction_path(),
                               stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
            if p.returncode == 0:
                self.compilation_status = Code.COMPILATION_OK
                self.compile_status_text = 'کد جاوا شما با موفقیت کامپایل شد.'
                self.save()
            elif p.returncode == 2:
                self.compilation_status = Code.COMPILATION_ERROR
                self.compile_status_text = p.stdout.decode("utf-8")
                self.save()
        elif self.language == Code.CPP:
            client_files = glob.glob(os.path.join(self.get_extraction_path(), '*.cpp'))
            subprocess.run(['rm', 'out'], cwd=self.get_extraction_path())
            p = subprocess.run(['g++'] + client_files + ['-o', 'out'], cwd=self.get_extraction_path(),
                               stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
            if p.returncode == 0:
                self.compilation_status = Code.COMPILATION_OK
                self.compile_status_text = 'کد ++C شما با موفقیت کامپایل شد.'
                self.save()
            elif p.returncode == 1:
                self.compilation_status = Code.COMPILATION_ERROR
                self.compile_status_text = p.stdout.decode("utf-8")
                self.save()
        return self.compilation_status

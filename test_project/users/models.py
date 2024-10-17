from django.db import models
from django.contrib.auth.models import AbstractUser
from conferences.models import Conference
from django.core.validators import RegexValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
# Create your models here.

class Participant(AbstractUser):
    def email_validator(value):
        if not value.endswitch("@esprit.tn"):
            raise ValidationError('only @esprit.tn domain allowed')
    cin_validator=RegexValidator(regex=r'^\d{8}$',
                                 message="8 digits"
                                 )
    cin=models.CharField(primary_key=True,max_length=8,validators=[cin_validator])
    email=models.EmailField(unique=True,max_length=255,validators=[email_validator])
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
 
    username=models.CharField(max_length=100,unique=True)
    USERNAME_FIELD='username'
    
    CHOICES=(
        ('etudiant','etudiant'),
        ('chercheur','chercheur'),
        ('docteur','docteur'),
        ('enseignant','enseignant')
        
    )
    participant_category=models.CharField(max_length=255, choices=CHOICES)
    reservations=models.ManyToManyField(Conference,through='Reservation',related_name='reservations')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural='participants'
    
    def __str__(self):
        return f"paticipant cin {self.cin} "
    
    
class Reservation(models.Model):
    conference=models.ForeignKey(Conference,on_delete=models.CASCADE)
    participant=models.ForeignKey(Participant,on_delete=models.CASCADE)
    confirmed=models.BooleanField(default=False)
    reservation_date=models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together=('conference','participant')
        verbose_name_plural='reservations'
    def clean(self):
        if self.conference.end_date > self.conference.start_date:
            raise ValidatorError('you can only reserve for upcoming confrences')
        reservation_count=Reservation.objects.filter(
            participant=self.participant,
            reservation_date__date=timezone.now.date()
        )
        if len(reservation_count)>=3:
            raise ValidationError('only 3 reservations per day')
        
    def __str__(self):
        return f"reservation conference {self.conference} participant {self.participant} "
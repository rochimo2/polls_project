import datetime
from django.forms import ModelForm, DateTimeField
from django.db import models
from django.utils import timezone
from django import forms

#5 de febrero
from django.urls import reverse


#from django.utils.encoding import python_2_unicode_compatible
# Create your models here.
class QuestionManager(models.Manager):
    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

class Question(models.Model):
    question_text = models.CharField("ingrese pregunta", max_length=200)
    pub_date = models.DateTimeField('fecha de publicacion')

    objects = QuestionManager()

    def __str__(self):
        return self.question_text


    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Publicado recientemente?'

# class Question(models.Model):
#     question_text = models.CharField("ingrese pregunta", max_length=200)
#     pub_date = models.DateTimeField('fecha de publicacion')

#     def get_absolute_url(self):
#         return reverse('choice_update_form', kwargs={'pk' : self.pk})


#     def was_published_recently(self):
#         now = timezone.now()
#         return now - datetime.timedelta(days=1) <= self.pub_date <= now
#     was_published_recently.admin_order_field = 'pub_date'
#     was_published_recently.boolean = True
#     was_published_recently.short_description = 'Publicado recientemente?'


# class ChoiceManager (models.Manager):
#     def get_choice(self):
#         qs = self.get_choice
#         if qs.count() == 0:
#             return "error message"

class ChoiceManager(models.Manager):
    def DoesNotExist(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 0:
            return None
        return qs

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    DoesNotExist = ChoiceManager()

    def __str__(self):
        return self.choice_text


# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)

#     def get_absolute_url(self):
#         return reverse('index', kwargs={'pk' : self.pk})

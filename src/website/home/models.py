from django.db import models
from django.contrib.auth.models import User

from home.util import *

TEST = 1
FINAL = 10


class SubManager(models.Manager):
  use_for_related_fields = True

  def most_recent(self):
    return self.all()[:5]
  
  def all(self):
    return self.order_by('tstamp')


class Submission(models.Model):
  objects = SubManager()

  user = models.ForeignKey(User, related_name="submissions")
  text = models.CharField(max_length=4280, null=False)
  score = models.FloatField(null=False)
  submit_type = models.IntegerField(default=TEST)
  tstamp = models.DateTimeField(auto_now_add=True)

  @property
  def score_str(self):
    return str(self.score)[:5]

  @property
  def prediction(self):
    return parse(self.text)



class VisSubmission(models.Model):

  user = models.ForeignKey(User, related_name="vis_submissions")
  url = models.CharField(max_length=1280, null=False)
  tstamp = models.DateTimeField(auto_now_add=True)

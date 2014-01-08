import django.forms as forms
from django.forms import *
from home.models import *
from registration.forms import *
from home.util import *

# submit_type:
# 1 = initial test
# 2 = final test

class SubmitForm(Form):

  text = forms.CharField(widget=forms.Textarea, 
      initial="Copy and paste your submission contents here")
  submit_type = forms.IntegerField(widget=forms.HiddenInput,
      initial=1)

  def clean_text(self):
    data = self.cleaned_data['text']
    try:
      prediction = parse(data)
      print prediction
      print CORRECT_DEMANDS

      score = compute_score(prediction)
      self.cleaned_data['score'] = score
    except Exception as e:
      raise forms.ValidationError("Could not parse submission.  Error: %s" %str(e))

    return data


  def clean_submit_type(self):
    self.cleaned_data['submit_type'] = self.cleaned_data.get('submit_type', 1)
    return self.cleaned_data['submit_type']

  def save(self, user):
    submission = Submission(
      user = user,
      text = self.cleaned_data['text'],
      score = self.cleaned_data['score'],
      submit_type = self.cleaned_data['submit_type']
    )
    submission.save()
    return submission


class FinalSubmitForm(Form):

  text = forms.CharField(widget=forms.Textarea, 
      initial="Copy and paste your submission contents here")
  submit_type = forms.IntegerField(widget=forms.HiddenInput,
      initial=2)

  def clean_text(self):
    data = self.cleaned_data['text']
    try:
      prediction = parse(data)
      print prediction

      # score = compute_score(prediction)
      # don't compute scores
      score = -1

      self.cleaned_data['score'] = score
    except Exception as e:
      raise forms.ValidationError("Could not parse submission.  Error: %s" %str(e))

    return data


  def clean_submit_type(self):
    self.cleaned_data['submit_type'] = self.cleaned_data.get('submit_type', 2)
    return self.cleaned_data['submit_type']

  def save(self, user):
    submission = Submission(
      user = user,
      text = self.cleaned_data['text'],
      score = self.cleaned_data['score'],
      submit_type = self.cleaned_data['submit_type']
    )
    submission.save()
    return submission




class VisForm(Form):
  url = forms.URLField()

  def save(self, user):
    s = VisSubmission(
        user = user,
        url = self.cleaned_data['url']
    )
    s.save()
    return s



The prediction challenge will XXX.  We will provide a training
dataset for you to construct models.  Then on YYY date we will
release an initial test dataset and provide N locations, specified
by lat, lon bounding boxes and a time window, for you to predict
the number of taxi routes initiated within the window.  You can
[submit](#submit) predictions for this dataset as many times as you
wish, and we will provide a leaderboard that updates your score on
each submission to track contestant progress against each other.
The initial test dataset is for validation purposes only and has
no effect on the final evaluation.

In the last week of the competition, we will release the final test
dataset for which contestants will be ultimately compared.  You may
submit as many times as you wish but the final scores will be release
only at the end of the competition.

# Rules

### One account per participant

### No sharing data 

### Don't try to deanonymize the data

### Team limits

There is not limit to your team size.

### Submission limits

Please don't DDOS the submission form.

# Submissions

## Submission Format

Each line contains the following information

<pre>    
    [location id]<SPACE>[number]
</pre>


The following example specifies that location 1 has demand 99, 2 has demand 105, and 3 has demand 209.

<pre>    
    1 99
    2 105
    3 209
</pre>


To clarify, we will use the following python program to parse your submission

<pre>    
    def parse(submission):
      """
      ARGS:
        submission is as string

      RETURN:
        dictionary of location -> demand number 
      """
      demands = {}
      try:
        lines = submission.split("\n")
        for line in lines:
          tokens = line.split(" ")
          locid = int(tokens[0])
          demand = int(tokens[1])
          demands[locid] = demand
      except:
        return {}
</pre>

## Make a submission

The final submission form will appear in the last week of competition.  You can use the form below to test your predictions.

<form action="/submit/" method="post">
  <textarea name="submission">Copy and paste your submission contents here</textarea>
  <button>submit</button>
</form>



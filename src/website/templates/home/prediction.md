# Rules

### One account per participant

### No sharing data 

### Don't try to deanonymize the data

Please don't

### Team limits

None

### Submission limits

Please don't DDOS us

# Submissions

## Submission Format

Each line contains the following information


    [location id]<SPACE>[number]


The following example specifies that location 1 has demand 99, 2 has demand 105, and 3 has demand 209.


    1 99
    2 105
    3 209


To clarify, we will use the following python program to parse your submission
    

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




## Make a submission

The final submission form will appear in the last week of competition.  You can use the form below to test your predictions.

<form>
  <textarea>Copy and paste your submission contents here</textarea>
  <button>submit</button>
</form>



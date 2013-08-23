

CORRECT_DEMANDS = {
  1: 90,
  2: 100, 
  3: 205
}


def compute_score(demands, correct_demands=None):
  if not correct_demands:
    correct_demands = CORRECT_DEMANDS
  sqerrs = []
  for key in correct_demands:
    trueval = correct_demands[key]
    if key in  demands:
      estval = demands[key]
      sqerrs.append(float(trueval - estval) ** 2)

  return sum(sqerrs) ** 0.5

def parse(text=""):
  """
  ARGS:
  text is a the submission as a string

  RETURN:
  dictionary of location -> demand number 
  """
  demands = {}
  try:
    lines = text.split("\n")
    for line in lines:
      line = line.strip()
      if not line: continue
      tokens = line.split(" ")
      locid = int(tokens[0])
      demand = int(tokens[1])
      demands[locid] = demand
    return demands
  except:
    return {}

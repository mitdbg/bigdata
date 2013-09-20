

CORRECT_DEMANDS = {
  1: 90,
  2: 100, 
  3: 205
}

CORRECT_DEMANDS = {
0 :  25 ,
1 :  6  ,
2 :  6  ,
3 :  49 ,
4 :  7  ,
5 :  36 ,
6 :  137,
7 :  0  ,
8 :  24 ,
9 :  7  ,
10:  42 ,
11:  44 ,
12:  45 ,
13:  74 ,
14:  7  ,
15:  15 ,
16:  0  ,
17:  17 ,
18:  49 ,
19:  35 ,
20:  41 ,
21:  0  ,
22:  6  ,
23:  120,
24:  6  ,
25:  22 ,
26:  85 ,
27:  3  ,
28:  50 ,
29:  51 ,
30:  0  ,
31:  12 ,
32:  2  ,
33:  2  ,
34:  39 ,
35:  50 ,
36:  52 ,
37:  1  
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

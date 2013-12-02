

CORRECT_DEMANDS = {
  1: 90,
  2: 100, 
  3: 205
}

TEST1_COUNTS = """0 9
1 0
2 80
3 46
4 20
5 41
6 125
7 79
8 0
9 85
10 4
11 13
12 19
13 64
14 41
15 54
16 1
17 0
18 89
19 103
20 57
21 106
22 21
23 86
24 41
25 72
26 60
27 174
28 43
29 0
30 145
31 59
32 37
33 19
34 33
35 1
36 2
37 56
38 24
39 15
40 38
41 102
42 45
43 0
44 51
45 0
46 4
47 16
48 29
49 8
50 66
51 5
52 0
53 39
54 50
55 49
56 53
57 0
58 53
59 18
60 41
61 25
62 10
63 11
64 0
65 59
66 1
67 10
68 0
69 0
70 14
71 1"""

CORRECT_DEMANDS = {}
for pair in map(lambda line: map(int, line.split()), TEST1_COUNTS.split('\n')):
  CORRECT_DEMANDS[pair[0]] = pair[1]





# worry about giant ints
def compute_score(demands, correct_demands=None):
  if not correct_demands:
    correct_demands = CORRECT_DEMANDS

  sqerrs = []
  for key in correct_demands:
    trueval = correct_demands[key]
    estval = demands.get(key, 0)
    err = float(trueval - estval) ** 2
    sqerrs.append(err)

  return 1. / (1. + sum(sqerrs) ** 0.5)

def parse(text=""):
  """
  ARGS:
  text is a the submission as a string

  RETURN:
  dictionary of location -> demand number 
  """
  demands = {}
  lines = text.split("\n")
  for line in lines:
    line = line.strip()
    if not line: continue
    tokens = line.split(" ")
    locid = int(tokens[0])
    demand = int(tokens[1])
    demands[locid] = demand
  return demands

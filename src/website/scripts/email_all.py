from header import *
from django.core.mail import send_mail, send_mass_mail

subject = "Updates to the datasets"
text = """Dear %s,

We have extended the provided datasets: 

* the dropoff data now spans from May to the end of November.  
* The weather data now goes to the end of the year.  
* Finally, we added the list of locations that the prediction challenge asks you to predict.  

All of these can be downloaded on the datasets page.

Thank you,
MIT Big Data Challenge
"""

subject = "Final prediction locations released"
text = """Dear %s,

We have released the ground truth for the inital prediction test.  You
can download it in the /datasets page.

We have also released the locations and the submission form for the final
prediction challenge.  Please note that scores for the final submissions
will not be revealed until the end of the challenge.

Thank you,
MIT Big Data Challenge
"""



datas = []
for user in User.objects.all():
  msg = text % user.username
  email = (subject, msg, "bigdatachallenge@gmail.com", (user.email,))
  datas.append(email)
totaln = len(datas)

print "email:   %s" % datas[0][3]
print "subject: %s" % datas[0][0]
print 
print "message:"
print datas[0][1]

send = False
if len(sys.argv) > 1:
  if sys.argv[1] == 'send':
    raw_input("mass sending to %s?  ctrl-c to abort!" % len(datas))
    send = True


if send:
  for n, data in enumerate(datas):
    try:
      print "sending to %d of %d: %s" % (n, totaln, data[3][0])
      send_mail(*data, fail_silently=False)
    except Exception as e:
      print "error %s " % e

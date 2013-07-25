MIT CSAIL Big Data Challenge
======================


[BigData@CSAIL](http://bigdata.csail.mit.edu) MIT and the City of
Boston are hosting a big data challenge seeking to develop innovative
prediction alogirthms and compelling visualizations of transportation
data around the Boston area.

The competition will run from XXX to YYY and is split into
[prediction](#prediction) and [visualization](#visualization)
challenges, each with prizes.


The competition is open to students from the MIT community There is a $1,000
prize that will be awarded to the team that can most accurately predict
ridership at a randomly selected set of locations based on the test data.



<a name="prediction" href="prediction"> Prediction Challenge</a>
============

Some paragraphs describing the problem and what is interesting.

## Objective

TODO: think about the specifics of the prediction result, and the model inputs
(discretized?  in what way?

The goal is to predict the demand (expected number of taxi rides given) for
taxis along all blocks within a 0.5 mile radius of a specific latitude,
longitude location in Boston during in a particular time window discretized to
30 minute time windows  (e.g., between 11:00pm and 2:30am on April 15, 2013
around Downtown Crossing), given the current events from that day, the
locations of major stores and venues, and the tweet stream leading up to the
time period.

We have collected XXX months worth of data (see below for descriptions
of the datasets).  We will provide XXX weeks worth of training data
and draw the test data randomly from XXX weeks of data.


[Click here for more details and to participate](/prediction)


<a name="visualization" href="visualization"> Visualization Challenge</a>
===============

Describe the audience for the vis and why it's worth participating in. 

## Objective

The goal is to visualize the data in an informative, beautiful, or
surprising way that illustrates taxi ridership in Boston and its
relationship to nearby events and locales.

We will have a judging panel consisting of visualization experts, data
scientists, and leaders from the city of Boston's transportation departments.

[Click here for more details and to participate](/visualization)

Prizes
=======

Prediction Challenge: $1000 Grand Prize, $500 Runner Up

Visualization Challenge:  $1000 Grand Prize, $500 Runner Up


The Datasets
==========

We will provide the following datasets of data from June and July or 2013.  Participants are allowed and encouraged to
find and use additional datasets, with the stipulation that the datasets are publically 
accessible.


* **Boston taxi cab data**: Every trip starting from Boston proper.  Includes start and end datetime, street address (if available) and lat/lon coordinates.
* **Local Events data**: Every Boston event.  Provided by Goby.
* **Tweet stream**: Every geocoded tweet originating from the Boston area.
* **MBTA data**: Every charlie card swipe.
* **Weather data**: Hourly weather information.


Partners
============

City of Boston

Goby

CMTdata

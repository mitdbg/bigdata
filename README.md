Lessons Learned
=================

* Check timezones when picking final submission cutoffs!
* Make sure each team only submits one account
* Make sure visualizations are still up


MIT CSAIL Big Data Challenge
======================

Late June Summer 2013, for one month

The challenge is hosted by BigData@CSAIL [http://bigdata.csail.mit.edu] and
seeks to develop innovative prediction algorithms and compelling visualizations
about transportation data from the City of Boston.

Prediction Challenge
============

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

The competition is open to students from the MIT community There is a $1,000
prize that will be awarded to the team that can most accurately predict
ridership at a randomly selected set of locations based on the test data.

Visualization Challenge
===============

TODO: who is the audience for the viz?

The goal is to visualize the data in an informative, beautiful, or
surprising way that illustrates taxi ridership in Boston and its
relationship to nearby events and locales.

We will have a judging panel consisting of visualization experts, data
scientists, and leaders from the city of Boston's transportation departments.


Prizes
=======

Prediction Challenge: $1000 Grand Prize, $500 Runner Up

Visualization Challenge:  $1000 Grand Prize, $500 Runner Up


The Datasets
==========

TODO

* describe the datasets in more detail
* goal: may to june data
* use your own data?  needs to be public?

.

* **MBTA demand**
* **Boston taxi cab data**: All
* **MBTA ridership**:
* **Local events data**: Boston events information (location, event type, description, category, etc)
* **Commercial venue data**: categorization and descriptions of all Boston commercial venues, including GPS locations.
* **Tweet stream**: all geocoded tweets within the Greater Boston area.
* **Points of Interest**: collection of venues that have been labeled as "interesting" points.
* **Hourly weather data**: temperature, temperature with wind chill, rain/shine/snow

<div style="position:absolute; top:0; z-index:2"> 
<h1> MIT Big Data Challenge </h1>
</div>


xxx

[BigData@CSAIL](http://bigdata.csail.mit.edu) and the City of
Boston are hosting a big data challenge seeking to develop innovative
prediction algorithms and compelling visualizations of taxi cab trips in the Boston area.

## Motivation for the Challenge
 The City of Boston is interested in gaining new insights into how people use public transportation to travel in and around the downtown Boston area.  With urban congestion on the rise, city planners are looking for ways to improve transportation such as providing people with more options to get from one place to another (walking, biking, driving, or using public transit) and by reducing and more efficiently routing vehicles in the city.

This MIT Big Data Challenge will focus on one mode of public transportation: Taxi Cabs.  Have you ever noticed that cabs are never around when you need them?  By better understanding patterns in taxi ridership, we hope to provide new insights for city planners, such as:

* How get more cabs where they are needed, when they are needed?  
* What are the ideal locations for cab stands? 
* When should the City add or remove cab stands?  
* How many cabs should be waiting around a specific location? 
* Are there viable alternatives to taking a cab? 
* How does taxi ridership patterns differ on weekdays vs. weekends?

This Big Data Challenge provides a unique opportunity to analyze City of Boston taxi data (XXXX taxi rides) and to combine multiple data sets including social media data, transit ridership, events data and weather data to effectively predict demand and better understand patterns in taxi ridership.  We hope this will result in new insights for the City of Boston and the public that whill improve transportation in our city (and the ability to get a cab when you need one)!


## Competition Overview

The competition is open to individuals or teams.  The only requirement is that one team member must be a member of the MIT community (have an Athena account and MIT certificates).

The competition will run from XXX to YYY and focuses on two tasks, prediction and visualization, with separate prizes in each category:

* _Prediction Challenge_:  Here the goal is to predict the number of taxi trips originating at different times of day from different locations around city.   A total of $5000 will be awarded (a $4000 winner and a $1000 runner-up).

* _Visualization Challenge_:  Here the goal is to produce the most compelling visualization (static, animated or interactive) of taxi activity in Boston. A total of $5000 will be awarded (a $4000 winner and a $1000 runner-up).


# <a name="prediction" href="prediction"> Prediction Challenge</a>

The goal of this challenge is to predict taxi demand (total # of taxi trips) in downtown Boston based on historical taxi data and other related data sets (weather, events, social media data).   Demand prediction will be within a specified (0.1 mile) radius of key locations in Boston during a specified half hour time window  (e.g., between 11 and 11:30pm on March 15, 2013 at the intersection of Summer St and Tremont St.).   The prize will be awarded to the team that most accurately predicts (with minimum mean-squared error) ridership at a provided  set of test locations based on the test data.

We have collected XXX months worth of data (see below for descriptions
of the datasets).  We will provide XXX weeks worth of training data
and draw the test data randomly from XXX weeks of data.


[Click here for more details and to participate](/prediction)


# <a name="visualization" href="visualization"> Visualization Challenge</a>

The goal is to visualize the taxi  data in an informative, beautiful, or surprising way.  We are particularly interested in visualizations that contrast or compare taxi/public transportation ridership in Downtown and relate them  to nearby events and locales.  Visualizations may include maps, animations or static graphics and ideally should reveal new or interesting trends and patterns.
We will have a judging panel consisting of visualization experts, data
scientists, and leaders from the city of Boston's transportation departments.

[Click here for more details and to participate](/visualization)


# The Datasets

We provide the following datasets on [this page](/datasets):

* **Boston taxi cab data**: Every trip starting from Boston proper.  Includes start and end datetime, street address (if available) and lat/lon coordinates.
* **Local Events data**: Every Boston event.  Provided by Goby.
* **Tweet stream**: Every geocoded tweet originating from the Boston area.
* **MBTA data**: Every charlie card swipe.
* **Weather data**: Hourly weather information.


Participants are allowed and encouraged to find and use additional datasets, with the stipulation that the datasets are publicly  accessible.


Partners
============

We are especially grateful to  our data parters who made this challenge possible.
These include:

City of Boston

CMTdata

Goby

MBTA

Twitter

# Judging Panel

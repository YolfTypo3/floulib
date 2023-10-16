=======
Floulib
=======

.. PyPI badge

.. image:: https://badge.fury.io/py/floulib.svg
   :alt: PyPI version
   :target: https://pypi.org/project/floulib/
    
.. Documentation at RTD — https://readthedocs.org

.. image:: https://readthedocs.org/projects/floulib/badge/?version=latest
   :alt: Documentation Status
   :target: https://floulib.readthedocs.io/en/latest/
   
Floulib is a library for fuzzy logic which was designed to implement 
exercices proposed in the second edition of the book in French "Logique floue : exercices corrigés" 
by Bernadette Bouchon-Meunier, Laurent Foulloy, Mohammed Ramdani, Cépadues-Editions.

It implements many operations on fuzzy subsets including representations of 
membership functions (discrete, triangle, trapezoid, multilinear, LR), operations on membership functions, rules, inference,
fuzzification, defuzzification, transformations of probability
distributions into possibility distributions (optimal transformation for unimodal symmetric distributions, 
two-side normalized transformation for other unimodal distributions) and many other features.

Floulib was designed for learning and teaching applications. 
Simplicity of use was sometimes sought to the detriment of performances.

Example
=======

The following exercice is provided to give a short overview of floulib.
See the API reference for other examples: https://floulib.readthedocs.io

Exercice
--------
 
1) John works in Paris and takes the subway for ten stops every morning.
In Paris, the approximate travel time is 1.3 minutes per station  
with a minimum of 1 minute per station and a maximum of 1.5 minutes per station.
John leaves his house at *about 8:35*, where *about h* is defined by a triangular membership function 
whose support is [*h* - 5 minutes, *h* + 5 minutes] and whose kernel is [*h*]. The walk from his house 
to the subway and from the subway to his office takes *about 10 minutes* longer where *about w* is modeled 
by a triangular membership function whose support is [*w* - 1 minute, *w* + 1 minute] and whose kernel is [*w*].

John has a one-hour meeting every day that starts at *about 9:00* where *about t* means
that it never starts before *t* but it is certain that the meeting started at *t* + 10 minutes.

What is the possibility and certainty that John will be on time for the meeting ?

2) Over several months, John noted the time he left the house, as well as his travel and walking times.
He found that the first can be modeled by a Gaussian distribution with a mean of 8:45 and a
standard deviation of 1.5 minutes. The second can be modeled by a Gaussian distribution with a mean of
12 minutes and a standard deviation of 0.7 minutes. The third can be modeled by a Gaussian distribution with a mean of
10 minutes and a standard deviation of 0.3 minutes.

What is the possibility and certainty that John will be on time for the meeting ?

Imports and special function
----------------------------

.. code:: python

    >>> from floulib import DistToPiMultilinear, Triangle, Multilinear
    >>> from datetime import timedelta
    >>> from scipy.stats import norm
    >>> import math

    >>> # Converts the labels to time
    >>> def convert_to_time(ax):
    >>>     labels = []
    >>>     xticks = ax.get_xticks()
    >>>     for xtick in xticks:
    >>>         labels.append('{:02d}:{:02d}'.format(int(xtick) // 60, int(xtick) % 60))
    >>>     ax.set_xticks(xticks, labels)

Question 1
----------

.. code:: python

    >>> # Defines the departure in minutes.
    >>> departure_schedule = timedelta(hours=8, minutes=35).total_seconds() // 60
    >>> departure1 = Triangle(departure_schedule - 5, departure_schedule, departure_schedule + 5)

    >>> # Defines the travel time in minutes
    >>> travel1 = Triangle(10, 13, 15)

    >>> # Defines the walking time in minutes
    >>> walking1 = Triangle(9, 10, 11)

    >>> # Computes the arrival time in minutes
    >>> arrival1 = departure1 + travel1 + walking1

    >>> # Defines the meeting schedule in minutes
    >>> meeting_schedule = timedelta(hours=9, minutes=10).total_seconds() // 60

    >>> # Defines the before meeting event
    >>> before_meeting = Multilinear(
            (0, 1),
            (meeting_schedule - 10, 1),
            (meeting_schedule, 0),
            (meeting_schedule + 60, 0)             
        )

    >>> # Plots memberships and displays the result
    >>> ax = before_meeting.plot(xlim = [520, 560], label = 'Before meeting').add_plot(arrival1, label = 'Arrival').ax
    >>> convert_to_time(ax)
    >>> print(f'PI(before _meeting, arrival) = {before_meeting.possibility(arrival1)}')
    >>> print(f'N(before _meeting, arrival) =  {before_meeting.necessity(arrival1)}')
    PI(before _meeting, arrival) = 1.0
    N(before _meeting, arrival) =  0.6666666666666714

.. image:: images/Example.question1.png
   :align: center
    
Question 2
----------

.. code:: python

    >>> # Defines the departure in minutes.
    >>> mean1 = departure_schedule
    >>> sigma1 = 1.5

    >>> # Defines the travel time in minutes
    >>> mean2 = 12
    >>> sigma2 = 0.7

    >>> # Defines the walking time in minutes
    >>> mean3 = 10
    >>> sigma3 = 0.3

    >>> # Defines the arrival time in minutes
    >>> # Events are independent, the arrival is a gaussian distribution
    >>> # with a mean equal to the sum of the means and the variance equals
    >>> # to the sum of the variance
    >>> mean4 = mean1 + mean2 + mean3
    >>> sigma4 = math.sqrt(sigma1**2 + sigma2**2 + sigma3**2)
    >>> normal_dist4 = norm(mean4, sigma4)
    >>> # Transforms the probability distribution into a possibility distribution
    >>> # using the multilinear approximation of the optimal transformation
    >>> arrival2 = DistToPiMultilinear(normal_dist4, mean4, 4*sigma4, 0.05)

    >>> # Plots memberships and displays the result
    >>> ax = before_meeting.plot(xlim = [520, 560], label = 'Before meeting').add_plot(arrival2, label = 'Arrival').ax
    >>> convert_to_time(ax)
    >>> print(f'PI(before _meeting, arrival) = {before_meeting.possibility(arrival2)}')
    >>> print(f'N(before _meeting, arrival) = {before_meeting.necessity(arrival2)}')
    PI(before _meeting, arrival) = 1.0
    N(before _meeting, arrival) = 0.9553095603664303    
        
.. image:: images/Example.question2.png    
   :align: center
       
Requirements
============

Floulib requires

* matplotlib
* numpy
* scipy
* shapely

Installing Floulib
==================

We recommend installing Floulib using one of the available built
distributions, for example using ``pip``:

.. code-block:: console

    $ pip install floulib  
    
In case of error you may have to install Shapely first.

.. code-block:: console

    $ pip install shapely
    $ pip install floulib
    
Support
=======

Bugs may be reported at https://github.com/YolfTypo3/floulib/issues.  

Copyright & License
===================

Floulib is licensed under GNU General Public License.   
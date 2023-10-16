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

Documentation
=============

See https://floulib.readthedocs.io.
       
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
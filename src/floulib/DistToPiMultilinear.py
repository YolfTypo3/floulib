# -*- coding: utf-8 -*-
"""
Created on Mon May  8 03:17:27 2023

@author: Laurent Foulloy
"""

from floulib.DistToPi import DistToPi
from floulib.Multilinear import Multilinear
from scipy.integrate import quad
from scipy.optimize import minimize_scalar
import numpy as np


class DistToPiMultilinear(Multilinear):
    """
    This class contains methods to approximate the optimal transformation
    of unimodal symmetric probability distributions into possibility distributions as
    multilinear fuzzy subsets.
    
    The optimal transformation of a unimodal symmetric probability distribution
    is a convex possibility distribution with respect to each side of the mode.The 
    surface under the possibility distribution is also convex. A 
    recursive algorithm can be used to compute a multilinear approximation of the 
    possibility distribution.
    
    .. note::
    
        DistToPiMultilinear is a subclass of :class:`Multilinear`, therefore all methods 
        in :class:`Multilinear` may be used. 
            
        Multilinear is a subclass of :class:`Plot`, therefore all methods 
        in :class:`Plot` may also be used.      
    
    """

    def __init__(self, dist, mode, scale, epsilon):
        """
        Constructor

        Parameters
        ----------
        dist : TYPE
            The probability distribution.
        mode : float
            The mode.
        scale : float
            The scale.
        epsilon : float
            The approximation error.

        Returns
        -------
        None.
        
        
        Example
        -------
        >>> from floulib import DistToPiMultilinear
        >>> import numpy as np
        >>> from scipy.stats import norm
        >>> mean = 0
        >>> sigma = 1
        >>> normal_dist = norm(mean, sigma) 
        >>> DistToPiMultilinear(normal_dist, mean, 4*sigma, 0.1).plot()
        
        .. image:: images/DistToPiMultilinear.__init__.png          
           
        """
        self.dist = dist
        self.mode = mode
        self.scale = scale
        self.epsilon = epsilon      
        self.points = self._multilinear_points()
        self._bounds = [self.points[0][0], self.points[-1][0]]
        self._universe = None  
  


    def pi_opt(self, x = None):
        """
        Computes the optimal possibility distribution

        Parameters
        ----------
        x : numpy.ndarray, optional
            The points where the optimal distribution is computed.
            The default is None.

        Returns
        -------
        DistToPi | Discrete
            The optimal possibility distribution (as a discrete fuzzy
            subset if x is not None).

        """
        if x is None:
            return DistToPi(self.dist)
        else: 
            return (DistToPi(self.dist))(x)
        


    def dpi(self, x):
        """
        Computes the possibility distribution for x.

        This method can be used as an interface with other libraries. 

        Parameters
        ----------
        x : numpy.ndarray
            The array of points.
            
        Returns
        -------
        y : numpy.ndarray
            The array of points.


        Example
        -------
        >>> from floulib import DistToPiMultilinear
        >>> import numpy as np
        >>> from scipy.stats import norm
        >>> import matplotlib.pyplot as plt
        >>> mean = 0
        >>> sigma = 1
        >>> normal_dist = norm(mean, sigma)
        >>> x = np.linspace(mean - 4*sigma, mean + 4*sigma, 1000)
        >>> fig, ax = plt.subplots()
        >>> ax.plot(x, DistToPiMultilinear(normal_dist, mean, 4*sigma, 0.1).dpi(x))
            
        .. image:: images/DistToPiMultilinear.dpi.png           
        """
        y = np.zeros_like(x) 
        for i in range(len(self.points)-1):
            slope = (self.points[i + 1][1] - self.points[i][1])/(self.points[i + 1][0] - self.points[i][0])
            intercept = self.points[i][1] - slope * self.points[i][0]
            indices = (self.points[i][0] <= x) & (x <= self.points[i + 1][0])
            y[indices] = x[indices]*slope + intercept
        return y   


             
    # Special method to represent the points in human-readable format 
    def print(self, display = 'all', format = '.3f'):
        """
        Special method to represent the points of the approximation
        in human-readable format

        Parameters
        ----------
        display : str , optional
            If display is 'left' or 'right', the approximation points
            for the LHS or the RHS with respect to the mode are displayed.
            The default is 'all'.
        format : str, optional
            The format for the display. The default is '.3f'.

        Returns
        -------
        None.
        
        Example
        -------
        >>> from floulib import DistToPiMultilinear
        >>> import numpy as np
        >>> from scipy.stats import norm
        >>> mean = 0
        >>> sigma = 1
        >>> normal_dist = norm(mean, sigma) 
        >>> DistToPiMultilinear(normal_dist, mean, 4*sigma, 0.1).print()
        -4.000 0.000
        -4.000 0.000
        -2.341 0.019
        -1.524 0.128
        -1.163 0.245
        -0.815 0.415
        -0.460 0.646
        0.000 1.000
        0.460 0.646
        0.815 0.415
        1.163 0.245
        1.524 0.128
        2.341 0.019
        4.000 0.000
        4.000 0.000


        """
        if display == 'left':
            start = 0
            stop = len(self.points)//2 + 1
        elif display == 'right': 
            start = len(self.points)//2
            stop = len(self.points)   
        else:
            start = 0
            stop = len(self.points)
        for i in range(start, stop):
            print(('{0:' + format + '} {1:' + format + '}').format(self.points[i][0], self.points[i][1]))
   
    
   
    ###
    # Private methods
    #    
    
    # Approximates the distribution
    def _approximate(self, a, b, epsilon):
        def surface(y):
            return (self.pi_opt().dpi(a)+self.pi_opt().dpi(y))*(y-a)/2.0 + (self.pi_opt().dpi(y)+self.pi_opt().dpi(b))*(b-y)/2.0
            
        e = (self.pi_opt().dpi(a) + self.pi_opt().dpi(b))*(b-a)/2.0 - quad(self.pi_opt().dpi, a, b)[0]
        if e < epsilon:
            return [(b, self.pi_opt().dpi(b))]
        else:
            y_min = minimize_scalar(surface, bounds=(a, b), method='Bounded').x
            return self._approximate(a, y_min, epsilon/2.0) + self._approximate(y_min, b, epsilon/2.0)




    # Computes the points of the multilinear approximation
    def _multilinear_points(self):
        points = self._approximate(self.mode, self.mode + self.scale, self.epsilon/2.0)
        points = points + [(points[-1][0] + 1e-9, 0)]
        sym_points = []
        for i in range(len(points)):
            sym_points = [(2*self.mode-points[i][0], points[i][1])] + sym_points
        return sym_points + [(self.mode, 1.0)] + points      
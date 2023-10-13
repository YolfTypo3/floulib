# -*- coding: utf-8 -*-
"""
Created on Mon May  8 03:17:27 2023

@author: Laurent Foulloy
"""

from floulib.Multilinear import Multilinear
import numpy as np
              

class LR(Multilinear):
    """
    Contains various methods to perform operations on LR (Left-Right)
    fuzzy intervals, with L(x) = R(x) = max(0, 1-x).
    
    .. note::
        
        LR is a subclass of :class:`Multilinear`, therefore all methods 
        in :class:`Multilinear` may be used. 
        
        Multilinear is a subclass of :class:`Plot`, therefore all methods 
        in :class:`Plot` may also be used.        
    
    """
    def __init__(self,  *args, label = '', color = None):
        """
        Constructor

        Parameters
        ----------
        *args : float
        
            With four positional arguments, the LR fuzzy interval is 
            trapezoidal
            
            - args[0] is m
            - args[1] is m_prime
            - args[2] is a
            - args[3] is b
            
            With three positional arguments, the LR fuzzy interal is
            triangular
            
            - args[0] is m
            - args[1] is a
            - args[2] is b   
            
        label : str, optional
            Label associated with the LR fuzzy interval. The default is ''.
        color : matplotlib.colors, optional
            Color associated with the LR fuzzy interval. The default is None.

        Raises
        ------
        Exception
            Raised if the number of positional arguments is not 3 or 4.

        Returns
        -------
        None.
        
        Example
        -------
        >>> from floulib import LR
        >>> A = LR(1,1,2, label='A')
        >>> B = LR(3,4,1,3, label='B')
        >>> A.plot(xlim=[0,8]).add_plot(B)   
        
        .. image:: images/LR.__init__.png 

        """
        self._label = label
        self._color = color
        if len(args) == 3:
            self.m = args[0]
            self.m_prime = args[0]
            self.a = args[1]
            self.b = args[2]      
        elif len(args) == 4: 
            self.m = args[0]
            self.m_prime = args[1]
            self.a = args[2]
            self.b = args[3]
        else:
            raise Exception("Usage: LR(m, m_prime, a, b) or LR(m, a, b)")
        if self.a == 0.0 and self.b == 0.0:
            self.points = np.array([(self.m - self.a - self._precision, 0), (self.m, 1.0), (self.m_prime, 1.0), (self.m_prime + self.b + self._precision, 0.0)], dtype = np.double)           
        elif self.a == 0.0:
            self.points = np.array([(self.m - self.a  - self._precision, 0), (self.m, 1.0), (self.m_prime, 1), (self.m_prime + self.b, 0.0)], dtype = np.double)          
        elif self.b == 0.0:    
            self.points = np.array([(self.m - self.a, 0.0), (self.m, 1.0), (self.m_prime, 1.0), (self.m_prime + self.b + self._precision, 0.0)], dtype = np.double)           
        else:            
            self.points = np.array([(self.m - self.a, 0.0), (self.m, 1.0), (self.m_prime, 1.0), (self.m_prime + self.b, 0.0)], dtype = np.double)           
        self._bounds = [self.m - self.a, self.m_prime + self.b]
        self._universe = None       



    def area(self):
        """
        Area of a LR fuzzy interval.

        Returns
        -------
        float
            Area of the LR fuzzy interval.
            
        Example
        -------
        >>> from floulib import LR
        >>> A = LR(1, 0.5, 1)
        >>> B = Trapezoid (0.5, 1, 2, 4)
        >>> print(f'Area: A = {A.area():.3f}, B = {B.area():.3f}')
        Area: A = 0.750, B = 2.250
        """
        return (self.m_prime - self.m) + (self.a + self.b)/2.0
    
    
    
    def centroid(self):
        """
        Centroid of a LR fuzzy interval.

        Returns
        -------
        float
            Centroid of the LR fuzzy interval.
            
        Example
        -------
        >>> from floulib import LR
        >>> A = LR(1, 0.5, 1)
        >>> B = Trapezoid (0.5, 1, 2, 4)
        >>> print(f'Centroid: A = {A.centroid():.3f}, B = {B.centroid():.3f}')  
        Centroid: A = 1.167, B = 1.944
        """
        a = self.m_prime - self.m
        b = self.m_prime + self.b - self.m + self.a
        c = self.a
        return self.m - self.a + (2*a*c + a*a + c*b + a*b + b*b)/(3*(a + b))
    
        """
        Kernel of a LR fuzzy interval.

        Returns
        -------
        numpy.ndarray
            The support of the LR fuzzy interval, i.e. [m, m_prime].

        """
        return np.array([self.m, self.m_prime], dtype = np.double)   
    
    

    def is_precise(self):
        """
        Returns True if the LR fuzzy interval is precise.

        Returns
        -------
        boolean

        Example
        -------
        >>> from floulib import LR
        >>> A = LR(1, 0.5, 1)
        >>> B = LR(1, 0, 0)
        >>> print(A.is_precise(), B.is_precise())
        False True
        """
        return self.a == 0.0 and self.b == 0 and self.m == self.m_prime 
    


    def membership(self, x):
        """
        Computes the grade of membership of a point x to the LR fuzzy interval.

        Parameters
        ----------
        x : float
            The point x.

        Returns
        -------
        y : float
            The grade of membership.
            
        Example
        -------
        >>> from floulib import LR
        >>> A = LR(1, 0.5, 1)
        >>> print(f'Grade of membership for x = 1.2 is {A.membership(1.2):.2f}')
        Grade of membership for x = 1.2 is 0.80
        """
        if x < self._bounds[0] or x > self._bounds[1]:
            y = 0.0
        elif self._bounds[0] <= x < self.m:
            y = self._L((self.m - x) / self.a)
        elif self.m <= x <= self.m_prime:
            y = 1.0
        else:
            y = self._R((x - self.m_prime) / self.b)  
        return y    
 
    
 
    def mode(self):
        """
        Mode of a LR fuzzy number.

        Returns
        -------
        float
            Mean of m and m_prime.

        Example
        -------
        >>> from floulib import LR
        >>> A = LR(1, 0.5, 1)
        >>> B = Trapezoid (0.5, 1, 2, 4)
        >>> print(f'Mode: A = {A.mode():.3f}, B = {B.mode():.3f}')  
        Mode: A = 1.000, B = 1.500
        """
        return (self.m + self.m_prime)/2.0        



    ###
    # Special methods
    #

    def __add__(self, other):
        """
        Implements + operator between two LR fuzzy intervals.

        Parameters
        ----------
        other : LR
            LR fuzzy interval to add.
            
        Raises
        ------
        TypeError
            Raised if the RHS operand is not an instance of :class:`LR`.             

        Returns
        -------
        LR
            Addition of the two LR fuzzy intervals.
            
        Example
        -------
        >>> from floulib import LR
        >>> A = LR(1,1,2, label = 'A')
        >>> B = LR(3,1,1, label = 'B')
        >>> C = (A+B).label('C=A+B')
        >>> A.plot(xlim=[0,8]).add_plot(B).add_plot(C)
        
        .. image:: images/LR.__add__.png        

        """
        if isinstance(other, LR):
            return LR(self.m + other.m, 
                      self.m_prime + other.m_prime, 
                      self.a + other.a,
                      self.b + other.b
                      )
        else:
            raise TypeError('The RHS operand of + operator must be an instance of LR.')


    def __neg__(self):
        """
        Implements - unary operator of a LR fuzzy interval.

        Returns
        -------
        LR
            Opposite of a LR fuzzy interval.

        Example
        -------    
        >>> from floulib import LR        
        >>> A = LR(1,1,2, label = 'A')
        >>> C = (-A).label('C=-A')
        >>> A.plot(xlim=[-4,4]).add_plot(C)
        
        .. image:: images/LR.__neg__.png    
        """
        return LR(-self.m_prime,
                  -self.m,
                  self.b,
                  self.a
                  )



    def __sub__(self, other):
        """
        Implements - operator between two LR fuzzy intervals.

        Parameters
        ----------
        other : LR
            LR fuzzy interval to substract.
            
        Raises
        ------
        TypeError
            Raised if the RHS operand is not an instance of :class:`LR`.            

        Returns
        -------
        LR
            Difference of the two LR fuzzy intervals.
            
        Example
        -------
        >>> from floulib import LR
        >>> A = LR(1,1,2, label = 'A')
        >>> B = LR(3,1,1, label = 'B')
        >>> C = (A-B).label('C=A-B')
        >>> A.plot(xlim=[-5,5]).add_plot(B).add_plot(C)
        
        .. image:: images/LR.__sub__.png               

        """
        if isinstance(other, LR):
            return LR(self.m - other.m_prime, 
                      self.m_prime - other.m, 
                      self.a + other.b,
                      self.b + other.a
                      )  
        else:
            raise TypeError('The RHS operand of - operator must be an instance of LR.')



    def __str__(self):
        """
        Special method for printable string representation.

        Returns
        -------
        str
            Printable string.
            
        Example
        -------
        >>> from floulib import LR
        >>> A = LR(1,1,2)
        >>> B = LR(3,4,1,3)
        >>> print(A+B)
        LR(4.00, 5.00, 2.00, 5.00)
        """
        if self.m == self.m_prime:
            return f'LR({self.m:.2f}, {self.a:.2f}, {self.b:.2f})'
        else:
            return f'LR({self.m:.2f}, {self.m_prime:.2f}, {self.a:.2f}, {self.b:.2f})'        



    ###
    # Private methods
    #
    
    # Defines the L function
    def _L(self, x):
     return max(0.0, 1.0 -x)
 
    
 
    # Defines the R function
    def _R(self, x):
     return max(0.0, 1.0 -x)        


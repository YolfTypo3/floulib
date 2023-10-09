# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 17:18:42 2023

@author: Laurent Foulloy
"""
       
from floulib.LR import LR


class Trapezoid(LR):
    """
    Class to define trapezoidal membership function.
    
    .. note::
        
        Trapezoid is a subclass of :class:`LR`, therefore all methods 
        in :class:`LR` may be used.
        
        LR is a subclass of :class:`Multilinear`, therefore all methods 
        in :class:`Multilinear` may be used. 
        
        Multilinear is a subclass of :class:`Plot`, therefore all methods 
        in :class:`Plot` may also be used.      
    
    """
    def __init__(self, a, m, m_prime, b, **kwargs):
        """
        Constructor

        Parameters
        ----------
        a : float
            Left coordinate of the support.
        m : float
            Left coordinate of the kernel.
        m_prime : float
            Right coordinate of the kernel.
        b : float
            Right coordinate of the support.
        **kwargs : TYPE
            Keyword arguments transmitted to the parent class.

        Returns
        -------
        None.

        Examples
        --------
        >>> from floulib import Trapezoid
        >>> A = Trapezoid(1,2,4,6, label = 'A')
        >>> A.plot()
        
        .. image:: images/Trapezoid.__init__.png

        """
        super().__init__(m, m_prime, m - a, b - m_prime, **kwargs)
       

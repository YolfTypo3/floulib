# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 17:18:42 2023

@author: Laurent Foulloy
"""
       
from floulib.LR import LR
       
       
class Triangle(LR):
    """
    Class to define triangular membership functions.
    
    .. note::
        
        Triangle is a subclass of :class:`LR`, therefore all methods 
        in :class:`LR` may be used.
        
        LR is a subclass of :class:`Multilinear`, therefore all methods 
        in :class:`Multilinear` may be used. 
        
        Multilinear is a subclass of :class:`Plot`, therefore all methods 
        in :class:`Plot` may also be used.     
    """
    def __init__(self, a, m, b, **kwargs):
        """
        Constructor

        Parameters
        ----------
        a : float
            Left coordinate of the support.
        m : float
            Mode.
        b : float
            Right coordinate of the support.
        **kwargs : TYPE
            Keyword arguments transmitted to the parent class.

        Returns
        -------
        None.

        Examples
        --------
        >>> from floulib import Triangle
        >>> A = Triangle(1,2,4, label = 'A')
        >>> A.plot()
        
        .. image:: images/Triangle.__init__.png
        
        """
        super().__init__(m, m - a, b - m, **kwargs)

# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 17:18:42 2023

@author: Laurent Foulloy
"""
       
from floulib.LR import LR

class Rectangle(LR):
    """
    Class to define rectangular membership function.
    
    .. note::
        
        Rectangle is a subclass of :class:`LR`, therefore all methods 
        in :class:`LR` may be used.
        
        LR is a subclass of :class:`Multilinear`, therefore all methods 
        in :class:`Multilinear` may be used. 
        
        Multilinear is a subclass of :class:`Plot`, therefore all methods 
        in :class:`Plot` may also be used.       
    """
    def __init__(self, a, b, **kwargs):
        """
        Constructor

        Parameters
        ----------
        a : float
            Left coordinate of the support.
        b : float
            Right coordinate of the support.
        **kwargs : 
            Keyword arguments transmitted to the parent class.

        Returns
        -------
        None.
        
        Examples
        --------
        >>> from floulib import Rectangle
        >>> A = Rectangle(1,2, label = 'A')
        >>> A.plot(xlim = [0,3])
        
        .. image:: images/Rectangle.__init__.png        

        """
        super().__init__(a, b, self._precision, self._precision, **kwargs)


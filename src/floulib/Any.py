# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 17:18:42 2023

@author: Laurent Foulloy
"""
       
from floulib.Singleton import Singleton

class Any(Singleton):
    """
    Class which creates a Singleton with a grade of membership equal to 1.0.
    Any() can be used in the Is() method in Rule().
    
    .. note::
        
        Any is a subclass of :class:`Singleton`, therefore all methods 
        in :class:`Singleton` may be used.        
    """
    
    def __init__(self):  
        """
        Constructor

        Returns
        -------
        None.

        """
        super().__init__('', 1.0)  
        

# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 17:18:42 2023

@author: Laurent Foulloy
"""
            

class Singleton:
    
    def __init__(self, universe, value = 0.0):
        """
        Constructor.

        Parameters
        ----------
        universe : str | float
            Universe of discourse.
        value : float, optional
            Grade of membership. The default is 0.0.

        Returns
        -------
        None.

        Example
        -------
        >>> from floulib import Singleton
        >>> A = Singleton('a', 0.8)
        >>> B = Singleton(2, 0.4)
        
        """
        self._universe = universe
        self._memberships = value
        
        
        
    def membership(self, x = None):
        """
        Grade of membership of the Singleton.
    
    
        Parameters
        ----------
        x : None
            Parameter has no effect

        Returns
        -------
        float
            Grade of membership
            
        Example
        -------            
        >>> from floulib import Singleton
        >>> A = Singleton('a', 0.8) 
        >>> print(A.membership())           
        0.8
        """        
        return self._memberships
    
    
   
    ###
    # Special methods
    #    
   
    def __str__(self):
        """
        Printable string representation.

        Returns
        -------
        str
            printable string
            
        Example
        -------            
        >>> from floulib import Singleton
        >>> from floulib import Singleton
        >>> A = Singleton('a', 0.8)
        >>> B = Singleton(2, 0.4)
        >>> print(f'A = {A}, B = {B}')               
        A = 0.800/a, B = 0.400/2
        """            
        return f'{self._memberships:.3f}/{self._universe}'


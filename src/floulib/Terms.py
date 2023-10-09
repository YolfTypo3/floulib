# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 17:18:42 2023

@author: Laurent Foulloy
"""

from floulib.Plot import Plot
from floulib.Term import Term  
       
class Terms(Plot):
    """
    This class contains methods to perform operations on terms. 
    
    .. note::
        
        Terms is a subclass of :class:`Plot`, therefore all methods in :class:`Plot` 
        may be used.    
    
    """
    def __init__(self, *args):
        """
        Constructor

        Parameters
        ----------
        *args : Term
            Arguments are instances of Term.

        Raises
        ------
        TypeError
            Raised if arguments are not instances of :class:`Term`.

        Returns
        -------
        None.

        Example
        -------
        >>> from floulib import LR, Term, Terms
        >>> A = Term('A', LR(1, 0.5, 1))
        >>> B = Term('B', LR(2, 1, 1))
        >>> C = Term('C', LR(3, 1, 0.5))  
        >>> T = Terms(A, B, C)
        >>> T.plot(xlim = [0, 4])
        
        .. image:: images/Terms.__init__.png  
        """
        for arg in args:
            if not isinstance(arg, Term):
                raise TypeError('Arguments must be instance of Term.')
        self._object = args            

        
        
    def refresh(self, x):
        """
        Refreshes the universe of discourse of the terms.
        
        This method may be used when universes of discourse associated with terms
        in set of rules are changed and need to be refresh.

        Parameters
        ----------
        x : numpy.ndarray
            The new universe of discourse.

        Returns
        -------
        None.

        """
        for obj in self._object:
            obj._meaning._universe = x
            
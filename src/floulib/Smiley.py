# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 17:18:42 2023

@author: Laurent Foulloy
"""


from floulib.Plot import Plot

class Smiley(Plot): 
    """
    Class to plot a smiley.
    
    .. note::
        
        Smiley is a subclass of :class:`Plot`, therefore all methods 
        in :class:`Plot` may be used.
    
    """
    def __init__(self, smile, color, eye = 1.0, label = ''):  
        """
        Constructor
    
        Parameters
        ----------
        smile : float
            Magnitude of the smile if in [0, 1] or the grimace
            id in [-1, 0].
        color : matplotlib.colors
            Color of the smiley.
        eye : float, optional
            Height of the eyes. The default is 1.0.
        label : str, optional
            Label associated with the LR fuzzy interval. The default is ''.
        Returns
        -------
        None.
        
        Example
        -------
        >>> from floulib import Smiley
        >>> Smiley(0.8, [0, 1, 0]).plot()
    
        .. image:: images/Smiley.__init__.png
        """
        self._label = label      
        self._color = color        
        self.smile = smile
        self.eye = eye

# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 17:18:42 2023

@author: Laurent Foulloy
"""

from floulib.Any import Any
from floulib.Discrete import Discrete
from floulib.Multilinear import Multilinear
from floulib.Singleton import Singleton
from floulib.Plot import Plot
from floulib.Term import Term
from floulib.Terms import Terms
import numbers
import numpy as np



class Variable(Plot):
    """
    This class contains methods to define and use variables to be used with
    rules. 
    
    .. note::
        
        Variable is a subclass of :class:`Plot`, therefore all methods in :class:`Plot` 
        may be used.

    """
    
    # Constructor
    def __init__(self, *args):
        """
        Constructor

        Parameters
        ----------
        *args : numpy.ndarray | Terms | numbers.Number | callable
            If only one argument is provided.
        *args_ : Singleton | Term 
            If several arguments of the same type are provided.
            
        Raises
        ------
        Exception
            Raised if no argument is provided.
        TypeError
            Raised if one argument is provided but is not an instance of 
            numpy.ndarray | Terms | numbers.Number | callable
        Exception
            Raised if several arguments are provided but are not of the same type.
        TypeError
            Raised if several arguments are provided but are not instances of
            Singleton or Term.

        Returns
        -------
        None.
        
        Example
        -------
        
        Numeric variables
        
        >>> from floulib import Term, Triangle, Rule, Variable
        >>> import numpy as np
        >>> A1 = Term('A1', Triangle(0, 5, 10, label = '$A_1$'))
        >>> B1 = Term('B1', Triangle(0, 2, 4, label = '$B_1$'))      
        >>> v1 = Variable(np.linspace(0,15, 1000))
        >>> v2 = Variable(np.linspace(0, 10, 1000))
        >>> R = Rule().If(v1.Is(A1)).Then(v2.Is(B1))  
        >>> A = Triangle(6, 8, 9).label('$A$')             
        >>> B = R.inference(v1.Is(A)).label('$B$')
        >>> B.plot().add_plot(B1, alpha = 0.3)
        
        .. image:: images/Variable.__init__1.png  
        
        Symbolic variables
        
        >>> from floulib import Discrete, Term, Terms, Triangle, Rule, Rules, Variable
        >>> import numpy as np
        >>> A1 = Term('A1', Triangle(0, 5, 10, label = '$A_1$'))
        >>> A2 = Term('A2', Triangle(5, 10, 15, label = '$A_2$'))
        >>> B1 = Term('B1', Triangle(0, 2, 4, label = '$B_1$'))
        >>> B2 = Term('B2', Triangle(2, 4, 6, label = '$B_2$'))        
        >>> v1 = Variable(A1, A2) # defined with instances of Term
        >>> T2 = Terms(B1,B2)
        >>> v2 = Variable(T2) # defined with one instance of Terms
        >>> R = Rules(
            Rule().If(v1.Is(A1)).Then(v2.Is(B2)),
            Rule().If(v1.Is(A2)).Then(v2.Is(B1))
            )   
        >>> A = Discrete(('A1', 0.3), ('A2', 0.5))             
        >>> B = R.inference(v1.Is(A)).label('$B$')
        >>> B.plot()
        
        .. image:: images/Variable.__init__2.png  
        """
        self._universe = None
        if len(args) == 0:
            raise Exception('Variable must have one or several parameters.')
        elif len(args) == 1:
            if isinstance(args[0], np.ndarray):
                self._universe = args[0]
                self._object = args[0]
            elif isinstance(args[0], Terms) or \
                    isinstance(args[0], Multilinear) or \
                    isinstance(args[0], Discrete):
                self._object = args[0]
            elif isinstance(args[0], numbers.Number):
                self._object = args[0]
            elif callable(args[0]):
                self._object = args[0]                
            else:
                _type = type(args[0])
                raise TypeError(f'Parameter of Variable() must be an instance of nd.ndarray|Terms|Multilinear|Discrete instead of {_type}.')
        else:
            ref = args[0]
            for arg in args:
                if type(arg) != type(ref):
                    raise Exception('All elements must have the same type.')
                if isinstance(arg, Singleton):
                    pass
                elif isinstance(arg, Term):
                    pass
                else:
                    raise TypeError('Arguments must be instance of Singleton or Term.')
            L = []
            if isinstance(ref, Singleton):
                for arg in args:
                    L.append((arg._universe, arg._memberships))  
                self._object = Discrete(*L)
            elif isinstance(ref, Term):
                self._object = Terms(*args)                 

    
         
    def Is(self, _object = None):
        """
        This method is used to set the "value" of a variable
        used in the definition of rules and in the inference.       

        Parameters
        ----------
        _object : Any | Discrete | Multilinear | Term | numbers.Number, optional
            The "value" to set. The default is None.

        Raises
        ------
        TypeError
            Raised if the parameter is not an instance of :class:`Any`, 
            :class:`Discrete`, :class:`Multilinear`, 
            numbers.Number or :class:`Term`.

        Returns
        -------
        Variable
            The variable object.
            
        Example
        -------
        
        See :meth:`Variable.__init__`.

        """
        if isinstance(_object, Term):
            if isinstance(self._object, np.ndarray):
                if _object._meaning._universe is None:
                    _object._meaning._universe = self._universe                
                return Variable(_object._meaning)
            elif isinstance(self._object, Terms):
                L = []
                for obj in self._object._object:
                    if _object == obj:
                        L.append((_object._term._universe, 1.0))
                    else:                      
                        L.append((obj._term._universe,0.0))
                return Variable(Discrete(*L))
            else:
                raise TypeError(f'The variable should have been created with an instance of numpy.ndarray or Terms instead of {type(self._object)}')
        elif isinstance(_object, Discrete):
            return Variable(_object)
        elif isinstance(_object, Multilinear):
            if _object._universe is None:
                _object._universe = self._universe
            return Variable(_object)
        elif isinstance(_object, numbers.Number):
            return Variable(_object)
        elif callable(_object):
            return Variable(_object)
        elif isinstance(_object, Any) and isinstance(self._object, Terms):
            L = []
            for obj in self._object._object:
                L.append((_object._universe, 1.0))
            return Variable(Discrete(*L))
        else:
            raise TypeError('Parameter of Is() must instances of Any or Discrete or Multilinear or numbers.Number or Term.')

    
    
    def Certainty(self, level):
        """
        Adds a certainty level to a variable
        (see :meth:`floulib.Discrete.Certainty`, 
        :meth:`floulib.Multilinear.Certainty`,
        :meth:`floulib.Term.Certainty` depending of the
        type of the object associated with the variable).

        Parameters
        ----------
        level : float
            The certainty level.
            
        Raises
        ------
        TypeError
            Raised if the object associated with the variable is not
            an instance of :class:`Discrete`, 
            :class:`Multilinear` or :class:`Term`.
            
        Returns
        -------
        Variable
            Variable with a certainty level.

        """
        if isinstance(self._object, Discrete) | isinstance(self._object, Multilinear) | isinstance(self._object, Term):
            return  Variable(self._object.Certainty(level))
        else:
            raise TypeError('Object associated with the variable must be an instance of Discrete, Multilinear or Term.')
    
    
    
    def Uncertainty(self, level):  
        """
        Adds an uncertainty level to a variable
        (see :meth:`floulib.Discrete.Uncertainty`, 
        :meth:`floulib.Multilinear.Uncertainty`,
        :meth:`floulib.Term.Uncertainty` depending of the
        type of the object associated with the variable).

        Parameters
        ----------
        level : float
            The uncertainty level.
            
        Raises
        ------
        TypeError
            Raised if the object associated with the variable is not
            an instance of :class:`Discrete`, 
            :class:`Multilinear` or :class:`Term`.

        Returns
        -------
        Variable
            Variable with an uncertainty level.

        """
        if isinstance(self._object, Discrete) | isinstance(self._object, Multilinear) | isinstance(self._object, Term):
            return  Variable(self._object.Uncertainty(level))
        else:
            raise TypeError('Object associated with the variable must be an instance of Discrete, Multilinear or Term.')

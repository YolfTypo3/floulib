# -*- coding: utf-8 -*-

import numpy as np

import numbers

      
from floulib.Discrete import Discrete
from floulib.LR import LR
from floulib.Multilinear import Multilinear
from floulib.Term import Term
from floulib.Terms import Terms
    
class Fuzzify:
    _object = None
    
    
    def __init__(self, *args):
        """
        Constructor

        Parameters
        ----------
        *args : Terms | numpy.ndarray | Tuple[Term]
        
            - numpy.ndarray for numeric fuzzification.            
            - Terms if only one parameter is given or
              several Term parameters for symbolic defuzzification.

        Raises
        ------
        TypeError
            Raised if the argument is not an instance of Terms or numpy.ndarray
            when one parameter is given.
        TypeError              
            Raised if args are not instances of :class:`Term` when several 
            parameters are given.

        Returns
        -------
        None.
        
        """
        if len(args) ==  1:
            if isinstance(args[0], Terms):
                self._object = args[0]._object 
            elif isinstance(args[0], np.ndarray):
                self._object = args[0] 
            else:
                raise TypeError('Parameter must be an instance of Terms or numpy.ndarray.')                
        elif len(args) >  1 :
            for arg in args:
                if not isinstance(arg, Term):
                    raise TypeError('Parameters must be instances of Term.')  
                self._object = args



    def numeric(self, *args):
        """
        Numeric fuzzification
        
        Parameters
        ----------
        x : numbers.Number | Multilinear | Discrete
            The parameter for the fuzzification.

        Raises
        ------
        TypeError
            Raised if the parameter is not an instance of numbers.Number,
            Multilinear or Discrete.

        Returns
        -------
        LR | Multilinear | Discrete
            
        Example
        -------
        >>> from floulib import Fuzzify, LR
        >>> x0 = 3
        >>> X0 = Fuzzify().numeric(x0)
        >>> X0.plot(xlim = [2, 4])
        >>> print(X0.is_precise())
        True
        
        .. image:: images/Fuzzify.numeric_1.png

        """
        if isinstance(args[0], numbers.Number):
            return LR(args[0], 0, 0)
        elif isinstance(args[0], Multilinear):
            return args[0]
        elif callable(args[0]):
            return args[0](self._object, *args[1:])
        else:
            raise TypeError ('Parameter of Fuzzify.numeric() must be callable or an instance of number.Numbers or Multilinear.')




    def symbolic(self,x):
        """
        Symbolic fuzzification

        Parameters
        ----------
        x : numbers.Number
            The imput.

        Raises
        ------
        Exception
            Raised if the Terms are not given in the constructor.

        Returns
        -------
        Discrete
            The symbolic fuzzy subset.
            
        Example
        -------
        >>> from floulib import Fuzzify, Term, Triangle
        >>> small = Term('small', Triangle(0, 0, 20))
        >>> big = Term('big', Triangle(0, 20, 20))
        >>> x0 = 12 
        >>> X0 = Fuzzify(small, big).symbolic(x0)
        >>> X0.plot()
        >>> print(X0)
        0.400/small + 0.600/big
        
        .. image:: images/Fuzzify.symbolic.png
        
        Other solution using Terms
        
        >>> from floulib import Fuzzify, Term, Terms, Triangle
        >>> small = Term('small', Triangle(0, 0, 20))
        >>> big = Term('big', Triangle(0, 20, 20))
        >>> T_size = Terms(small, big)
        >>> x0 = 12 
        >>> X0 = Fuzzify(T_size).symbolic(x0)
        >>> X0.plot()
        >>> print(X0)
        0.400/small + 0.600/big       

        """
        if not isinstance(self._object[0], Term):
            raise Exception('You must define the terms to use symbolic method.')
        else:
            L = []
            for obj in self._object:
                L.append((obj._term._universe, obj._meaning.membership(x)))
            return Discrete(*L)




    def symbolic_upper(self, x):
        """
        Upper symbolic fuzzification
        
        The upper symbolic fuzzification is obtained by computing, for 
        each term, its possibiliy knowing the input.

        Parameters
        ----------
        x : Multilinear | Discrete
            The input.

        Raises
        ------
        Exception
            Raised if terms are not provided to the constructor.
        TypeError    
            Raised if x is not an instance of Multilinear or Discrete.

        Returns
        -------
        Discrete
            The symbolic fuzzy subset.
            
        Example
        -------
        
        >>> from floulib import Fuzzify, LR, Term, Terms, Triangle
        >>> small = Term('small', Triangle(0, 0, 20, label = 'small'))
        >>> big = Term('big', Triangle(0, 20, 20, label = 'big'))
        >>> T_size = Terms(small, big)
        >>> A = LR(12, 1, 1, label = 'A') 
        >>> X0 = Fuzzify(T_size).symbolic_upper(A)
        >>> T_size.plot(nrows = 2).add_plot(A).add_plot(X0, index = 1)
        >>> print(X0)
        0.429/small + 0.619/big
        
        .. image:: images/Fuzzify.symbolic_upper.png

        """
        if not isinstance(self._object[0], Term):
            raise Exception('You must define the terms to use symbolic_uper method.')        
        if isinstance(x, Multilinear):
            L = []
            for obj in self._object:
                L.append((obj._term._universe, obj._meaning.possibility(x)))
            return Discrete(*L)
        elif isinstance(x, Discrete):
            L = []
            for obj in self._object:
                temp = np.minimum(x.points[:,1], np.vectorize(obj._meaning.membership)(x.points[:,0]))
                L.append((obj._term, max(temp)))
            return Discrete(*L)            
        else:
            raise TypeError('Parameter must be an instance of Multilinear or Discrete.')    



    def symbolic_lower(self,x):
        """
        Lower symbolic fuzzification
        
        The lower symbolic fuzzification is obtained by computing, for 
        each term, its necessity knowing the input.
        

        Parameters
        ----------
        x : Multilinear | Discrete
            The input.

        Raises
        ------
        Exception
            Raised if terms are not provided to the constructor.
        TypeError    
            Raised if x is not an instance of Multilinear.

        Returns
        -------
        Discrete
            The symbolic fuzzy subset.
            
        Example
        -------
        
        >>> from floulib import Fuzzify, LR, Term, Terms, Triangle
        >>> small = Term('small', Triangle(0, 0, 20, label = 'small'))
        >>> big = Term('big', Triangle(0, 20, 20, label = 'big'))
        >>> T_size = Terms(small, big)
        >>> A = LR(12, 1, 1, label = 'A') 
        >>> X0 = Fuzzify(T_size).symbolic_lower(A)
        >>> T_size.plot(nrows = 2).add_plot(A).add_plot(X0, index = 1)
        >>> print(X0)
        0.381/small + 0.571/big
        
        .. image:: images/Fuzzify.symbolic_lower.png              

        """
        if not isinstance(self._object[0], Term):
            raise Exception('You must define the terms to use symbolic_uper method.')        
        if isinstance(x, Multilinear):            
            L = []
            for obj in self._object:
                L.append((obj._term._universe, obj._meaning.necessity(x)))
            return Discrete(*L)
        else:
            raise TypeError('Parameter must be an instance of Multilinear.') 

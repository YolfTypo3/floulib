# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 17:18:42 2023

@author: Laurent Foulloy
"""
from floulib.Discrete import Discrete       
from floulib.Term import Term
from floulib.Terms import Terms
import numpy as np
import numbers


  
class Defuzzify: 
    _object = None
    
    def __init__(self, *args):
        """
        Constructor

        Parameters
        ----------
        *args : None | Terms | numpy.ndarray | Tuple[Term]
            - None fornumeric defuzzification of a discrete fuzzy subset.
            - numpy.ndarray for numeric defuzzification.
            - Terms if only one parameter is given or
              several Term parameters for symbolic defuzzification.

        Raises
        ------
        TypeError
            Raised if the argument is not an instance of :class:`Terms` or 
            numpy.ndarray when one parameter is given.
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
        Numeric defuzzification

        Parameters
        ----------
        *args : callable | Discrete | Multilinear | Term
            The fuzzy set to defuzzify.

        Raises
        ------
        TypeError
            Raised if Defuzzify() was created without a numpy.ndarray parameter
            if the parameter is callable.
        TypeError
            Raised if parameter is not callable or an instance of Discrete, 
            Multilinear or Term.

        Returns
        -------
        float
            Result of the defuzzification.
            
        Example
        -------
        
        Defuzzificaion of a multilinear fuzzy subset.
        
        >>> from floulib import Defuzzify, LR
        >>> import numpy as np
        >>> A = LR(1, 0.5, 1) 
        >>> u = Defuzzify(np.linspace(0, 4, 1000)).numeric(A)   
        >>> print(u) 
        1.1666683383450254        
        
        Defuzzification of discrete fuzzy subset.
        
        >>> from floulib import Defuzzify, Discrete
        >>> A = Discrete((1, 0.1), (2, 0.4), (3, 0.1)) 
        >>> u = Defuzzify().numeric(A)   
        >>> print(u) 
        2.0000000000000004   
        
        Defuzzificaion of a Term.
        
        >>> from floulib import Defuzzify, LR, Term
        >>> import numpy as np
        >>> A = Term('A', LR(1, 0.5, 1)) 
        >>> u = Defuzzify(np.linspace(0, 4, 1000)).numeric(A)   
        >>> print(u) 
        1.1666683383450254                

        """
        if callable(args[0]):
            if self._object is not None:
                x = args[0](self._object)
            else:
                raise TypeError('Defuzzify() must be created with a numpy.ndarray parameter to use Defuzzify.numeric with a callable parameter.')
        elif isinstance(args[0], Discrete):
            x = args[0]
        elif isinstance(args[0], Term):
            if self._object is not None:
                x = args[0]._meaning(self._object)
            else:
                raise TypeError('Defuzzify() must be created with a numpy.ndarray parameter to use Defuzzify.numeric with a callable parameter.')
        else:
            raise TypeError ('Parameter of Defuzzify.numeric() must be callable or an instance of Discrete, Multilinear or Term.')            
        if isinstance(x._universe[0], numbers.Number):
            return np.prod(x.points, axis=1).sum()/np.sum(x.points[:,1])
        raise Exception('Universe for Defuzzify.numeric() nust contain instances of numbers.Number.')
                
        
        


    def symbolic(self, x, method = 'WAM-C', key = None):
        """
        Symbolic defuzzification

        Parameters
        ----------
        x : TYPE
            DESCRIPTION.
        method : str, optional
            Defuzzificaion method. The default is 'WAM-C'.
            possible values are:
                
                - CoS: Center of sums
                - WAM-C: Weighted Average Method using centroids
                - WAM-M: Weighted Average Method using modes
                - WAM_P: Weighted Average Method using prototypes
                
        key : string, optional
            key for the prototype in WAM-P method. The default is None.

        Raises
        ------
        Exception
            Raised if Defuzzify() is not created with terms.
        TypeError
            Raised if the parameter is not an instance of Discrete.
        Exception 
            Raised if the defuzzification is not CoS, WAM-C, WAM-M or WAM-P.

        Returns
        -------
        float
            Result of the defuzzification.
            
        Example    
        -------
        
        >>> from floulib import Defuzzify, Discrete, Term, Triangle
        >>> import numpy as np
        >>> B1 = Term('B1', Triangle(0, 5, 10, label = '$B_1$'))
        >>> B2 = Term('B2', Triangle(5, 10, 15, label = '$B_2$'))
        >>> B3 = Term('B3', Triangle(10, 15, 25, label = '$B_3$'))
        >>> T = Terms(B1, B2, B3)
        >>> A = Discrete(('B1', 0.0), ('B2', 0.3), ('B3', 0.7)) 
        >>> u1 = Defuzzify(T).symbolic(A)
        >>> u2 = Defuzzify(T).symbolic(A, method = 'CoS')
        >>> print(u1, u2)
        14.666666666666666 15.185185185185185
        
        """
        if self._object is None:
            raise Exception('You must define the terms to use Defuzzify.symbolic() method.')
        if isinstance(x, Discrete):
            universe = np.vectorize(lambda term: term._term._universe)(self._object)
            num = 0.0
            den = 0.0
            for point in x.points:
                index = np.where(universe == point[0])[0][0]
                if method == 'WAM-C':
                    num =  num + point[1] * self._object[index].centroid()
                    den = den + point[1]
                elif method == 'WAM-P':
                    if self._object[index].prototype is None:
                        raise Exception('Prototype must be defined to use method WAM-P in Defuzzify.symbolic().')
                    if isinstance(self._object[index].prototype, dict) and key is not None and key in self._object[index].prototype:
                        prototype = self._object[index].prototype[key]
                    else:
                        prototype = self._object[index].prototype
                    if isinstance(prototype, list):
                        num =  num + np.array([point[1]]) * np.array(prototype)
                    else:
                        num =  num + point[1] * prototype
                    den = den + point[1]                          
                elif method == 'WAM-M':
                    num =  num + point[1] * self._object[index].mode()
                    den = den + point[1]  
                elif method == 'CoS':
                    num = num + point[1] * self._object[index].area() * self._object[index].centroid()
                    den = den +  point[1] * self._object[index].area()
                else:
                    raise Exception('Unknown defuzzification method in Defuzzify.symbolic().')
            return num / den
        else:
            raise TypeError('Parameter of Defuzzify.symbolic() must be an instance of Discrete.')            
  
        

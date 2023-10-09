# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 17:18:42 2023

@author: Laurent Foulloy
"""

from floulib.Plot import Plot
import numbers
import numpy as np


    
class Discrete(Plot):
    """
    This class contains methods to perform operations on discrete
    fuzzy subsets.
    
    .. note::
        
        Discrete is a subclass of :class:`Plot`, therefore all methods in :class:`Plot` 
        may be used.    
    
    """
    
    _precision = 1e-9      
    

    def __init__(self, *args, label = ''):
        """
        Constructor

        Parameters
        ----------
        *args : Tuple(str, float) | Tuple(str, float) | numpy.ndarray | str
            - If tuples are provided, the first element is the item of the 
              universe of discourse, the second element is the grade of 
              membership.
            - If only one argument is provided and its type is numpy.ndarray,
              a discrete fuzzy subset is generated. Its universe of discourse
              is the argument and the grades of membership are equal to 0.
            - If there are several arguments which are not tuples a discrete 
              subset is generated. Its universe of discourse
              is the argument and the grades of membership are equal to 0.
        label : str, optional
            The label associated with the discrete fuzzy subset. The default is ''.

        Raises
        ------
        TypeError
            Raised is one argument is provided and is not an instance 
            of numpy.ndarray.

        Returns
        -------
        None.

        Example
        -------
        
        Parameters are tuple on linguistic universe of discourse
        
        >>> from floulib import Discrete
        >>> import numpy as np
        >>> A = Discrete(('a', 0.5), ('b', 0.3), label = 'A')
        >>> print(A)
        0.500/a + 0.300/b
        
        Parameters are tuple on numeric universe of discourse
        
        >>> B = Discrete((1.0, 0.8), (2, 0.4), label = 'B')        
        >>> print(B)
        0.800/1 + 0.400/2
        
        Parameter type is numpy.ndarray
        
        >>> x = np.arange(0, 6, 1)
        >>> C = Discrete(x, label = 'C')
        >>> print(C)   
        0.000/0 + 0.000/1 + 0.000/2 + 0.000/3 + 0.000/4 + 0.000/5       
        
        Parameter types are str
        
        >>> D = Discrete('x', 'y', 'z', label = 'D')
        >>> print(D)
        0.000/x + 0.000/y + 0.000/z
        
        """
        self._label = label
        if len(args) == 1 and isinstance(args[0], np.ndarray):
            if isinstance(args[0][0], numbers.Number):
                args = [(point, 0.0) for point in args[0]]
            else:
                raise TypeError('Parameter must be an instance of numpy.ndarray when only one argument is given.')
        elif not isinstance(args[0], tuple) and not isinstance(args[0], np.ndarray):  
            args = [(point, 0.0) for point in args]
        self.points = np.array(args, dtype = object)
        self._universe = self.points[:, 0]
        self._memberships = self.points[:, 1]

    
            

    def composition(self, x, relation): 
        """
        Computes the image of the input x by a relation.

        Parameters
        ----------
        x : Discrete
            The inout discrete fuzzy set.
        relation : function
            The relation  must have two parameters. The first one is a tuple
            which contains the components of the universe of discourse of the 
            inputs. The second one is the output element.

        Raises
        ------
        TypeError
            Raised if x is not an instance of :class:`Discrete`.

        Returns
        -------
        Discrete
            The result.

        Example
        -------
        >>> from floulib import Discrete
        >>> import numpy as np
        >>> A = Discrete((0, 0.1), (1, 0.3), (2, 0.5), (3, 0.2))
        >>> x = np.arange(0, 10, 1)
        >>> # Computes the image of A by the function y=x^2
        >>> C = Discrete(x).composition(A, relation = lambda x,y: 1 if y == x[0]**2 else 0)
        >>> C.label('C')
        >>> C.plot(s = 20) 
        >>> print(C)
        0.100/0 + 0.300/1 + 0.000/2 + 0.000/3 + 0.500/4 + 0.000/5 + 0.000/6 
        + 0.000/7 + 0.000/8 + 0.200/9
        
        .. image:: images/Discrete.composition.png         
        """
        if isinstance(x, Discrete):
            res = np.copy(self.points)
            for i in range(len(res)): 
                for point in x.points:
                    y = relation((point[0], res[i][0]), res[i][0])
                    res[i][1] = max(res[i][1], min(point[1], y))
            return Discrete(*res)  
        else:
            raise TypeError('Parameter must be an instance of Discrete.')              
 
    
    
    # Alpha-cut of the discrete fuzzy subset
    def cut(self, alpha):
        """
        Computes the alpha-cut of a discrete fuzzy subset.

        Parameters
        ----------
        alpha : float
            The level of the cut.

        Returns
        -------
        numpy.ndarray
            The alpha cut.
            
        Example
        -------
        >>> from floulib import Discrete
        >>> A = Discrete(('a', 0.5), ('b', 0.8), ('c', 1.0), ('d', 0.4), ('e', 0))
        >>> print(A.cut(0.5))
        ['a' 'b' 'c']
        """
        return self._universe[np.where(self._memberships >= alpha)]
    
    
    
    def cut_strict(self, alpha):
        """
        Computes the strict alpha-cut of a discrete fuzzy subset.

        Parameters
        ----------
        alpha : float
            The level of the cut.

        Returns
        -------
        numpy.ndarray
            The strict alpha cut.
            
        Example
        -------
        >>> from floulib import Discrete
        >>> A = Discrete(('a', 0.5), ('b', 0.8), ('c', 1.0), ('d', 0.4), ('e', 0))
        >>> print(A.cut_strict(0.5))
        ['b' 'c']

        """
        return self._universe[np.where(self._memberships > alpha)] 
    
 
    
    def extension(self, x, func, precision = 0.01):
        """
        Computes Zadeh's extension principle.
        
        Parameters
        ----------
        x : Discrete
            The input discrete fuzzy set.
        func : function
            The function must have two parameters. The first one is a tuple
            which contains the components of the universe of discourse of the 
            inputs. The second one is the output element.
        precision : float, optional
            The precision for accepting, for a given y, x as f-1(y). Default is 0.01.
        Raises
        ------
        TypeError
            Raised if x is not an instance of :class:`Discrete`.

        Returns
        -------
        Discrete
            The result.
            
        Example
        -------
        >>> from floulib import Discrete
        >>> import numpy as np
        >>> A = Discrete((0, 0.1), (1, 0.3), (2, 0.5), (3, 0.2))
        >>> B = Discrete((0, 0.2), (1, 0.5), (2, 0.2), (3, 0.1))
        >>> x = np.arange(0, 11, 1)
        >>> # Computes the sum of A by B
        >>> C = Discrete(x).extension(A*B, func = lambda x,y: x[0]+x[1])
        >>> C.label('C')
        >>> C.plot(s = 20)
        >>> print(C)
        0.100/0 + 0.200/1 + 0.300/2 + 0.500/3 + 0.200/4 + 0.200/5 + 0.100/6 
        + 0.000/7 + 0.000/8 + 0.000/9 + 0.000/10

        .. image:: images/Discrete.extension1.png  
        
        Case where the approximation is used. The choices of the steps and the precision
        are quite sensitive to obtain a valuable result.
        
        >>> from floulib import Discrete, LR
        >>> import math
        >>> import numpy as np
        >>> D = LR(2,1, 1)
        >>> x = np.arange(0, 4, 0.001)
        >>> y = np.arange(0, 11, 0.01)
        >>> E = Discrete(y).extension(D(x), func = lambda x,y: x*x + math.sqrt(x))
        >>> E.label('E').plot()

        .. image:: images/Discrete.extension2.png          

        """
        if isinstance(x, Discrete):
            res = np.copy(self.points)
            indices = np.where(x.points[:, 1] > 0)          
            points_filtered = x.points[indices]
            for i in range(len(res)):
                for point in points_filtered:
                    y = func(point[0], res[i][0])
                    if y is not None and abs(y - res[i][0]) < precision:
                        res[i][1] = max(res[i][1], point[1])                          
            return Discrete(*res)         
        
        else:
            raise TypeError('Parameter must be an instance of Discrete.')      


    
    def kernel(self):
        """
        Computes the kernel a discrete fuzzy subset.

        Returns
        -------
        numpy.ndarray
            The kernel.

        Example
        -------
        >>> from floulib import Discrete
        >>> A = Discrete(('a', 0.5), ('b', 0.8), ('c', 1.0), ('d', 0.4), ('e', 0))
        >>> print(A.kernel())
        ['c']
        """
        return self.cut(1.0)



    def membership(self, x):
        """
        Computes the grade of membership of an item x of the universe 
        of discourse.

        Parameters
        ----------
        x : float | str
            Item of the universe of discourse.
            
        Raises
        ------
        Exception
            Raised if x does not belong to the universe of discourse.             

        Returns
        -------
        float
            Grade of membership.
            
        Example
        -------
        >>> from floulib import Discrete
        >>> A = Discrete(('a', 0.5), ('b', 0.3))
        >>> print(A.membership('b'))
        O.3
        >>> B = Discrete((1, 0.8), (2, 0.4))
        >>> print(B.membership(2))
        0.4
        """
        index = np.where(self._universe == x)[0]
        if len(index) > 0:
            return  self._memberships[index[0]] 
        else:
            raise Exception(f'In Discrete.membership, the item "{x}" must be in the universe of discourse.')
  
   
    
    def support(self):
        """
        Computes the support of a discrete fuzzy subset. 

        Returns
        -------
        numpy.ndarray
            The support.
            
        Example
        -------
        >>> from floulib import Discrete
        >>> A = Discrete(('a', 0.5), ('b', 0.8), ('c', 1.0), ('d', 0.4), ('e', 0))
        >>> print(A.support())
        ['a' 'b' 'c' 'd']            

        """
        return self.cut_strict(0.0)



    def Certainty(self, level):
        """
        Adds a certainty level to the duscrete fuzzy subset.
        
        This method is generally used with variables in rules. For this
        reason, it starts with the capital letter C.

        Parameters
        ----------
        value : float
            The certainty level.

        Returns
        -------
        Discrete
            The discrete fuzzy subset with certainty level.
            
        Example
        -------
        >>> from floulib import Discrete
        >>> A = Discrete(('a', 0.5), ('b', 0.8), ('c', 1.0), ('d', 0.4), ('e', 0))
        >>> A.label('A')  
        >>> B = A.Certainty(0.3).label('A with 0.3 certainty level')
        >>> A.plot(nrows = 2).add_plot(B, index = 1)
        >>> print(B)
        0.700/a + 0.800/b + 1.000/c + 0.700/d + 0.700/e  

        .. image:: images/Discrete.Certainty.png           

        """
        return self.Uncertainty(1 - level)



    def Uncertainty(self, level):
        """
        Adds an uncertainty level to the discrete fuzzy subset.
        
        This method is generally used with variables in rules. For this
        reason, it starts with the capital letter U.

        Parameters
        ----------
        level : float
            The uncertainty level.

        Returns
        -------
        Multilinear
            The discrete fuzzy subset with uncertainty level.
            
        Example
        -------
        >>> from floulib import Discrete
        >>> A = Discrete(('a', 0.5), ('b', 0.8), ('c', 1.0), ('d', 0.4), ('e', 0))
        >>> A.label('A')  
        >>> B = A.Uncertainty(0.3).label('A with 0.3 uncertainty level')
        >>> A.plot(nrows = 2).add_plot(B, index = 1)
        >>> print(B)
        0.500/a + 0.800/b + 1.000/c + 0.400/d + 0.300/e
        
        .. image:: images/Discrete.Uncertainty.png 
        
        """
        points = np.copy(self.points)
        for i, objet in enumerate(points):
            points[i] = (points[i][0], max(points[i][1], level))
        return Discrete(*points)  


 
    ###
    #
    # Special methods
    #

    def __and__(self, other):
        """
        Special method for using the opertor & as
        the intersection of two discrete fuzzy subsets. 

        Parameters
        ----------
        other : Discrete
            The RHS discrete fuzzy subset.
            
        Raises
        ------
        TypeError
            Raised if the RHS operand is not an instance of :class:`Discrete`.            

        Returns
        -------
        Discrete
            The intersection.
            
        Example
        -------
        >>> from floulib import Discrete
        >>> A = Discrete(('a', 0.5), ('b', 0.3), label = 'A')
        >>> B = Discrete(('b', 0.6), ('c', 0.2), label = 'B')
        >>> C = (A & B).label('C = A & B')
        >>> print(f'A = {A}')
        >>> print(f'B = {B}')
        >>> print(f'C = A & B = {C}')
        >>> C.plot()  
        A = 0.500/a + 0.300/b
        B = 0.600/b + 0.200/c
        C = A & B = 0.300/b
        
        .. image:: images/Discrete.__and__.png    

        """     
        if isinstance(other, Discrete):
            universe = np.intersect1d(self._universe, other._universe)
            res = []
            for x in universe:
                index1 = np.where(self._universe == x)[0]
                index2 = np.where(other._universe == x)[0]
                t = (x, 0.0)
                if index1.size > 0 and index2.size > 0:
                    t = (x, min(self._memberships[index1[0]], other._memberships[index2][0]))
                res.append(t)
            return Discrete(*res)   
        else:
            raise TypeError('The RHS operand of & must be used an instance of Discrete.')        
        
    
    
    def __or__(self, other):
        """
        Special method for using the opertor | as
        the union of two discrete fuzzy subsets. 

        Parameters
        ----------
        other : Discrete
            The RHS discrete fuzzy subset.
            
        Raises
        ------
        TypeError
            Raised if the RHS operand is not an instance of :class:`Discrete`.
            
        Returns
        -------
        Discrete
            The union.
            
        Example
        -------
        >>> from floulib import Discrete
        >>> A = Discrete(('a', 0.5), ('b', 0.3), label = 'A')
        >>> B = Discrete(('b', 0.6), ('c', 0.2), label = 'B')
        >>> C = (A | B).label('C = A | B')
        >>> print(f'A = {A}')
        >>> print(f'B = {B}')
        >>> print(f'C = A | B = {C}')
        >>> C.plot()  
        A = 0.500/a + 0.300/b
        B = 0.600/b + 0.200/c
        C = A | B = 0.500/a + 0.600/b + 0.200/c
        
        .. image:: images/Discrete.__or__.png    

        """
        if isinstance(other, Discrete):
            universe = np.union1d(self._universe, other._universe)
            res = []
            for x in universe:
                index1 = np.where(self._universe == x)[0]
                index2 = np.where(other._universe == x)[0]
                t = (x, 0.0)
                if index1.size == 0:
                    t = (x, other._memberships[index2[0]])
                elif index2.size == 0:
                    t = (x, self._memberships[index1[0]]) 
                else:
                    t = (x, max(self._memberships[index1[0]], other._memberships[index2[0]]))
                res.append(t)
            return Discrete(*res)  
        else:
            raise TypeError('The RHS operand of | must be used an instance of Discrete.')
            
            
    
    def __invert__(self):
        """
        Special method for using the unary opertor ~ as
        the complement of a discrete fuzzy subset. 

        Returns
        -------
        Discrete
            The complement.
            
        Example
        -------
        >>> from floulib import Discrete
        >>> A = Discrete(('a', 0.5), ('b', 0.3), label = 'A')
        >>> C = (~A).label('C = ~A')
        >>> print(f'A = {A}')
        >>> print(f'C = ~A = {C}')
        >>> C.plot()  
        A = 0.500/a + 0.300/b
        C = ~A = 0.500/a + 0.700/b
        
        .. image:: images/Discrete.__invert__.png    

        """
        res = []
        for i, x in enumerate(self._universe):
            res.append((x, 1.0 - self._memberships[i]))
        return Discrete(*res) 
    
    
    def __mul__(self, other):
        """
        Special method to compute the cartesian product of two discrete
        fuzzy subsets.

        Parameters
        ----------
        other : Discrete
            The other discrete fuzzy subset.
            
        Raises
        ------
        TypeError
            Raised if the RHS operand is not an instance of :class:`Discrete`.
            
        Returns
        -------
        Discrete
            The cartesian product.

        Example
        -------
        >>> from floulib import Discrete
        >>> A = Discrete(('a', 0.5), ('b', 0.3), label = 'A')
        >>> B = Discrete(('b', 0.6), ('c', 0.2), label = 'B')
        >>> C = (A * B).label('C = A * B')
        >>> print(f'A = {A}')
        >>> print(f'B = {B}')
        >>> print(f'C = A * B = {C}')
        >>> C.plot()  
        A = 0.500/a + 0.300/b
        B = 0.600/b + 0.200/c
        C = A * B = 0.500/('a', 'b') + 0.200/('a', 'c') + 0.300/('b', 'b') + 0.200/('b', 'c')
        
        .. image:: images/Discrete.__mul__.png   
        """
        if isinstance(other, Discrete):
            cartesian_product = np.array(
                np.meshgrid(
                    np.arange(len(self._universe)), 
                    np.arange(len(other._universe))
                )
            ).T.reshape(-1,2)
            L = []
            for i in range(len(cartesian_product)):
                x = cartesian_product[i][0]
                y = cartesian_product[i][1]
                L.append((
                        (self._universe[x], 
                         other._universe[y]
                        ), 
                        min(
                            self._memberships[x], 
                            other._memberships[y])
                        )
                )
            return Discrete(*L)    
        else:
            raise TypeError('The RHS operand of * must be used an instance of Discrete.')


    def __getitem__(self, index):
        return self._memberships[index]


    def __str__(self, _format = 3):
        """
        Special method for printable string representation.

        Parameters
        ----------
        _format : int, optional
            Number of decimal digits. The default is 3.

        Returns
        -------
        result : str
            Printable string.
            
        Example
        -------
        >>> from floulib import Discrete
        >>> A = Discrete(('a', 0.5), ('b', 0.3))  
        >>> print(f'A = {A}')
        A = 0.500/a + 0.300/b
        """
        result = ''
        for x in self.points:
            if len(result) != 0:                
                result = result + r' + {:.{}f}/{}'.format(x[1], _format, x[0]) 
            else:
                result = r'{:.{}f}/{}'.format(x[1], _format, x[0])
        return result   

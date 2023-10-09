# -*- coding: utf-8 -*-

from floulib.Plot import Plot
from floulib.Discrete import Discrete
import numpy as np

   
class Multilinear(Plot):
    """
    Contains methods to perform operations on multilinear
    fuzzy subsets.
    
    .. note::
        
        Multilinear is a subclass of :class:`Plot`, therefore all methods 
        in :class:`Plot` may be used.      
    """
    _precision = 1e-9  


    def __init__(self, *args, label = '', color = None):
        """
        Constructor

        Parameters
        ----------
        *args : Tuple[float, float]
            Several tuple containing the point of the universe of discourse
            and the grade of membership for this point.
        label : str, optional
            Label associated with the multilinear fuzzy subset. The default is ''.
        color : matplotlib.colors, optional
            Color associated with the multilinear fuzzy subset. The default is None.

        Returns
        -------
        None.
        
        Example
        -------
        >>> from floulib import Multilinear
        >>> A = Multilinear((0.0, 0.0), (1.0, 1.0), (1.5, 1.0), (2.0, 0.5), (3.0, 1.0), (3.5, 1.0), (4.0, 0.0))
        >>> A.plot()
        
        .. image:: images/Multilinear.__init__.png        

        """
        self._label = label
        self._color = color
        self.points = np.array(args, dtype = np.double)     
        for i in range(len(self.points) - 1):
            if self.points[i + 1][0] ==  self.points[i][0]:
                if self.points[i + 1][1] > self.points[i][1]:
                    self.points[i][0] =self.points[i][0] - self._precision
                if self.points[i + 1][1] < self.points[i][1]:
                    self.points[i + 1][0] =self.points[i + 1][0] + self._precision        
        self._bounds = [self.points[0][0], self.points[-1][0]]
        self._universe = None 
        
         

    def cut(self, alpha):
        """
        Computes the alpha-cut of the multilinear fuzzy subset.

        Parameters
        ----------
        alpha : float
            The level.

        Returns
        -------
        alpha_cut : numpy.ndarray
            The alpha-cut.
            
        Example
        -------
        >>> from floulib import Multilinear
        >>> alpha = 0.8
        >>> A = Multilinear((0.0, 0.0), (1.0, 1.0), (1.5, 1.0), (2.0, 0.5), (3.0, 1.0), (3.5, 1.0), (4.0, 0.0))
        >>> B = Multilinear((0.0, alpha), (4.0, alpha))
        >>> A.plot().add_plot(B, linestyle = '--')
        >>> print(A.cut(alpha))
        [[1.  1.7]
         [2.6 3.6]]
            
        .. image:: images/Multilinear.cut.png

        """
        other = Multilinear( 
            (self.points[0][0], alpha),
            (self.points[-1][0], alpha)
            )
        points =self.__and__(other).points
        indices = np.where(np.abs(points[:, 1] - alpha) < self._precision)[0]
        paquets = np.split(indices, np.where(np.diff(indices) != 1)[0] + 1)
        alpha_cut = np.array([[points[t[0]][0], points[t[-1]][0]] for t in paquets])
        return alpha_cut



    def kernel(self):
        """
        Returns the kernel of the multilinear fuzzy subset.

        Returns
        -------
        numpy.ndarray
            The kernel.
            
        Example
        -------
        >>> from floulib import Multilinear
        >>> A = Multilinear((0.0, 0.0), (1.0, 1.0), (1.5, 1.0), (2.0, 0.5), (3.0, 1.0), (3.5, 1.0), (4.0, 0.0))
        >>> A.plot()
        >>> print(A.kernel())
        [[1.  1.5]
         [3.  3.5]]
        
        .. image:: images/Multilinear.kernel_1.png
        
        >>> B = Multilinear((0.0, 0.0), (1.0, 1.0), (3.5, 1.0), (4.0, 0.0))
        >>> B.plot()
        >>> print(B.kernel())
        [[1.  3.5]]
        
        .. image:: images/Multilinear.kernel_2.png        
        
        """
        return self.cut(1.0)
    
    
    
    def max(self):
        """
        Computes the maximum grade of membership.

        Returns
        -------
        float
            The maximum grade of membership.
            
        Example
        -------
        >>> from floulib import LR, Multilinear
        >>> A = Multilinear((0.0, 0.0), (0.5, 0.3), (1.5, 0.0))
        >>> A.plot()
        >>> print(A.max())
        0.3
        
        .. image:: images/Multilinear.max.png

        """
        return np.max(self.points[:, 1])    
    
    
    
    def membership(self, x):
        """
        Computes the grade of membership for x.

        Parameters
        ----------
        x : float
            Point where the grade of membership is computed.

        Returns
        -------
        float
            Grade of membership.
            
        Example
        -------
        >>> from floulib import Multilinear
        >>> A = Multilinear((0.0, 0.0), (1.0, 1.0), (1.5, 1.0), (2.0, 0.5), (3.0, 1.0), (3.5, 1.0), (4.0, 0.0))
        >>> print(A.membership(1.8))   
        0.7
        """
        if x < self._bounds[0]:
            return float(self.points[0][1])
        elif x > self._bounds[1]:
            return float(self.points[-1][1])
        for i in range(len(self.points)):
            if self.points[i][0] > x:
                slope = (self.points[i][1] - self.points[i - 1][1]) / (self.points[i][0] - self.points[i - 1][0])
                intercept = self.points[i - 1][1] - slope * self.points[i - 1][0]
                y = x*slope + intercept
                return y   
        if self.points[i][0] - self.points[i-1][0] == 0:
            return self.points[i][1]
        slope = (self.points[i][1] - self.points[i - 1][1]) / (self.points[i][0] - self.points[i - 1][0])
        intercept = self.points[i - 1][1] - slope * self.points[i - 1][0]
        y = min(max(x*slope + intercept, 0.0), 1.0)
        return y    
    
    
 
    # Builds the membership for a list of y-values 
    def mf(self, x):
        """
        Computes the grades of membership for all points in x.
        
        This method can be used as an interface with other libraries. 

        Parameters
        ----------
        x : numpy.ndarray
            The array of points.

        Returns
        -------
        y : numpy.ndarray
            The grades of membership array.
            
        Example
        -------
        >>> from floulib import LR
        >>> import numpy as np
        >>> import matplotlib.pyplot as plt
        >>> A = LR(1, 0.5, 1)
        >>> x = np.linspace(0, 5, 1000)
        >>> fig, ax = plt.subplots()
        >>> ax.plot(x, A.mf(x))
            
        .. image:: images/Multilinear.mf.png
        
        """
        y = np.zeros_like(x) 
        for i in range(len(x)):
            y[i] = self.membership(x[i])
        return y    
 
    
    
    def min(self):
        """
        Computes the minimim grade of membership.

        Returns
        -------
        float
            The maximum grade of membership.
            
        Example
        -------
        >>> from floulib import LR, Multilinear
        >>> A = Multilinear((0.0, 0.0), (0.5, 0.3), (1.5, 0.0))
        >>> (~A).plot()
        >>> print((~A).min())
        0.7
        
        .. image:: images/Multilinear.min.png

        """        
        return np.min(self.points[:, 1])       
    
    
    
    def necessity(self, dpi):
        """
        Computes the necessity of the multilinear fuzzy subset knowing 
        the distribution of possibility dpi.

        Parameters
        ----------
        dpi : Multilinear
            The possibility distribution.

        Raises
        ------
        TypeError
            Raised if the parameter is not an instance of :class:`Multilinear`.

        Returns
        -------
        Multilinear
            The necessity.
            
        Example
        -------
        >>> from floulib import LR, Multilinear
        >>> A = Multilinear((0.0, 1.0), (0.5, 1.0), (1.5, 0.0), (2.0, 0.0), label = 'A')
        >>> B = LR(1, 0.25, 0.25, label = 'B')
        >>> A.plot().add_plot(B)
        
        .. image:: images/Multilinear.necessity.png
        
        >>> print(A.necessity(B))            
        0.40000000000000036
        """
        if isinstance(dpi, Multilinear):
            return self.__or__(~dpi).min()  
        else:
            raise TypeError('Parameter of Multilinear.necessity() must be an instance of Multilinear.')

    
    
   
    def possibility(self, dpi):
        """
        Computes the possibility of the multilinear fuzzy subset knowing the 
        distribution of possibility dpi.

        Parameters
        ----------
        dpi : Multilinear
            The possibility distribution.

        Raises
        ------
        TypeError
            Raised if the parameter is not an instance of :class:`Multilinear`.

        Returns
        -------
        Multilinear
            The possibility.

        Example
        -------
        >>> from floulib import LR, Multilinear
        >>> A = Multilinear((0.0, 1.0), (0.5, 1.0), (1.5, 0.0), (2.0, 0.0), label = 'A')
        >>> B = LR(1, 0.25, 0.25, label = 'B')
        >>> A.plot().add_plot(B)
        
        .. image:: images/Multilinear.possibility.png
        
        >>> print(A.possibility(B))
        0.6
        """
        if isinstance(dpi, Multilinear):
            return self.__and__(dpi).max()  
        else:
            raise TypeError('Parameter of Multilinear.possibility() must be an instance of Multilinear.')
   
        
    
    def support(self):
        """
        Returns the support of the multilinear fuzzy subset.

        Returns
        -------
        numpy.ndarray
            The kernel.
            
        Example
        -------
        >>> from floulib import Multilinear
        >>> A = Multilinear((0.0, 0.0), (1.0, 1.0), (1.5, 1.0), (2.0, 0.0), (2.5, 0.0), (3.0, 1.0), (3.5, 1.0), (4.0, 0.0))
        >>> A.plot()
        >>> print(A.support())
        [[0.  2. ]
         [2.5 4. ]]
        
        .. image:: images/Multilinear.support_1.png
        
        >>> B = Multilinear((0.0, 0.0), (1.0, 1.0), (3.5, 1.0), (4.0, 0.0))
        >>> B.plot()
        >>> print(B.support())
        [[0. 4.]]
        
        .. image:: images/Multilinear.support_2.png   

        """
        l = len(self.points)
        T = np.arange(l)
        indices = np.where(self.points[:, 1] == 0.0)[0]
        neg_mask = ~np.in1d(T,indices)
        packets = np.split(T[neg_mask], np.where(np.diff(T[neg_mask]) != 1)[0]+1)
        L = []
        for i in range(len(packets)):
            inf = max(packets[i][0]-1, 0)
            sup = min(packets[i][-1] + 1, l - 1)
            L.append((self.points[inf][0], self.points[sup][0]))
        return np.array(L)
    
    
    
    def translate(self, delta):
        """
        Translation over the x-axis all the points whose x-coordinates
        are greater than the smallest one and smaller than the
        greatest one.

        Parameters
        ----------
        delta : float
            The value for the translation.

        Returns
        -------
        Multilinear
            The translated multilinear fuzzy subset.
            
        Example
        -------
        >>> from floulib import LR, Multilinear
        >>> A = Multilinear((0.0, 1.0), (0.5, 1.0), (1.5, 0.0), (2.0, 0.0), label = 'A')
        >>> B = A.translate(0.5).label('B')
        >>> A.plot().add_plot(B)
        
        .. image:: images/Multilinear.translate.png
        
        Points (0.5, 1.0) and (1.5, 0.0) are translated by 0.5 but
        points (0.0, 1.0) and (2.0, 0.0) are not translated.

        """
        T = self.points    
        res1 = np.where((T[:,0] > T[0][0]) & (T[:,0] < T[-1][0]), (T[:,0] + delta, T[:,1]), (T[:,0], T[:,1]))
        res1 = res1.transpose().reshape(-1, 2)
        return Multilinear(*res1)  



    def universe(self, x):
        """
        Sets the universe of discourse.

        Parameters
        ----------
        x : numpy.ndarray
            The universe of discourse.

        Returns
        -------
        Multilinear
            The multilinear fuzzy subset.

        """
        self._universe = x
        return self 
    


    def Certainty(self, level):
        """
        Adds a certainty level to the multilinear fuzzy subset.
        
        This method is generally used with variables in rules. For this
        reason, it starts with the capital letter C.

        Parameters
        ----------
        level : float
            The certainty level.

        Returns
        -------
        Multilinear
            The multilinear fuzzy subset with certainty level.
            
        Example
        -------
        >>> from floulib import Multilinear
        >>> A = Multilinear((0.0, 0.0), (0.5, 0.0), (0.75, 1.0), (1.5, 0.0), (2.0, 0.0), label = 'A')
        >>> B = A.Certainty(0.3).label('A with 0.3 certainty level')
        >>> A.plot(nrows = 2).add_plot(B, index = 1)
        
        .. image:: images/Multilinear.Certainty.png    

        """        
        
        return self.Uncertainty(1 - level)
    


    def Uncertainty(self, level):
        """
        Adds an uncertainty level to the multilinear fuzzy subset.
        
        This method is generally used with variables in rules. For this
        reason, it starts with the capital letter U.

        Parameters
        ----------
        level : float
            The uncertainty level.

        Returns
        -------
        Multilinear
            The multilinear fuzzy subset with uncertainty level.
            
        Example
        -------
        >>> from floulib import Multilinear
        >>> A = Multilinear((0.0, 0.0), (0.5, 0.0), (0.75, 1.0), (1.5, 0.0), (2.0, 0.0), label = 'A')
        >>> B = A.Uncertainty(0.3).label('A with 0.3 uncertainty level')
        >>> A.plot(nrows = 2).add_plot(B, index = 1)
        
        .. image:: images/Multilinear.Uncertainty.png    

        """
        return self.__or__(Multilinear((self._bounds[0]-self._precision, level), (self._bounds[1] + self. _precision, level))).universe(self._universe)



    ####
    #
    # Special methods
    #    
    
    def __and__(self, other):
        """
        Special method for using the operator & as
        the intersection of two multilinear fuzzy subsets.

        Parameters
        ----------
        other : Multilinear
            The RHS multilinear fuzzy subset.

        Raises
        ------
        TypeError
            Raised if the RHS operand is not an instance of :class:`Multilinear`.

        Returns
        -------
        Multilinear
            The intersection.
            
        Example
        -------
        >>> from floulib import LR, Multilinear
        >>> A = Multilinear((0.0, 1.0), (0.5, 1.0), (1.5, 0.0), (2.0, 0.0), label = 'A')
        >>> B = LR(1, 0.25, 0.25, label = 'B') 
        >>> C = (A & B).label('C = A & B')
        >>> A.plot(nrows = 2).add_plot(B).add_plot(C, index = 1)
        
        .. image:: images/Multilinear.__and__.png        

        """
        if isinstance(other, Multilinear):
            return self._apply(other, min) 
        else:
            raise TypeError('The RHS operand of & must be an instance of Multilinear.')



    def __call__(self, x):
        """
        Special method to transform a multilinear fuzzy subset into
        a discrete fuzzy subsets.

        Parameters
        ----------
        x : numpy.ndarray
            The universe of discourse on which the transformation is 
            performed.

        Raises
        ------
        TypeError
            Raised if the parameter is not an instance of numpy.ndarray.

        Returns
        -------
        Discrete
            The discrete fuzzy subset.
            
        Example
        -------
        >>> from floulib import Multilinear
        >>> import numpy as np
        >>> A = Multilinear((0.0, 1.0), (0.5, 1.0), (1.5, 0.0), (2.0, 0.0))
        >>> C = A(np.linspace(0, 2, 50))           
        >>> A.plot(nrows = 2).add_plot(C, index = 1)
        
        .. image:: images/Multilinear.__call__.png  
        """
        if isinstance(x, np.ndarray):
            points = [(point, self.membership(point)) for point in x]
            return Discrete(*points)  
        else:
            raise TypeError('Parameter must be an array.')



    def __invert__(self):
        """
        Special method for using the unary operator ~ as the 
        complement of a multlinear fuzzy subsets.

        Returns
        -------
        Multilinear
            The complement.
            
        Example
        -------
        >>> from floulib import Multilinear
        >>> A = Multilinear((0.0, 1.0), (0.5, 1.0), (1.5, 0.0), (2.0, 0.0), label = 'A')
        >>> B = (~A).label('B = ~Ã')
        >>> A.plot().add_plot(B)
        
        .. image:: images/Multilinear.__invert__.png                

        """
        res = np.array(self.points)
        res[:, 1] = np.vectorize(lambda y: 1 - y)(res[:, 1])
        return Multilinear(*res)       
 
    

    def __neg__(self):
        """
        Special method for using the unary operator - as the 
        opposite of a multlinear fuzzy subsets.

        Returns
        -------
        Multilinear
            The opposite.
            
        Example
        -------
        >>> from floulib import Multilinear
        >>> A = Multilinear((0.0, 1.0), (0.5, 1.0), (1.5, 0.0), (2.0, 0.0))
        >>> C = (-A ).label('C = -A')
        >>> C.plot() 

        .. image:: images/Multilinear.__neg__.png              

        """
        res = np.array(self.points)
        res[:, 0] = np.vectorize(lambda x: -x)(np.flip(res[:, 0]))
        res[:, 1] = np.flip(res[:, 1])
        return Multilinear(*res)  

    

    def __or__(self, other):
        """
        Special method for using the operator | as
        the union of two multilinear fuzzy subsets.       

        Parameters
        ----------
        other : Multilinear
            The RHS multilinear fuzzy subset.

        Raises
        ------
        TypeError
            Raised if the RHS operand is not an instance of :class:`Multilinear`.

        Returns
        -------
        Multilinear
            The union.
            
        Example
        -------
        >>> from floulib import LR, Multilinear
        >>> A = Multilinear((0.0, 1.0), (0.5, 1.0), (1.5, 0.0), (2.0, 0.0), label = 'A')
        >>> B = LR(1, 0.25, 0.25, label = 'B') 
        >>> C = (A | B).label('C = A | B')
        >>> A.plot(nrows = 2).add_plot(B).add_plot(C, index = 1)  

        .. image:: images/Multilinear.__or__.png                 

        """
        if isinstance(other, Multilinear):
            return self._apply(other, max) 
        else:
            raise TypeError('The RHS operand of | must be an instance of Multilinear.')



    def __rmul__(self, other):
        """
        Special method for using the operator * with a number
        as the LHS operand. Its multiplies the grades of membership
        of the multilinear fuzzy subset by the LHS operand and 
        truncates them to 1.

        Parameters
        ----------
        other : int | float
            The LHS operand.

        Raises
        ------
        TypeError
            Raised the the LHS in not an instance of int or float.

        Returns
        -------
        Multilinear
            The result.
            
        Example
        -------
        >>> from floulib import Multilinear
        >>> A = Multilinear((0.0, 1.0), (0.5, 1.0), (1.5, 0.0), (2.0, 0.0), label = 'A')
        >>> C = (1.5*A).label('C')
        >>> A.plot(nrows = 2).add_plot(C, index = 1) 

        .. image:: images/Multilinear.__rmul__.png              
        """
        if isinstance(other, float) or isinstance(other, int):
            res = np.array(self.points)
            res[:, 1] = np.vectorize(lambda y: other*y)(res[:, 1]) 
            other = Multilinear( 
                (self.points[0][0], 1.0),
                (self.points[-1][0], 1.0)
                )
            return Multilinear(*res).__and__(other)
        else:
            raise TypeError('The product is defined only for int or real.')
    
    
    
    def __xor__(self, other):
        """
        Special method for using the operator ^ as
        the symetric difference of two multilinear fuzzy subsets.         

        Parameters
        ----------
        other : Multilinear
            The other multilinear fuzzy subset.

        Raises
        ------
        TypeError
            Raised if other is not an instance of :class:`Multilinear`.

        Returns
        -------
        Multilinear
            The symetric difference.
            
        Example
        -------
        >>> from floulib import LR, Multilinear
        >>> A = Multilinear((0.0, 1.0), (0.5, 1.0), (1.5, 0.0), (2.0, 0.0), label = 'A')
        >>> B = LR(1, 0.25, 0.25, label = 'B') 
        >>> C = (A ^ B).label('C = A ^ B')
        >>> A.plot(nrows = 2).add_plot(B).add_plot(C, index = 1)  

        .. image:: images/Multilinear.__xor__.png               

        """          
        if isinstance(other, Multilinear):    
            return (self & ~other) | (~self & other)  
        else:
            raise TypeError('The RHS operand of ^ must be an instance of Multilinear.')
          

    ####
    #
    # Private methods
    #         

    # Applies a function to two multilinear fuzzy subsets.    
    def _apply(self, other, func):
        points = np.unique(self._build_points(other)[:, 0])
        res = np.array([np.vectorize(self.membership)(points),
        np.vectorize(other.membership)(points)])       
        res = np.vectorize(func)(*res)
        res = np.column_stack((points, res))
        return Multilinear(*res)  


    # builds the list of all points when operation on two multilinear fuzzy sets.    
    def _build_points(self, other):
        res = np.concatenate((self.points, other.points))
        for i in range(len(self.points) - 1):
            for j in range(len(other.points) - 1):
                temp = self._segments_intersection(
                    self.points[i],
                    self.points[i + 1],
                    other.points[j],
                    other.points[j + 1]
                    )
                if len(temp) > 0  and not np.all(np.isin(temp, res)):
                    res = np.append(res, [temp], axis = 0)           
        return res 
          
                
    # Intersection of segments P1,P2 and P3,P4.
    def _segments_intersection(self, P1, P2, P3, P4):
        # None of lines' length could be 0.
        if ((P1[0] == P2[0] and P1[1] == P2[1]) or (P3[0] == P4[0] and P3[1] == P4[1])):
            return []
        # The denominators for the equations for ua and ub are the same.
        den = ((P4[1] - P3[1]) * (P2[0] - P1[0]) - (P4[0] - P3[0]) * (P2[1] - P1[1]))
        # Lines are parallel when denominator equals to 0,
        # No intersection point
        if den == 0:
            return []
        # Avoid the divide overflow
        ua = ((P4[0] - P3[0]) * (P1[1] - P3[1]) - (P4[1] - P3[1]) * (P1[0] - P3[0])) / (den + 1e-16)
        ub = ((P2[0] - P1[0]) * (P1[1] - P3[1]) - (P2[1] - P1[1]) * (P1[0] - P3[0])) / (den + 1e-16)
        # if ua and ub lie between 0 and 1.
        # Whichever one lies within that range then the corresponding line segment contains the intersection point.
        # If both lie within the range of 0 to 1 then the intersection point is within both line segments.
        if (ua < 0 or ua > 1 or ub < 0 or ub > 1):
            return []
        # Return a list with the x and y coordinates of the intersection
        x = P1[0] + ua * (P2[0] - P1[0])
        y = P1[1] + ua * (P2[1] - P1[1])
        return (x, y)                 
                

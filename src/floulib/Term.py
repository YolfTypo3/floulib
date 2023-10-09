# -*- coding: utf-8 -*-


from floulib.LR import LR
from floulib.Multilinear import Multilinear
from floulib.Plot import Plot
from floulib.Singleton import Singleton

    
class Term(Plot):
    """
    This class contains methods to define and use a term for
    linguistic variable, especially for rules in fuzzy controller.
    In general, a term is the association of a string like "small" 
    and its meaning, i.e. the membership function associated with 
    the term.
    
    In special cases, variable may contain purely linguistic terms
    which have no meaning associated with.
    
    .. note::
        
        Term is a subclass of :class:`Plot`, therefore all methods in :class:`Plot` 
        may be used.
    
    """
    
    prototype = None
    """
    Prototype associated with the term to be used in the symbolic
    defuzzification (method WAM-P). The prototype can be:
        
        - a scalar,
        - a list of scalars,
        - a dict containing scalar or list of scalars.
    """

    
    def __init__(self, *args):
        """
        Constructor

        Parameters
        ----------
        *args : str | Multilinear
            
            - If the type of args is str, args defines the name of the term.
            - If args is Multilinear, args defines the meaning of the term.

        Raises
        ------
        Exception
            Raised if the number of positional arguments is equal to 0 
            or greater than 2.
        TypeError
            Raised if there is one positional argument which is not an 
            instance of str.

        Returns
        -------
        None.
        
        Example
        -------
        
        Generates the term A as the association of the Singleton('A') and its 
        meaning provided by the LR fuzzy subset LR(1, 0.5, 0.5).
        
        >>> from floulib import Term
        >>> A = Term('A', LR(1, 0.5, 0.5))
        
        Same as above        

        >>> A = Term(LR(1, 0.5, 0.5), 'A')
        
        Creates the term A as the Singleton('A') with no meaning.
        
        >>> A = Term('A')
        
        """
        self._term = Singleton('')
        self._meaning = None
        if len(args) == 0 or len(args) > 2:
            raise Exception('Term() accepts one or two arguments only.')
        if len(args) == 1 and not isinstance(args[0], str):
            raise TypeError('Argument of Term() must be an instance of str when only one argument is provided.')
        for arg in args:
            if isinstance(arg, Multilinear):
                self._meaning = arg
            elif isinstance(arg, str):
                self._term = Singleton(arg)
            else:
                raise TypeError('Arguments of Term() must be instances of Multilinear and str. ')



    def area(self):
        """
        Area of the meaning of the term
        (see  :meth:`floulib.LR.area`).
        
        Raises
        ------
        TypeError
            Raised is the meaning associated with the term is not an instance 
            of :class:`LR`.
            
        Returns
        -------
        float
            The area.

        """
        if isinstance(self._meaning, LR):
            return self._meaning.area() 
        else:
            raise TypeError('The meaning associated with the term must be an instance of LR.')



    def centroid(self):
        """
        Centroid of the meaning of the term
        (see :meth:`floulib.LR.centroid`).
        
        Raises
        ------
        TypeError
            Raised is the meaning associated with the term is not an instance 
            of :class:`LR`.        

        Returns
        -------
        float
            The centroid.

        """
        if isinstance(self._meaning, LR):        
            return self._meaning.centroid() 
        else:
            raise TypeError('The meaning associated with the term must be an instance of LR.')    
    
      
      
    def membership(self, x): 
        """
        Computes the grade of membership to the meaning for x
        (see :meth:`floulib.Multilinear.membership`).

        Parameters
        ----------
        x : float
            Point where the grade of membership is computed.
            
        Raises
        ------
        TypeError
            Raised is the meaning associated with the term is not an instance 
            of :class:`Multilinear`.

        Returns
        -------
        float
            Grade of membership.

        """
        if isinstance(self._meaning, Multilinear):
            return self._meaning.membership(x)  
        else:
            raise TypeError('The meaning associated with the term must be an instance of Multilinear.')      
    
    

    def mode(self):
        """
        Mode of the meaning of the term
        (see  :meth:`floulib.LR.mode`).
        
        Raises
        ------
        TypeError
            Raised is the meaning associated with the term is not an instance 
            of :class:`LR`.              

        Returns
        -------
        float
            The mode.

        """
        if isinstance(self._meaning, LR):   
            return self._meaning.mode()   
        else:
            raise TypeError('The meaning associated with the term must be an instance of LR.')  
    
    
    
    def necessity(self, dpi):
        """       
        Computes the necessity of the meaning of the term knowing 
        the distribution of possibility dpi
        (see  :meth:`floulib.Multilinear.necessity`).

        Parameters
        ----------
        dpi : Multilinear
            The possibility distribution.

        Raises
        ------
        TypeError
            Raised by the private method Term._get_meaning() if the parameter 
            is not an instance of :class:`Term` or :class:`Multilinear`.

        Returns
        -------
        Multilinear
            The necessity.
            
        """
        return self._meaning.necessity(self._get_meaning(dpi)) 
    
    
    
    def possibility(self, dpi):
        """
        Computes the possibility of the meaning of the term knowing the 
        distribution of possibility dpi
        (see  :meth:`floulib.Multilinear.possibility`).

        Parameters
        ----------
        dpi : Multilinear
            The possibility distribution.

        Raises
        ------
        TypeError
            Raised by the private method Term._get_meaning() if the parameter 
            is not an instance of :class:`Term` or :class:`Multilinear`.

        Returns
        -------
        Multilinear
            The possibility.

        """
        return self._meaning.possibility(self._get_meaning(dpi))    



    def Certainty(self, level):
        """
        Adds a certainty level to the meaning of a term
        (see  :meth:`floulib.Multilinear.Certainty`).

        Parameters
        ----------
        level : float
            The certainty level.
            
        Raises
        ------
        TypeError
            Raised is the meaning associated with the term is not an instance
            of :class:`Multilinear`.                

        Returns
        -------
        Multilinear
            The multilinear fuzzy subset with certainty level.


        """
        if isinstance(self._meaning, Multilinear):
            return self._meaning.Certainty(level)    
        else:
            raise TypeError('The meaning associated with the term must be an instance of Multilinear.')      
    
    
    def Uncertainty(self, level):
        """
        Adds an uncertainty level to the meaning of a term
        (see  :meth:`floulib.Multilinear.Uncertainty`).

        Parameters
        ----------
        level : float
            The uncertainty level.

        Raises
        ------
        TypeError
            Raised is the meaning associated with the term is not an instance
            of :class:`Multilinear`.    

        Returns
        -------
        Multilinear
            The multilinear fuzzy subset with uncertainty level.

        """
        if isinstance(self._meaning, Multilinear):
            return self._meaning.Uncertainty(level)     
        else:
            raise TypeError('The meaning associated with the term must be an instance of Multilinear.')  



    ###
    #
    # Special method
    #
    
    def __and__(self, other):
        """
        Special method for using the operator & between
        two instances of Term. It returns the intersection
        of the meanings of the terms 
        (see  :meth:`floulib.Multilinear.__and__`).

        Parameters
        ----------
        other : Term
            The RHS operand.
            
        Raises
        ------
        TypeError
            Raised is the meaning associated with the term is not an instance
            of :class:`Multilinear`.            

        Returns
        -------
        Multilinear
            The intersection of the meanings.

        """
        if isinstance(self._meaning, Multilinear):
            return self._meaning.__and__(self._get_meaning(other))
        else:
            raise TypeError('The meaning associated with the term must be an instance of Multilinear.')     
    
    
    
    def __invert__(self):
        """
        Special method for using the unary operator ~ as the 
        complement of a term
        (see  :meth:`floulib.Multilinear.__invert__`).
        
        Raises
        ------
        TypeError
            Raised is the meaning associated with the term is not an instance 
            of :class:`Multilinear`.        
        
        Returns
        -------
        Multilinear
            The complement of the meaning.
        """
        if isinstance(self._meaning, Multilinear):
            return self._meaning.__invert__()      
        else:
            raise TypeError('The meaning associated with the term must be an instance of Multilinear.')     
    
    
    
    def __neg__(self):
        """
        Special method for using the unary operator - as the 
        opposite of a term
        (see  :meth:`floulib.Multilinear.__neg__`).
        
        Raises
        ------
        TypeError
            Raised is the meaning associated with the term is not an instance 
            of :class:`Multilinear`.        

        Returns
        -------
        Multilinear
            The opposite of the meaning.         
        """  
        if isinstance(self._meaning, Multilinear):
            return self._meaning.__neg__()  
        else:
            raise TypeError('The meaning associated with the term must be an instance of Multilinear.')  



    def __or__(self, other):
        """
        Special method for using the operator | between
        two instances of Term. It returns the union
        of the meanings of the terms 
        (see  :meth:`floulib.Multilinear.__or__`).

        Parameters
        ----------
        other : Term
            The RHS operand.
            
        Raises
        ------
        TypeError
            Raised is the meaning associated with the term is not an instance 
            of :class:`Multilinear`.            

        Returns
        -------
        Multilinear
            The union of the meanings.
        """        
        if isinstance(self._meaning, Multilinear):
            return self._meaning.__or__(self._get_meaning(other))  
        else:
            raise TypeError('The meaning associated with the term must be an instance of Multilinear.')  



    def __rmul__(self, other):   
        """
        Special method for using the opertor * with a number
        as the LHS operand. Its multiplies the grades of membership
        of themeaning of the term by the LHS operand and 
        truncates them to 1 
        (see  :meth:`floulib.Multilinear.__rmul__`).

        Parameters
        ----------
        other : Term
            The RHS operand.
            
        Raises
        ------
        TypeError
            Raised is the meaning associated with the term is not an instance 
            of :class:`Multilinear`.            

        Returns
        -------
        Multilinear
            The result.
        """   
        if isinstance(self._meaning, Multilinear):
            return self._meaning.__rmul__(other)      
        else:
            raise TypeError('The meaning associated with the term must be an instance of Multilinear.')   
 
    
  
    def __xor__(self, other):
        """
        Special method for using the opertor ^ between
        two instances of Term. It returns the symmetric difference
        of the meanings of the terms 
        (see  :meth:`floulib.Multilinear.__xor__`).

        Parameters
        ----------
        other : Term
            The RHS operand.
            
        Raises
        ------
        TypeError
            Raised is the meaning associated with the term is not an instance 
            of :class:`Multilinear`.            

        Returns
        -------
        Multilinear
            The symmetric difference of the meanings.
        """
        if isinstance(self._meaning, Multilinear):
            return self._meaning.__xor__(self._get_meaning(other))  
        else:
            raise TypeError('The meaning associated with the term must be an instance of Multilinear.')      


            
    ###
    # Private methods
    #   
    
           
    def _get_meaning(self, parameter):
        if isinstance(parameter, Term):
            return parameter._meaning
        elif isinstance(parameter, Multilinear):
            return parameter
        else:
            raise Exception('Parameter of Term._get_meaning() must be an instance of Term or Multilinear.')            
 
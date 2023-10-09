# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 17:18:42 2023

@author: Laurent Foulloy
"""

from floulib.Discrete import Discrete
from floulib.LR import LR
from floulib.Multilinear import Multilinear
from floulib.Operator import Operator
from floulib.Plot import Plot
from floulib.Variable import Variable
from shapely.geometry import Polygon
import numpy as np
import time

  
class Rule(Plot):
    """
    This class contains methods to define and use a rule.
    """

    _ruleIf = None
    _ruleThen = None
    _ruleWeight = None


    def inference(self, *args, **kwargs): 
        """
        Computes the image of a fuzzy subsets by a rule.

        Parameters
        ----------
        *args : Variable
            Antecedents.
        **kwargs :  Operator| bool
            - R: the implication operator. Default is :meth:`Operator.R_KD`.
            - T: the modus ponens triangular norm. Default is :meth:`Operator.T_Z`.
            - T1: the triangular norm to combine antecedents. Default is :meth:`Operator.T_Z`.
            - time: If True, the computing time for the inference is displayed. Default is False.

        Returns
        -------
        Discrete
            The result.
            
        Example
        -------
        >>> from floulib import Term, Triangle, Rule, Variable
        >>> import numpy as np
        >>> A1 = Term('A1', Triangle(0, 5, 10, label = '$A_1$'))
        >>> B1 = Term('B1', Triangle(0, 2, 4, label = '$B_1$'))      
        >>> v1 = Variable(np.linspace(0,15, 1000))
        >>> v2 = Variable(np.linspace(0, 10, 1000))
        >>> R = Rule().If(v1.Is(A1)).Then(v2.Is(B1))
        >>> A = Triangle(6, 8, 9).label('$A$')             
        >>> B = R.inference(v1.Is(A)).label('$B$')
        >>> A.plot(nrows = 2, xlim = [0,10]).add_plot(A1, alpha = 0.3).add_plot(B, xlim = [0,4], index= 1).add_plot(B1, index = 1, alpha = 0.3)
        
        .. image:: images/Rule.inference.png          
        """
        if 'T' not in kwargs:
            T = Operator().T_Z
        else:
            T = kwargs['T']    
        if 'T1' not in kwargs:
            T1 = Operator().T_Z
        else:
            T1 = kwargs['T1']                
        if 'R' not in kwargs:
            R = Operator().R_KD
        else:
            R = kwargs['R']
        # Verifications
        if len(args) != len(self._ruleIf):
            raise Exception('Length of If parts and number of arguments must be the same.')
        for ifPart in self._ruleIf:
            if not isinstance(ifPart, Variable):
                raise Exception('Variables in the If part must be instances of Variable.')  
            elif isinstance(ifPart._object, Multilinear) and  ifPart._object._universe is None:
                raise Exception('Variables in the If part must have a universe.')
        if not isinstance(self._ruleThen, Variable):
            raise Exception('Variable in the Then part must be an instance of Variable.')             
        precise_inputs = True
        for arg in args:
            if not isinstance(arg, Variable):
                raise TypeError('Variables in the antecedent part of the inference must be instances of Variable.')             
            if isinstance(arg._object, LR):
                precise_inputs = precise_inputs and arg._object.is_precise()
            else:
                precise_inputs = False
                
        if precise_inputs:
            return self._inference_with_precise_inputs(*args, **kwargs)
        
        # Computes f_A_prime 
        tstart = time.time()
        L = []   
        for arg in args:
            L.append(np.vectorize(arg._object.membership)(arg._object._universe))
        A_prime =  np.meshgrid(*L)         
        if len(args) > 1:
            f_A_prime = A_prime[0]
            for i in range(1, len(args)):
                f_A_prime = np.vectorize(T1)(f_A_prime, A_prime[i])
        else:
            f_A_prime = A_prime
        # print(f'f_A.prime = {f_A_prime}\n')          
        # Computes f_A
        L = []
        for ifPart in self._ruleIf: 
            L.append(np.vectorize(ifPart._object.membership)(ifPart._object._universe))
        A =  np.meshgrid(*L)  
        if len(args) > 1:
            f_A = A[0]
            for i in range(1, len(args)):
                f_A = np.vectorize(T1)(f_A, A[i])
        else:
            f_A = A   
        # print(f'f_A = {f_A}\n')         
        # Computes f_B
        f_B = np.vectorize(self._ruleThen._object.membership)(self._ruleThen._object._universe)
        if self._ruleWeight is not None:
            f_B = self._ruleWeight * f_B    
        # print(f'f_B = {f_B}\n' )
        # Computes f_B_prime
        L = []
        for i in range(len(self._ruleThen._object._universe)):
            f_R = np.vectorize(R)(f_A, f_B[i]) 
            f_B_prime = np.max(np.vectorize(T)(f_A_prime, f_R))            
            L.append((self._ruleThen._object._universe[i], f_B_prime))
        if 'time' in kwargs and kwargs['time']:
            tstop = time.time() 
            print(f'MPG in {tstop - tstart} s\n' )
        # return Variable(Discrete(*L)) 
        return Discrete(*L)     
    
    
    def If(self, *args):
        """
        Defines the If part of a rule.

        Parameters
        ----------
        *args : Variable
            Any number of variables.

        Returns
        -------
        Rule
            The rule object.

        """
        self._ruleIf = args
        return self    
    
    
    
    def Then(self, ruleThen):
        """
        Defines the Then part of a rule.

        Parameters
        ----------
        ruleThen : Variable
            The variable for the Then part.

        Returns
        -------
        Rule
            The rule object.

        """
        self._ruleThen = ruleThen
        return self  
    
    
    
    def Weight(self, ruleWeight):
        """
        Defines the Weigth of the rule

        Parameters
        ----------
        ruleWeight : float
            The weight.

        Returns
        -------
        Rule
            The rule object.

        """
        self._ruleWeight = ruleWeight
        return self  
    
       
    ###
    # Private methods
    #       
    
    def _inference_with_precise_inputs(self, *args, **kwargs):
        if 'R' not in kwargs:
            R = Operator().R_KD
        else:
            R = kwargs['R']    
        if 'T' not in kwargs:
            T = Operator().T_Z
        else:
            T = kwargs['T']               
        # Gets the precise inputs        
        x = []   
        for arg in args:
            x.append(arg._object.m)
        # Computes f_A for x
        L = []
        alpha = 1.0
        for i in range(len(self._ruleIf)): 
            alpha = T(alpha, self._ruleIf[i]._object.membership(x[i])) 
        # Computes f_B
        L = []
        f_B = np.vectorize(self._ruleThen._object.membership)(self._ruleThen._object._universe)
        # Computes f_B_prime
        L = []
        for i in range(len(self._ruleThen._object._universe)):
            f_B_prime = np.vectorize(R)(alpha, f_B[i])
            L.append((self._ruleThen._object._universe[i], f_B_prime))
        # return Variable(Discrete(*L))  
        return Discrete(*L)     
    
    
    def _sugeno_controller(self, *args):
 
        res = 1   
        for i in range(len(args)):
            res = Operator().T_P(res, self._ruleIf[i]._object.membership(args[i]._object))            

        x = np.vectorize(lambda obj: obj._object)(args)
        return Discrete((self._ruleThen._object(*x), res))    

        
        
    def _support(self, implication = False):
        A = self._ruleIf[0]._object.support()
        B = self._ruleThen._object.support()
        not_A = (~self._ruleIf[0]._object).kernel()
        # X = [self._ruleIf[0].bounds()[0], self._ruleIf[0].bounds()[1]]
        # Y = [self._ruleThen.bounds()[0], self._ruleThen.bounds()[1]]    
        X = [self._ruleIf[0]._object._bounds[0], self._ruleIf[0]._object._bounds[1]]
        Y = [self._ruleThen._object._bounds[0], self._ruleThen._object._bounds[1]]            
        B_X = Polygon([
            (X[0], B[0][0]), (X[0], B[0][1]),
            (X[1], B[0][1]), (X[1], B[0][0]), (X[0], B[0][0])
            ])    
        B_X = Polygon()            
        for i in range(0, len(B)):
            temp =  Polygon([
                (X[0], B[i][0]), (X[0], B[i][1]),
                (X[1], B[i][1]), (X[1], B[i][0]), (X[0], B[i][0])
                ])
            B_X = B_X.union(temp)  
        if implication:
            not_A_Y = Polygon([
                (not_A[0][0], Y[0]), (not_A[0][0], Y[1]),
                (not_A[0][1], Y[1]), (not_A[0][1], Y[0])
                ])  
            not_A_Y = Polygon()         
            for i in range(0, len(not_A)):
                if not_A[i][0] != not_A[i][1]:
                    temp =  Polygon([
                        (not_A[i][0], Y[0]), (not_A[i][0], Y[1]),
                        (not_A[i][1], Y[1]), (not_A[i][1], Y[0])
                        ])
                    not_A_Y = not_A_Y.union(temp) 
            P = not_A_Y.union(B_X)    
        else:
            A_Y = Polygon([
                (A[0][0], Y[0]), (A[0][1], Y[0]),
                (A[0][1], Y[1]), (A[0][0], Y[1])
                ])
            A_Y = Polygon()
            for i in range(0, len(A)):
                temp =  Polygon([
                    (A[i][0], Y[0]), (A[i][1], Y[0]),
                    (A[i][1], Y[1]),  (A[i][0], Y[1])
                    ])
                A_Y = A_Y.union(temp)  
            P = A_Y.intersection(B_X) 
        return P

    
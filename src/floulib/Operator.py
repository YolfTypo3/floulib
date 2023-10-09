# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 17:18:42 2023

@author: Laurent Foulloy
"""
  
class Operator:
    
    ###
    # Triangular norms
    #
    
    def T_L(self, x, y):  
        """
        Lukasiewicz triangular norm. 

        Parameters
        ----------
        x : float

        y : float

        Returns
        -------
        float
            max(x + y -1, 0)

        """
        return max(x + y -1.0, 0.0)  
    
    
    def T_P(self, x, y):
        """
        Probabilistic triangular norm. 

        Parameters
        ----------
        x : float

        y : float

        Returns
        -------
        float
            x * y

        """
        return x * y
    
    
    def T_Z(self, x, y): 
        """
        Zadeh triangular norm.

        Parameters
        ----------
        x : float

        y : float


        Returns
        -------
        float
            min(x, y)

        """
        return min(x, y)    
    

    ###
    # Triangular conorms
    #
    
    def S_L(self, x, y):
        """
        Lukasiewicz triangular conorm. 

        Parameters
        ----------
        x : float

        y : float

        Returns
        -------
        float
            min(x + y, 1)

        """        
        return min(x + y, 1)
    
    
    def S_P(self, x, y):
        """
        Probabilistic triangular conorm. 

        Parameters
        ----------
        x : float

        y : float

        Returns
        -------
        float
            x + y - x * y

        """        
        return x + y - x * y 
    
    
    def S_Z(self, x,y):
        """
        Zadeh triangular conorm

        Parameters
        ----------
        x : float

        y : float


        Returns
        -------
        float
            max(x, y)

        """
        return max(x, y)

    ###
    # Implications
    
   
    def R_BG(self, x, y):
        """
        Brower-Gödel implication
        
        Parameters
        ----------
        x : float

        y : float


        Returns
        -------
        float
            1 if x <= y
            y else
        """          
        if x <= y:
            return 1.0
        else:
            return y    
    
    
    def R_KD(self, x, y):
        
        """
        Kleene-Dienes implication

        Parameters
        ----------
        x : float

        y : float


        Returns
        -------
        float
            max(1 - x, y)
        """   
        return max(1.0 - x, y)

       
        
    def R_L(self, x, y):
        """
        Lukasiewicz implication

        Parameters
        ----------
        x : float

        y : float


        Returns
        -------
        float
            min(1 - x + y, 1)
        """        
        return min(1.0 - x + y, 1.0)  
    
    
    def R_M(self,x, y):
        """
        Mamdani so-called "implication"
        
        This so-called implication, widely used in fuzzy control
        is in fact a triangular norm (conjonctive representation of
        the rules).

        Parameters
        ----------
        x : float

        y : float


        Returns
        -------
        float
            min(x, y)
        """                  
        return min(x, y)
    
    
    def R_P(self,x, y):
        """
        Larsen so-called "implication"
        
        This so-called implication, also used in fuzzy control
        is in fact a triangular norm (conjonctive representation of
        the rules).

        Parameters
        ----------
        x : float

        y : float


        Returns
        -------
        float
            x * y
        """           
        
        return x * y


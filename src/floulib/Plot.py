# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 17:18:42 2023

@author: Laurent Foulloy
"""

import floulib as fl
from matplotlib.patches import Ellipse
import matplotlib.pyplot as plt
import numbers
import numpy as np
from shapely.plotting import plot_polygon


class Plot:
    """
    This class contains methods to plot various object.
    """
    
    ax = None
    """
    The Axes of the subplot.
    """
    
    _is_ploted = False
    _color = None
    _label = ''
    
    
    def plot(self, nrows = 1, ncols = 1, **kwargs):
       """
       Generic plot method

       Parameters
       ----------
       nrows : int, optional
           Number of rows of the plot. The default is 1.
       ncols : int, optional
           Number of columns of the plot. The default is 1.
       **kwargs : 
           
           - For :class:`Discrete`:
               - index: index of the plot. The default is 0.
               - xlim: x-limit for the plot. The default is None.
               - ylim: y-limit for the plot. The default is [0, 1.05].
               - coeff: coefficient used for scatter plot. The default is 0.25.
               - scatter: if True scatter plot is used otherwise conventional 
                 plot is used. Default is True.
               - any keyword argument accepted by matplotlib.scatter if scatter 
                 is True or by matplotlib.plot otherwise.
                 
           - For :class:`Multilinear`:
               - index: index of the plot. The default is 0.            
               - xlim: x-limit for the plot. The default is None.
               - ylim: y-limit for the plot. The default is [0, 1.05].                
               - vlines: if True, dashed vertical lines are plotted for
                 each point. Default is False.
               - any keyword argument accepted by matplotlib.plot.
                 
           - For :class:`Rule` or :class:`Rules`:
               - xlim: x-limit for the plot. The default is None.
               - ylim: y-limit for the plot. The default is None.                
               - implication: if True, an implicative view of the rule is 
                 considered for plotting the support, otherwise conjunctive
                 view is considered. Default is False. 
               - any keyword argument accepted by shapely.plotting.plot_polygon.

           - For :class:`Smiley`:
               - index: index of the plot. The default is 0.  
               
           - For :class:`Term` or :class:`Terms`:
               - index: index of the plot. The default is 0.
               - any keyword argument accepted by matplotlib.plot.

           - For :class:`Variable`:
               - index: index of the plot. The default is 0.
               - any keyword argument accepted by the type of the variable.

       Returns
       -------
       Plot
           The plot.
           
       
       
           
       """
       fig, self.ax = plt.subplots(nrows, ncols)
       self._is_plotted = False
       return self._plot(**kwargs)     
    
    

    def add_plot(self, other = None, **kwargs):
        """
        Adds a plot to a plot.

        Parameters
        ----------
        other : Discrete | Multilinear | Rule | Rules | Smiley | Term | Terms | Variable
            Parameter to add in the plot.
        **kwargs :
            Same parameters as for the method plot.

        Raises
        ------
        Exception
            Raised if the parmeter other is not provided.

        Returns
        -------
        Plot
            The plot.
            
        Example
        -------
        >>> from floulib import Discrete, Triangle
        >>> A = Triangle( 1, 2, 3, label = 'A')
        >>> B = Triangle(2, 3, 4, label = 'B')
        >>> A.plot(xlim = [0, 5]).add_plot(B)
        
        .. image:: images/Plot.add_plot_1.png
        
        >>> C = Discrete(('a', 0.3), ('b', 0.6), label = 'C')
        >>> A.plot(rows = 2, xlim = [0, 5]).add_plot(B).add_plot(C, index = 1)
        
        .. image:: images/Plot.add_plot_2.png
        """
        if other is not None:
            other.ax = self.ax
            other._is_plotted = self._is_plotted
            return other._plot(**kwargs)  
        else:
            raise Exception('Parameter of add_plot() is missing.')
    
    
    
    def color(self, color):
        """
        Sets the color of the plot.

        Parameters
        ----------
        color : matplotlib.colors
            The color.

        Returns
        -------
        Multilinear
            The multilinear fuzzy subset.
            
        Example
        -------
        >>> from floulib import Triangle
        >>> A = Triangle( 1, 2, 3)
        >>> A.color('orange').plot()
        
        .. image:: images/Plot.color.png
        
        """
        self._color = color 
        return self   
    


    def label(self, label):
        """
        Sets the label associated with the plot.

        Parameters
        ----------
        label : str
            The label.

        Returns
        -------
        Plot
            The plot object.
            
        Example
        -------
        >>> from floulib import Triangle
        >>> A = Triangle( 1, 2, 3)
        >>> A.label('A').plot()
        
        .. image:: images/Plot.label.png            
        """
        self._label = label
        return self       
    



    ###
    # Private methods
    #    

    # Gets the axes.          
    def _get_ax(self, index):
        if isinstance(self.ax, plt.Axes):
            return self.ax
        elif isinstance(self.ax, np.ndarray):
            if len(self.ax.shape) == 1:
                if index < self.ax.shape[0]:
                    return self.ax[index]
        else:
            print('_get_ax', type(self.ax))
            raise Exception('Should not go here')
                

    # Generic plot method.     
    def _plot(self, **kwargs):
        # print('-->', kwargs, type(self))
        
        if isinstance(self, fl.Multilinear):
            return self._plot_multilinear(**kwargs)
        elif isinstance(self, fl.Discrete):
            return self._plot_discrete(**kwargs)
        elif isinstance(self, fl.Variable):
            self._object._label = self._label
            self._set_context(to_object = self._object)
            obj = self._object._plot(**kwargs)
            self._set_context(from_object = obj)
            return self
        elif isinstance(self, fl.Term):   
            self._set_context(to_object = self._meaning)
            obj = self._meaning._plot(**kwargs)
            self._set_context(from_object = obj)
            return self
        elif isinstance(self, fl.Terms):
            return self._plot_terms(**kwargs)        
        elif isinstance(self, fl.Rule):
            return self._plot_rule(**kwargs)
        elif isinstance(self, fl.Rule):
            return self._plot_rules(**kwargs) 
        elif isinstance(self, fl.Rules):
            return self._plot_rules(**kwargs)        
        elif isinstance(self, fl.Smiley):
            return self._plot_smiley(**kwargs)       
        else:
            raise Exception(f'Plot() is not defined for {type(self)}')
        

    # Plots discrete fuzzy subsets.
    def _plot_discrete(self, index = 0, xlim = None, ylim = [0, 1.05], coeff = 0.25, scatter = True, **kwargs):
        if 'label' not in kwargs and self._label != '':
            kwargs['label'] = self._label
        if isinstance(self._universe[0], numbers.Number):
            x = self._universe
            y = self._memberships
            if not scatter:
                self._get_ax(index).set_ylim(ylim)
                self._get_ax(index).plot(x, y, **kwargs)              
            else:
                if 's' not in kwargs:
                    kwargs['s'] = 2  
                self._get_ax(index).set_ylim(ylim)                
                self._get_ax(index).scatter(x, y, **kwargs)                  
            if xlim is None:
                xlim = [x[0], x[-1]] 
            self._get_ax(index).set_xlim(xlim)               
            if 'label' in kwargs:
                self._get_ax(index).legend()
        else:
            for i in range(len(self.points)):              
                self._get_ax(index).set_ylim(ylim)  
                self._get_ax(index).plot([i, i], [0, self.points[i][1]], linestyle='dotted', **kwargs)
                self._get_ax(index).scatter(i, self.points[i][1], s = 20)
                if 'label' in kwargs:
                    self._get_ax(index).legend()
                    kwargs.pop('label')
            length = len(self.points) 
            self._get_ax(index).set_xlim([-(length - 1)*coeff, (length - 1)*(1.0 + coeff)])
            self._get_ax(index).set_xticks(range(length))  
            self._get_ax(index).set_xticklabels(self._universe)  
        self._is_plotted = True
        return self  


    # Plots multilinear fuzzy subsets.
    def _plot_multilinear(self, index = 0, xlim = None, ylim = [0, 1.05], vlines = False, **kwargs):          
        if self._color is not None:
            kwargs['color'] = self._color
        if 'label' not in kwargs and self._label != '':
            kwargs['label'] = self._label  

        if xlim is None:
            if self._is_plotted:
                start = self._get_ax(0).get_xlim()[0]
                stop = self._get_ax(0).get_xlim()[1]
            else:
                start = self.points[0][0]
                stop =  self.points[-1][0]
        else:
            start = xlim[0]
            stop = xlim[1]      
            
        pts = np.array([(start, self.points[0][1])])
        pts = np.concatenate((pts, self.points))
        pts = np.concatenate((pts, [(stop, self.points[len(self.points) - 1][1])]))
        x = pts[:, 0]
        y = pts[:, 1]

        self._get_ax(index).set_ylim(ylim)              
        self._get_ax(index).plot(x, y, **kwargs)          
        self._get_ax(index).set_xlim([start, stop])           
        color = self._get_ax(index).get_lines()[-1].get_color()
        if vlines:
            indices = np.where(y > 0.0)
            for i in indices[0]:
                self._get_ax(index).vlines(x[i], ymin = 0, ymax = y[i], color = color, linestyle = '--', linewidth = 0.85)         
        saved_label = None
        for i in range(len(pts) - 1):
            if abs(x[i+1] - x[i]) <= 10*self._precision:
                if 'label' in kwargs:
                    if saved_label is None:
                        saved_label = kwargs['label']
                    kwargs['label'] = ''
                if 'color' in kwargs:
                    kwargs.pop('color')  
                if 'linestyle' not in kwargs:
                    kwargs['linestyle'] = '--' 
                self._get_ax(index).plot([x[i], x[i + 1]], [y[i], y[i + 1]], color = 'white', **kwargs)    
        if saved_label is not None:
            kwargs['label'] = saved_label
        if 'label' in kwargs and kwargs['label'] != '':
            self._get_ax(index).legend()   
            
        self._is_plotted = True    
        return self        


    # Plots a rule.
    def _plot_rule(self, implication = False, xlim = None, ylim = None, **kwargs):
        if self._color is not None:
            kwargs['color'] = self._color  
        plot_polygon(self._support(implication), ax = self.ax, add_points = False, **kwargs)
        if xlim is not None:
            self.ax.set_xlim(xlim)
        else:
            self.ax.set_xlim(self._ruleIf[0]._object._bounds[0], self._ruleIf[0]._object._bounds[1])
        if ylim is not None:    
            self.ax.set_ylim(ylim)
        else:        
            self.ax.set_ylim(self._ruleThen._object._bounds[0], self._ruleThen._object._bounds[1])
        if 'label' in kwargs:
            self.ax.legend()   
        return self  
    
    
    # Plots rules.
    def _plot_rules(self, implication = False, xlim = None, ylim = None, **kwargs):
        if self._color is not None:
            kwargs['color'] = self._color
        plot_polygon(self._support(implication), ax=self.ax, add_points=False, **kwargs)
        if xlim is not None:
            self.ax.set_xlim(xlim)
        else:
            self.ax.set_xlim(self._object[0]._ruleIf[0]._object._bounds[0], self._object[0]._ruleIf[0]._object._bounds[1])
        if ylim is not None:    
            self.ax.set_ylim(ylim)
        else:        
            self.ax.set_ylim(self._object[0]._ruleThen._object._bounds[0], self._object[0]._ruleThen._object._bounds[1])
        if 'label' in kwargs:
            self.ax.legend()   
        return self    
    

    # Plots a smiley.
    def _plot_smiley(self, index = 0, **kwargs):
        head = plt.Circle((0, 0), 1, color = self._color)
        head.set_facecolor(self._color)
        self._get_ax(index).add_artist(head)
        left_eye = Ellipse((-0.4, 0.2), 0.2, 0.25*self.eye, color='black')
        right_eye = Ellipse((0.4, 0.2), 0.2, 0.25*self.eye, color='black')
        self._get_ax(index).add_artist(left_eye)
        self._get_ax(index).add_artist(right_eye)
        angles = np.linspace(np.pi/10, 9*np.pi/10, 100)
        self._get_ax(index).plot(0.5*np.cos(angles), -0.5 - self.smile*0.3*np.sin(angles)+np.sign(self.smile)*0.3*np.sin(np.pi/10), color='black')  
        self._get_ax(index).set_xlim(-1.2, 1.2)
        self._get_ax(index).set_ylim(-1.2, 1.2)
        self._get_ax(index).set_xticks([])
        self._get_ax(index).set_yticks([])
        self._get_ax(index).set_aspect('equal') 
        if self._label != '':
            self._get_ax(index).legend([self._label])    
        self._is_plotted = True    
        return self       

        
    # Plots terms.            
    def _plot_terms(self, index = 0, **kwargs):
        obj = self._object[0]
        if self.ax is None:
            obj.plot(**kwargs)
            self.ax = obj.ax
            self._is_plotted = obj._is_plotted
        else:
            obj.ax = self.ax
            obj._is_plotted = self._is_plotted 
            obj._plot(**kwargs)
            self.ax = obj.ax
            self._is_plotted = obj._is_plotted            
        for i in range(1, len(self._object)):
            self.add_plot(self._object[i], **kwargs)
        return self        


    # Sets self context from object.
    def _set_context(self, from_object = None, to_object = None):
        if from_object is None:
            from_object = self
        if to_object is None:
            to_object = self            
        to_object.ax = from_object.ax
        to_object._is_plotted = from_object._is_plotted         
        
  
     
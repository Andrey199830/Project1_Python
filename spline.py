from PyQt5.QtCore import QPointF, QPoint, pyqtSignal
from PyQt5.QtGui import QPolygonF
from typing import List
from knot import Knot
import copy

import math

class Spline():

    def __init__(self) -> None:
        
        self.knots: List[Knot] = [] 
        self.curve = None 
        
        self.subdivs=50 
        self.uStep = 1.0 / self.subdivs 

        self.subdivsBezier=50
        self.tStep=1.0/self.subdivsBezier
        P=QPointF(0,0)

        self.historySpline: List = [[] for i in range(31)] 
        self.historySplineKnotIndex:List = [[] for i in range(31)]  
        self.historySplineKnotIndexVivod: List = []   

        self.addPointscurentknots: List = [[] for i in range(1)]
        self.addPointscurentknotsVivod: List = [1]
        self.ChangePolLine = "Kochanek–Bartels"  
        

    def get_knots(self) -> List[Knot]:
        return self.knots


    def get_historyspline(self):
        return self.historySpline
    

    def get_historySplineKnotIndex(self):  
        return self.historySplineKnotIndex


    def get_historySplineKnotIndexVivod(self):
        return self.historySplineKnotIndexVivod
    

    def get_addPointscurentknots(self):
        return self.addPointscurentknots


    def get_addPointscurentknotsVivod(self):
        return self.addPointscurentknotsVivod
    
    
    def ResulPolyline(self, Value:str):    
        self.ChangePolLine = Value
    
      
    def get_curve(self) -> QPolygonF:
        
        if (self.ChangePolLine == 'Kochanek–Bartels'):
            if self.curve is None:
                    self._interpolate()
            return self.curve or QPolygonF()
        
        if (self.ChangePolLine == 'Bezier'):
            if self.curve is None:
                    self._Bezier()
            return self.curve or QPolygonF()
        
        if (self.ChangePolLine == 'Poline'):   
            if self.curve is None:
                points=[knot.pos for knot in self.knots]
            return QPolygonF(points) or QPolygonF()
            

    def insert_knot(self, index, pos) -> None:  
        if index==None:
            self.knots.append(Knot(QPointF(pos))) 
        else:
            self.index_knot=index+1
            self.knots.insert(self.index_knot, Knot(QPointF(pos))) 
        self.curve=None
        
    def delete_knot(self, index) -> None:   
            self.knots.pop(index)   
            self.curve=None

    def up_knots(self, index, pos) -> None:  
        self.knots[index].pos = QPointF(pos)
        self.curve=None

    def get_knot_by_pos(self, pos: QPointF) -> int:    
        for index, knot in enumerate(self.knots):
            if(knot.pos-pos).manhattanLength()<8:  
                return index


    def set_current_knot(self, index, value: Knot):
        if not self.knots:
            return
        self.knots[index] = value
        self.curve = None


    def SplineHistory(self, NumberPlace, index):   
     
        if((NumberPlace)>len(self.historySpline)):
            self.historySpline.pop(0)
            self.historySpline.append([])
            NumberPlace=len(self.historySpline)

            self.historySplineKnotIndex.pop(0)
            self.historySplineKnotIndex.append([])

        self.knots_copy = copy.deepcopy(self.get_knots())         
        self.historySpline[NumberPlace-1]=self.knots_copy
        self.historySplineKnotIndex[NumberPlace-1].append(index)    
        self.curve = None

        
    def set_current_polyline(self, value:str):    
        self.ChangePolLine = value
        self.curve = None
        return self.ChangePolLine


    def ResulSavePolyline(self):    
        return self.ChangePolLine

    
    def _interpolate(self) -> QPolygonF: 
        if len(self.knots) < 2:
            return

        self.curve = QPolygonF()

        for k in range(len(self.knots) - 1):
            prev: Knot = self.knots[k] if k == 0 else self.knots[k - 1]
            cur: Knot = self.knots[k]
            next1: Knot = self.knots[k + 1]
            next2: Knot = (
                self.knots[k + 1] if k + 2 >= len(self.knots) else self.knots[k + 2]
            )

            t = cur.tension
            b = cur.bias
            c = cur.continuity

            d0 = (
                0.5
                * (1 - t)
                * (
                    (1 + b) * (1 - c) * (cur.pos - prev.pos)
                    + (1 - b) * (1 + c) * (next1.pos - cur.pos)
                )
            )

            t = next1.tension
            b = next1.bias
            c = next1.continuity

            d1 = (
                0.5
                * (1 - t)
                * (
                    (1 + b) * (1 + c) * (next1.pos - cur.pos)
                    + (1 - b) * (1 - c) * (next2.pos - next1.pos)
                )
            )

            u = 0.0
            for _ in range(self.subdivs):
                
                u2 = u * u
                u3 = u * u * u
                
                self.curve.append(
                    (2 * u3 - 3 * u2 + 1) * cur.pos
                    + (-2 * u3 + 3 * u2) * next1.pos
                    + (u3 - 2 * u2 + u) * d0
                    + (u3 - u2) * d1
                )
                u += self.uStep

        self.curve.append(self.knots[-1].pos)
        


    def _Bezier(self) -> QPolygonF: 
        
        if len(self.knots) < 2:
            return
        
        self.curve = QPolygonF()
 
        def P(x: float):
            P=QPointF(0,0)
            i=0
            for i in range(len(self.knots)):
                P = P + ( (math.factorial(len(self.knots)-1)) / ((math.factorial(i))*(math.factorial(len(self.knots)-i-1))) )* pow((1-x),(len(self.knots)-1-i))*pow(x,i)*self.knots[i].pos  
            return P
          
        t = 0.0
        for _ in range(self.subdivsBezier+1):
            self.curve.append(P(t))
            t = t + self.tStep
    

       
import sys
from PyQt5.QtWidgets import QWidget, QLabel, QMessageBox
from PyQt5.QtGui import QPainter, QColor, QPalette, QPen, QBrush
from PyQt5.QtCore import Qt, pyqtSignal, QPointF
from spline import Spline
from control_panel import ControlPanel
from knot import Knot
from typing import List
import pickle              
import copy


class SplineView(QWidget):
    
    current_knot_changed = pyqtSignal(Knot) 
    current_polyline = pyqtSignal(str) 
    
    def __init__(self, parent = None)->None:
        super().__init__(parent)
        
        self.spline=Spline()
    
        self.cur_knot_index=None    
        self.Editor = False    

        self.ClickMouse=0      
        self.undoClick=0       
        self.RedoClick=0 
        self.current_pos=0

        self.CheckClick=False        
        self.takepoints=None
        self.MouseOtpyst=False

        self.EmtyMas=False
        self.CliclMouseBool=False


    def paintEvent(self, event) -> None: 
        bg_color=self.palette().color(QPalette.Base)   
        curve_color=QColor(138,43,226)  
        curve_color_point = QColor(0,255,0) 
        painter=QPainter(self)
        painter.fillRect(self.rect(), bg_color)     
        painter.setPen(QPen(curve_color, 3, Qt.SolidLine))  
        painter.setRenderHints(QPainter.HighQualityAntialiasing) 

        painter.drawPolyline(self.spline.get_curve()) 
        painter.setBrush(QBrush(curve_color_point, Qt.SolidPattern)) 
        
        for index, knot in enumerate(self.spline.get_knots()):
            radius =  6 if self.cur_knot_index == index else 4 
            painter.drawEllipse(knot.pos, radius, radius)

        self.update()
        return super().paintEvent(event)
    
 
    def mousePressEvent(self, event) -> None:
        
        if event.button() == Qt.LeftButton: 
            self.CheckClick=False
            self.EmtyMas=False
           
            index=self.spline.get_knot_by_pos(event.pos()) 
    
            if index is not None:
                if(self.undoClick!=0):                                                                   
                            self.ClickMouse=self.ClickMouse+1       
                            self.spline.SplineHistory(self.ClickMouse, self.cur_knot_index)              
                            self.undoClick=0
                            self.RedoClick=0 
                            self.takepoints=self.cur_knot_index
                
                self.cur_knot_index = index
                self.copy_knots=copy.deepcopy(self.spline.get_knots())
                self.current_knot_changed.emit(self.copy_knots[self.cur_knot_index]) 

                if(index!=self.takepoints):
                        self.ClickMouse = self.ClickMouse+1
                        self.spline.SplineHistory(self.ClickMouse, self.cur_knot_index)
                        self.takepoints=index
                return
            else:
                if(self.undoClick!=0):                                                               
                    if(not self.spline.get_knots()):              
                        self.ClickMouse=self.ClickMouse+1
                        self.spline.SplineHistory(self.ClickMouse, -2)
                        self.undoClick=0
                        self.RedoClick=0
                        self.EmtyMas=True 
                    else:
                        self.ClickMouse=self.ClickMouse+1  
                        self.spline.SplineHistory(self.ClickMouse, self.cur_knot_index)                    
                        self.undoClick=0
                        self.RedoClick=0   
    
                self.spline.insert_knot(self.cur_knot_index, event.pos())
                self.cur_knot_index = len(self.spline.get_knots())-1    
                    
                if(self.EmtyMas==True):
                    self.current_knot_changed.emit(Knot(QPointF(0,0))) 
                else:
                    self.copy_knots=copy.deepcopy(self.spline.get_knots())
                    self.current_knot_changed.emit(self.copy_knots[self.cur_knot_index]) 

                
                self.ClickMouse = self.ClickMouse+1
                self.spline.SplineHistory(self.ClickMouse, self.cur_knot_index)
                self.takepoints=len(self.spline.get_knots())-1    



        if event.button() == Qt.RightButton:          
            
                if not self.spline.get_knots():  
                    return
                elif self.cur_knot_index is not None:
                    self.spline.delete_knot(self.cur_knot_index)       
                    self.cur_knot_index = len(self.spline.get_knots())-1    
                
                    if(self.undoClick!=0):                                                                  
                        self.ClickMouse=self.ClickMouse+1       
                        self.spline.SplineHistory(self.ClickMouse, self.cur_knot_index)                     
                        self.undoClick=0
                        self.RedoClick=0
                    
                    self.ClickMouse = self.ClickMouse+1
                    self.spline.SplineHistory(self.ClickMouse, self.cur_knot_index)
                    self.takepoints=len(self.spline.get_knots())-1 
                
                else:
                
                    return 
        
                if (len(self.spline.get_knots())==0):
                    self.current_knot_changed.emit(Knot(QPointF(0,0)))
                else:
                    self.copy_knots=copy.deepcopy(self.spline.get_knots())
                    self.current_knot_changed.emit(self.copy_knots[self.cur_knot_index])  
     
        self.spline.curve=None
        self.update()
        return super().mousePressEvent(event)
    
    
    def DefineBool(self, bool_condition:bool): 
        self.Editor = bool_condition
        self.DoneShiftMouseadd()
    
    
    def mouseMoveEvent(self, event):                   
 
                if(self.undoClick!=0):                                                                
                    self.ClickMouse=self.ClickMouse+1       
                    self.spline.SplineHistory(self.ClickMouse, self.cur_knot_index)                     
                    self.undoClick=0
                    self.RedoClick=0   
                
                
                self.CheckClick=False
                if self.Editor == True: 
                    self.spline.up_knots(self.cur_knot_index, event.pos())
                    self.copy_knots=copy.deepcopy(self.spline.get_knots())
                    self.current_knot_changed.emit(self.copy_knots[self.cur_knot_index])            
                    self.CheckClick=True
                
                self.update()
                self.spline.curve=None
                return super().mouseMoveEvent(event)
    

    def mouseReleaseEvent(self, event):                      
       
        self.MouseOtpyst=True
        self.update()
        self.spline.curve=None
        self.DoneShiftMouseadd()
        return super().mouseReleaseEvent(event)
    
    
    def DoneShiftMouseadd(self):
        
        if (self.CheckClick == True and self.Editor == False and self.MouseOtpyst==True):
      
                self.ClickMouse=self.ClickMouse+1       
                self.spline.SplineHistory(self.ClickMouse, self.cur_knot_index)
                self.CheckClick = False
                self.MouseOtpyst=False

        self.update()
        self.spline.curve=None
    

    def set_current_knot(self, value: Knot): 
        
        if(self.undoClick!=0):
            self.ClickMouse=self.ClickMouse+1 
            self.spline.SplineHistory(self.ClickMouse, self.cur_knot_index)
            self.undoClick=0
            self.RedoClick=0
       
        self.spline.set_current_knot(self.cur_knot_index, value)

        self.ClickMouse = self.ClickMouse+1
        self.spline.SplineHistory(self.ClickMouse, self.cur_knot_index)
        
        self.update() 
        self.spline.curve = None


    def set_current_Polyline(self, Value: str):    
         self.spline.set_current_polyline(Value)
         self.update() 

  
    def SaveAs(self):            
        f = open('Spline', 'wb')
        pickle.dump([self.spline.get_knots(), self.cur_knot_index, self.spline.ResulSavePolyline()], f) 
        f.close()


    def Open(self):         

        for k in range(len(self.spline.get_knots())):
            self.spline.delete_knot(-1)
        
        f = open('Spline', 'rb')
        loadData = pickle.load(f)    
        self.spline.get_knots()[1:1]=loadData[0]  
        self.cur_knot_index=loadData[1]  
        self.ChangePolLine=loadData[2] 
        self.spline.ResulPolyline(self.ChangePolLine)
    
        self.current_knot_changed.emit(self.spline.get_knots()[self.cur_knot_index])
        self.current_polyline.emit(self.ChangePolLine)
        self.update()


    def UndoViewSplineHistory(self):
     
        if(self.ClickMouse>len(self.spline.get_historyspline())):
            self.ClickMouse=len(self.spline.get_historyspline())
            self.CliclMouseBool=True

        self.undoClick=self.undoClick+1
       
        self.current_pos=self.ClickMouse-self.undoClick+self.RedoClick-1
        
        if(self.current_pos<0):
           
            if(self.CliclMouseBool==False):
                self.spline.get_knots().clear()
                self.undoClick=self.undoClick-1
                self.current_knot_changed.emit(Knot(QPointF(0,0))) 
                self.update()
                self.spline.curve=None
            else:    
                self.undoClick=self.undoClick-1
        
        else:      
            self.spline.get_knots().clear()
            self.copy_history=copy.deepcopy(self.spline.get_historyspline())
            self.spline.get_knots()[1:1]=(self.copy_history[self.current_pos])
            
            self.spline.get_historySplineKnotIndexVivod()[:]=[]
            self.spline.get_historySplineKnotIndexVivod()[1:1]=self.spline.get_historySplineKnotIndex()[self.current_pos]
            self.cur_knot_index = self.spline.get_historySplineKnotIndexVivod()[0]
    
            self.copy_knots=copy.deepcopy(self.spline.get_knots())

            if (not self.copy_knots):
                self.current_knot_changed.emit(Knot(QPointF(0,0))) 
            else:
                self.current_knot_changed.emit(self.copy_knots[self.cur_knot_index]) 
         
        self.update()
        self.spline.curve=None   
        
    
    def RedoViewSplineHistory(self):
        
        self.current_pos=self.ClickMouse-self.undoClick+self.RedoClick-1

        if(self.ClickMouse-self.undoClick+self.RedoClick-1-1<0 and not self.spline.get_knots()):
            self.current_pos=-1
            self.RedoClick=self.RedoClick-1

        if(self.current_pos > self.ClickMouse-2):
            return
        
        else:
            self.RedoClick=self.RedoClick+1
            self.current_pos=self.current_pos+1
            self.spline.get_knots().clear()
        
            self.copy_history=copy.deepcopy(self.spline.get_historyspline())
            self.spline.get_knots()[1:1]=(self.copy_history[self.current_pos])
          
            self.spline.get_historySplineKnotIndexVivod()[:]=[]
            self.spline.get_historySplineKnotIndexVivod()[1:1]=self.spline.get_historySplineKnotIndex()[self.current_pos]
            self.cur_knot_index = self.spline.get_historySplineKnotIndexVivod()[0]
            self.copy_knots=copy.deepcopy(self.spline.get_knots())
            
            if (not self.copy_knots):
                self.current_knot_changed.emit(Knot(QPointF(0,0))) 
            else:
                self.current_knot_changed.emit(self.copy_knots[self.cur_knot_index])
         
        self.update()
        self.spline.curve=None   
        self.spline.get_curve()



    def About(self):    
        alert = QMessageBox()
        alert.setWindowTitle("Информация")
        alert.setText("Автор: Борисов Андрей Александрович \nОписание проекта находится в файле README.txt")
        alert.exec()


    
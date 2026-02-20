from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSpinBox, QDoubleSpinBox,  QComboBox, QLabel  

from PyQt5.QtCore import QPointF, pyqtSignal  
from knot import Knot
from spline import Spline


class ControlPanel(QWidget):
    state_changed = pyqtSignal(Knot)                 
    changedPolyline = pyqtSignal(str)  

    def __init__(self, width: int, height: int, parent = None):  
        super().__init__(parent)

        self.spline=Spline()

        self.state = Knot(QPointF(0,0)) 
    
        layout = QHBoxLayout()   
    
        self.x_spinbox = QSpinBox()
        self.x_spinbox.setMaximum(width)
        self.x_spinbox.setPrefix('X = ')     

        self.x_spinbox.valueChanged.connect(self.set_x)  

        self.x_spinbox.setSingleStep(20)  

        self.y_spinbox = QSpinBox()
        self.y_spinbox.setMaximum(height)
        self.y_spinbox.setPrefix('Y = ')     

        self.y_spinbox.valueChanged.connect(self.set_y)

        self.y_spinbox.setSingleStep(20)

        layout.addWidget(self.x_spinbox)
        layout.addWidget(self.y_spinbox)

        def create_spinbox(prefix:str, min: float, max: float, slot) ->QDoubleSpinBox:
            spin=QDoubleSpinBox()
            spin.setPrefix(prefix)
            spin.setMinimum(min)
            spin.setMaximum(max)

            spin.setSingleStep(0.1)

            spin.valueChanged.connect(slot)

            layout.addWidget(spin)
            return spin

        self.t_spinbox = create_spinbox('T = ', -1000, 1000, self.set_tension) 
        self.b_spinbox = create_spinbox('B = ', -1000, 1000, self.set_bias)
        self.c_spinbox = create_spinbox('C = ', -1000, 1000, self.set_continuity)


        self.label = QLabel()
        layout.addWidget(self.label)
        self.label.setText('Change polyline')
        self.ChangePolylien = QComboBox(self)
        layout.addWidget(self.ChangePolylien)
        
        self.ChangePolylien.addItems(['Kochanek–Bartels', 'Bezier', 'Poline'])
        self.ChangePolylien.currentIndexChanged.connect(self.CurrentValue)
        
        self.setLayout(layout)

            
    def set_x(self, value: float):
        if value == self.state.pos.x():
            return
        self.state.pos.setX(value)    
        self.state_changed.emit(self.state)
        

    def set_y(self, value: float):
        if value == self.state.pos.y():
           return
        self.state.pos.setY(value)
        self.state_changed.emit(self.state)
    
       
    def set_tension(self, value: float):
        if value == self.state.tension:
            return
        self.state.tension = round(value,1)
        self.state_changed.emit(self.state)
   

    def set_bias(self, value: float):
        if value == self.state.bias:
            return
        self.state.bias = round(value,1)
        self.state_changed.emit(self.state)
        

    def set_continuity(self, value: float):
        if value == self.state.continuity:
            return
        self.state.continuity = round(value,1)
        self.state_changed.emit(self.state)
        

    def set_state(self, value: Knot):   
        self.state = value
        self.x_spinbox.setValue(round(value.pos.x()))
        self.y_spinbox.setValue(round(value.pos.y()))
        self.t_spinbox.setValue(round(value.tension,1))
        self.b_spinbox.setValue(round(value.bias,1))
        self.c_spinbox.setValue(round(value.continuity,1))

    
    def CurrentValue(self):
        Polylien= self.ChangePolylien.currentText()
        self.changedPolyline.emit(Polylien)
    
    
    def set_Polyline(self, value: str):
        self.changePol = value
        self.ChangePolylien.setCurrentText(self.changePol)
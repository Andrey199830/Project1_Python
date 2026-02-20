from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt, QSize, pyqtSignal


from spline_view import SplineView
from control_panel import ControlPanel


class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.button_condition=False
        
        self.spline_view = SplineView()
       
        menubar=self.menuBar()            

        self.setCentralWidget(self.spline_view)  

        menubar=self.menuBar()            

        file_menu=menubar.addMenu('File')

        file_Save=file_menu.addAction('Save(Ctr+S)')  
        file_Save.triggered.connect(self.spline_view.SaveAs)

        file_Open=file_menu.addAction('Open(Ctr+O)')  
        file_Open.triggered.connect(self.spline_view.Open)
        
        close_action=file_menu.addAction('Close')
        close_action.triggered.connect(self.close)

        file_menu=menubar.addMenu('Edit')
        Undo_action=file_menu.addAction('Undo(Ctr+Z)')
        Undo_action.triggered.connect(self.spline_view.UndoViewSplineHistory)

        Redo_action=file_menu.addAction('Redo(Shift+Ctr+Z)')
        Redo_action.triggered.connect(self.spline_view.RedoViewSplineHistory)

        about_menu=menubar.addAction('About')
        about_menu.triggered.connect(self.spline_view.About)
    
        control_panel = ControlPanel(self.spline_view.maximumWidth(), self.spline_view.maximumHeight())
        self.statusBar().addWidget(control_panel)  
        
        control_panel.state_changed.connect(self.spline_view.set_current_knot)  
        self.spline_view.current_knot_changed.connect(control_panel.set_state)  

        control_panel.changedPolyline.connect(self.spline_view.set_current_Polyline) 
        self.spline_view.current_polyline.connect(control_panel.set_Polyline)


    def keyPressEvent(self, button):
        if button.key() == Qt.Key_Shift:
            self.button_condition=True
            self.spline_view.DefineBool(self.button_condition)

        if button.modifiers() & Qt.ControlModifier: 
            if button.key() == Qt.Key_S :
                self.spline_view.SaveAs()

        if button.modifiers() & Qt.ControlModifier:
            if button.key() == Qt.Key_O :
                self.spline_view.Open()
       
        if button.modifiers() & Qt.ControlModifier:
            if button.modifiers() & Qt.ShiftModifier:
                if button.key() == Qt.Key_Z :
                    self.spline_view.RedoViewSplineHistory()
            elif button.key() == Qt.Key_Z :
                    self.spline_view.UndoViewSplineHistory()
        

    def keyReleaseEvent(self, button):
        if button.key() == Qt.Key_Shift:
                self.button_condition=False
                self.spline_view.DefineBool(self.button_condition)
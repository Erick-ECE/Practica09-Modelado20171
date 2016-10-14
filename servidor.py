import sys
from PyQt4 import QtGui, QtCore, uic
import random

class Serpiente():
    def __init__(self, red, green, blue):
        self.color = (red, green, blue)
        self.cuerpo =  [[0,0],[0,1],[0,2], [0,3], [0,4], [0,5], [0,6], [0,7], [0,8]]
        self.longitud = len(self.cuerpo)
        self.direccion = 1 #Inicialmente va a la derecha

class VentanaServidor(QtGui.QMainWindow):
    def __init__(self):
        super(VentanaServidor, self).__init__()
        uic.loadUi('servidor.ui', self)
        self.juegoComenzado = self.juegoPausado = False
        self.timer = None
        self.serpientes = []
        self.serpientes_len = len(self.serpientes)
        self.tabla.setSelectionMode(QtGui.QTableWidget.NoSelection)
        self.actualizarCeldas()
        self.llenarTabla()
        self.columnas.valueChanged.connect(self.actualizarTabla)
        self.filas.valueChanged.connect(self.actualizarTabla)
        self.spinBox.valueChanged.connect(self.actualizarTimer)
        self.botonInicio.clicked.connect(self.actualizaJuego)
        self.botonTermino.hide()
        self.botonTermino.clicked.connect(self.terminarJuego)
        self.show()

    def llenarTabla(self):
        for i in range(self.tabla.rowCount()):
            for j in range(self.tabla.columnCount()):
                self.tabla.setItem(i, j, QtGui.QTableWidgetItem())
                self.tabla.item(i,j).setBackground(QtGui.QColor(255,255,255))

    def actualizarCeldas(self):
        self.tabla.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.tabla.verticalHeader().setResizeMode(QtGui.QHeaderView.Stretch)

    def actualizarTabla(self):
        rows = self.filas.value()
        columns = self.columnas.value()
        self.tabla.setRowCount(rows)
        self.tabla.setColumnCount(columns)
        self.llenarTabla()

    def actualizarTimer(self):
        value = self.spinBox.value()
        self.timer.setInterval(value)

    def actualizaJuego(self):
        if not self.juegoComenzado:
            self.botonTermino.show()
            self.botonInicio.setText('Pausar el Juego')
            serpiente = Serpiente(random.randrange(0,255), random.randrange(0,255), random.randrange(0,255))
            self.serpientes.append(serpiente)
            self.serpientes_len += 1
            self.colorearSerpientes()
            self.timer = QtCore.QTimer(self)
            self.timer.timeout.connect(self.moverSerpientes)
            self.timer.start(200)
            self.tabla.installEventFilter(self)
            self.juegoComenzado = True
        elif self.juegoComenzado and not self.juegoPausado:
            self.timer.stop()
            self.juegoPausado = True
            self.botonInicio.setText("Continuar juego")
        elif self.juegoComenzado and self.juegoPausado:
            self.timer.start()
            self.juegoPausado = False
            self.botonInicio.setText("Pausar Juego")

    def terminarJuego(self):
        self.timer.stop()
        self.serpientes = []
        self.juegoComenzado = False
        self.juegoPausado = False
        self.botonTermino.hide()
        self.botonInicio.setText('Iniciar Juego')
        self.llenarTabla()

    def colorearSerpientes(self):
        for serpiente in self.serpientes:
            for cuerpo_part in serpiente.cuerpo:
                self.tabla.item(cuerpo_part[0], cuerpo_part[1]).setBackground(QtGui.QColor(serpiente.color[0], serpiente.color[1], serpiente.color[2]))

    def moverSerpientes(self):
        for serpiente in self.serpientes:
            if self.colision(serpiente):
                self.serpientes.remove(serpiente)
                self.serpientes_len -= 1
                if self.serpientes_len == 0:
                    self.terminarJuego()
                    return
                self.llenarTabla()
            self.tabla.item(serpiente.cuerpo[0][0],serpiente.cuerpo[0][1]).setBackground(QtGui.QColor(255,255,255))
            aux = 1
            for cuerpo_part in serpiente.cuerpo[0:-1]:
                cuerpo_part[0] = serpiente.cuerpo[aux][0]
                cuerpo_part[1] = serpiente.cuerpo[aux][1]
                aux += 1

            if serpiente.direccion == 0:
                if serpiente.cuerpo[-1][0] != 0:
                    serpiente.cuerpo[-1][0] -= 1
                else:
                    serpiente.cuerpo[-1][0] = self.tabla.rowCount()-1
            elif serpiente.direccion == 1:
                if serpiente.cuerpo[-1][1] < self.tabla.columnCount()-1:
                    serpiente.cuerpo[-1][1] += 1
                else:
                    serpiente.cuerpo[-1][1] = 0
            elif serpiente.direccion == 2:
                if serpiente.cuerpo[-1][0] < self.tabla.rowCount()-1:
                    serpiente.cuerpo[-1][0] += 1
                else:
                    serpiente.cuerpo[-1][0] = 0
            elif serpiente.direccion == 3:
                if serpiente.cuerpo[-1][1] != 0:
                    serpiente.cuerpo[-1][1] -= 1
                else:
                    serpiente.cuerpo[-1][1] = self.tabla.columnCount()-1
        self.colorearSerpientes()

    def colision(self, serpiente):
        for current_serpiente in self.serpientes:
            if serpiente != current_serpiente:
                if serpiente.cuerpo[-1][0] == current_serpiente.cuerpo[-1][0] and (
                    serpiente.cuerpo[-1][1] == current_serpiente.cuerpo[-1][1]):
                    return True

            for cuerpo_part in current_serpiente.cuerpo[0:-1]:
                if serpiente.cuerpo[-1][0] == cuerpo_part[0] and (
                    serpiente.cuerpo[-1][1] == cuerpo_part[1]):
                    return True
            return False

    def eventFilter(self, source, event):
        if (event.type() == QtCore.QEvent.KeyPress) and (
            source is self.tabla):
            key = event.key()
            if (key == QtCore.Qt.Key_Up and
                source is self.tabla):
                for serpiente in self.serpientes:
                    if serpiente.direccion != 2:
                        serpiente.direccion = 0
            elif (key == QtCore.Qt.Key_Down and
                source is self.tabla):
                for serpiente in self.serpientes:
                    if serpiente.direccion != 0:
                        serpiente.direccion = 2
            elif (key == QtCore.Qt.Key_Right and
                source is self.tabla):
                for serpiente in self.serpientes:
                    if serpiente.direccion != 3:
                        serpiente.direccion = 1
            elif (key == QtCore.Qt.Key_Left and
                source is self.tabla):
                for serpiente in self.serpientes:
                    if serpiente.direccion != 1:
                        serpiente.direccion = 3
        return QtGui.QMainWindow.eventFilter(self, source, event)

def main():
    app = QtGui.QApplication(sys.argv)
    window = VentanaServidor()
    sys.exit(app.exec_())

main()

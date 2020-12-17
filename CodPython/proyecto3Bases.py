from PyQt5.QtCore import *
from qgis.core import *
import qgis.utils
import psycopg2
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *


# creación de una nueva capa
vl = QgsVectorLayer("POINT?crs=EPSG:4326", "empresas", "memory")
# Instanciación del proveedor de datos de la nueva capa

pr = vl.dataProvider()

# add fields
pr.addAttributes( [ QgsField("nombre", QVariant.String)] )

# Instanciación del gruporaíz del arbol de capas

layerTree = iface.layerTreeCanvasBridge().rootGroup()

# Inserción de la nueva capa en la pocisión 0 del panel de capas
layerTree.insertChildNode(0, QgsLayerTreeLayer(vl))

canvas = qgis.utils.iface.mapCanvas()
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Filtros")
        self.setGeometry(0, 0, 320, 270)
        self.UiComponents()
        
        self.show()
    def showDate(self):
        # Función a ejecutar por el hilo
        def ver_datos(valor):
            conn = psycopg2.connect(
                host="localhost",
                database="localproyecto3db2",
                user="remote_user",
                password="admin")
            cur = conn.cursor()
            if(valor=='1'):
                cur.execute("select nombre,st_astext(geom) from empresa where (departamentos->>'nombre')='Contabilidad'")
            if(valor=='2'):
                cur.execute("select nombre,st_astext(geom) from empresa where (departamentos->>'nombre')='RRHH'")
            if(valor=='3'):
                cur.execute("select nombre,st_astext(geom) from empresa where (departamentos->>'nombre')='Registro'")
            
            empresas = cur.fetchall() 
            vl.startEditing()
            for row in empresas:
                print(row[0])
                feature = QgsFeature()
                feature.setGeometry( QgsGeometry.fromWkt(row[1]))
                feature.setAttributes([row[0]])
                # Inicia edición agrega la geometría y acepta los cambios
                pr.addFeatures( [feature] )
            vl.commitChanges()
            # Actualiza la extensión de la nueva capa 
            vl.updateExtents() 
            canvas.setExtent(vl.extent())
        data = self.cb.currentText()
        ver_datos(data)
    def UiComponents(self):
        self.cb = QComboBox(self)
        l1 = QLabel(self)
        l1.setText("Elija filtro")
        self.cb.addItems(["1","2","3"])
        l1.setGeometry(QtCore.QRect(35, 30, 150, 22))
        self.cb.setGeometry(QtCore.QRect(100, 30, 150, 22))
        button = QPushButton(self)
        button.setText("Aplicar filtro")
        button.pressed.connect(self.showDate)
        button.setGeometry(100, 75, 150, 30)
        
window = Window()


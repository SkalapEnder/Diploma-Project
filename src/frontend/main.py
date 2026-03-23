from PySide6.QtGui import (QStandardItemModel, QStandardItem, QPixmap)
from PySide6.QtWidgets import (QApplication, QMainWindow, QDialog, QPushButton, QFileDialog, QGraphicsScene, QGraphicsPixmapItem)
from PySide6.QtCore import Qt, QRectF
from ui_import import Ui_MainWindow, Ui_AboutDialog
import sys
import os

zoomStep = 0.1
zoomFactor = 1.0

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.set_controls_enabled(False)
        
        self.model = QStandardItemModel()
        self.ui.imageListViewer.setModel(self.model)
        
        self.scene = QGraphicsScene()
        self.ui.graphicsView.setScene(self.scene)

        self.image_paths = []
        
        self.ui.actionAbout.triggered.connect(self.open_about)
        self.ui.actionExit.triggered.connect(self.close_app)
        self.ui.actionLoadImages.triggered.connect(self.open_images)
        
        self.ui.imageListViewer.clicked.connect(self.show_selected_image)
        self.ui.pushButtonLoadImages.clicked.connect(self.open_images)
        self.ui.pushButtonDeleteImage.clicked.connect(self.delete_selected_image)
        self.ui.pushButtonDeleteAll.clicked.connect(self.delete_all)
        
        self.ui.pushButtonImageZoomIn.clicked.connect(self.zoom_in)
        self.ui.pushButtonImageZoomOut.clicked.connect(self.zoom_out)

        
    def open_about(self):
        self.about = QDialog()
        self.about_ui = Ui_AboutDialog()
        self.about_ui.setupUi(self.about)
        self.about.exec() 
        
    def close_app(self):
        sys.exit(self.app.exec())
    
    # Image Loader    
    def open_images(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select image files",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.tiff *.tif)"
        )

        if files:
            self.send_to_image_list(files)

    def send_to_image_list(self, file_list):
        #self.model.clear()
        self.image_paths += file_list
        
        for f in file_list:
            item = QStandardItem(os.path.basename(f))
            item.setEditable(False)
            self.model.appendRow(item)
            
        self.set_controls_enabled(len(self.image_paths) > 0)
    
    def delete_selected_image(self):
        selected_index = self.ui.imageListViewer.currentIndex()
        if not selected_index.isValid():
            return
        
        del self.image_paths[selected_index.row()]
        self.model.removeRow(selected_index.row())
        
        self.scene.clear()
        self.set_controls_enabled(len(self.image_paths) > 0)
    
    def delete_all(self):
        self.image_paths = []
        self.model.clear()
        self.scene.clear()
        self.set_controls_enabled(False)
    
    # Graphics View 
    def show_selected_image(self, index):
        file_path = self.image_paths[index.row()]
        pixmap = QPixmap(file_path)
        
        self.scene.clear()

        item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(item)

        self.ui.graphicsView.fitInView(QRectF(pixmap.rect()), Qt.KeepAspectRatio)
        
    def zoom_in(self):
        zoomFactor = 1 + zoomStep
        self.ui.graphicsView.scale(zoomFactor, zoomFactor)
    
    def zoom_out(self):
        zoomFactor = 1 - zoomStep
        self.ui.graphicsView.scale(zoomFactor, zoomFactor)
        
    def set_controls_enabled(self, enabled):
        self.ui.pushButtonDeleteImage.setEnabled(enabled)
        self.ui.pushButtonDeleteAll.setEnabled(enabled)
        self.ui.pushButtonImageZoomIn.setEnabled(enabled)
        self.ui.pushButtonImageZoomOut.setEnabled(enabled)
        
        self.ui.comboMethods.setEnabled(enabled)
        self.ui.ScaleFactorBox.setEnabled(enabled)
        self.ui.customWidthBox.setEnabled(enabled)
        self.ui.customHeightBox.setEnabled(enabled)
        self.ui.resizeButton.setEnabled(enabled)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
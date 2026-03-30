from PySide6.QtGui import (QStandardItemModel, QStandardItem, QPixmap)
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QDialog, QPushButton, QFileDialog, QGraphicsScene, QGraphicsPixmapItem, QVBoxLayout)
from PySide6.QtCore import Qt, QRectF

from frontend.ui_import import *
from frontend.requestManager import RequestManager
import backend.mock_backend as mock_backend

import sys
import os

zoomStep = 0.1
zoomFactor = 1.0
listMaxSize = 100

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.request_manager = RequestManager(mock_backend)
        
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
        self.ui.SRBox.stateChanged.connect(self.set_controls_for_sr)
        self.ui.resizeButton.clicked.connect(self.process_images)

    # Misc ---------------------------------------------    
    def open_about(self):
        self.about = QDialog()
        self.about_ui = Ui_AboutDialog()
        self.about_ui.setupUi(self.about)
        self.about.exec() 
        
    def close_app(self):
        sys.exit(app.exec())
    
    # Image Loader -------------------------------------    
    def open_images(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select image files",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.tiff *.tif)"
        )
        if files:
            self.upload_images(files)

    def upload_images(self, file_list):
        self.model.clear()
        self.image_paths = file_list
        i = 0
        for f in file_list:
            if i >= listMaxSize: break
            item = QStandardItem(os.path.basename(f))
            item.setEditable(False)
            self.model.appendRow(item)
            i+=1
            
        self.set_controls_enabled(len(self.image_paths) > 0)
    
    def delete_selected_image(self):
        selected_index = self.ui.imageListViewer.currentIndex()
        if not selected_index.isValid():
            return
        
        del self.image_paths[selected_index.row()]
        self.model.removeRow(selected_index.row())
        
        self.scene.clear()
        self.set_controls_enabled(len(self.image_paths) > 0)
        self.ui.SRBox.setChecked(False)
        self.ui.infoImageSize.setText("Size:")
        self.ui.infoImageFormat.setText("Format:")
    
    def delete_all(self):
        self.image_paths = []
        self.model.clear()
        self.scene.clear()
        self.set_controls_enabled(False)
        self.ui.SRBox.setChecked(False)
        self.ui.infoImageSize.setText("Size:")
        self.ui.infoImageFormat.setText("Format:")
    
    # Graphics View -------------------------------------
    def show_selected_image(self, index):
        file_path = self.image_paths[index.row()]
        fileFormat = os.path.splitext(file_path)[1].upper()
        pixmap = QPixmap(file_path)
        
        self.scene.clear()
        self.scene.addPixmap(pixmap)

        item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(item)
        
        self.scene.addPixmap(pixmap)
        self.ui.graphicsView.setScene(self.scene)
        
        self.scene.setSceneRect(pixmap.rect())
        self.ui.graphicsView.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
        
        self.ui.graphicsView.centerOn(item)
        
        self.ui.infoImageSize.setText("Size: " + str(pixmap.width()) + " x " + str(pixmap.height()))
        self.ui.infoImageFormat.setText("Format: " + fileFormat)
        
        
    def zoom_in(self):
        zoomFactor = 1 + zoomStep
        self.ui.graphicsView.scale(zoomFactor, zoomFactor)
    
    def zoom_out(self):
        zoomFactor = 1 - zoomStep
        self.ui.graphicsView.scale(zoomFactor, zoomFactor)
    
    # UX --------------------------------------------------------
    def set_controls_enabled(self, enabled):
        self.ui.pushButtonDeleteImage.setEnabled(enabled)
        self.ui.pushButtonDeleteAll.setEnabled(enabled)
        self.ui.pushButtonImageZoomIn.setEnabled(enabled)
        self.ui.pushButtonImageZoomOut.setEnabled(enabled)
        
        self.ui.AIScaleFactorBox.setEnabled(enabled)
        self.ui.comboMethods.setEnabled(enabled)
        self.ui.ScaleFactorBox.setEnabled(enabled)
        self.ui.ScaleFactorBox_2.setEnabled(enabled)
        self.ui.ScaleFactorBox_3.setEnabled(enabled)
        
        self.ui.customWidthBox.setEnabled(enabled)
        self.ui.customHeightBox.setEnabled(enabled)
        self.ui.resizeButton.setEnabled(enabled)
        self.ui.SRBox.setEnabled(enabled)
        
        self.ui.radioScaleFactor.setEnabled(enabled)
        self.ui.radioScaleFactor_2.setEnabled(enabled)
        self.ui.radioCustomResolution.setEnabled(enabled)
        
    
    def set_controls_for_sr(self, enabled):
        self.ui.comboMethods.setEnabled(not enabled)
        self.ui.radioScaleFactor.setEnabled(not enabled)
        self.ui.radioScaleFactor_2.setEnabled(not enabled)
        self.ui.radioCustomResolution.setEnabled(not enabled)
        self.ui.customWidthBox.setEnabled(not enabled)
        self.ui.customHeightBox.setEnabled(not enabled)
        self.ui.ScaleFactorBox.setEnabled(not enabled)
        self.ui.ScaleFactorBox_2.setEnabled(not enabled)
        self.ui.ScaleFactorBox_3.setEnabled(not enabled)
    
    # Backend Communication -------------------------------------
    def process_images(self):
        params = {}

        # Choose ONE mode
        if self.ui.radioScaleFactor.isChecked() & self.ui.radioScaleFactor.isEnabled():
            params["mode"] = "scale"
            params["scale"] = round(self.ui.ScaleFactorBox.value(), 2)

        elif self.ui.radioScaleFactor_2.isChecked() & self.ui.radioScaleFactor_2.isEnabled():
            params["mode"] = "reconstruct"
            params["reconstruct"] = {
                "first": round(self.ui.ScaleFactorBox_2.value(), 2),
                "second": round(self.ui.ScaleFactorBox_3.value(), 2)
            }

        elif self.ui.radioCustomResolution.isChecked() & self.ui.radioCustomResolution.isEnabled():
            params["mode"] = "custom"
            params["custom"] = {
                "width": self.ui.customWidthBox.value(),
                "height": self.ui.customHeightBox.value()
            }

        elif self.ui.SRBox.isChecked():
            params["mode"] = "super_resolution"
            params["scale"] = self.ui.AIScaleFactorBox.value()
            
        else:
            self.call_error("Please select a processing mode!")
            return

        # Operation selection
        operation = self.get_selected_operation()

        response = self.request_manager.process(
            image_paths=self.image_paths,
            operation=operation,
            params=params
        )

        if response.success:
            #self.put_statistics()
            self.call_info("Images processed successfully!")
        else:
            self.call_error("Error processing images: " + response.message)

    def get_selected_operation(self):
        mapping = {
            "Nearest Neighbor": "NN",
            "Bilinear": "Bilin",
            "Bicubic": "Bicub",
            "Spline": "Spline"
        }

        selected = self.ui.comboMethods.currentText()
        return mapping[selected]

    def put_statistics(self):
        # Placeholder for statistics display
        self.ui.numResizedImages.setText("Resized Images: " + str(len(self.image_paths)))
        self.ui.chosenMethod.setText("Method: " + self.ui.comboMethods.currentText())
    
    def call_info(self, message):
        info_dialog = QDialog(self)
        info_dialog.setWindowTitle("Info")
        info_dialog.setModal(True)
        
        layout = QVBoxLayout()
        label = QLabel(message)
        layout.addWidget(label)
        
        button = QPushButton("OK")
        button.clicked.connect(info_dialog.accept)
        layout.addWidget(button)
        
        info_dialog.setLayout(layout)
        info_dialog.exec()
    
    def call_error(self, message):
        error_dialog = QDialog(self)
        error_dialog.setWindowTitle("Error")
        error_dialog.setModal(True)
        
        layout = QVBoxLayout()
        label = QLabel(message)
        layout.addWidget(label)
        
        button = QPushButton("OK")
        button.clicked.connect(error_dialog.accept)
        layout.addWidget(button)
        
        error_dialog.setLayout(layout)
        error_dialog.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
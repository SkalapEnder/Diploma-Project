from PySide6.QtGui import (QStandardItemModel, QStandardItem, QPixmap)
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QDialog, QPushButton, QFileDialog, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, QVBoxLayout)
from PySide6.QtCore import Qt, QRectF, QItemSelectionModel

from frontend.ui_import import *
from frontend.requestManager import RequestManager
from frontend.resultsManager import ResultManager

import sys
import os

zoomStepBack = 0.9
zoomStepForward = 1.1
listMaxSize = 100
SRInterCode = 10

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.request_manager = RequestManager()
        self.results_manager = ResultManager()
        
        self.set_controls_enabled(False)
        
        self.model_input = QStandardItemModel()
        self.ui.imageListViewer.setModel(self.model_input)
        self.model_output = QStandardItemModel()
        self.ui.imageListViewer_2.setModel(self.model_output)
        self.ui.imageListViewer.selectionModel().selectionChanged.connect(self.sync_selection)
        self.ui.imageListViewer_2.selectionModel().selectionChanged.connect(self.sync_selection)
        
        self.scene_input = QGraphicsScene()
        self.scene_output = QGraphicsScene()

        self.ui.graphicsView.setScene(self.scene_input)
        self.ui.graphicsView_2.setScene(self.scene_output)

        self.image_paths = []
        self.processed_paths = []
        self.zoom_level = 1.0
        
        self.ui.actionAbout.triggered.connect(self.open_about)
        self.ui.actionExit.triggered.connect(self.close_app)
        self.ui.actionLoadImages.triggered.connect(self.open_images)
        
        self.ui.clearButton.clicked.connect(self.clear_all)
        self.ui.imageListViewer.clicked.connect(self.show_selected_input_image)
        self.ui.imageListViewer_2.clicked.connect(self.show_selected_output_image)
        self.ui.pushButtonLoadImages.clicked.connect(self.open_images)
        self.ui.pushButtonDeleteImage.clicked.connect(self.delete_selected_image)
        self.ui.pushButtonDeleteAll.clicked.connect(self.delete_all)
        
        self.ui.pushButtonImageZoomIn.clicked.connect(self.zoom_in)
        self.ui.pushButtonImageZoomOut.clicked.connect(self.zoom_out)
        self.ui.SRBox.stateChanged.connect(self.set_controls_for_sr)
        self.ui.resizeButton.clicked.connect(self.process_images)
        
        self.ui.graphicsView.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.ui.graphicsView_2.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        
        self.ui.graphicsView.horizontalScrollBar().valueChanged.connect(
            lambda v: self.sync_scroll(v, "horizontal", source=self.ui.graphicsView, target=self.ui.graphicsView_2))
        self.ui.graphicsView_2.horizontalScrollBar().valueChanged.connect(
            lambda v: self.sync_scroll(v, "horizontal", source=self.ui.graphicsView_2, target=self.ui.graphicsView))

        # Sync Vertical
        self.ui.graphicsView.verticalScrollBar().valueChanged.connect(
            lambda v: self.sync_scroll(v, "vertical", source=self.ui.graphicsView, target=self.ui.graphicsView_2))
        self.ui.graphicsView_2.verticalScrollBar().valueChanged.connect(
            lambda v: self.sync_scroll(v, "vertical", source=self.ui.graphicsView_2, target=self.ui.graphicsView))

    # Base ---------------------------------------------    
    def open_about(self):
        self.about = QDialog()
        self.about_ui = Ui_About()
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
            self.upload_input_images(files[:listMaxSize])

    def upload_input_images(self, file_list,):
        self.model_input.clear()
        self.model_output.clear()
        self.image_paths = file_list
        self.processed_paths = []
        i = 0
        for f in file_list:
            if i >= listMaxSize: break
            item = QStandardItem(os.path.basename(f))
            item.setEditable(False)
            self.model_input.appendRow(item)
            i+=1
            
        self.set_controls_enabled(len(self.image_paths) > 0)
    
    def upload_processed_images(self, processed_list):
        self.model_output.clear()
        self.processed_paths = processed_list
        i = 0
        for f in processed_list:
            if i >= listMaxSize:
                break

            item = QStandardItem(os.path.basename(f))
            item.setEditable(False)

            self.model_output.appendRow(item)
            i += 1
    
    def delete_selected_image(self):
        selected_index = self.ui.imageListViewer.currentIndex()
        if not selected_index.isValid():
            return
        
        row = selected_index.row()

        if row < len(self.image_paths):
            del self.image_paths[row]
        self.model_input.removeRow(row)

        if row < len(self.processed_paths):
            del self.processed_paths[row]
        
        if row < self.model_output.rowCount():
            self.model_output.removeRow(row)

        # 4. Clear both Graphics Scenes
        self.scene_input.clear()
        self.scene_output.clear()
        self.set_controls_enabled(len(self.image_paths) > 0)
        self.ui.SRBox.setChecked(False)
        self.ui.infoImageSize.setText("Size (Input):")
        self.ui.infoImageSize_2.setText("Size (Output):")
        
        has_images = len(self.image_paths) > 0
        self.set_controls_enabled(has_images)
    
    def delete_all(self):
        self.image_paths = []
        self.model_input.clear()
        self.model_output.clear()
        self.scene_input.clear()
        self.scene_output.clear()
        self.set_controls_enabled(False)
        self.ui.SRBox.setChecked(False)
        self.ui.infoImageSize.setText("Size (Input):")
        self.ui.infoImageSize_2.setText("Size (Output):")
    
    # Graphics View -------------------------------------
    def show_selected_input_image(self, index):
        self._show_image(self.image_paths, self.ui.graphicsView, self.scene_input, index, self.ui.infoImageSize, True)

    def show_selected_output_image(self, index):
        self._show_image(self.processed_paths, self.ui.graphicsView_2, self.scene_output, index, self.ui.infoImageSize_2, False)

    def _show_image(self, paths, graphics_view, scene, index, size_label, isInput):
        self.zoom_level = 1.0
        
        if len(paths) <= 0:
            return
        file_path = paths[index.row()]
        file_format = os.path.splitext(file_path)[1].upper()
        pixmap = QPixmap(file_path)
        
        scene.clear() 
        item = QGraphicsPixmapItem(pixmap)
        scene.addItem(item)
        scene.setSceneRect(QRectF(pixmap.rect()))
        
        graphics_view.fitInView(scene.sceneRect(), Qt.KeepAspectRatio)

        size_label.setText(f"Size ({"Input" if isInput else "Output"}): {pixmap.width()} x {pixmap.height()}")
    
    def zoom_in(self):
        self.sync_zoom(zoomStepForward)

    def zoom_out(self):
        self.sync_zoom(zoomStepBack)
    
    # UX --------------------------------------------------------
    def set_controls_enabled(self, enabled):
        self.ui.pushButtonDeleteImage.setEnabled(enabled)
        self.ui.pushButtonDeleteAll.setEnabled(enabled)
        self.ui.pushButtonImageZoomIn.setEnabled(enabled)
        self.ui.pushButtonImageZoomOut.setEnabled(enabled)
        
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
        self.ui.CSVBox.setEnabled(enabled)
        self.ui.outputFormatBox.setEnabled(enabled)
        self.ui.clearButton.setEnabled(enabled)
        
    def set_controls_for_sr(self, enabled):
        self.ui.comboMethods.setEnabled(not enabled)
        self.ui.radioCustomResolution.setEnabled(not enabled)
        self.ui.radioScaleFactor.setChecked(True)
        self.ui.radioCustomResolution.setChecked(False)
        self.ui.customWidthBox.setEnabled(not enabled)
        self.ui.customHeightBox.setEnabled(not enabled)
        self.ui.ScaleFactorBox.setEnabled(not enabled)
        self.ui.ScaleFactorBox_2.setEnabled(not enabled)
        self.ui.ScaleFactorBox_3.setEnabled(not enabled)
        self.ui.SRBox_Model.setEnabled(enabled)
        self.ui.AIScaleFactorBox.setEnabled(enabled)
    
    def sync_selection(self, selected, deselected):
        if not selected.indexes():
            return
        index = selected.indexes()[0]
        
        self.ui.imageListViewer_2.selectionModel().select(
            self.model_output.index(index.row(), 0), 
            QItemSelectionModel.ClearAndSelect
        )
        
        self._show_image(self.image_paths, self.ui.graphicsView, self.scene_input, index, self.ui.infoImageSize, True)
        
        if index.row() < len(self.processed_paths):
            self._show_image(self.processed_paths, self.ui.graphicsView_2, self.scene_output, index, self.ui.infoImageSize_2, False)
    
    def sync_scroll(self, value, orientation, source, target):
        if target.signalsBlocked():
            return
            
        source_bar = source.horizontalScrollBar() if orientation == "horizontal" else source.verticalScrollBar()
        target_bar = target.horizontalScrollBar() if orientation == "horizontal" else target.verticalScrollBar()
        
        if source_bar.maximum() > 0:
            percentage = value / source_bar.maximum()
            
            target.blockSignals(True)
            target_bar.setValue(int(percentage * target_bar.maximum()))
            target.blockSignals(False)
    
    def sync_zoom(self, factor):
        self.zoom_level *= factor
    
        self.zoom_level = max(0.1, min(self.zoom_level, 10.0))
        
        for view, scene in [(self.ui.graphicsView, self.scene_input), 
                            (self.ui.graphicsView_2, self.scene_output)]:
            
            view.resetTransform()
            view.fitInView(scene.sceneRect(), Qt.KeepAspectRatio)
            
            view.scale(self.zoom_level, self.zoom_level)

    def clear_all(self):
        self.image_paths = []
        self.processed_paths = []
        self.model_input.clear()
        self.model_output.clear()
        self.scene_input.clear()
        self.scene_output.clear()
        self.set_controls_enabled(False)
        self.ui.SRBox.setChecked(False)
        self.ui.infoImageSize.setText("Size (Input):")
        self.ui.infoImageSize_2.setText("Size (Output):")
        self.clear_statistics()
        
    # Backend Communication -------------------------------------
    def process_images(self):
        params = {}

        # Choose ONE mode
        if self.ui.radioScaleFactor.isChecked() & self.ui.radioScaleFactor.isEnabled():
            params["mode"] = "one_way"
            params["scale"] = round(self.ui.ScaleFactorBox.value(), 2) if not self.ui.SRBox.isChecked() else self.ui.AIScaleFactorBox.value()
            params["ai"] = False if not self.ui.SRBox.isChecked() else True

        elif self.ui.radioScaleFactor_2.isChecked() & self.ui.radioScaleFactor_2.isEnabled():
            params["mode"] = "reconstruct"
            params["reconstruct"] = {
                "first": round(self.ui.ScaleFactorBox_2.value(), 2) if not self.ui.SRBox.isChecked() else round(1 / self.ui.AIScaleFactorBox.value(), 2),
                "second": round(self.ui.ScaleFactorBox_3.value(), 2) if not self.ui.SRBox.isChecked() else self.ui.AIScaleFactorBox.value()
            }
            params["ai"] = False if not self.ui.SRBox.isChecked() else True

        elif self.ui.radioCustomResolution.isChecked() & self.ui.radioCustomResolution.isEnabled():
            params["mode"] = "custom"
            params["custom"] = {
                "width": self.ui.customWidthBox.value(),
                "height": self.ui.customHeightBox.value()
            }
            params["ai"] = False
            
        else:
            self.call_error("Please select a processing mode!")
            return

        
        if self.ui.SRBox.isChecked():
            model = self.ui.SRBox_Model.currentText()
            scale = self.ui.AIScaleFactorBox.value()
            
            if(not self.check_model(model, scale)):
                self.call_error("Model file not found for selected configuration!" +
                               "Please, make sure the model file exists in the 'models' folder.")
                return
            if model == "EDSR" and len(image_path) > 10:
                self.call_info("Warning! Upscale more than 10 images may cause long frezees (longer than 12-15 minutes) or even system crash! Be careful using this model!")
            params["model_name"] = self.ui.SRBox_Model.currentText().lower()

        params["interpolation"] = self.get_selected_interpolation() if not self.ui.SRBox.isChecked() else SRInterCode
        
        params["output_format"] = self.ui.outputFormatBox.currentText().lower()
        
        response = self.request_manager.process(
            image_paths = self.image_paths,
            params = params
        )

        if response.success:
            self.put_statistics(response.results)
            if self.ui.CSVBox.isChecked():
                self.results_manager.export_csv(response.results, response.id)

            self.processed_paths = [r["output_path"] for r in response.results] 
            self.upload_processed_images(self.processed_paths)
            
            self.call_info("Images processed successfully! Time taken: " + str(round(response.time_ms / 1000, 3)) + " seconds")
            
        else:
            self.call_error("Error processing images: " + response.message)

    def put_statistics(self, results):
        aggregates = self.results_manager.aggregate_results(results)
        
        self.ui.infoProcessTimeMin.setText(str(round(aggregates["time_min"] / 1000, 3)))
        self.ui.infoProcessTimeAvg.setText(str(round(aggregates["time_avg"] / 1000, 3)))
        self.ui.infoProcessTimeMax.setText(str(round(aggregates["time_max"] / 1000, 3)))
        
        self.ui.infoThroughputMin.setText(str(round(aggregates["throughput_min"] / 1000000, 3)))
        self.ui.infoThroughputAvg.setText(str(round(aggregates["throughput_avg"] / 1000000, 3)))
        self.ui.infoThroughputMax.setText(str(round(aggregates["throughput_max"] / 1000000, 3)))
        
        self.ui.infoMSEMin.setText(str(round(aggregates["mse_min"], 3)))
        self.ui.infoMSEAvg.setText(str(round(aggregates["mse_avg"], 3)))
        self.ui.infoMSEMax.setText(str(round(aggregates["mse_max"], 3)))
        
        self.ui.infoPSNRMin.setText(str(round(aggregates["psnr_min"], 3)))
        self.ui.infoPSNRAvg.setText(str(round(aggregates["psnr_avg"], 3)))
        self.ui.infoPSNRMax.setText(str(round(aggregates["psnr_max"], 3)))
        
        self.ui.infoSSIMMin.setText(str(round(aggregates["ssim_min"], 3)))
        self.ui.infoSSIMAvg.setText(str(round(aggregates["ssim_avg"], 3)))
        self.ui.infoSSIMMax.setText(str(round(aggregates["ssim_max"], 3)))

    def check_model(self, model_name, model_scale):
        filename = f"{model_name}_x{int(model_scale)}.pb"

        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(current_dir, ".."))
        
        model_path = os.path.join(project_root, "models", filename)
        
        print(f"DEBUG: Checking for: {model_path}")
        return os.path.isfile(model_path)

    # Misc --------------------------
    def get_selected_interpolation(self):
        mapping = {
            "Nearest Neighbor": 0,
            "Bilinear": 1,
            "Bicubic": 2,
            "Lanczos": 4,
        }

        selected = self.ui.comboMethods.currentText()
        return mapping[selected]
    
    def clear_statistics(self):
        self.ui.infoProcessTimeMin.setText("-")
        self.ui.infoProcessTimeAvg.setText("-")
        self.ui.infoProcessTimeMax.setText("-")
        
        self.ui.infoThroughputAvg.setText("-")
        self.ui.infoThroughputMin.setText("-")
        self.ui.infoThroughputMax.setText("-")
        
        self.ui.infoMSEMin.setText("-")
        self.ui.infoMSEAvg.setText("-")
        self.ui.infoMSEMax.setText("-")
        
        self.ui.infoPSNRMin.setText("-")
        self.ui.infoPSNRAvg.setText("-")
        self.ui.infoPSNRMax.setText("-")
        
        self.ui.infoSSIMMin.setText("-")
        self.ui.infoSSIMAvg.setText("-")
        self.ui.infoSSIMMax.setText("-")

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
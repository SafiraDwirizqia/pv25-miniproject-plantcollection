import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt
from UI_plantCollection import Ui_MainWindow


class PlantCollectionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.plants = []
        self.status = self.statusBar()

        self.setup_components()
        self.connect_signals()
        self.apply_styles()
        self.update_status()

    def setup_components(self):
        self.ui.type_combo.addItems(["", "Hias", "Obat", "Sayur", "Buah", "Lainnya"])
        self.ui.health_combo.addItems(["", "Sehat", "Sakit", "Layak Tanam"])

        self.ui.table.setColumnCount(5)
        self.ui.table.setHorizontalHeaderLabels(
            ["Nama", "Jenis", "Perawatan", "Usia (bulan)", "Kesehatan"]
        )
        self.ui.table.setEditTriggers(self.ui.table.NoEditTriggers)
        self.ui.table.setGeometry(370, 30, 1100, 880)
        self.ui.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.ui.add_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.ui.reset_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.ui.delete_btn.setCursor(QCursor(Qt.PointingHandCursor))

    def connect_signals(self):
        self.ui.add_btn.clicked.connect(self.add_plant)
        self.ui.reset_btn.clicked.connect(self.reset_form)
        self.ui.delete_btn.clicked.connect(self.delete_selected)

    def apply_styles(self):
        self.setStyleSheet("""
            QLabel {
                font-size: 22px;
            }
            QLineEdit, QComboBox, QSpinBox {
                font-size: 22px;
                padding: 5px;
            }
            QPushButton {
                font-size: 22px;
                padding: 8px;
                border-radius: 5px;
            }
            QPushButton#add_btn {
                background-color: #4CAF50;
                color: white;
            }
            QPushButton#add_btn:hover {
                background-color: #45a049;
            }
            QPushButton#reset_btn {
                background-color: #FFA500;
                color: white;
            }
            QPushButton#reset_btn:hover {
                background-color: #e69500;
            }
            QPushButton#delete_btn {
                background-color: #f44336;
                color: white;
            }
            QPushButton#delete_btn:hover {
                background-color: #d32f2f;
            }
            QRadioButton {
                font-size: 22px;
            }
            QTableWidget {
                background-color: #f9f9f9;
                font-size: 22px;
            }
        """)

    def add_plant(self):
        name = self.ui.name_input.text()
        plant_type = self.ui.type_combo.currentText()
        age = self.ui.age_spin.value()
        health = self.ui.health_combo.currentText()

        if self.ui.easy.isChecked():
            care_level = "Mudah"
        elif self.ui.medium.isChecked():
            care_level = "Sedang"
        elif self.ui.hard.isChecked():
            care_level = "Sulit"
        else:
            care_level = ""

        if not name or not care_level:
            QMessageBox.warning(self, "Input Error", "Harap lengkapi semua data.")
            return

        plant = {
            "name": name,
            "type": plant_type,
            "care": care_level,
            "age": age,
            "health": health
        }
        self.plants.append(plant)

        row_position = self.ui.table.rowCount()
        self.ui.table.insertRow(row_position)
        self.ui.table.setItem(row_position, 0, QTableWidgetItem(name))
        self.ui.table.setItem(row_position, 1, QTableWidgetItem(plant_type))
        self.ui.table.setItem(row_position, 2, QTableWidgetItem(care_level))
        self.ui.table.setItem(row_position, 3, QTableWidgetItem(str(age)))
        self.ui.table.setItem(row_position, 4, QTableWidgetItem(health))

        self.update_status()
        self.reset_form()

    def reset_form(self):
        self.ui.name_input.clear()
        self.ui.type_combo.setCurrentIndex(0)

        self.ui.easy.setAutoExclusive(False)
        self.ui.medium.setAutoExclusive(False)
        self.ui.hard.setAutoExclusive(False)
        self.ui.easy.setChecked(False)
        self.ui.medium.setChecked(False)
        self.ui.hard.setChecked(False)
        self.ui.easy.setAutoExclusive(True)
        self.ui.medium.setAutoExclusive(True)
        self.ui.hard.setAutoExclusive(True)

        self.ui.age_spin.setValue(0)
        self.ui.health_combo.setCurrentIndex(0)

    def delete_selected(self):
        selected_row = self.ui.table.currentRow()
        if selected_row >= 0:
            self.ui.table.removeRow(selected_row)
            if selected_row < len(self.plants):
                del self.plants[selected_row]
            self.update_status()
        else:
            QMessageBox.warning(self, "Peringatan", "Pilih baris yang ingin dihapus.")

    def update_status(self):
        self.status.showMessage(f"Total tanaman: {len(self.plants)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PlantCollectionApp()
    window.show()
    sys.exit(app.exec_())
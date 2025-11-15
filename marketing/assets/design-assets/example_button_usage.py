#!/usr/bin/env python3
"""
Example: Using the button resources in a PyQt6 application.
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize

# Import the compiled resource file
import buttons_rc


class ButtonDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PhiGEN Tactical Buttons Demo")
        self.setStyleSheet("background-color: #1a1a1a;")

        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(10)

        # Button definitions: (resource_path, label, callback)
        buttons = [
            (":/buttons/retrieve_v2_ultra_smooth.png", "Retrieve Data", self.on_retrieve),
            (":/buttons/generate_v2_ultra_smooth.png", "Generate", self.on_generate),
            (":/buttons/save_v2_ultra_smooth.png", "Save", self.on_save),
            (":/buttons/copy_v2_ultra_smooth.png", "Copy", self.on_copy),
            (":/buttons/list_v2_ultra_smooth.png", "List", self.on_list),
            (":/buttons/lock_v2_ultra_smooth.png", "Lock", self.on_lock),
            (":/buttons/unlock_v2_ultra_smooth.png", "Unlock", self.on_unlock),
            (":/buttons/set_master_v2_ultra_smooth.png", "Set Master", self.on_set_master),
            (":/buttons/set_vault_v2_ultra_smooth.png", "Set Vault", self.on_set_vault),
            (":/buttons/copy_path_v2_ultra_smooth.png", "Copy Path", self.on_copy_path),
        ]

        # Create buttons
        for icon_path, label, callback in buttons:
            btn = QPushButton()
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(QSize(220, 80))
            btn.setFixedSize(220, 80)
            btn.clicked.connect(callback)
            btn.setStyleSheet("""
                QPushButton {
                    border: none;
                    background: transparent;
                }
                QPushButton:hover {
                    transform: scale(1.05);
                }
                QPushButton:pressed {
                    transform: scale(0.95);
                }
            """)
            layout.addWidget(btn)

        layout.addStretch()

    def on_retrieve(self):
        print("RETRIEVE clicked")

    def on_generate(self):
        print("GENERATE clicked")

    def on_save(self):
        print("SAVE clicked")

    def on_copy(self):
        print("COPY clicked")

    def on_list(self):
        print("LIST clicked")

    def on_lock(self):
        print("LOCK clicked")

    def on_unlock(self):
        print("UNLOCK clicked")

    def on_set_master(self):
        print("SET MASTER clicked")

    def on_set_vault(self):
        print("SET VAULT clicked")

    def on_copy_path(self):
        print("COPY PATH clicked")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ButtonDemo()
    window.show()
    sys.exit(app.exec())

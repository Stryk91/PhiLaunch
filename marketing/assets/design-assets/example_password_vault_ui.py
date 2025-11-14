#!/usr/bin/env python3
"""
Example: Password Vault UI using all tactical-style resources.
Demonstrates buttons, text inputs, list panel, and title.
"""

import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                              QHBoxLayout, QPushButton, QLabel, QLineEdit,
                              QSpinBox, QListWidget)
from PyQt6.QtGui import QPixmap, QIcon, QPalette, QColor, QFont
from PyQt6.QtCore import Qt, QSize

# Import the compiled resource file
import buttons_rc


class PasswordVaultUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PhiGEN Password Vault")
        self.setStyleSheet("background-color: #0a0a0a;")
        self.resize(900, 700)

        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title_label = QLabel()
        title_pixmap = QPixmap(":/ui/title_password_vault_ultra_smooth.png")
        title_label.setPixmap(title_pixmap)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # Text input section
        inputs_layout = QVBoxLayout()
        inputs_layout.setSpacing(15)

        # Association input (with label overlay on background image)
        assoc_container = self.create_text_input("Association", ":/ui/text_input_long_ultra_smooth.png")
        inputs_layout.addLayout(assoc_container)

        # Password input (with label overlay)
        password_container = self.create_text_input("Input Password", ":/ui/text_input_long_ultra_smooth.png", password_mode=True)
        inputs_layout.addLayout(password_container)

        # Password length input (short with arrows)
        length_container = self.create_length_input()
        inputs_layout.addLayout(length_container)

        main_layout.addLayout(inputs_layout)

        # Password list panel
        list_container = QWidget()
        list_layout = QVBoxLayout(list_container)
        list_layout.setContentsMargins(0, 0, 0, 0)

        # Background image for list
        list_bg = QLabel()
        list_bg_pixmap = QPixmap(":/ui/list_panel_ultra_smooth.png")
        list_bg.setPixmap(list_bg_pixmap)
        list_bg.setFixedSize(600, 400)

        # Overlay actual list widget on the background
        self.password_list = QListWidget(list_bg)
        self.password_list.setGeometry(20, 20, 560, 360)  # Inset from background edges
        self.password_list.setStyleSheet("""
            QListWidget {
                background: transparent;
                border: none;
                color: #39ff14;
                font-family: 'Xolonium', 'Courier New', monospace;
                font-size: 12px;
                selection-background-color: rgba(57, 255, 20, 0.3);
            }
            QListWidget::item {
                padding: 5px;
            }
        """)

        # Sample data
        self.password_list.addItems([
            "gmail.com - admin@example.com",
            "github.com - developer123",
            "bank.com - user_account",
            "social.media - username",
        ])

        list_layout.addWidget(list_bg, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(list_container)

        # Button section
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)

        # Create buttons
        button_configs = [
            (":/buttons/generate_v2_ultra_smooth.png", "Generate", self.on_generate),
            (":/buttons/save_v2_ultra_smooth.png", "Save", self.on_save),
            (":/buttons/retrieve_v2_ultra_smooth.png", "Retrieve", self.on_retrieve),
            (":/buttons/lock_v2_ultra_smooth.png", "Lock", self.on_lock),
            (":/buttons/unlock_v2_ultra_smooth.png", "Unlock", self.on_unlock),
        ]

        for icon_path, label, callback in button_configs:
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
            buttons_layout.addWidget(btn)

        main_layout.addLayout(buttons_layout)
        main_layout.addStretch()

    def create_text_input(self, placeholder, bg_image_path, password_mode=False):
        """Create a text input with background image and overlay QLineEdit."""
        container = QHBoxLayout()

        # Background image
        bg_label = QLabel()
        bg_pixmap = QPixmap(bg_image_path)
        bg_label.setPixmap(bg_pixmap)
        bg_label.setFixedSize(500, 50)

        # Overlay text input
        text_input = QLineEdit(bg_label)
        text_input.setGeometry(40, 10, 420, 30)
        text_input.setPlaceholderText(placeholder)

        if password_mode:
            text_input.setEchoMode(QLineEdit.EchoMode.Password)

        text_input.setStyleSheet("""
            QLineEdit {
                background: transparent;
                border: none;
                color: #39ff14;
                font-family: 'Xolonium', 'Courier New', monospace;
                font-size: 14px;
                padding: 0px;
            }
            QLineEdit::placeholder {
                color: rgba(57, 255, 20, 0.3);
            }
        """)

        container.addWidget(bg_label)
        container.addStretch()

        return container

    def create_length_input(self):
        """Create password length input with arrows."""
        container = QHBoxLayout()

        # Label
        label = QLabel("Password Length:")
        label.setStyleSheet("color: #6fff4a; font-size: 14px; font-family: 'Xolonium';")
        container.addWidget(label)

        # Background with spinbox overlay
        bg_label = QLabel()
        bg_pixmap = QPixmap(":/ui/text_input_short_arrows_ultra_smooth.png")
        bg_label.setPixmap(bg_pixmap)
        bg_label.setFixedSize(200, 50)

        # Overlay spinbox
        spinbox = QSpinBox(bg_label)
        spinbox.setGeometry(20, 10, 120, 30)
        spinbox.setMinimum(8)
        spinbox.setMaximum(128)
        spinbox.setValue(16)
        spinbox.setStyleSheet("""
            QSpinBox {
                background: transparent;
                border: none;
                color: #39ff14;
                font-family: 'Xolonium', 'Courier New', monospace;
                font-size: 16px;
                font-weight: bold;
                padding: 0px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                background: transparent;
                border: none;
                width: 0px;
            }
        """)

        container.addWidget(bg_label)
        container.addStretch()

        return container

    def on_generate(self):
        print("GENERATE clicked - Creating new password...")

    def on_save(self):
        print("SAVE clicked - Saving password...")

    def on_retrieve(self):
        print("RETRIEVE clicked - Loading password...")

    def on_lock(self):
        print("LOCK clicked - Locking vault...")

    def on_unlock(self):
        print("UNLOCK clicked - Unlocking vault...")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Set application font
    font = QFont("Xolonium", 10)
    app.setFont(font)

    window = PasswordVaultUI()
    window.show()
    sys.exit(app.exec())

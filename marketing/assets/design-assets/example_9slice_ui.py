#!/usr/bin/env python3
"""
Example: Password Vault UI using 9-slice border-image scaling.
This demonstrates proper dynamic sizing with border-image-slice.
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                              QHBoxLayout, QPushButton, QLabel, QLineEdit,
                              QSpinBox, QTextEdit, QMessageBox, QInputDialog,
                              QListWidget, QListWidgetItem)
from PyQt6.QtGui import QPixmap, QIcon, QFont
from PyQt6.QtCore import Qt, QSize, QTimer

# Import the compiled resource file
import buttons_rc

# Add parent directory to path for backend import
sys.path.insert(0, str(Path(__file__).parent.parent))

# Backend import
from password_vault_backend import PasswordVault, PasswordGenerator


class PasswordVault9SliceUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PhiGEN Password Vault - 9-Slice Borders")
        self.setStyleSheet("background-color: #0a0a0a;")
        self.resize(900, 750)

        # Backend instance
        self.vault = PasswordVault()

        # Get the absolute path to the TEMPSVG directory
        self.assets_dir = Path(__file__).parent

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

        # Association input with 9-slice border
        assoc_label = QLabel("Association:")
        assoc_label.setStyleSheet("color: #6fff4a; font-size: 12px;")
        inputs_layout.addWidget(assoc_label)

        self.assoc_input = QLineEdit()
        self.assoc_input.setPlaceholderText("e.g., gmail.com, github.com")
        self.assoc_input.setMinimumHeight(50)
        self.assoc_input.setStyleSheet(f"""
            QLineEdit {{
                border-image: url({self.assets_dir / 'text_input_9slice_ultra_smooth.png'}) 20 20 20 20 stretch;
                padding: 10px 40px;
                background-color: rgba(10, 15, 10, 0.95);
                color: #39ff14;
                font-family: 'Xolonium', 'Courier New', monospace;
                font-size: 14px;
                selection-background-color: rgba(57, 255, 20, 0.3);
            }}
            QLineEdit::placeholder {{
                color: rgba(57, 255, 20, 0.3);
            }}
        """)
        inputs_layout.addWidget(self.assoc_input)

        # Username input with 9-slice border
        user_label = QLabel("Username:")
        user_label.setStyleSheet("color: #6fff4a; font-size: 12px;")
        inputs_layout.addWidget(user_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("e.g., user@example.com or handle")
        self.username_input.setMinimumHeight(50)
        self.username_input.setStyleSheet(f"""
            QLineEdit {{
                border-image: url({self.assets_dir / 'text_input_9slice_ultra_smooth.png'}) 20 20 20 20 stretch;
                padding: 10px 40px;
                background-color: rgba(10, 15, 10, 0.95);
                color: #39ff14;
                font-family: 'Xolonium', 'Courier New', monospace;
                font-size: 14px;
                selection-background-color: rgba(57, 255, 20, 0.3);
            }}
            QLineEdit::placeholder {{
                color: rgba(57, 255, 20, 0.3);
            }}
        """)
        inputs_layout.addWidget(self.username_input)

        # Password input with 9-slice border
        password_label = QLabel("Input Password:")
        password_label.setStyleSheet("color: #6fff4a; font-size: 12px;")
        inputs_layout.addWidget(password_label)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Generated password will appear here")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(50)
        self.password_input.setStyleSheet(f"""
            QLineEdit {{
                border-image: url({self.assets_dir / 'text_input_9slice_ultra_smooth.png'}) 20 20 20 20 stretch;
                padding: 10px 40px;
                background-color: rgba(10, 15, 10, 0.95);
                color: #39ff14;
                font-family: 'Xolonium', 'Courier New', monospace;
                font-size: 14px;
                selection-background-color: rgba(57, 255, 20, 0.3);
            }}
            QLineEdit::placeholder {{
                color: rgba(57, 255, 20, 0.3);
            }}
        """)
        inputs_layout.addWidget(self.password_input)

        # Password length input
        length_layout = QHBoxLayout()
        length_label = QLabel("Password Length:")
        length_label.setStyleSheet("color: #6fff4a; font-size: 14px;")
        length_layout.addWidget(length_label)

        self.length_spinbox = QSpinBox()
        self.length_spinbox.setMinimum(8)
        self.length_spinbox.setMaximum(128)
        self.length_spinbox.setValue(16)
        self.length_spinbox.setFixedSize(100, 40)
        self.length_spinbox.setStyleSheet("""
            QSpinBox {
                background-color: #1a1a1a;
                border: 2px solid #39ff14;
                border-radius: 5px;
                color: #39ff14;
                font-family: 'Xolonium', 'Courier New', monospace;
                font-size: 16px;
                font-weight: bold;
                padding: 5px;
            }
            QSpinBox::up-button {
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 20px;
                border-left: 1px solid #39ff14;
                background-color: #0d0d0d;
            }
            QSpinBox::up-button:hover {
                background-color: rgba(57, 255, 20, 0.2);
            }
            QSpinBox::up-arrow {
                image: none;
                border: 4px solid transparent;
                border-bottom: 6px solid #39ff14;
                margin-top: 2px;
            }
            QSpinBox::down-button {
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 20px;
                border-left: 1px solid #39ff14;
                background-color: #0d0d0d;
            }
            QSpinBox::down-button:hover {
                background-color: rgba(57, 255, 20, 0.2);
            }
            QSpinBox::down-arrow {
                image: none;
                border: 4px solid transparent;
                border-top: 6px solid #39ff14;
                margin-bottom: 2px;
            }
        """)
        length_layout.addWidget(self.length_spinbox)
        length_layout.addStretch()
        inputs_layout.addLayout(length_layout)

        main_layout.addLayout(inputs_layout)

        # Password list with 9-slice border (THIS IS THE KEY CHANGE)
        list_label = QLabel("Stored Passwords:")
        list_label.setStyleSheet("color: #6fff4a; font-size: 14px; font-weight: bold;")
        main_layout.addWidget(list_label)

        self.password_list = QTextEdit()
        self.password_list.setReadOnly(True)
        self.password_list.setMinimumSize(600, 300)
        # THIS IS WHERE 9-SLICE MAGIC HAPPENS
        self.password_list.setStyleSheet(f"""
            QTextEdit {{
                border-image: url({self.assets_dir / 'list_panel_9slice_ultra_smooth.png'}) 40 40 40 40 stretch;
                padding: 45px;
                background-color: rgba(5, 10, 6, 0.95);
                color: #39ff14;
                font-family: 'Xolonium', 'Courier New', monospace;
                font-size: 12px;
                selection-background-color: rgba(57, 255, 20, 0.3);
            }}
            QScrollBar:vertical {{
                background: #0a0a0a;
                width: 12px;
                border-left: 1px solid #39ff14;
            }}
            QScrollBar::handle:vertical {{
                background: #39ff14;
                border-radius: 2px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: #6fff4a;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)

        # Sample data
        self.password_list.setPlainText("""
gmail.com          | admin@example.com     | ****************
github.com         | developer123          | ****************
bank.com           | user_account          | ****************
social.media       | username              | ****************
work.corporate     | john.doe              | ****************
cloud.storage      | personal@email.com    | ****************
""".strip())

        main_layout.addWidget(self.password_list)

        # Button section
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)

        button_configs = [
            ("generate", ":/buttons/generate_v2_ultra_smooth.png", self.on_generate),
            ("save", ":/buttons/save_v2_ultra_smooth.png", self.on_save),
            ("retrieve", ":/buttons/retrieve_v2_ultra_smooth.png", self.on_retrieve),
            ("lock", ":/buttons/lock_v2_ultra_smooth.png", self.on_lock),
            ("unlock", ":/buttons/unlock_v2_ultra_smooth.png", self.on_unlock),
        ]
        self.buttons = {}
        for name, icon_path, callback in button_configs:
            btn = QPushButton()
            btn.setObjectName(f"btn_{name}")
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
            self.buttons[name] = btn

        main_layout.addLayout(buttons_layout)
        main_layout.addStretch()

        # After building UI: master password flow
        self.initialize_master_flow()
        # Initial list load (if unlocked)
        self.refresh_password_list()

    # ==== Backend wiring helpers ====
    def initialize_master_flow(self):
        try:
            if not self.vault.has_master_password():
                # First run: set master password
                ok = False
                while not ok:
                    pwd, accepted = QInputDialog.getText(self, "Create Master Password",
                                                        "Enter a new master password:",
                                                        QLineEdit.EchoMode.Password)
                    if not accepted:
                        QMessageBox.warning(self, "Master Password Required",
                                            "A master password is required to initialize the vault.")
                        continue
                    if len(pwd) < 6:
                        QMessageBox.warning(self, "Weak Password",
                                            "Please choose at least 6 characters.")
                        continue
                    ok = self.vault.set_master_password(pwd)
                    if not ok:
                        QMessageBox.critical(self, "Error", "Failed to set master password.")
                self.set_locked_ui(False)
            else:
                # Existing vault: prompt unlock
                self.prompt_unlock()
        except Exception as e:
            QMessageBox.critical(self, "Initialization Error", str(e))

    def prompt_unlock(self):
        while self.vault.is_locked:
            pwd, accepted = QInputDialog.getText(self, "Unlock Vault",
                                                "Enter master password:",
                                                QLineEdit.EchoMode.Password)
            if not accepted:
                # Keep UI locked and exit loop
                break
            if self.vault.unlock(pwd):
                self.set_locked_ui(False)
                self.refresh_password_list()
                return
            else:
                QMessageBox.warning(self, "Unlock Failed", "Incorrect master password.")
        self.set_locked_ui(self.vault.is_locked)

    def set_locked_ui(self, locked: bool):
        # Disable inputs and actions when locked
        for w in [self.assoc_input, self.username_input, self.password_input,
                  self.length_spinbox]:
            w.setEnabled(not locked)
        # Buttons: enable only unlock when locked
        # We find buttons by traversing children of main window
        for btn in self.findChildren(QPushButton):
            icon = btn.icon()
            # crude check via assigned slots; enable/disable accordingly
            if btn.clicked.receivers() > 0:
                # Heuristic: disable all then re-enable unlock
                btn.setEnabled(not locked)
        # Specifically ensure unlock button enabled and lock button disabled when locked
        # by checking object names if any; we didn't set names, so re-enable all and rely on actions
        if locked:
            self.password_list.setPlainText("[Vault locked] Unlock to view entries.")
        
    def refresh_password_list(self):
        if self.vault.is_locked:
            return
        try:
            entries = self.vault.get_all_passwords()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load entries: {e}")
            return
        # Render as masked list
        lines = []
        header = f"{'Association':18s} | {'Username':20s} | {'Password':16s}"
        lines.append(header)
        lines.append("-" * len(header))
        for ent in entries:
            masked = "*" * min(16, len(ent.password))
            lines.append(f"{ent.association:18s} | {ent.username:20s} | {masked}")
        self.password_list.setPlainText("\n".join(lines) if lines else "(No entries)")

    # ==== Button callbacks ====
    def on_generate(self):
        try:
            length = self.length_spinbox.value()
            password = PasswordGenerator.generate(length)
            self.password_input.setText(password)
        except Exception as e:
            QMessageBox.warning(self, "Generate Error", str(e))

    def on_save(self):
        if self.vault.is_locked:
            QMessageBox.information(self, "Locked", "Unlock the vault first.")
            self.prompt_unlock()
            return
        assoc = self.assoc_input.text().strip()
        user = self.username_input.text().strip()
        pwd = self.password_input.text()
        if not assoc or not user or not pwd:
            QMessageBox.information(self, "Missing Data", "Association, username, and password are required.")
            return
        try:
            self.vault.add_password(assoc, user, pwd)
            self.refresh_password_list()
            # Clear input fields after successful save
            self.assoc_input.clear()
            self.username_input.clear()
            self.password_input.clear()
            QMessageBox.information(self, "Saved", f"Password for {assoc} saved successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Save Error", str(e))

    def on_retrieve(self):
        # For now, refresh the list view
        self.refresh_password_list()

    def on_lock(self):
        try:
            self.vault.lock()
            self.set_locked_ui(True)
            # Keep password field obscured
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        except Exception as e:
            QMessageBox.warning(self, "Lock Error", str(e))

    def on_unlock(self):
        self.prompt_unlock()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Set application font
    font = QFont("Xolonium", 10)
    app.setFont(font)

    window = PasswordVault9SliceUI()
    window.show()

    print("=" * 70)
    print("9-SLICE BORDER DEMO")
    print("=" * 70)
    print("Try resizing the window to see the borders scale dynamically!")
    print("The corners stay crisp while edges stretch smoothly.")
    print("=" * 70)

    sys.exit(app.exec())

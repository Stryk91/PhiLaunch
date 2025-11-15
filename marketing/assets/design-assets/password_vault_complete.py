#!/usr/bin/env python3
"""
PhiGEN Password Vault - COMPLETE FUNCTIONAL VERSION
All features implemented: interactive list, copy, delete, auto-lock, strength indicator
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                              QHBoxLayout, QPushButton, QLabel, QLineEdit,
                              QSpinBox, QMessageBox, QInputDialog,
                              QListWidget, QListWidgetItem, QSizePolicy)
from PyQt6.QtGui import QPixmap, QIcon, QFont
from PyQt6.QtCore import Qt, QSize, QTimer

# Import the compiled resource file
import buttons_rc

# Add parent directory to path for backend import
sys.path.insert(0, str(Path(__file__).parent.parent))

# Backend import
from password_vault_backend import PasswordVault, PasswordGenerator


class PasswordVaultComplete(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PhiGEN Password Vault")
        self.setStyleSheet("background-color: #0a0a0a;")

        # Set initial size - smaller to fit on most screens
        self.resize(950, 700)
        self.setMinimumSize(900, 700)  # Increased min height to prevent clipping

        # Make sure window can be resized
        self.statusBar().setSizeGripEnabled(True)
        self.setMaximumSize(16777215, 16777215)  # Qt's default maximum size

        # Backend instance
        self.vault = PasswordVault()

        # Get the absolute path to the TEMPSVG directory
        self.assets_dir = Path(__file__).parent

        # Auto-lock timer (5 minutes)
        self.auto_lock_timer = QTimer()
        self.auto_lock_timer.timeout.connect(self.auto_lock)
        self.auto_lock_timer.setInterval(300000)  # 5 minutes

        # Clipboard clear timer
        self.clipboard_timer = QTimer()
        self.clipboard_timer.timeout.connect(self.clear_clipboard)

        # Store current entries for retrieval
        self.current_entries = []

        # Build UI first
        self.setup_ui()

        # Then handle master password flow
        self.initialize_master_flow()

        # Initial list load (if unlocked)
        self.refresh_password_list()

        # Start auto-lock timer if unlocked
        if not self.vault.is_locked:
            self.auto_lock_timer.start()

    def setup_ui(self):
        """Setup main UI."""
        central = QWidget()
        central.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(8)  # Reduced from 15 to prevent clipping
        main_layout.setContentsMargins(15, 8, 15, 8)  # Reduced from 20 to save space
        main_layout.setSizeConstraint(QVBoxLayout.SizeConstraint.SetDefaultConstraint)

        # Title
        title_label = QLabel()
        title_pixmap = QPixmap(":/ui/title_password_vault_ultra_smooth.png")
        title_label.setPixmap(title_pixmap)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setScaledContents(False)
        title_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        main_layout.addWidget(title_label)

        # Input section
        inputs_layout = QVBoxLayout()
        inputs_layout.setSpacing(6)  # Reduced from 10 to save vertical space

        # Association input
        assoc_label = QLabel("Association (e.g., gmail.com):")
        assoc_label.setStyleSheet("color: #6fff4a; font-size: 11px;")
        inputs_layout.addWidget(assoc_label)

        self.assoc_input = QLineEdit()
        self.assoc_input.setPlaceholderText("Website or service name")
        self.assoc_input.setMinimumHeight(50)
        self.assoc_input.setMaximumHeight(50)
        self.assoc_input.textChanged.connect(self.reset_auto_lock_timer)
        self.assoc_input.setStyleSheet(f"""
            QLineEdit {{
                border-image: url({self.assets_dir / 'text_input_9slice_ultra_smooth.png'}) 20 20 20 20 stretch;
                padding: 10px 40px;
                background-color: rgba(10, 15, 10, 0.95);
                color: #39ff14;
                font-family: 'Xolonium', 'Courier New', monospace;
                font-size: 13px;
            }}
            QLineEdit::placeholder {{ color: rgba(57, 255, 20, 0.3); }}
        """)
        inputs_layout.addWidget(self.assoc_input)

        # Username input
        user_label = QLabel("Username / Email:")
        user_label.setStyleSheet("color: #6fff4a; font-size: 11px;")
        inputs_layout.addWidget(user_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username or email address")
        self.username_input.setMinimumHeight(50)
        self.username_input.setMaximumHeight(50)
        self.username_input.textChanged.connect(self.reset_auto_lock_timer)
        self.username_input.setStyleSheet(self.assoc_input.styleSheet())
        inputs_layout.addWidget(self.username_input)

        # Password input with show/hide button
        pass_label = QLabel("Password:")
        pass_label.setStyleSheet("color: #6fff4a; font-size: 11px;")
        inputs_layout.addWidget(pass_label)

        password_row = QHBoxLayout()
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Generated password will appear here")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        self.password_input.setMinimumHeight(50)
        self.password_input.setMaximumHeight(50)
        self.password_input.textChanged.connect(self.on_password_changed)
        self.password_input.setStyleSheet(self.assoc_input.styleSheet())
        password_row.addWidget(self.password_input)

        # Show/Hide button
        self.show_hide_btn = QPushButton("👁")
        self.show_hide_btn.setFixedSize(50, 50)
        self.show_hide_btn.clicked.connect(self.toggle_password_visibility)
        self.show_hide_btn.setStyleSheet("""
            QPushButton {
                background-color: #1a1a1a;
                border: 2px solid #39ff14;
                border-radius: 5px;
                color: #39ff14;
                font-size: 18px;
            }
            QPushButton:hover { background-color: rgba(57, 255, 20, 0.2); }
        """)
        password_row.addWidget(self.show_hide_btn)
        inputs_layout.addLayout(password_row)

        # Password strength indicator
        self.strength_label = QLabel("")
        self.strength_label.setStyleSheet("color: #6fff4a; font-size: 10px; font-style: italic;")
        inputs_layout.addWidget(self.strength_label)

        # Password length
        length_layout = QHBoxLayout()
        length_label = QLabel("Password Length:")
        length_label.setStyleSheet("color: #6fff4a; font-size: 12px;")
        length_layout.addWidget(length_label)

        self.length_spinbox = QSpinBox()
        self.length_spinbox.setMinimum(8)
        self.length_spinbox.setMaximum(128)
        self.length_spinbox.setValue(16)
        self.length_spinbox.setFixedSize(100, 40)
        self.length_spinbox.valueChanged.connect(self.reset_auto_lock_timer)
        self.length_spinbox.setStyleSheet("""
            QSpinBox {
                background-color: #1a1a1a;
                border: 2px solid #39ff14;
                border-radius: 5px;
                color: #39ff14;
                font-size: 14px;
                font-weight: bold;
                padding: 5px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 18px;
                border-left: 1px solid #39ff14;
                background-color: #0d0d0d;
            }
            QSpinBox::up-arrow { border: 4px solid transparent; border-bottom: 6px solid #39ff14; }
            QSpinBox::down-arrow { border: 4px solid transparent; border-top: 6px solid #39ff14; }
        """)
        length_layout.addWidget(self.length_spinbox)
        length_layout.addStretch()
        inputs_layout.addLayout(length_layout)

        main_layout.addLayout(inputs_layout)

        # Password list (INTERACTIVE)
        list_label = QLabel("Stored Passwords (double-click to load):")
        list_label.setStyleSheet("color: #6fff4a; font-size: 13px; font-weight: bold;")
        main_layout.addWidget(list_label)

        self.password_list = QListWidget()
        self.password_list.setMinimumSize(500, 180)  # Reduced from 200 to prevent clipping
        self.password_list.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.password_list.itemDoubleClicked.connect(self.on_list_item_double_clicked)
        self.password_list.itemClicked.connect(self.reset_auto_lock_timer)
        self.password_list.setStyleSheet(f"""
            QListWidget {{
                border-image: url({self.assets_dir / 'list_panel_9slice_ultra_smooth.png'}) 40 40 40 40 stretch;
                padding: 45px;
                background-color: rgba(5, 10, 6, 0.95);
                color: #39ff14;
                font-family: 'Xolonium', 'Courier New', monospace;
                font-size: 11px;
            }}
            QListWidget::item {{
                padding: 5px;
                border-bottom: 1px solid rgba(57, 255, 20, 0.1);
            }}
            QListWidget::item:selected {{
                background-color: rgba(57, 255, 20, 0.2);
            }}
            QListWidget::item:hover {{
                background-color: rgba(57, 255, 20, 0.1);
            }}
        """)
        main_layout.addWidget(self.password_list)

        # Button section
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(8)

        button_configs = [
            ("generate", ":/buttons/generate_v2_ultra_smooth.png", self.on_generate),
            ("save", ":/buttons/save_v2_ultra_smooth.png", self.on_save),
            ("retrieve", ":/buttons/retrieve_v2_ultra_smooth.png", self.on_retrieve),
            ("copy", ":/buttons/copy_v2_ultra_smooth.png", self.on_copy_password),
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
                QPushButton { border: none; background: transparent; }
                QPushButton:pressed { transform: scale(0.95); }
            """)
            buttons_layout.addWidget(btn)
            self.buttons[name] = btn

        main_layout.addLayout(buttons_layout)

    # ==== Backend wiring helpers ====
    def initialize_master_flow(self):
        try:
            if not self.vault.has_master_password():
                # First run: set master password
                ok = False
                while not ok:
                    pwd, accepted = QInputDialog.getText(self, "Create Master Password",
                                                        "Enter a new master password (min 8 characters):",
                                                        QLineEdit.EchoMode.Password)
                    if not accepted:
                        QMessageBox.warning(self, "Master Password Required",
                                            "A master password is required to initialize the vault.")
                        continue
                    if len(pwd) < 8:
                        QMessageBox.warning(self, "Weak Password",
                                            "Please choose at least 8 characters.")
                        continue
                    ok = self.vault.set_master_password(pwd)
                    if not ok:
                        QMessageBox.critical(self, "Error", "Failed to set master password.")
                self.set_locked_ui(False)
                QMessageBox.information(self, "Success", "Vault created! Your passwords are now secure.")
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
                break
            if self.vault.unlock(pwd):
                self.set_locked_ui(False)
                self.refresh_password_list()
                self.auto_lock_timer.start()
                return
            else:
                QMessageBox.warning(self, "Unlock Failed", "Incorrect master password.")
        self.set_locked_ui(self.vault.is_locked)

    def set_locked_ui(self, locked: bool):
        """Disable/enable UI elements based on lock state."""
        for w in [self.assoc_input, self.username_input, self.password_input,
                  self.length_spinbox, self.show_hide_btn]:
            w.setEnabled(not locked)

        # Show/hide appropriate buttons based on lock state
        for name, btn in self.buttons.items():
            if locked:
                # When locked: only unlock button enabled, rest disabled
                btn.setEnabled(name == "unlock")
                btn.setVisible(name == "unlock" or name != "lock")  # Hide lock, show unlock
                if name == "unlock":
                    btn.setVisible(True)
                elif name == "lock":
                    btn.setVisible(False)
            else:
                # When unlocked: all buttons except unlock enabled
                btn.setEnabled(name != "unlock")
                btn.setVisible(name != "unlock")  # Hide unlock, show lock
                if name == "lock":
                    btn.setVisible(True)

        if locked:
            self.password_list.clear()
            item = QListWidgetItem("[Vault Locked] Click UNLOCK button to access")
            item.setFlags(Qt.ItemFlag.NoItemFlags)
            self.password_list.addItem(item)
            self.strength_label.setText("")

    def refresh_password_list(self):
        """Refresh the password list display."""
        self.password_list.clear()
        if self.vault.is_locked:
            return

        try:
            self.current_entries = self.vault.get_all_passwords()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load entries: {e}")
            return

        if not self.current_entries:
            item = QListWidgetItem("No passwords stored yet. Click GENERATE to create one!")
            item.setFlags(Qt.ItemFlag.NoItemFlags)
            self.password_list.addItem(item)
            return

        # Add entries to list
        for entry in self.current_entries:
            masked = "*" * min(16, len(entry.password))
            display_text = f"{entry.association:25s}  |  {entry.username:25s}  |  {masked}"
            item = QListWidgetItem(display_text)
            item.setData(Qt.ItemDataRole.UserRole, entry.id)
            self.password_list.addItem(item)

    # ==== Button callbacks ====
    def on_generate(self):
        """Generate new password."""
        try:
            length = self.length_spinbox.value()
            password = PasswordGenerator.generate(length)
            self.password_input.setText(password)
            self.reset_auto_lock_timer()

            score, strength = PasswordGenerator.calculate_strength(password)
            QMessageBox.information(self, "Password Generated",
                                   f"Generated {length}-character password\nStrength: {strength} ({score}/100)")
        except Exception as e:
            QMessageBox.warning(self, "Generate Error", str(e))

    def on_save(self):
        """Save current password to vault."""
        if self.vault.is_locked:
            QMessageBox.information(self, "Locked", "Unlock the vault first.")
            self.prompt_unlock()
            return

        assoc = self.assoc_input.text().strip()
        user = self.username_input.text().strip()
        pwd = self.password_input.text()

        if not assoc or not user or not pwd:
            QMessageBox.information(self, "Missing Data",
                                   "Association, username, and password are required.")
            return

        try:
            self.vault.add_password(assoc, user, pwd)
            self.refresh_password_list()
            # Clear input fields
            self.assoc_input.clear()
            self.username_input.clear()
            self.password_input.clear()
            self.strength_label.setText("")
            QMessageBox.information(self, "Saved", f"Password for {assoc} saved successfully!")
            self.reset_auto_lock_timer()
        except Exception as e:
            QMessageBox.critical(self, "Save Error", str(e))

    def on_retrieve(self):
        """Retrieve/load selected password from list."""
        current_item = self.password_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "No Selection",
                               "Please select a password from the list or double-click an entry.")
            return

        entry_id = current_item.data(Qt.ItemDataRole.UserRole)
        if entry_id is None:
            return

        try:
            entry = self.vault.get_password_by_id(entry_id)
            if entry:
                self.assoc_input.setText(entry.association)
                self.username_input.setText(entry.username)
                self.password_input.setText(entry.password)
                QMessageBox.information(self, "Retrieved",
                                       f"Loaded password for {entry.association}")
                self.reset_auto_lock_timer()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to retrieve: {str(e)}")

    def on_copy_password(self):
        """Copy password to clipboard with auto-clear."""
        password = self.password_input.text()

        if not password:
            # Try to copy from selected list item
            current_item = self.password_list.currentItem()
            if current_item:
                entry_id = current_item.data(Qt.ItemDataRole.UserRole)
                if entry_id:
                    try:
                        entry = self.vault.get_password_by_id(entry_id)
                        if entry:
                            password = entry.password
                    except:
                        pass

        if password:
            clipboard = QApplication.clipboard()
            clipboard.setText(password)
            QMessageBox.information(self, "Copied",
                                   "Password copied to clipboard!\nWill auto-clear in 30 seconds.")

            # Clear clipboard after 30 seconds
            self.clipboard_timer.start(30000)
            self.reset_auto_lock_timer()
        else:
            QMessageBox.warning(self, "No Password", "No password to copy!")

    def on_list_item_double_clicked(self, item):
        """Handle double-click on list item."""
        entry_id = item.data(Qt.ItemDataRole.UserRole)
        if entry_id is None:
            return

        # Show options dialog
        reply = QMessageBox.question(self, "Password Entry Options",
                                     "What would you like to do?",
                                     QMessageBox.StandardButton.Open |
                                     QMessageBox.StandardButton.Close |
                                     QMessageBox.StandardButton.Cancel)

        if reply == QMessageBox.StandardButton.Open:
            # Load entry
            self.on_retrieve()
        elif reply == QMessageBox.StandardButton.Close:
            # Delete entry
            self.delete_entry(entry_id)

    def delete_entry(self, entry_id):
        """Delete a password entry."""
        reply = QMessageBox.question(self, "Confirm Delete",
                                     "Are you sure you want to delete this password?\nThis cannot be undone!",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.vault.delete_password(entry_id)
                self.refresh_password_list()
                QMessageBox.information(self, "Deleted", "Password entry deleted.")
                self.reset_auto_lock_timer()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete: {str(e)}")

    def on_lock(self):
        """Lock the vault."""
        reply = QMessageBox.question(self, "Lock Vault",
                                     "Are you sure you want to lock the vault?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self.vault.lock()
            self.auto_lock_timer.stop()
            self.set_locked_ui(True)
            QMessageBox.information(self, "Locked", "Vault locked successfully!")

    def on_unlock(self):
        """Unlock the vault."""
        self.prompt_unlock()

    def auto_lock(self):
        """Auto-lock after timeout."""
        self.vault.lock()
        self.auto_lock_timer.stop()
        self.set_locked_ui(True)
        QMessageBox.warning(self, "Auto-Lock", "Vault auto-locked due to inactivity (5 minutes).")

    def reset_auto_lock_timer(self):
        """Reset the auto-lock timer on user activity."""
        if not self.vault.is_locked:
            self.auto_lock_timer.stop()
            self.auto_lock_timer.start()

    def clear_clipboard(self):
        """Clear clipboard after timeout."""
        clipboard = QApplication.clipboard()
        clipboard.clear()
        self.clipboard_timer.stop()

    def toggle_password_visibility(self):
        """Toggle password visibility."""
        if self.password_input.echoMode() == QLineEdit.EchoMode.Password:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.show_hide_btn.setText("🙈")
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.show_hide_btn.setText("👁")
        self.reset_auto_lock_timer()

    def on_password_changed(self):
        """Update password strength indicator when password changes."""
        password = self.password_input.text()
        if password:
            score, strength = PasswordGenerator.calculate_strength(password)

            # Color based on strength
            if score < 50:
                color = "#ff4444"  # Red
            elif score < 70:
                color = "#ffaa00"  # Orange
            elif score < 90:
                color = "#39ff14"  # Green
            else:
                color = "#00ffff"  # Cyan

            self.strength_label.setText(f"Strength: {strength} ({score}/100)")
            self.strength_label.setStyleSheet(f"color: {color}; font-size: 10px; font-weight: bold;")
        else:
            self.strength_label.setText("")
        self.reset_auto_lock_timer()

    def closeEvent(self, event):
        """Handle window close."""
        if not self.vault.is_locked:
            reply = QMessageBox.question(self, "Exit",
                                        "Do you want to lock the vault before exiting?",
                                        QMessageBox.StandardButton.Yes |
                                        QMessageBox.StandardButton.No |
                                        QMessageBox.StandardButton.Cancel)

            if reply == QMessageBox.StandardButton.Yes:
                self.vault.lock()
                event.accept()
            elif reply == QMessageBox.StandardButton.No:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setFont(QFont("Xolonium", 10))

    window = PasswordVaultComplete()
    window.show()

    sys.exit(app.exec())

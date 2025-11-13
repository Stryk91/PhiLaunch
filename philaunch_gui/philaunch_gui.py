#!/usr/bin/env python3
"""
PhiLaunch Control Center - Tactical Automation Dashboard
Remote execution and monitoring interface for PhiLaunch automation framework
"""

import os
import sys
import subprocess
import threading
import time
from pathlib import Path
from datetime import datetime

# DPI fix MUST come before PyQt6 imports
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "0"
os.environ["QT_SCALE_FACTOR"] = "1"
os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTreeWidget, QTreeWidgetItem, QTextEdit,
    QSplitter, QFrame, QScrollArea
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QObject
from PyQt6.QtGui import QFont

# Import color palette
try:
    from philaunch_colors import COLORS, INTERACTION_STATES, COMPONENT_COLORS
except ImportError:
    # Fallback if running from different directory
    sys.path.insert(0, str(Path(__file__).parent))
    from philaunch_colors import COLORS, INTERACTION_STATES, COMPONENT_COLORS


class PhiLaunchSignals(QObject):
    """Signal emitter for thread-safe UI updates"""
    update_output = pyqtSignal(str)
    update_tasks = pyqtSignal(list)
    update_status = pyqtSignal(str, str)  # (metric_name, value)


class PhiLaunchControlCenter(QMainWindow):
    """
    PhiLaunch Control Center - Main GUI Application
    Tactical automation dashboard with remote execution capabilities
    """

    def __init__(self):
        super().__init__()

        # Paths
        self.home_dir = Path.home()
        self.automation_dir = self.home_dir / "automation"
        self.scripts_dir = self.home_dir

        # State
        self.dragging = False
        self.drag_position = None
        self.selected_script = None
        self.selected_task = None
        self.monitoring_active = False

        # Signals for thread-safe updates
        self.signals = PhiLaunchSignals()
        self.signals.update_output.connect(self.append_output)
        self.signals.update_tasks.connect(self.refresh_task_list)
        self.signals.update_status.connect(self.update_metric)

        # Setup window
        self.setWindowTitle("PhiLaunch Control Center")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.resize(1650, 950)
        self.setMinimumSize(1400, 800)

        # Build UI
        self.setup_ui()

        # Start auto-refresh timer (every 2 seconds)
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.auto_refresh)
        self.refresh_timer.start(2000)

        # Initial load
        self.load_scripts()
        self.refresh_tasks()
        self.refresh_system_status()

    def setup_ui(self):
        """Build the complete UI hierarchy"""
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)

        # Apply base styling
        central.setStyleSheet(f"""
            QWidget {{
                background-color: {COLORS['bg_base']};
                color: {COLORS['text_primary']};
                font-family: 'Monospace';
            }}
        """)

        # Main layout
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Add components
        main_layout.addWidget(self.create_title_bar())
        main_layout.addWidget(self.create_toolbar())
        main_layout.addWidget(self.create_three_pane_layout())
        main_layout.addWidget(self.create_status_bar())

    def create_title_bar(self) -> QWidget:
        """Custom title bar with window controls"""
        title_bar = QWidget()
        title_bar.setFixedHeight(32)
        title_bar.setStyleSheet(f"""
            QWidget {{
                background-color: {COLORS['bg_panel']};
                border-bottom: 2px solid {COLORS['border_bright']};
            }}
        """)

        layout = QHBoxLayout(title_bar)
        layout.setContentsMargins(10, 0, 10, 0)

        # Title
        title_label = QLabel("⚡ PHILAUNCH CONTROL CENTER")
        title_label.setFont(QFont("Monospace", 12, QFont.Weight.Bold))
        title_label.setStyleSheet(f"color: {COLORS['primary']};")
        layout.addWidget(title_label)

        layout.addStretch()

        # Window controls
        btn_minimize = self.create_window_button("─", self.showMinimized)
        btn_maximize = self.create_window_button("□", self.toggle_maximize)
        btn_close = self.create_window_button("×", self.close)

        layout.addWidget(btn_minimize)
        layout.addWidget(btn_maximize)
        layout.addWidget(btn_close)

        return title_bar

    def create_window_button(self, text: str, callback) -> QPushButton:
        """Create window control button"""
        btn = QPushButton(text)
        btn.setFixedSize(32, 28)
        btn.setFont(QFont("Monospace", 14, QFont.Weight.Bold))
        btn.clicked.connect(callback)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLORS['text_secondary']};
                border: none;
            }}
            QPushButton:hover {{
                background-color: {COLORS['bg_card']};
                color: {COLORS['primary']};
            }}
        """)
        return btn

    def create_toolbar(self) -> QWidget:
        """System status toolbar with indicators"""
        toolbar = QWidget()
        toolbar.setFixedHeight(50)
        toolbar.setStyleSheet(f"""
            QWidget {{
                background-color: {COLORS['bg_panel']};
                border-bottom: 1px solid {COLORS['border_dim']};
            }}
        """)

        layout = QHBoxLayout(toolbar)
        layout.setContentsMargins(15, 8, 15, 8)

        # System indicators
        self.indicator_cpu = self.create_indicator("CPU", "...", COLORS['info'])
        self.indicator_ram = self.create_indicator("RAM", "...", COLORS['info'])
        self.indicator_tasks = self.create_indicator("TASKS", "0", COLORS['info'])
        self.indicator_ssh = self.create_indicator("SSH", "...", COLORS['info'])

        layout.addWidget(self.indicator_cpu)
        layout.addWidget(self.create_separator())
        layout.addWidget(self.indicator_ram)
        layout.addWidget(self.create_separator())
        layout.addWidget(self.indicator_tasks)
        layout.addWidget(self.create_separator())
        layout.addWidget(self.indicator_ssh)

        layout.addStretch()

        # Quick action buttons
        btn_refresh = self.create_action_button("🔄", "Refresh", self.refresh_all)
        btn_terminal = self.create_action_button("💻", "Terminal", self.open_terminal)
        btn_status = self.create_action_button("📊", "Status", self.run_status_check)

        layout.addWidget(btn_refresh)
        layout.addWidget(btn_terminal)
        layout.addWidget(btn_status)

        return toolbar

    def create_indicator(self, label: str, value: str, color: str) -> QWidget:
        """Create status indicator widget"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(2)

        lbl_name = QLabel(label)
        lbl_name.setFont(QFont("Monospace", 8))
        lbl_name.setStyleSheet(f"color: {COLORS['text_secondary']};")
        lbl_name.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl_value = QLabel(value)
        lbl_value.setFont(QFont("Monospace", 11, QFont.Weight.Bold))
        lbl_value.setStyleSheet(f"color: {color};")
        lbl_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_value.setObjectName(f"indicator_{label.lower()}_value")

        layout.addWidget(lbl_name)
        layout.addWidget(lbl_value)

        return widget

    def create_separator(self) -> QFrame:
        """Create vertical separator line"""
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setStyleSheet(f"""
            QFrame {{
                color: {COLORS['border_dim']};
                max-width: 1px;
            }}
        """)
        return separator

    def create_action_button(self, icon: str, text: str, callback) -> QPushButton:
        """Create toolbar action button"""
        btn = QPushButton(f"{icon} {text}")
        btn.setFont(QFont("Monospace", 10))
        btn.clicked.connect(callback)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {INTERACTION_STATES['normal_bg']};
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border_dim']};
                border-radius: 4px;
                padding: 6px 12px;
            }}
            QPushButton:hover {{
                background-color: {INTERACTION_STATES['hover_bg']};
                border: 1px solid {COLORS['border_bright']};
                color: {COLORS['primary']};
            }}
            QPushButton:pressed {{
                background-color: {INTERACTION_STATES['pressed_bg']};
            }}
        """)
        return btn

    def create_three_pane_layout(self) -> QSplitter:
        """Main three-pane layout: Scripts | Output | Actions"""
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(3)
        splitter.setStyleSheet(f"""
            QSplitter::handle {{
                background-color: {COLORS['border_dim']};
            }}
            QSplitter::handle:hover {{
                background-color: {COLORS['border_bright']};
            }}
        """)

        # Left pane: Script tree (420px)
        splitter.addWidget(self.create_left_pane())

        # Middle pane: Output viewer (840px)
        splitter.addWidget(self.create_middle_pane())

        # Right pane: Actions (420px)
        splitter.addWidget(self.create_right_pane())

        # Set initial sizes
        splitter.setSizes([420, 840, 420])

        return splitter

    def create_left_pane(self) -> QWidget:
        """Left pane: Script and task navigation tree"""
        pane = QWidget()
        pane.setStyleSheet(f"background-color: {COLORS['bg_panel']};")

        layout = QVBoxLayout(pane)
        layout.setContentsMargins(10, 10, 10, 10)

        # Header
        header = QLabel("📜 AUTOMATION & TASKS")
        header.setFont(QFont("Monospace", 11, QFont.Weight.Bold))
        header.setStyleSheet(f"color: {COLORS['primary']}; padding: 5px;")
        layout.addWidget(header)

        # Tree widget
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setFont(QFont("Monospace", 10))
        self.tree.itemClicked.connect(self.on_tree_item_clicked)
        self.tree.setStyleSheet(f"""
            QTreeWidget {{
                background-color: {COLORS['bg_card']};
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border_dim']};
                border-radius: 4px;
                padding: 5px;
            }}
            QTreeWidget::item {{
                padding: 6px;
                border-left: 3px solid transparent;
            }}
            QTreeWidget::item:hover {{
                background-color: {INTERACTION_STATES['hover_bg']};
                color: {COLORS['primary']};
            }}
            QTreeWidget::item:selected {{
                background-color: {INTERACTION_STATES['selected_bg']};
                border-left: 3px solid {COLORS['primary']};
                color: {COLORS['primary']};
                font-weight: bold;
            }}
        """)

        layout.addWidget(self.tree)

        return pane

    def create_middle_pane(self) -> QWidget:
        """Middle pane: Live output viewer"""
        pane = QWidget()
        pane.setStyleSheet(f"background-color: {COLORS['bg_panel']};")

        layout = QVBoxLayout(pane)
        layout.setContentsMargins(10, 10, 10, 10)

        # Header
        header = QLabel("📺 LIVE OUTPUT")
        header.setFont(QFont("Monospace", 11, QFont.Weight.Bold))
        header.setStyleSheet(f"color: {COLORS['primary']}; padding: 5px;")
        layout.addWidget(header)

        # Output text area
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setFont(QFont("Monospace", 9))
        self.output_text.setStyleSheet(f"""
            QTextEdit {{
                background-color: {COLORS['bg_input']};
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border_dim']};
                border-radius: 4px;
                padding: 10px;
            }}
        """)
        self.output_text.append(self.get_welcome_message())

        layout.addWidget(self.output_text)

        return pane

    def create_right_pane(self) -> QWidget:
        """Right pane: Quick actions"""
        pane = QWidget()
        pane.setStyleSheet(f"background-color: {COLORS['bg_panel']};")

        layout = QVBoxLayout(pane)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Header
        header = QLabel("⚡ QUICK ACTIONS")
        header.setFont(QFont("Monospace", 11, QFont.Weight.Bold))
        header.setStyleSheet(f"color: {COLORS['primary']}; padding: 5px;")
        layout.addWidget(header)

        # Action buttons
        actions = [
            ("▶ RUN SCRIPT", self.run_selected_script, COMPONENT_COLORS['task_running']),
            ("🔴 STOP TASK", self.stop_selected_task, COMPONENT_COLORS['task_stopped']),
            ("📋 VIEW LOGS", self.view_logs, COLORS['info']),
            ("🔄 RESTART SSH", self.restart_ssh, COLORS['warning']),
            ("📱 PHONE SHORTCUTS", self.show_phone_shortcuts, COLORS['info']),
        ]

        for text, callback, color in actions:
            btn = QPushButton(text)
            btn.setFont(QFont("Monospace", 10, QFont.Weight.Bold))
            btn.setMinimumHeight(45)
            btn.clicked.connect(callback)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['bg_card']};
                    color: {color};
                    border: 2px solid {COLORS['border_dim']};
                    border-radius: 6px;
                    padding: 10px;
                }}
                QPushButton:hover {{
                    background-color: {INTERACTION_STATES['hover_bg']};
                    border: 2px solid {COLORS['border_bright']};
                }}
                QPushButton:pressed {{
                    background-color: {INTERACTION_STATES['pressed_bg']};
                }}
            """)
            layout.addWidget(btn)

        layout.addStretch()

        return pane

    def create_status_bar(self) -> QWidget:
        """Bottom status bar"""
        status_bar = QWidget()
        status_bar.setFixedHeight(28)
        status_bar.setStyleSheet(f"""
            QWidget {{
                background-color: {COLORS['bg_panel']};
                border-top: 1px solid {COLORS['border_dim']};
            }}
        """)

        layout = QHBoxLayout(status_bar)
        layout.setContentsMargins(15, 4, 15, 4)

        self.status_label = QLabel("Ready")
        self.status_label.setFont(QFont("Monospace", 9))
        self.status_label.setStyleSheet(f"color: {COLORS['text_secondary']};")

        layout.addWidget(self.status_label)
        layout.addStretch()

        version_label = QLabel("PhiLaunch v1.0 | 192.168.50.149:2222")
        version_label.setFont(QFont("Monospace", 8))
        version_label.setStyleSheet(f"color: {COLORS['text_dim']};")
        layout.addWidget(version_label)

        return status_bar

    # === Data Loading Methods ===

    def load_scripts(self):
        """Load scripts into tree"""
        self.tree.clear()

        # Automation scripts
        automation_root = QTreeWidgetItem(self.tree, ["▼ AUTOMATION SCRIPTS"])
        automation_root.setFont(0, QFont("Monospace", 10, QFont.Weight.Bold))

        automation_scripts = [
            ("🏠", "home-control.sh"),
            ("🚀", "launch-script.sh"),
            ("⏱", "start-long-task.sh"),
        ]

        for icon, script in automation_scripts:
            item = QTreeWidgetItem(automation_root, [f"  ├─ {icon} {script}"])
            item.setData(0, Qt.ItemDataRole.UserRole, str(self.automation_dir / script))

        # Monitoring scripts
        monitor_root = QTreeWidgetItem(self.tree, ["▼ MONITORING"])
        monitor_root.setFont(0, QFont("Monospace", 10, QFont.Weight.Bold))

        monitor_scripts = [
            ("🎮", "wow_monitor.sh"),
            ("✓", "wow_quick_check.sh"),
            ("📊", "system_info_checker.sh"),
            ("📈", "status_monitor.sh"),
        ]

        for icon, script in monitor_scripts:
            script_path = self.scripts_dir / script
            if script_path.exists():
                item = QTreeWidgetItem(monitor_root, [f"  ├─ {icon} {script}"])
                item.setData(0, Qt.ItemDataRole.UserRole, str(script_path))

        # Running tasks section (will be populated by refresh)
        self.tasks_root = QTreeWidgetItem(self.tree, ["▼ RUNNING TASKS"])
        self.tasks_root.setFont(0, QFont("Monospace", 10, QFont.Weight.Bold))

        self.tree.expandAll()

    def refresh_tasks(self):
        """Refresh running tmux sessions"""
        try:
            result = subprocess.run(
                ['tmux', 'list-sessions', '-F', '#{session_name}'],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                tasks = result.stdout.strip().split('\n') if result.stdout.strip() else []
                self.signals.update_tasks.emit(tasks)
            else:
                self.signals.update_tasks.emit([])

        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.signals.update_tasks.emit([])

    def refresh_task_list(self, tasks: list):
        """Update task list in tree (thread-safe)"""
        # Clear existing tasks
        while self.tasks_root.childCount() > 0:
            self.tasks_root.removeChild(self.tasks_root.child(0))

        # Add current tasks
        for task in tasks:
            if task:
                item = QTreeWidgetItem(self.tasks_root, [f"  ├─ ▶ {task}"])
                item.setData(0, Qt.ItemDataRole.UserRole, f"task:{task}")
                item.setForeground(0, self.palette().color(self.palette().ColorRole.Base))

        # Update task count indicator
        self.update_metric("TASKS", str(len(tasks)))

    def refresh_system_status(self):
        """Refresh system metrics"""
        threading.Thread(target=self._fetch_system_status, daemon=True).start()

    def _fetch_system_status(self):
        """Fetch system status in background thread"""
        try:
            # CPU usage (simplified)
            cpu_result = subprocess.run(
                ['sh', '-c', "top -bn1 | grep 'Cpu(s)' | awk '{print $2}' | cut -d'%' -f1"],
                capture_output=True,
                text=True,
                timeout=5
            )
            cpu = cpu_result.stdout.strip() if cpu_result.returncode == 0 else "??"

            # Memory usage
            mem_result = subprocess.run(
                ['sh', '-c', "free | grep Mem | awk '{print int($3/$2 * 100)}'"],
                capture_output=True,
                text=True,
                timeout=5
            )
            mem = mem_result.stdout.strip() if mem_result.returncode == 0 else "??"

            # SSH status
            ssh_result = subprocess.run(
                ['systemctl', 'is-active', 'ssh'],
                capture_output=True,
                text=True,
                timeout=5
            )
            ssh = "✓" if ssh_result.stdout.strip() == "active" else "✗"

            # Update UI
            self.signals.update_status.emit("CPU", f"{cpu}%")
            self.signals.update_status.emit("RAM", f"{mem}%")
            self.signals.update_status.emit("SSH", ssh)

        except Exception:
            pass

    def update_metric(self, name: str, value: str):
        """Update metric indicator (thread-safe)"""
        indicator = self.findChild(QLabel, f"indicator_{name.lower()}_value")
        if indicator:
            indicator.setText(value)

    # === Event Handlers ===

    def on_tree_item_clicked(self, item, column):
        """Handle tree item selection"""
        data = item.data(0, Qt.ItemDataRole.UserRole)
        if data:
            if str(data).startswith("task:"):
                self.selected_task = str(data).split(":", 1)[1]
                self.selected_script = None
                self.log_output(f"Selected task: {self.selected_task}")
                self.show_task_output(self.selected_task)
            else:
                self.selected_script = str(data)
                self.selected_task = None
                self.log_output(f"Selected script: {Path(self.selected_script).name}")

    def auto_refresh(self):
        """Auto-refresh handler (called every 2 seconds)"""
        self.refresh_tasks()
        if self.monitoring_active:
            self.refresh_system_status()

    # === Action Methods ===

    def run_selected_script(self):
        """Run the selected script"""
        if not self.selected_script:
            self.log_output("⚠ No script selected")
            return

        script_path = Path(self.selected_script)
        script_name = script_path.stem

        self.log_output(f"🚀 Launching {script_name} in background...")

        try:
            # Use start-long-task.sh to run in tmux
            launcher = self.automation_dir / "start-long-task.sh"
            if launcher.exists():
                subprocess.Popen([
                    'bash',
                    str(launcher),
                    script_name,
                    f'bash {script_path}'
                ])
                self.log_output(f"✓ Task '{script_name}' started in tmux session")
                QTimer.singleShot(1000, self.refresh_tasks)
            else:
                # Direct execution
                subprocess.Popen(['bash', str(script_path)])
                self.log_output(f"✓ Script executed directly")

        except Exception as e:
            self.log_output(f"✗ Error: {str(e)}")

    def stop_selected_task(self):
        """Stop the selected tmux task"""
        if not self.selected_task:
            self.log_output("⚠ No task selected")
            return

        self.log_output(f"🔴 Stopping task: {self.selected_task}")

        try:
            subprocess.run(['tmux', 'kill-session', '-t', self.selected_task], timeout=5)
            self.log_output(f"✓ Task '{self.selected_task}' stopped")
            QTimer.singleShot(500, self.refresh_tasks)
        except Exception as e:
            self.log_output(f"✗ Error: {str(e)}")

    def view_logs(self):
        """View recent logs"""
        self.log_output("📋 Fetching recent logs...")
        threading.Thread(target=self._fetch_logs, daemon=True).start()

    def _fetch_logs(self):
        """Fetch logs in background"""
        try:
            result = subprocess.run(
                ['journalctl', '-n', '20', '--no-pager'],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                self.signals.update_output.emit(f"\n=== RECENT LOGS ===\n{result.stdout}\n")
            else:
                self.signals.update_output.emit("✗ Failed to fetch logs\n")
        except Exception as e:
            self.signals.update_output.emit(f"✗ Error: {str(e)}\n")

    def restart_ssh(self):
        """Restart SSH server"""
        self.log_output("🔄 Restarting SSH server...")
        try:
            subprocess.run(['sudo', 'systemctl', 'restart', 'ssh'], timeout=10)
            self.log_output("✓ SSH server restarted")
            QTimer.singleShot(1000, self.refresh_system_status)
        except Exception as e:
            self.log_output(f"✗ Error: {str(e)}")

    def show_phone_shortcuts(self):
        """Show phone shortcuts reference"""
        shortcuts_file = self.home_dir / "PHONE-SHORTCUTS.md"
        if shortcuts_file.exists():
            self.log_output("📱 Opening PHONE-SHORTCUTS.md...")
            subprocess.Popen(['xdg-open', str(shortcuts_file)])
        else:
            self.log_output("⚠ PHONE-SHORTCUTS.md not found")

    def show_task_output(self, task_name: str):
        """Show live output from tmux task"""
        self.log_output(f"\n=== OUTPUT FROM: {task_name} ===\n")
        threading.Thread(target=self._capture_task_output, args=(task_name,), daemon=True).start()

    def _capture_task_output(self, task_name: str):
        """Capture tmux task output"""
        try:
            result = subprocess.run(
                ['tmux', 'capture-pane', '-pt', task_name, '-S', '-50'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                self.signals.update_output.emit(result.stdout + "\n")
            else:
                self.signals.update_output.emit(f"✗ Could not capture output from {task_name}\n")
        except Exception as e:
            self.signals.update_output.emit(f"✗ Error: {str(e)}\n")

    def run_status_check(self):
        """Run home-control.sh status"""
        self.log_output("📊 Running system status check...")
        threading.Thread(target=self._run_status_check, daemon=True).start()

    def _run_status_check(self):
        """Run status check in background"""
        try:
            control_script = self.automation_dir / "home-control.sh"
            if control_script.exists():
                result = subprocess.run(
                    ['bash', str(control_script), 'status'],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                self.signals.update_output.emit(f"\n{result.stdout}\n")
            else:
                self.signals.update_output.emit("✗ home-control.sh not found\n")
        except Exception as e:
            self.signals.update_output.emit(f"✗ Error: {str(e)}\n")

    def open_terminal(self):
        """Open system terminal"""
        try:
            subprocess.Popen(['x-terminal-emulator'])
            self.log_output("✓ Terminal opened")
        except:
            try:
                subprocess.Popen(['xterm'])
                self.log_output("✓ Terminal opened")
            except Exception as e:
                self.log_output(f"✗ Could not open terminal: {str(e)}")

    def refresh_all(self):
        """Refresh everything"""
        self.log_output("🔄 Refreshing all data...")
        self.load_scripts()
        self.refresh_tasks()
        self.refresh_system_status()
        self.monitoring_active = True
        self.log_output("✓ Refresh complete")

    # === Helper Methods ===

    def log_output(self, message: str):
        """Log message to output (thread-safe wrapper)"""
        self.signals.update_output.emit(f"[{datetime.now().strftime('%H:%M:%S')}] {message}\n")

    def append_output(self, text: str):
        """Append text to output area (must be called from main thread)"""
        self.output_text.append(text)
        self.output_text.verticalScrollBar().setValue(
            self.output_text.verticalScrollBar().maximum()
        )
        self.status_label.setText(text.strip().split('\n')[-1][:80])

    def get_welcome_message(self) -> str:
        """Get welcome message"""
        return f"""╔════════════════════════════════════════════════════════════╗
║  PHILAUNCH CONTROL CENTER - TACTICAL AUTOMATION DASHBOARD  ║
║  Remote Execution & Monitoring Interface                   ║
╚════════════════════════════════════════════════════════════╝

System initialized at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Select a script or task from the left panel to begin.

Quick Actions:
  - Select script → Click "RUN SCRIPT"
  - View running tasks under "RUNNING TASKS"
  - Click task to view live output
  - Use toolbar buttons for quick operations

"""

    # === Window Control Methods ===

    def toggle_maximize(self):
        """Toggle maximize/restore window"""
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def mousePressEvent(self, event):
        """Handle mouse press for window dragging"""
        if event.button() == Qt.MouseButton.LeftButton:
            if event.position().y() <= 32:  # Title bar height
                self.dragging = True
                self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        """Handle mouse move for window dragging"""
        if self.dragging and event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)

    def mouseReleaseEvent(self, event):
        """Handle mouse release"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False


def main():
    """Application entry point"""
    app = QApplication(sys.argv)
    app.setFont(QFont("Monospace", 10))

    # Check X server
    if 'DISPLAY' not in os.environ:
        print("Error: No X server detected!")
        print("WSL users: Ensure WSLg is installed or VcXsrv is running")
        sys.exit(1)

    window = PhiLaunchControlCenter()
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()

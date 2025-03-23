import gui
import sys




# --- Run App ---
app = gui.QApplication(sys.argv)
window = gui.MainWindow()
window.show()
sys.exit(app.exec())
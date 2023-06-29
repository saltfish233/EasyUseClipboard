from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QClipboard
from PyQt5.QtCore import  QMimeData

# Create QApplication instance
app = QApplication([])

# Get the clipboard instance
clipboard = QApplication.clipboard()

# Create QMimeData object
mime_data = QMimeData()

# Set custom format data
custom_data = "Custom data"
mime_data.setData("application/custom-format", custom_data.encode())

# Set QMimeData object to clipboard
clipboard.setMimeData(mime_data)

print(clipboard.mimeData().formats())

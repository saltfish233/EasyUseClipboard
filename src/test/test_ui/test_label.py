from PyQt5.QtWidgets import QApplication, QLabel

# Create QApplication instance
app = QApplication([])

# Create QLabel instance
label = QLabel()

# Set HTML content to the QLabel
html_content = "<h1>Hello, <span style='color: red;'>World!</span></h1>"
label.setText(html_content)

# Show the QLabel
label.show()

# Start the application event loop
app.exec()

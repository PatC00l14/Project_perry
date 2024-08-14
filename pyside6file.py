import sys
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton,
                               QVBoxLayout, QGridLayout, QComboBox, QMessageBox)

class InputDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Input Dialog')

        # Create main layout
        self.main_layout = QVBoxLayout()
        self.grid_layout = QGridLayout()
        
        # Number of devices dropdown
        num_devices_label = QLabel('Number of Devices:')
        self.num_devices_dropdown = QComboBox(self)
        self.num_devices_dropdown.addItems([str(i) for i in range(1, 9)])
        self.num_devices_dropdown.currentIndexChanged.connect(self.create_device_inputs)

        # Add to grid layout
        self.grid_layout.addWidget(num_devices_label, 0, 0)
        self.grid_layout.addWidget(self.num_devices_dropdown, 1, 0)
        
        # Container for device on/off dropdowns
        self.device_on_off_layout = QVBoxLayout()
        self.grid_layout.addLayout(self.device_on_off_layout, 0, 1, 2, 1)

        # Initialize the device_on_off_inputs list
        self.device_on_off_inputs = []

        # Device x, y, z variables
        device_xyz_label = QLabel('Device x, y, z:')
        self.device_x = QLineEdit(self)
        self.device_y = QLineEdit(self)
        self.device_z = QLineEdit(self)

        self.grid_layout.addWidget(device_xyz_label, 0, 2)
        self.grid_layout.addWidget(self.device_x, 1, 2)
        self.grid_layout.addWidget(self.device_y, 2, 2)
        self.grid_layout.addWidget(self.device_z, 3, 2)

        # Device material dropdown
        device_material_label = QLabel('Device Material:')
        self.device_material_dropdown = QComboBox(self)
        self.device_material_dropdown.addItems([str(i) for i in range(1, 7)])
        
        self.grid_layout.addWidget(device_material_label, 0, 3)
        self.grid_layout.addWidget(self.device_material_dropdown, 1, 3)
        
        # Number of layers dropdown
        num_layers_label = QLabel('Number of Layers:')
        self.num_layers_dropdown = QComboBox(self)
        self.num_layers_dropdown.addItems([str(i) for i in range(1, 6)])
        self.num_layers_dropdown.currentIndexChanged.connect(self.create_layer_inputs)

        self.grid_layout.addWidget(num_layers_label, 0, 4)
        self.grid_layout.addWidget(self.num_layers_dropdown, 1, 4)

        # Containers for layers
        self.layer_layouts = [QVBoxLayout() for _ in range(5)]
        self.layer_labels = ['Heights:', 'Widths:', 'Length:', 'Materials:', 'Heat Power:']
        for i, (label, layer_layout) in enumerate(zip(self.layer_labels, self.layer_layouts)):
            self.grid_layout.addWidget(QLabel(label), 0, 5 + i)
            self.grid_layout.addLayout(layer_layout, 1, 5 + i, 3, 1)
        
        # Initialize the layer_inputs list
        self.layer_inputs = [[] for _ in range(5)]

        # Additional single input fields
        self.single_inputs_labels = ['Heat Sink:', 'Body Mesh:', 'Ridge Mesh:', 'Ridge Height:']
        self.single_inputs = [QLineEdit(self) for _ in range(4)]
        for i, (label, single_input) in enumerate(zip(self.single_inputs_labels, self.single_inputs)):
            self.grid_layout.addWidget(QLabel(label), 0, 10 + i)
            self.grid_layout.addWidget(single_input, 1, 10 + i)

        # Additional three input fields
        self.three_input_label = QLabel('Heat Sink x, y, z:')
        self.three_inputs = [QLineEdit(self) for _ in range(3)]
        self.grid_layout.addWidget(self.three_input_label, 0, 14)
        for i, input_field in enumerate(self.three_inputs):
            self.grid_layout.addWidget(input_field, 1 + i, 14)
        
        # Single final input field as dropdown
        self.final_input_label = QLabel('Heat Sink Material:')
        self.final_input_dropdown = QComboBox(self)
        self.final_input_dropdown.addItems([str(i) for i in range(7)])
        
        self.grid_layout.addWidget(self.final_input_label, 0, 15)
        self.grid_layout.addWidget(self.final_input_dropdown, 1, 15)

        # Create submit button
        self.submit_button = QPushButton('Submit', self)
        self.submit_button.clicked.connect(self.show_values)

        # Add grid layout and submit button to main layout
        self.main_layout.addLayout(self.grid_layout)
        self.main_layout.addWidget(self.submit_button)

        self.setLayout(self.main_layout)

    def create_device_inputs(self):
        # Clear previous device inputs
        while self.device_on_off_layout.count():
            child = self.device_on_off_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Get the selected number of devices
        num_devices = int(self.num_devices_dropdown.currentText())

        # Initialize the device_on_off_inputs list
        self.device_on_off_inputs = []

        # Create new device input fields based on the selected number
        for i in range(num_devices):
            label = QLabel(f'Device {i + 1} Status:')
            dropdown = QComboBox(self)
            dropdown.addItems(['on', 'off'])
            self.device_on_off_inputs.append(dropdown)

            self.device_on_off_layout.addWidget(label)
            self.device_on_off_layout.addWidget(dropdown)

    def create_layer_inputs(self):
        # Clear previous layer inputs
        for layer_layout in self.layer_layouts:
            while layer_layout.count():
                child = layer_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

        # Get the selected number of layers
        num_layers = int(self.num_layers_dropdown.currentText())

        # Initialize layer_inputs list
        self.layer_inputs = [[] for _ in range(5)]
        for i in range(num_layers):
            for j in range(5):
                if j == 3:  # Materials column
                    dropdown = QComboBox(self)
                    dropdown.addItems([str(i) for i in range(1, 7)])
                    self.layer_inputs[j].append(dropdown)
                    layer_layout = self.layer_layouts[j]
                    layer_layout.addWidget(dropdown)
                else:
                    line_edit = QLineEdit(self)
                    self.layer_inputs[j].append(line_edit)
                    self.layer_layouts[j].addWidget(line_edit)

    def show_values(self):
        num_devices = self.num_devices_dropdown.currentText()
        device_on_off_values = [dropdown.currentText() for dropdown in self.device_on_off_inputs]
        device_x = self.device_x.text()
        device_y = self.device_y.text()
        device_z = self.device_z.text()
        device_material = self.device_material_dropdown.currentText()
        num_layers = self.num_layers_dropdown.currentText()
        layer_values = [[line_edit.text() if isinstance(line_edit, QLineEdit) else line_edit.currentText() 
                         for line_edit in layer] for layer in self.layer_inputs]
        single_values = [line_edit.text() for line_edit in self.single_inputs]
        three_values = [line_edit.text() for line_edit in self.three_inputs]
        final_value = self.final_input_dropdown.currentText()

        # Display gathered values in a message box
        QMessageBox.information(self, 'Input Values',
                                f'Number of Devices: {num_devices}\n' +
                                '\n'.join([f'Device {i+1} Status: {val}' for i, val in enumerate(device_on_off_values)]) +
                                f'\nDevice x: {device_x}\nDevice y: {device_y}\nDevice z: {device_z}\n' +
                                f'Device Material: {device_material}\nNumber of Layers: {num_layers}\n' +
                                '\n'.join([f'{label} {", ".join(vals)}' for label, vals in zip(self.layer_labels, layer_values)]) +
                                '\n'.join([f'{label} {val}' for label, val in zip(self.single_inputs_labels, single_values)]) +
                                f'\nHeat Sink x,y,z: {", ".join(three_values)}\nHeat Sink Material: {final_value}'
                                )

def main():
    app = QApplication(sys.argv)
    ex = InputDialog()
    ex.show()
    app.exec()

if '__main__' == '__main__':
    main()
    



import os
from PySide2 import QtWidgets
from mapclientplugins.fieldworkmodelserialiserstep.ui_configuredialog import Ui_Dialog

INVALID_STYLE_SHEET = 'background-color: rgba(239, 0, 0, 50)'
DEFAULT_STYLE_SHEET = 'background-color: rgba(255, 255, 255, 50)'


class ConfigureDialog(QtWidgets.QDialog):
    """
    Configure dialog to present the user with the options to configure this step.
    """

    def __init__(self, parent=None):
        '''
        Constructor
        '''
        QtWidgets.QDialog.__init__(self, parent)

        self._ui = Ui_Dialog()
        self._ui.setupUi(self)

        self._workflow_location = None

        self._previousGFLoc = ''
        self._previousEnsLoc = ''
        self._previousMeshLoc = ''
        self._previousPathLoc = ''

        self._makeConnections()

    def _makeConnections(self):
        self._ui.gfLocButton.clicked.connect(self._gfLocClicked)
        self._ui.gfLocLineEdit.textChanged.connect(self._gfLocEdited)
        self._ui.ensLocButton.clicked.connect(self._ensLocClicked)
        self._ui.ensLocLineEdit.textChanged.connect(self._ensLocEdited)
        self._ui.meshLocButton.clicked.connect(self._meshLocClicked)
        self._ui.meshLocLineEdit.textChanged.connect(self._meshLocEdited)
        self._ui.pathLocButton.clicked.connect(self._pathLocClicked)
        self._ui.pathLocLineEdit.textChanged.connect(self._pathLocEdited)

    def setWorkflowLocation(self, location):
        self._workflow_location = location

    def accept(self):
        """
        Override the accept method so that we can confirm saving an
        invalid configuration.
        """
        result = QtWidgets.QMessageBox.Yes
        if not self.validate():
            result = QtWidgets.QMessageBox.warning(self, 'Invalid Configuration',
                                                   'This configuration is invalid.  Unpredictable behaviour may result if you choose \'Yes\', are you sure you want to save this configuration?)',
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)

        if result == QtWidgets.QMessageBox.Yes:
            QtWidgets.QDialog.accept(self)

    def validate(self):
        """
        Validate the configuration dialog fields.  For any field that is not valid
        set the style sheet to the INVALID_STYLE_SHEET.  Return the outcome of the
        overall validity of the configuration.
        """
        output_path = self._ui.gfLocLineEdit.text()
        output_directory = os.path.dirname(output_path)
        non_empty = len(output_path)

        if not os.path.isabs(output_directory):
            output_directory = os.path.join(self._workflow_location, output_directory)

        output_directory_valid = os.path.exists(output_directory) and non_empty

        self._ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(output_directory_valid)
        self._ui.gfLocLineEdit.setStyleSheet(DEFAULT_STYLE_SHEET if output_directory_valid else INVALID_STYLE_SHEET)

        other_fields = [self._ui.ensLocLineEdit, self._ui.meshLocLineEdit, self._ui.pathLocLineEdit]
        for field in other_fields:
            path = field.text()
            if not os.path.isabs(path):
                path = os.path.join(self._workflow_location, path)
            field_valid = os.path.exists(path) and len(path)
            field.setStyleSheet(DEFAULT_STYLE_SHEET if field_valid else INVALID_STYLE_SHEET)

        return output_directory_valid

    def getConfig(self):
        """
        Get the current value of the configuration from the dialog.
        """
        self._previousGFLoc = self._ui.gfLocLineEdit.text()
        self._previousEnsLoc = self._ui.ensLocLineEdit.text()
        self._previousMeshLoc = self._ui.meshLocLineEdit.text()
        self._previousPathLoc = self._ui.pathLocLineEdit.text()
        config = {}
        config['GF Filename'] = self._ui.gfLocLineEdit.text()
        config['Ensemble Filename'] = self._ui.ensLocLineEdit.text()
        config['Mesh Filename'] = self._ui.meshLocLineEdit.text()
        config['Path'] = self._ui.pathLocLineEdit.text()
        return config

    def setConfig(self, config):
        """
        Set the current value of the configuration for the dialog.
        """
        self._previousGFLoc = config['GF Filename']
        self._previousEnsLoc = config['Ensemble Filename']
        self._previousMeshLoc = config['Mesh Filename']
        self._previousPathLoc = config['Path']
        self._ui.gfLocLineEdit.setText(config['GF Filename'])
        self._ui.ensLocLineEdit.setText(config['Ensemble Filename'])
        self._ui.meshLocLineEdit.setText(config['Mesh Filename'])
        self._ui.pathLocLineEdit.setText(config['Path'])

    def _gfLocClicked(self):
        location = QtWidgets.QFileDialog.getSaveFileName(self, 'Select File Location', self._previousGFLoc)
        if location[0]:
            self._previousGFLoc = location[0]

            if self._workflow_location:
                self._ui.gfLocLineEdit.setText(os.path.relpath(location[0], self._workflow_location))
            else:
                self._ui.gfLocLineEdit.setText(location[0])

    def _gfLocEdited(self):
        self.validate()

    def _ensLocClicked(self):
        location = QtWidgets.QFileDialog.getSaveFileName(self, 'Select File Location', self._previousEnsLoc)
        if location[0]:
            self._previousEnsLoc = location[0]

            if self._workflow_location:
                self._ui.ensLocLineEdit.setText(os.path.relpath(location[0], self._workflow_location))
            else:
                self._ui.ensLocLineEdit.setText(location[0])

    def _ensLocEdited(self):
        self.validate()

    def _meshLocClicked(self):
        location = QtWidgets.QFileDialog.getSaveFileName(self, 'Select File Location', self._previousMeshLoc)
        if location[0]:
            self._previousMeshLoc = location[0]

            if self._workflow_location:
                self._ui.meshLocLineEdit.setText(os.path.relpath(location[0], self._workflow_location))
            else:
                self._ui.meshLocLineEdit.setText(location[0])

    def _meshLocEdited(self):
        self.validate()

    def _pathLocClicked(self):
        location = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Path Folder', self._previousPathLoc)
        if location:
            self._previousPathLoc = location

            if self._workflow_location:
                self._ui.pathLocLineEdit.setText(os.path.relpath(location, self._workflow_location))
            else:
                self._ui.pathLocLineEdit.setText(location)

    def _pathLocEdited(self):
        self.validate()

from PySide2 import QtWidgets
from mapclientplugins.fieldworkmodelserialiserstep.ui_configuredialog import Ui_Dialog

INVALID_STYLE_SHEET = 'background-color: rgba(239, 0, 0, 50)'
DEFAULT_STYLE_SHEET = 'background-color: rgba(255, 255, 255, 50)'


class ConfigureDialog(QtWidgets.QDialog):
    '''
    Configure dialog to present the user with the options to configure this step.
    '''

    def __init__(self, parent=None):
        '''
        Constructor
        '''
        QtWidgets.QDialog.__init__(self, parent)

        self._ui = Ui_Dialog()
        self._ui.setupUi(self)

        # Keep track of the previous identifier so that we can track changes
        # and know how many occurrences of the current identifier there should
        # be.
        self._previousIdentifier = ''
        self._previousGFLoc = ''
        self._previousEnsLoc = ''
        self._previousMeshLoc = ''
        self._previousPathLoc = ''
        # Set a place holder for a callable that will get set from the step.
        # We will use this method to decide whether the identifier is unique.
        self.identifierOccursCount = None

        self._makeConnections()

    def _makeConnections(self):
        self._ui.idLineEdit.textChanged.connect(self.validate)
        self._ui.gfLocButton.clicked.connect(self._gfLocClicked)
        self._ui.gfLocLineEdit.textChanged.connect(self._gfLocEdited)
        self._ui.ensLocButton.clicked.connect(self._ensLocClicked)
        self._ui.ensLocLineEdit.textChanged.connect(self._ensLocEdited)
        self._ui.meshLocButton.clicked.connect(self._meshLocClicked)
        self._ui.meshLocLineEdit.textChanged.connect(self._meshLocEdited)
        self._ui.pathLocButton.clicked.connect(self._pathLocClicked)
        self._ui.pathLocLineEdit.textChanged.connect(self._pathLocEdited)

    def accept(self):
        '''
        Override the accept method so that we can confirm saving an
        invalid configuration.
        '''
        result = QtWidgets.QMessageBox.Yes
        if not self.validate():
            result = QtWidgets.QMessageBox.warning(self, 'Invalid Configuration',
                                                   'This configuration is invalid.  Unpredictable behaviour may result if you choose \'Yes\', are you sure you want to save this configuration?)',
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)

        if result == QtWidgets.QMessageBox.Yes:
            QtWidgets.QDialog.accept(self)

    def validate(self):
        '''
        Validate the configuration dialog fields.  For any field that is not valid
        set the style sheet to the INVALID_STYLE_SHEET.  Return the outcome of the 
        overall validity of the configuration.
        '''
        # Determine if the current identifier is unique throughout the workflow
        # The identifierOccursCount method is part of the interface to the workflow framework.
        idValue = self.identifierOccursCount(self._ui.idLineEdit.text())
        idValid = (idValue == 0) or (idValue == 1 and self._previousIdentifier == self._ui.idLineEdit.text())
        if idValid:
            self._ui.idLineEdit.setStyleSheet(DEFAULT_STYLE_SHEET)
        else:
            self._ui.idLineEdit.setStyleSheet(INVALID_STYLE_SHEET)

        # ok button can be pressed as long as id is okay, rest of configs
        # don't have to be valid
        self._ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(idValid)

        gfLocValid = len(self._ui.gfLocLineEdit.text()) > 0
        if gfLocValid:
            self._ui.gfLocLineEdit.setStyleSheet(DEFAULT_STYLE_SHEET)
        else:
            self._ui.gfLocLineEdit.setStyleSheet(INVALID_STYLE_SHEET)

        valid = idValid and gfLocValid
        # self._ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(valid)

        return valid

    def getConfig(self):
        '''
        Get the current value of the configuration from the dialog.  Also
        set the _previousIdentifier value so that we can check uniqueness of the
        identifier over the whole of the workflow.
        '''
        self._previousIdentifier = self._ui.idLineEdit.text()
        self._previousGFLoc = self._ui.gfLocLineEdit.text()
        self._previousEnsLoc = self._ui.ensLocLineEdit.text()
        self._previousMeshLoc = self._ui.meshLocLineEdit.text()
        self._previousPathLoc = self._ui.pathLocLineEdit.text()
        config = {}
        config['identifier'] = self._ui.idLineEdit.text()
        config['GF Filename'] = self._ui.gfLocLineEdit.text()
        config['Ensemble Filename'] = self._ui.ensLocLineEdit.text()
        config['Mesh Filename'] = self._ui.meshLocLineEdit.text()
        config['Path'] = self._ui.pathLocLineEdit.text()
        return config

    def setConfig(self, config):
        '''
        Set the current value of the configuration for the dialog.  Also
        set the _previousIdentifier value so that we can check uniqueness of the
        identifier over the whole of the workflow.
        '''
        self._previousIdentifier = config['identifier']
        self._previousGFLoc = config['GF Filename']
        self._previousEnsLoc = config['Ensemble Filename']
        self._previousMeshLoc = config['Mesh Filename']
        self._previousPathLoc = config['Path']
        self._ui.idLineEdit.setText(config['identifier'])
        self._ui.gfLocLineEdit.setText(config['GF Filename'])
        self._ui.ensLocLineEdit.setText(config['Ensemble Filename'])
        self._ui.meshLocLineEdit.setText(config['Mesh Filename'])
        self._ui.pathLocLineEdit.setText(config['Path'])

    def _gfLocClicked(self):
        location = QtWidgets.QFileDialog.getSaveFileName(self, 'Select File Location', self._previousGFLoc)
        if location[0]:
            self._previousGFLoc = location[0]
            self._ui.gfLocLineEdit.setText(location[0])

    def _gfLocEdited(self):
        self.validate()

    def _ensLocClicked(self):
        location = QtWidgets.QFileDialog.getSaveFileName(self, 'Select File Location', self._previousEnsLoc)
        if location[0]:
            self._previousEnsLoc = location[0]
            self._ui.ensLocLineEdit.setText(location[0])

    def _ensLocEdited(self):
        self.validate()

    def _meshLocClicked(self):
        location = QtWidgets.QFileDialog.getSaveFileName(self, 'Select File Location', self._previousMeshLoc)
        if location[0]:
            self._previousMeshLoc = location[0]
            self._ui.meshLocLineEdit.setText(location[0])

    def _meshLocEdited(self):
        self.validate()

    def _pathLocClicked(self):
        location = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Path Folder', self._previousPathLoc)
        if location:
            self._previousPathLoc = location
            self._ui.pathLocLineEdit.setText(location)

    def _pathLocEdited(self):
        self.validate()

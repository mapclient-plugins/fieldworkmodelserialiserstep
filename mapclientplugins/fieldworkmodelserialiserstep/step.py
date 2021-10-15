"""
MAP Client Plugin - Fieldwork Model Serialiser Step
Saves a fieldwork geometric_field to disk. Inputs are a GF and
a list of filenames for the GF, ensemble, mesh, and path. If
list of filenames is input, they override the filenames in
the plugin config. Filenames for ensemble, mesh, and path
can be None in input list, or empty strings in config.
"""

import os

import json

from mapclient.mountpoints.workflowstep import WorkflowStepMountPoint
from mapclientplugins.fieldworkmodelserialiserstep.configuredialog import ConfigureDialog


class FieldworkModelSerialiserStep(WorkflowStepMountPoint):
    """
    Step for saving a fieldwork model to disk.
    """

    def __init__(self, location):
        super(FieldworkModelSerialiserStep, self).__init__('Fieldwork Model Serialiser', location)
        self._configured = False  # A step cannot be executed until it has been configured.
        self._category = 'Sink'
        # Add any other initialisation code here:
        # Ports:

        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'ju#fieldworkmodel'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'python#string'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'python#string'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'python#string'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'python#string'))

        self._config = {}
        self._config['GF Filename'] = ''
        self._config['Ensemble Filename'] = ''
        self._config['Mesh Filename'] = ''
        self._config['Path'] = ''

        self._GF = None
        self._GFFilename = None
        self._ensFilename = None
        self._meshFilename = None
        self._path = None

        self._identifier = ''

    def execute(self):
        """
        Add your code here that will kick off the execution of the step.
        Make sure you call the _doneExecution() method when finished.  This method
        may be connected up to a button in a widget for example.
        """
        # Put your execute step code here before calling the '_doneExecution' method.
        if self._GFFilename is not None:
            gfFilename = os.path.join(self._location, self._GFFilename)
        else:
            # gfFilename = os.path.join(self._location, self._config['GF Filename'])
            gfFilename = self._config['GF Filename']
            if not os.path.isabs(gfFilename):
                gfFilename = os.path.join(self._location, gfFilename)

        if self._ensFilename is not None:
            ensFilename = self._ensFilename
        elif self._config['Ensemble Filename'] == '':
            ensFilename = None
        else:
            # ensFilename = self._config['Ensemble Filename']
            ensFilename = self._config['Ensemble Filename']
            if not os.path.isabs(ensFilename):
                ensFilename = os.path.join(self._location, ensFilename)

        if self._meshFilename is not None:
            meshFilename = self._meshFilename
        elif self._config['Mesh Filename'] == '':
            meshFilename = None
        else:
            # meshFilename = self._config['Mesh Filename']
            meshFilename = self._config['Mesh Filename']
            if not os.path.isabs(meshFilename):
                meshFilename = os.path.join(self._location, meshFilename)

        if self._path is not None:
            path = self._path
        elif self._config['Path'] == '':
            path = ''
        else:
            # path = self._config['Path']
            path = self._config['Path']
            if not os.path.isabs(path):
                path = os.path.join(self._location, path)

        print('serialising fieldwork model to:')
        print(gfFilename + '.geof')
        if ensFilename != None:
            print(ensFilename + '.ens')
        if meshFilename != None:
            print(meshFilename + '.mesh')
        if path != '':
            print('path: ' + path)

        self._GF.save_geometric_field(gfFilename, ensFilename, meshFilename, path)
        self._doneExecution()

    def setPortData(self, index, data_in):
        """
        Add your code here that will set the appropriate objects for this step.
        The index is the index of the port in the port list.  If there is only one
        uses port for this step then the index can be ignored.
        """
        if index == 0:
            self._GF = data_in  # ju fieldworkmodel
        elif index == 1:
            self._GFFilename = data_in  # String
        elif index == 2:
            self._ensFilename = data_in  # String
        elif index == 3:
            self._meshFilename = data_in  # String
        else:
            self._path = data_in

    def configure(self):
        """
        This function will be called when the configure icon on the step is
        clicked.  It is appropriate to display a configuration dialog at this
        time.  If the conditions for the configuration of this step are complete
        then set:
            self._configured = True
        """
        dlg = ConfigureDialog(self._main_window)
        dlg.setWorkflowLocation(self._location)
        dlg.setConfig(self._config)
        dlg.validate()
        dlg.setModal(True)

        if dlg.exec_():
            self._config = dlg.getConfig()

        self._configured = dlg.validate()
        self._configuredObserver()

    def getIdentifier(self):
        """
        The identifier is a string that must be unique within a workflow.
        """
        return self._identifier

    def setIdentifier(self, identifier):
        """
        The framework will set the identifier for this step when it is loaded.
        """
        self._identifier = identifier

    def serialize(self):
        """
        Add code to serialize this step to disk. Returns a json string for
        mapclient to serialise.
        """
        return json.dumps(self._config, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def deserialize(self, string):
        """
        Add code to deserialize this step from disk. Parses a json string
        given by mapclient
        """
        self._config.update(json.loads(string))

        d = ConfigureDialog()
        d.setWorkflowLocation(self._location)
        d.setConfig(self._config)
        self._configured = d.validate()

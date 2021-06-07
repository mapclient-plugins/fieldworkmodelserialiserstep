
'''
MAP Client Plugin - Fieldwork Model Serialiser Step
Saves a fieldwork geometric_field to disk. Inputs are a GF and 
a list of filenames for the GF, ensemble, mesh, and path. If 
list of filenames is input, they override the filenames in 
the plugin config. Filenames for ensemble, mesh, and path 
can be None in input list, or empty strings in config.
'''
import json

from mapclient.mountpoints.workflowstep import WorkflowStepMountPoint
from mapclientplugins.fieldworkmodelserialiserstep.configuredialog import ConfigureDialog

class FieldworkModelSerialiserStep(WorkflowStepMountPoint):
    '''
    Step for saving a fieldwork model to disk.
    '''

    def __init__(self, location):
        super(FieldworkModelSerialiserStep, self).__init__('Fieldwork Model Serialiser', location)
        self._configured = False # A step cannot be executed until it has been configured.
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
        self._config['identifier'] = ''
        self._config['GF Filename'] = ''
        self._config['Ensemble Filename'] = ''
        self._config['Mesh Filename'] = ''
        self._config['Path'] = ''

        self._GF = None
        self._GFFilename = None
        self._ensFilename = None
        self._meshFilename = None
        self._path = None

    def execute(self):
        '''
        Add your code here that will kick off the execution of the step.
        Make sure you call the _doneExecution() method when finished.  This method
        may be connected up to a button in a widget for example.
        '''
        # Put your execute step code here before calling the '_doneExecution' method.
        if self._GFFilename!=None:
            gfFilename = self._GFFilename
        else:
            gfFilename = self._config['GF Filename']

        if self._ensFilename!=None:
            ensFilename = self._ensFilename
        elif self._config['Ensemble Filename']=='':
            ensFilename = None
        else:
            ensFilename = self._config['Ensemble Filename']

        if self._meshFilename!=None:
            meshFilename = self._meshFilename
        elif self._config['Mesh Filename']=='':
            meshFilename = None
        else:
            meshFilename = self._config['Mesh Filename']

        if self._path!=None:
            path = self._path
        elif self._config['Path']=='':
            path = ''
        else:
            path = self._config['Path']

        print('serialising fieldwork model to:')
        print(gfFilename+'.geof')
        if ensFilename!=None:
            print(ensFilename+'.ens')
        if meshFilename!=None:
            print(meshFilename+'.mesh')
        if path!='':
            print('path: '+path)
        
        self._GF.save_geometric_field(gfFilename, ensFilename, meshFilename, path)
        self._doneExecution()

    def setPortData(self, index, dataIn):
        '''
        Add your code here that will set the appropriate objects for this step.
        The index is the index of the port in the port list.  If there is only one
        uses port for this step then the index can be ignored.
        '''
        if index == 0:
            self._GF = dataIn # ju#fieldworkmodel
        elif index == 1:
            self._GFFilename = dataIn # String
        elif index == 2:
            self._ensFilename = dataIn # String
        elif index == 3:
            self._meshFilename = dataIn # String
        else:
            self._path = dataIn

    def configure(self):
        '''
        This function will be called when the configure icon on the step is
        clicked.  It is appropriate to display a configuration dialog at this
        time.  If the conditions for the configuration of this step are complete
        then set:
            self._configured = True
        '''
        dlg = ConfigureDialog()
        dlg.identifierOccursCount = self._identifierOccursCount
        dlg.setConfig(self._config)
        dlg.validate()
        dlg.setModal(True)
        
        if dlg.exec_():
            self._config = dlg.getConfig()
        
        self._configured = dlg.validate()
        self._configuredObserver()

    def getIdentifier(self):
        '''
        The identifier is a string that must be unique within a workflow.
        '''
        return self._config['identifier']

    def setIdentifier(self, identifier):
        '''
        The framework will set the identifier for this step when it is loaded.
        '''
        self._config['identifier'] = identifier

    def serialize(self):
        '''
        Add code to serialize this step to disk. Returns a json string for
        mapclient to serialise.
        '''
        return json.dumps(self._config, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def deserialize(self, string):
        '''
        Add code to deserialize this step from disk. Parses a json string
        given by mapclient
        '''
        self._config.update(json.loads(string))

        d = ConfigureDialog()
        d.identifierOccursCount = self._identifierOccursCount
        d.setConfig(self._config)
        self._configured = d.validate()


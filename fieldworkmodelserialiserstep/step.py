
'''
MAP Client Plugin - Fieldwork Model Serialiser Step
Saves a fieldwork geometric_field to disk. Inputs are a GF and 
a list of filenames for the GF, ensemble, mesh, and path. If 
list of filenames is input, they override the filenames in 
the plugin config. Filenames for ensemble, mesh, and path 
can be None in input list, or empty strings in config.
'''
import os

from PySide import QtGui
from PySide import QtCore

from mountpoints.workflowstep import WorkflowStepMountPoint
from fieldworkmodelserialiserstep.configuredialog import ConfigureDialog

from fieldwork.field import geometric_field


class FieldworkModelSerialiserStep(WorkflowStepMountPoint):
    '''
    Skeleton step which is intended to be a helpful starting point
    for new steps.
    '''

    def __init__(self, location):
        super(FieldworkModelSerialiserStep, self).__init__('Fieldwork Model Serialiser', location)
        self._configured = False # A step cannot be executed until it has been configured.
        self._category = 'Output'
        # Add any other initialisation code here:
        # Ports:
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'ju#fieldworkmodel'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'ju#fieldworkmodelfilenames'))
        self._config = {}
        self._config['identifier'] = ''
        self._config['GF Filename'] = ''
        self._config['Ensemble Filename'] = ''
        self._config['Mesh Filename'] = ''
        self._config['Path'] = ''

        self._GF = None
        self._filenames = None


    def execute(self):
        '''
        Add your code here that will kick off the execution of the step.
        Make sure you call the _doneExecution() method when finished.  This method
        may be connected up to a button in a widget for example.
        '''
        # Put your execute step code here before calling the '_doneExecution' method.
        if self._filenames!=None:
            gfFilename = self._filenames[0]
            ensFilename = self._filenames[1]
            meshFilename = self._filenames[2]
            path = self._filenames[3]
        else:
            gfFilename = self._config['GF Filename']
            if len(self._config['Ensemble Filename'])==0:
                ensFilename = None
            if len(self._config['Mesh Filename'])==0:
                meshFilename = None
            if len(self._config['Path'])==0:
                path = None

        self._GF.save_geometric_field(gfFilename, ensFilename, meshFilename, path=path)
        self._doneExecution()

    def setPortData(self, index, dataIn):
        '''
        Add your code here that will set the appropriate objects for this step.
        The index is the index of the port in the port list.  If there is only one
        uses port for this step then the index can be ignored.
        '''
        if index == 0:
            self._GF = dataIn # ju#fieldworkmodel
        else:
            self._filenames = dataIn # ju#fieldworkmodelfilenames

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

    def serialize(self, location):
        '''
        Add code to serialize this step to disk.  The filename should
        use the step identifier (received from getIdentifier()) to keep it
        unique within the workflow.  The suggested name for the file on
        disk is:
            filename = getIdentifier() + '.conf'
        '''
        configuration_file = os.path.join(location, self.getIdentifier() + '.conf')
        conf = QtCore.QSettings(configuration_file, QtCore.QSettings.IniFormat)
        conf.beginGroup('config')
        conf.setValue('identifier', self._config['identifier'])
        conf.setValue('GF Filename', self._config['GF Filename'])
        conf.setValue('Ensemble Filename', self._config['Ensemble Filename'])
        conf.setValue('Mesh Filename', self._config['Mesh Filename'])
        conf.setValue('Path', self._config['Path'])
        conf.endGroup()


    def deserialize(self, location):
        '''
        Add code to deserialize this step from disk.  As with the serialize 
        method the filename should use the step identifier.  Obviously the 
        filename used here should be the same as the one used by the
        serialize method.
        '''
        configuration_file = os.path.join(location, self.getIdentifier() + '.conf')
        conf = QtCore.QSettings(configuration_file, QtCore.QSettings.IniFormat)
        conf.beginGroup('config')
        self._config['identifier'] = conf.value('identifier', '')
        self._config['GF Filename'] = conf.value('GF Filename', '')
        self._config['Ensemble Filename'] = conf.value('Ensemble Filename', '')
        self._config['Mesh Filename'] = conf.value('Mesh Filename', '')
        self._config['Path'] = conf.value('Path', '')
        conf.endGroup()

        d = ConfigureDialog()
        d.identifierOccursCount = self._identifierOccursCount
        d.setConfig(self._config)
        self._configured = d.validate()



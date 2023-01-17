Fieldwork Model Serialiser Step
===============================

MAP Client plugin for writing a Fieldwork mesh to file.

Requires
--------
- GIAS3 : https://github.com/musculoskeletal/gias3

Inputs
------
- **string** [str] : Path of the .geof file to be written.
- **string** [str] : Path of the .ens to be written.
- **string** [str] : Path of the .mesh to be written.
- **string** [str][Optional] : Path prefix of the files to be written.

Outputs
-------
- **fieldworkmodel** [GIAS3 GeometricField instance] : The Fieldwork mesh read from file.

Configuration
-------------
- **identifier** : Unique name for the step.
- **GF Filename** : Path of the .geof file to be read.
- **Ensemble Filename** [Optional]: Path of the .ens to be read.
- **Mesh Filename** [Optional] : Path of the .mesh to be read.
- **Path** [Optional]: Path prefix of the files to be read.

Usage
-----
This step is used to read a Fieldwork mesh from file. A Fieldwork mesh is a piece-wise parametric mesh composed of an ensemble of elements interpolated by Lagrange polynomials controlled by the coordinates of nodes within each element. The key pieces of information of a mesh are its nodal coordinates which define the meshes geometry, the type of Lagrange polynomials used to interpolate each element, and the connectivity and shapes of the element. As such, a Fieldwork model is read from 3 files:

- **.geof** : a GeometricField file that contains the nodal coordinates, and therefore the geometry of the mesh;
- **.ens** : an Ensemble file that contains information about the polynomial functions of the mesh's elements.;
- **.mesh** : a Mesh file that contains the connectivity of mesh elements and the shape of each element.

See Fieldwork Model Serialiser Step to write a Fieldwork mesh to file.


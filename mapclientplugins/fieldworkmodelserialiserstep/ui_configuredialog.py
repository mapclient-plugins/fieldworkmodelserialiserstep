# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'configuredialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(524, 222)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.configGroupBox = QGroupBox(Dialog)
        self.configGroupBox.setObjectName(u"configGroupBox")
        self.formLayout = QFormLayout(self.configGroupBox)
        self.formLayout.setObjectName(u"formLayout")
        self.label1 = QLabel(self.configGroupBox)
        self.label1.setObjectName(u"label1")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.gfLocLineEdit = QLineEdit(self.configGroupBox)
        self.gfLocLineEdit.setObjectName(u"gfLocLineEdit")

        self.horizontalLayout.addWidget(self.gfLocLineEdit)

        self.gfLocButton = QPushButton(self.configGroupBox)
        self.gfLocButton.setObjectName(u"gfLocButton")

        self.horizontalLayout.addWidget(self.gfLocButton)


        self.formLayout.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout)

        self.label2 = QLabel(self.configGroupBox)
        self.label2.setObjectName(u"label2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.ensLocLineEdit = QLineEdit(self.configGroupBox)
        self.ensLocLineEdit.setObjectName(u"ensLocLineEdit")

        self.horizontalLayout_2.addWidget(self.ensLocLineEdit)

        self.ensLocButton = QPushButton(self.configGroupBox)
        self.ensLocButton.setObjectName(u"ensLocButton")

        self.horizontalLayout_2.addWidget(self.ensLocButton)


        self.formLayout.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout_2)

        self.label3 = QLabel(self.configGroupBox)
        self.label3.setObjectName(u"label3")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label3)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.meshLocLineEdit = QLineEdit(self.configGroupBox)
        self.meshLocLineEdit.setObjectName(u"meshLocLineEdit")

        self.horizontalLayout_3.addWidget(self.meshLocLineEdit)

        self.meshLocButton = QPushButton(self.configGroupBox)
        self.meshLocButton.setObjectName(u"meshLocButton")

        self.horizontalLayout_3.addWidget(self.meshLocButton)


        self.formLayout.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout_3)

        self.label4 = QLabel(self.configGroupBox)
        self.label4.setObjectName(u"label4")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label4)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.pathLocLineEdit = QLineEdit(self.configGroupBox)
        self.pathLocLineEdit.setObjectName(u"pathLocLineEdit")

        self.horizontalLayout_4.addWidget(self.pathLocLineEdit)

        self.pathLocButton = QPushButton(self.configGroupBox)
        self.pathLocButton.setObjectName(u"pathLocButton")

        self.horizontalLayout_4.addWidget(self.pathLocButton)


        self.formLayout.setLayout(3, QFormLayout.FieldRole, self.horizontalLayout_4)


        self.gridLayout.addWidget(self.configGroupBox, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        QWidget.setTabOrder(self.gfLocLineEdit, self.gfLocButton)
        QWidget.setTabOrder(self.gfLocButton, self.ensLocLineEdit)
        QWidget.setTabOrder(self.ensLocLineEdit, self.ensLocButton)
        QWidget.setTabOrder(self.ensLocButton, self.meshLocLineEdit)
        QWidget.setTabOrder(self.meshLocLineEdit, self.meshLocButton)
        QWidget.setTabOrder(self.meshLocButton, self.pathLocLineEdit)
        QWidget.setTabOrder(self.pathLocLineEdit, self.pathLocButton)
        QWidget.setTabOrder(self.pathLocButton, self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Configure Fieldwork Model Serialiser Step", None))
        self.configGroupBox.setTitle("")
        self.label1.setText(QCoreApplication.translate("Dialog", u"GF Filename:  ", None))
        self.gfLocButton.setText(QCoreApplication.translate("Dialog", u"...", None))
        self.label2.setText(QCoreApplication.translate("Dialog", u"Ensemble Filename:  ", None))
        self.ensLocButton.setText(QCoreApplication.translate("Dialog", u"...", None))
        self.label3.setText(QCoreApplication.translate("Dialog", u"Mesh Filename:  ", None))
        self.meshLocButton.setText(QCoreApplication.translate("Dialog", u"...", None))
        self.label4.setText(QCoreApplication.translate("Dialog", u"Path:  ", None))
        self.pathLocButton.setText(QCoreApplication.translate("Dialog", u"...", None))
    # retranslateUi


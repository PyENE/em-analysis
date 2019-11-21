from openalea.vpltk.qt import QtCore, QtGui

from openalea.core.system import systemnodes
from openalea.core.observer import lock_notify
from openalea.deploy.util import get_metadata
from openalea.visualea.node_widget import NodeWidget


class GetDataBrowser(NodeWidget, QtGui.QDialog):
    ''' This widget permits to select a shared data file located in a given Python 
    package. The data file is searched among the data nodes of the PackageManager. '''
    def __init__(self, node, parent):

        QtGui.QDialog.__init__(self, parent)
        NodeWidget.__init__(self, node)

        self.gridlayout = QtGui.QGridLayout(self)
        self.gridlayout.setContentsMargins(3, 3, 3, 3)
        self.gridlayout.setSpacing(5)

        self.package_lineedit_label = QtGui.QLabel('1. Set the package', self)
        self.gridlayout.addWidget(self.package_lineedit_label, 0, 0)
        
        self.package_lineedit = QtGui.QLineEdit(self)
        self.gridlayout.addWidget(self.package_lineedit, 0, 1, 1, 3)
        self.connect(self.package_lineedit, 
                     QtCore.SIGNAL("textChanged()"), 
                     self.package_changed)

        self.metadata_textedit = QtGui.QTextEdit('', self)
        self.metadata_textedit.setReadOnly(True)
        self.metadata_textedit.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.gridlayout.addWidget(self.metadata_textedit, 1, 1, 1, 3)

        self.glob_lineedit_label = QtGui.QLabel('2.Filter the data: (e.g., *.dat)', self)
        self.gridlayout.addWidget(self.glob_lineedit_label, 2, 0)

        self.glob_lineedit = QtGui.QLineEdit(self)
        self.gridlayout.addWidget(self.glob_lineedit, 2, 1, 1, 2)
        self.connect(self.glob_lineedit, 
                     QtCore.SIGNAL("textChanged()"), 
                     self.glob_changed)

        self.filenames_combobox_label = QtGui.QLabel('3. Select the data file:', self)
        self.gridlayout.addWidget(self.filenames_combobox_label, 3, 0)

        self.filenames_combobox = QtGui.QComboBox(self)
        self.connect(self.filenames_combobox,
                     QtCore.SIGNAL("activated()"), 
                     self.filename_changed)
        self.gridlayout.addWidget(self.filenames_combobox, 3, 1, 1, 3)

        self.setWindowTitle("GetDatabrowser")
        self.setGeometry(250, 200, 350, 550)
        
        self.filename2filepath_mapping = {}
        self.updating = False

        self.notify(node, ("input_modified", 'all'))
        self.notify(node, ("caption_modified", node.get_caption()))
    

    def notify(self, sender, event):
        ''' Update the widgets according to the notification sent by the node ''' 
        
        if event[0] == 'caption_modified':
            self.window().setWindowTitle(event[1])

        if(event[0] == "input_modified"):
            if event[1] == 0:
                self.update_input_package()
                self.update_filenames_combobox()
                self.update_output_filepath()
            elif event[1] == 1:
                self.update_input_glob()
                self.update_filenames_combobox()
                self.update_output_filepath()
            elif event[1] == 2:
                self.update_output_filepath()
            elif event[1] == 'all':
                self.update_input_package()
                self.update_input_glob()
                self.update_filenames_combobox()
                self.update_output_filepath()
        

    @lock_notify
    def update_input_package(self):
        ''' Update the input package text edit '''
        package = self.node.get_input(0)
        if self.updating or package is None: return
        self.updating = True
        self.package_lineedit.setText(package)
        self._update_metadata_textedit(package)
        self.updating = False
        
        
    def _update_metadata_textedit(self, package):
        ''' Update the text editor with the metadata '''
        try:
            metadata = get_metadata(package)
        except:
            self.metadata_textedit.setText("Can not retrieve metainfo from %s." % package)
        else:
            br_length = len('<br/>')
            txt = "<p style=\"color:red\"><b>Package %s metadata</b></p>" % package
            for line in metadata:
                values = line.split(':')
                if len(values) == 2:
                    val1, val2 = values
                else:
                    val1 = ''
                    val2 = line
                if val1 == 'Home-page':
                    txt = '%s<b>%s</b>: <a href="%s">web documentation</a><br/>' % (txt, val1.title(), val2)
                elif val1 == '':
                    txt = txt[:-br_length]
                    txt = '%s %s<br/>' % (txt, val2)
                else:
                    txt = '%s<b>%s</b>: %s<br/>' % (txt, val1 , val2)
    
            self.metadata_textedit.setText(txt)
        
    
    @lock_notify
    def update_input_glob(self):
        ''' Update the glob pattern text edit '''
        globpattern = self.node.get_input(1)
        if self.updating or globpattern is None: return
        self.updating = True
        self.glob_lineedit.setText(globpattern)
        self.updating = False
    
        
    @lock_notify
    def update_filenames_combobox(self):
        ''' Update the combo box with the filenames '''
        package = self.node.get_input(0)
        globpattern = self.node.get_input(1)
        if self.updating or package is None or globpattern is None: return
        self.updating = True
        self.filenames_combobox.clear()
        self.filename2filepath_mapping.clear()
        try:
            __import__(package, fromlist=[''])
        except:
            pass
        else:
            data = systemnodes.get_data(globpattern, package)
            self.filename2filepath_mapping.update(data)
            self.filenames_combobox.addItems(self.filename2filepath_mapping.keys())
        self.updating = False
        
        
    @lock_notify
    def update_output_filepath(self):
        ''' Update the output port '''
        output_filepath = None
        package = self.node.get_input(0)
        globpattern = self.node.get_input(1)
        input_filename = self.node.get_input(2)
        if self.updating or package is None or input_filename is None: return
        self.updating = True
        input_filename_index = self.filenames_combobox.findText(input_filename)
        self.filenames_combobox.setCurrentIndex(input_filename_index)
        output_filepath = self.filename2filepath_mapping.get(input_filename)
        self.node.set_output(0, output_filepath)
        self.updating = False


    def package_changed(self, package):
        ''' Called on package change '''
        self.node.set_input(0, str(package))
        

    def glob_changed(self, globpattern):
        ''' Called on glob change '''
        self.node.set_input(1, str(globpattern))


    def filename_changed(self, filename):
        ''' Called on filename change '''
        self.node.set_input(2, str(filename))
        


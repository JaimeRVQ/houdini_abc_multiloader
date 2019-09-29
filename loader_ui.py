# -*- coding: UTF-8 -*-
"""
Author: Jaime Rivera
File: loader_ui.py
Date: 2019.09.21
Revision: 2019.09.21
Copyright: Copyright Jaime Rivera 2019 | www.jaimervq.com
           The program(s) herein may be used, modified and/or distributed in accordance with the terms and conditions
           stipulated in the Creative Commons license under which the program(s) have been registered. (CC BY-SA 4.0)

Brief:

"""

__author__ = 'Jaime Rivera <jaime.rvq@gmail.com>'
__copyright__ = 'Copyright 2019, Jaime Rivera'
__credits__ = []
__license__ = 'Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)'
__maintainer__ = 'Jaime Rivera'
__email__ = 'jaime.rvq@gmail.com'
__status__ = 'Development'

from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore

import os

import houdini_utils
reload(houdini_utils)


# -------------------------------- CONSTANTS -------------------------------- #

# ICONS PATH
ICONS_PATH = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/') + '/icons/'

# STYLESHEETS
GENERAL_COLOR = 'rgb(50,50,60)'
DARKER_GENERAL_COLOR = 'rgb(25,25,35)'
SCROLLBAR_COLOR = 'rgb(75,75,85)'

BUTTON_STYLE = "QPushButton{{height:{HEIGHT}px; icon-size:{ICON_SIZE}px; font:{FONT_SIZE}px;" \
               "border: 2px solid; border-color: {LIGHT} {DARK} {DARK} {LIGHT}}}" \
               "QPushButton:pressed{{border: 2px solid; border-color: {DARK} {LIGHT} {LIGHT} {DARK}}}" \
               "QPushButton:hover:!pressed{{background:{LIGHT}; border-color: gray {DARK} {DARK} gray}}"

SCROLLBAR_STYLE = "QScrollBar:vertical {{background: {BACKGROUND}; width: 13px;}}" \
                  "QScrollBar::handle:vertical" \
                  "{{border: 0px solid red; border-radius:5px; background: {SCROLLBAR};min-height: 20px;}}" \
                  "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{background: none;}}" \
                  "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{background: none;}}" \
                  "".format(BACKGROUND=GENERAL_COLOR, SCROLLBAR=SCROLLBAR_COLOR)

SMALL_VERT_SCROLLBAR_STYLE = "QScrollBar:vertical {{background: {BACKGROUND}; width: 7px;}}" \
                             "QScrollBar::handle:vertical" \
                             "{{border: 0px solid red; border-radius:3px; background: {SCROLLBAR};min-height: 20px;}}" \
                             "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{background: none;}}" \
                             "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{background: none;}}" \
                             "".format(BACKGROUND=GENERAL_COLOR, SCROLLBAR=SCROLLBAR_COLOR)

SMALL_HORIZ_SCROLLBAR_STYLE = "QScrollBar:horizontal {{background: {BACKGROUND}; height: 7px;}}" \
                              "QScrollBar::handle:horizontal" \
                              "{{border: 0px solid red; border-radius:3px; background: {SCROLLBAR};min-width: 10px;}}" \
                              "QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{background: none;}}" \
                              "QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{background: none;}}" \
                              "".format(BACKGROUND=GENERAL_COLOR, SCROLLBAR=SCROLLBAR_COLOR)

# FONTS
BIG_WHITE_FONT = QtGui.QFont('arial', 16)
SMALL_WHITE_FONT = QtGui.QFont('arial', 10)


# -------------------------------- WIDGET CLASSES -------------------------------- #

class MultiImporter(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        # STYLE
        self.resize(450, 700)
        self.setWindowTitle('ABC multi-loader')
        self.setStyleSheet('background-color:{}; color:white;'.format(GENERAL_COLOR))

        # SUBGROUPS
        self.MAX_SUBGROUPS = 10
        self.total_subgroups = 0

        self.group_columns = 2

        self.groups_row_id = 0
        self.groups_column_id = -1

        # ALREADY CREATED GROUPS
        self.already_created = 0

        # WIDGETS
        self.grid = QtWidgets.QGridLayout()
        self.setLayout(self.grid)
        row = 0

        self.add_group_btn = QtWidgets.QPushButton()
        self.add_group_btn.setText('Add new group')
        self.add_group_btn.setStyleSheet(BUTTON_STYLE.format(LIGHT=SCROLLBAR_COLOR, DARK=DARKER_GENERAL_COLOR,
                                                             HEIGHT=25, ICON_SIZE=10, FONT_SIZE=12))
        self.grid.addWidget(self.add_group_btn, row, 0, 1, 2)
        row += 1

        scroll_area = QtWidgets.QScrollArea()
        self.scrollable_widget = QtWidgets.QWidget()
        self.scrollable_widget.setLayout(QtWidgets.QGridLayout())
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.scrollable_widget)
        scroll_area.setStyleSheet(SCROLLBAR_STYLE)
        self.grid.addWidget(scroll_area, row, 0, 1, 2)
        row += 1

        self.grid.setColumnMinimumWidth(1, 200)
        remap_action = QtWidgets.QAction(self)
        remap_action.setText('Locate an alembic file')
        remap_action.setIcon(QtGui.QIcon(ICONS_PATH + 'file.svg'))
        remap_action.triggered.connect(self.remap_abc_origin)

        for i in range(3):
            self.grid.addWidget(QtWidgets.QLabel('Search abc file:'), row, 0, 1, 1)
            abc_input = AbcLine()
            abc_input.setObjectName('abc_input_' + str(i))
            abc_input.addAction(remap_action)
            abc_input.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
            self.grid.addWidget(abc_input, row, 1, 1, 1)
            row += 1

        self.grid.setRowMinimumHeight(row, 30)
        row += 1

        self.create_all_btn = QtWidgets.QPushButton()
        self.create_all_btn.setText('Create all groups')
        self.create_all_btn.setIcon(QtGui.QIcon(ICONS_PATH + 'geo.svg'))
        self.create_all_btn.setStyleSheet(BUTTON_STYLE.format(LIGHT=SCROLLBAR_COLOR, DARK=DARKER_GENERAL_COLOR,
                                                              HEIGHT=40, ICON_SIZE=32, FONT_SIZE=16))
        self.grid.addWidget(self.create_all_btn, row, 0, 1, 2)

        # INITIALIZE
        self.make_connections()
        self.show()

    def make_connections(self):
        self.add_group_btn.clicked.connect(self.add_new_group)
        self.create_all_btn.clicked.connect(self.create_all_geos)

    def add_new_group(self):
        if self.total_subgroups == self.MAX_SUBGROUPS:
            return

        self.groups_column_id += 1
        if self.groups_column_id < self.group_columns:
            self.scrollable_widget.layout().addWidget(GeoGroup(), self.groups_row_id, self.groups_column_id, 1, 1)
        else:
            self.groups_column_id = 0
            self.groups_row_id += 1
            self.scrollable_widget.layout().addWidget(GeoGroup(), self.groups_row_id, self.groups_column_id, 1, 1)

        self.total_subgroups += 1

    def remap_abc_origin(self):
        target_file = QtWidgets.QFileDialog.getOpenFileName(self, 'Enter new file path', '', 'Alembic files (*.abc)')
        if target_file[0]:
            qline = self.focusWidget()
            qline.setText(target_file[0])

    def create_all_geos(self):
        for i in range(10):
            item = self.scrollable_widget.layout().itemAt(i)
            if item:
                group = item.widget()
                group.create_a_geo_group(self.already_created)
                self.already_created += 1


class AbcLine(QtWidgets.QLineEdit):

    def __init__(self):
        QtWidgets.QLineEdit.__init__(self)
        self.setReadOnly(True)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)

    def mousePressEvent(self, *args, **kwargs):
        self.selectAll()
        QtWidgets.QLineEdit.mousePressEvent(self, *args, **kwargs)

    def mouseMoveEvent(self, *args, **kwargs):
        pass

    def dropEvent(self, event):
        if isinstance(event.source(), QtWidgets.QLineEdit) or isinstance(event.source(), AbcLine):
            self.setText(event.source().text())


class GeoGroup(QtWidgets.QFrame):
    counter = 0

    def __init__(self):
        GeoGroup.counter += 1
        QtWidgets.QFrame.__init__(self)

        # ABSTRACT PROPERTIES
        self.valid_paths = {}

        # WIDGET
        self.setObjectName('GeoGroup')
        self.setStyleSheet('QFrame#GeoGroup{border:1px solid gray; border-radius:5px;}')
        self.setMinimumHeight(200)

        self.setAcceptDrops(True)

        self.group_box = QtWidgets.QVBoxLayout()
        self.setLayout(self.group_box)

        self.group_name = QtWidgets.QLineEdit()
        self.group_name.setAcceptDrops(False)
        self.group_name.setText('Geo_{}'.format(GeoGroup.counter))
        self.group_name.setAlignment(QtCore.Qt.AlignCenter)
        self.group_name.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp('[A-Za-z]+[A-Za-z_0-9]*')))
        self.group_name.setStyleSheet('border:none')
        self.group_box.addWidget(self.group_name)

        self.abcs_list = QtWidgets.QListWidget()
        self.abcs_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.abcs_list.setStyleSheet('QListWidget{border:none; font-size:16px;} ' +
                                     SMALL_VERT_SCROLLBAR_STYLE + SMALL_HORIZ_SCROLLBAR_STYLE)

        self.group_box.addWidget(self.abcs_list)
        self.group_box.setStretch(1, 100)

        self.check_create = QtWidgets.QCheckBox()
        self.check_create.setChecked(True)
        self.check_create.setText('Create')
        self.check_create.setToolTip('If unchecked, this group will not be created')
        self.group_box.addWidget(self.check_create)

        # ACTIONS
        multi_add_action = QtWidgets.QAction(self)
        multi_add_action.setText('Add multiple alembic paths')
        multi_add_action.setIcon(QtGui.QIcon(ICONS_PATH + 'file.svg'))
        multi_add_action.triggered.connect(self.multi_add)
        self.addAction(multi_add_action)

        remove_selected_action = QtWidgets.QAction(self)
        remove_selected_action.setText('Remove selected')
        remove_selected_action.setIcon(QtGui.QIcon(ICONS_PATH + 'remove.svg'))
        remove_selected_action.triggered.connect(self.remove_selected)
        self.addAction(remove_selected_action)

        clear_all_action = QtWidgets.QAction(self)
        clear_all_action.setText('Clear all paths')
        clear_all_action.setIcon(QtGui.QIcon(ICONS_PATH + 'clear.svg'))
        clear_all_action.triggered.connect(self.clear_all)
        self.addAction(clear_all_action)
        self.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

    def multi_add(self):
        multiple_paths = \
        QtWidgets.QFileDialog.getOpenFileNames(self, 'Select alembic files', '', 'Alembic files (*.abc)')[0]

        if multiple_paths:
            for full_path in multiple_paths:
                self.add_a_path(full_path)

    def remove_selected(self):
        selected_items = self.abcs_list.selectedItems()

        for item in selected_items:
            abc = item.text()
            row = self.abcs_list.row(item)
            self.abcs_list.takeItem(row)
            self.valid_paths.pop(abc)

    def clear_all(self):
        self.abcs_list.clear()
        self.valid_paths.clear()

    def dropEvent(self, event):
        mime_data = event.mimeData()

        if mime_data.hasText() and os.path.exists(mime_data.text()):
            self.add_a_path(mime_data.text())

    def add_a_path(self, full_path):
        abc_name = full_path.split('/')[-1]
        if abc_name in self.valid_paths:
            return

        new_item = QtWidgets.QListWidgetItem()
        new_item.setText(abc_name)

        self.abcs_list.addItem(new_item)

        self.valid_paths[abc_name] = full_path

    def create_a_geo_group(self, x_id):
        if not self.valid_paths or not self.check_create.isChecked(): return

        output_dict = {'name': self.group_name.text(),
                       'x_id': x_id,
                       'abc_paths': self.valid_paths}
        houdini_utils.create_geo(output_dict)


# -------------------------------- REPATH WIDGET/DIALOG -------------------------------- #

class RepathTable(QtWidgets.QDialog):

    def __init__(self, abc_nodes_and_paths):
        QtWidgets.QDialog.__init__(self)

        self.setWindowTitle('Redefine abc paths')
        self.resize(950, 400)
        self.setStyleSheet('background-color:{}; color:white;'.format(GENERAL_COLOR))

        ly = QtWidgets.QVBoxLayout()
        self.setLayout(ly)

        self.repaths_table = QtWidgets.QTableWidget()
        self.repaths_table.verticalHeader().setVisible(False)
        self.repaths_table.insertColumn(0)
        self.repaths_table.insertColumn(0)
        self.repaths_table.setHorizontalHeaderLabels(['Node', 'Abc path'])
        header = self.repaths_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        ly.addWidget(self.repaths_table)

        for node in abc_nodes_and_paths:
            self.repaths_table.insertRow(0)
            self.repaths_table.setRowHeight(0, 30)

            node_item = QtWidgets.QLabel()
            node_item.setText('  ' + node + '  ')
            node_item.setFont(SMALL_WHITE_FONT)
            self.repaths_table.setCellWidget(0, 0, node_item)

            path_item = AbcRepathLine()
            path_item.setText(abc_nodes_and_paths[node])
            path_item.setFont(BIG_WHITE_FONT)
            self.repaths_table.setCellWidget(0, 1, path_item)

        self.repath_all_btn = QtWidgets.QPushButton()
        self.repath_all_btn.setText('Repath all')
        self.repath_all_btn.setStyleSheet(BUTTON_STYLE.format(LIGHT=SCROLLBAR_COLOR, DARK=DARKER_GENERAL_COLOR,
                                                              HEIGHT=30, ICON_SIZE=25, FONT_SIZE=14))
        self.repath_all_btn.clicked.connect(self.launch_reassignations)
        ly.addWidget(self.repath_all_btn)

        self.exec_()

    def remap_abc_origin(self, row):
        target_file = QtWidgets.QFileDialog.getOpenFileName(self, 'Enter new file path', '', 'Alembic files (*.abc)')
        if target_file[0]:
            item = self.repaths_table.cellWidget(row, 1)
            item.setText(target_file[0])

    def launch_reassignations(self):
        new_abc_nodes_and_paths = {}

        for i in range(self.repaths_table.rowCount()):
            node = self.repaths_table.cellWidget(i, 0).text().strip()
            new_path = self.repaths_table.cellWidget(i, 1).text().strip()

            new_abc_nodes_and_paths[node] = new_path

        houdini_utils.set_multiple_filenames(new_abc_nodes_and_paths)
        self.close()


class AbcRepathLine(QtWidgets.QLineEdit):

    def __init__(self):
        QtWidgets.QLineEdit.__init__(self)
        self.setReadOnly(True)

        self.setStyleSheet('border:none')

        remap_action = QtWidgets.QAction(self)
        remap_action.setText('Redefine this alembic path')
        remap_action.setIcon(QtGui.QIcon(ICONS_PATH + 'file.svg'))
        remap_action.triggered.connect(self.redefine_abc_path)

        self.addAction(remap_action)
        self.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

    def redefine_abc_path(self):
        target_file = QtWidgets.QFileDialog.getOpenFileName(self, 'Enter new file path', '', 'Alembic files (*.abc)')
        if target_file[0]:
            self.setText(target_file[0])
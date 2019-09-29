# -*- coding: UTF-8 -*-
"""
Author: Jaime Rivera
File: houdini_utils.py
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


import os

import hou

# -------------------------------- CONSTANTS -------------------------------- #

OBJ_NODE = 'obj/'

REPATH_WIDGET_SCRIPT ='''
from houdini_abc_multiloader import houdini_utils
reload(houdini_utils)
houdini_utils.launch_repaths(hou.pwd().path())
'''

# -------------------------------- METHODS -------------------------------- #

def create_geo(geo_dict):
    group_name = geo_dict['name']
    obj = hou.node(OBJ_NODE)
    g = obj.createNode('geo', group_name)
    g.setPosition((geo_dict['x_id']*3, 0))
    add_repath_button(g.path())

    merge = g.createNode('merge', 'MERGE_{}'.format(group_name))
    merge.setPosition((0, -3))

    abc_paths = geo_dict['abc_paths']
    count = 0
    for abc in abc_paths:
        geo_name = os.path.splitext(abc)[0]
        abc_node = g.createNode('alembic', geo_name)
        abc_node.setParms({'fileName' : abc_paths[abc]})
        abc_node.setPosition((count*2.5, 0))

        merge.setInput(count, abc_node)

        count +=1

def add_repath_button(node_path):
    geo_node = hou.node(node_path)

    b = hou.ButtonParmTemplate('repath_abcs', 'Repath_abcs')
    b.setScriptCallbackLanguage(hou.scriptLanguage.Python)
    b.setScriptCallback(REPATH_WIDGET_SCRIPT.format(node_path))

    geo_node.addSpareParmFolder('REPATH ABCS')
    geo_node.addSpareParmTuple(b, ('REPATH ABCS',))

def launch_repaths(node_path):
    abc_nodes_and_paths = {}

    this_node = hou.node(node_path)
    children = this_node.children()

    for c in children:
        if c.type().name() == 'alembic':
            abc_nodes_and_paths[c.path()] = c.parm('fileName').eval()

    import loader_ui
    reload(loader_ui)

    loader_ui.RepathTable(abc_nodes_and_paths)

def set_multiple_filenames(nodes_and_paths):
    for node in nodes_and_paths:
        print node + '/fileName'
        parm = hou.parm(node + '/fileName')
        parm.set(nodes_and_paths[node])
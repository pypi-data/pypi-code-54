#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  4 14:33:12 2020

@author: Rajiv Sambasivan
"""

from amlnx_adapter.graph_params import GraphParams
from amlnx_adapter.arangoDB_networkx_arango_adapter import ArangoDB_Networkx_Adapter

def test_conn():
    gp = GraphParams()
    cfg = {}
    cfg[gp.DB_USER_NAME] = "TUThteu92kx6d6vy5bv8hjdgi"
    cfg[gp.DB_NAME] = "TUTunnln6vscrstef2r6mz5b"
    cfg[gp.DB_CONN_PROTOCOL] = 'https'
    cfg[gp.DB_PASSWORD] = 'TUT2p6okjbkwd5ygusspxc9gl'
    cfg[gp.DB_SERVICE_HOST] = '5904e8d8a65f.arangodb.cloud'
    cfg[gp.DB_VERTEX_COL] = {'account': {'Balance', 'account_type', 'customer_id', 'rank'},\
       'bank': {'Country', 'Id', 'bank_id', 'bank_name'},\
       'branch':{'City', 'Country', 'Id', 'bank_id', 'branch_id', 'branch_name'},\
       'Class':{'concrete', 'label', 'name'},\
       'customer': {'Name', 'Sex', 'Ssn', 'rank'}}
    cfg[gp.DB_EDGE_COL] = {'accountHolder': {'_from', '_to'},\
       'Relationship': {'_from', '_to', 'label', 'name', 'relationshipType'},\
       'transaction': {'_from', '_to'}}
    cfg[gp.DB_DATA_QUERY] = 'FOR ratings in Ratings  return {''user'': ratings._from,\
    ''movie'': ratings._to, ''rating'': ratings.ratings}'
    ma = ArangoDB_Networkx_Adapter(graph_config = cfg)
    
    return ma
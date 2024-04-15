
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'IRC_PART PASSWORD PORT_PART SLASH TEXT_PART\n    main : IRC_PART TEXT_PART after_server\n    \n    after_server : PORT_PART after_port\n                 | after_port\n    \n    after_port :\n               | SLASH after_slash\n    \n    after_slash :\n                | TEXT_PART PASSWORD\n                | PASSWORD\n                | TEXT_PART\n    '
    
_lr_action_items = {'IRC_PART':([0,],[2,]),'$end':([1,3,4,5,6,7,8,9,10,11,12,],[0,-4,-1,-4,-3,-6,-2,-5,-9,-8,-7,]),'TEXT_PART':([2,7,],[3,10,]),'PORT_PART':([3,],[5,]),'SLASH':([3,5,],[7,7,]),'PASSWORD':([7,10,],[11,12,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'main':([0,],[1,]),'after_server':([3,],[4,]),'after_port':([3,5,],[6,8,]),'after_slash':([7,],[9,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> main","S'",1,None,None,None),
  ('main -> IRC_PART TEXT_PART after_server','main',3,'p_main','lexer.py',41),
  ('after_server -> PORT_PART after_port','after_server',2,'p_after_server','lexer.py',47),
  ('after_server -> after_port','after_server',1,'p_after_server','lexer.py',48),
  ('after_port -> <empty>','after_port',0,'p_after_port','lexer.py',53),
  ('after_port -> SLASH after_slash','after_port',2,'p_after_port','lexer.py',54),
  ('after_slash -> <empty>','after_slash',0,'p_after_slash','lexer.py',59),
  ('after_slash -> TEXT_PART PASSWORD','after_slash',2,'p_after_slash','lexer.py',60),
  ('after_slash -> PASSWORD','after_slash',1,'p_after_slash','lexer.py',61),
  ('after_slash -> TEXT_PART','after_slash',1,'p_after_slash','lexer.py',62),
]

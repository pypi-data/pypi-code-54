# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: huajiweb/proto/Widget.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='huajiweb/proto/Widget.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=b'\n\x1cstreamlit/proto/Widget.proto\"-\n\x0cWidgetStates\x12\x1d\n\x07widgets\x18\x01 \x03(\x0b\x32\x0c.WidgetState\"\xe5\x01\n\x0bWidgetState\x12\n\n\x02id\x18\x01 \x01(\t\x12\x17\n\rtrigger_value\x18\x02 \x01(\x08H\x00\x12\x14\n\nbool_value\x18\x03 \x01(\x08H\x00\x12\x15\n\x0b\x66loat_value\x18\x04 \x01(\x01H\x00\x12\x13\n\tint_value\x18\x05 \x01(\x12H\x00\x12\x16\n\x0cstring_value\x18\x06 \x01(\tH\x00\x12$\n\x0fint_array_value\x18\x08 \x01(\x0b\x32\t.IntArrayH\x00\x12(\n\x11\x66loat_array_value\x18\x07 \x01(\x0b\x32\x0b.FloatArrayH\x00\x42\x07\n\x05value\"\x1b\n\nFloatArray\x12\r\n\x05value\x18\x01 \x03(\x01\"\x19\n\x08IntArray\x12\r\n\x05value\x18\x01 \x03(\x12\x62\x06proto3'
)




_WIDGETSTATES = _descriptor.Descriptor(
  name='WidgetStates',
  full_name='WidgetStates',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='widgets', full_name='WidgetStates.widgets', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=32,
  serialized_end=77,
)


_WIDGETSTATE = _descriptor.Descriptor(
  name='WidgetState',
  full_name='WidgetState',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='WidgetState.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='trigger_value', full_name='WidgetState.trigger_value', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='bool_value', full_name='WidgetState.bool_value', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='float_value', full_name='WidgetState.float_value', index=3,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='int_value', full_name='WidgetState.int_value', index=4,
      number=5, type=18, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='string_value', full_name='WidgetState.string_value', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='int_array_value', full_name='WidgetState.int_array_value', index=6,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='float_array_value', full_name='WidgetState.float_array_value', index=7,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='value', full_name='WidgetState.value',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=80,
  serialized_end=309,
)


_FLOATARRAY = _descriptor.Descriptor(
  name='FloatArray',
  full_name='FloatArray',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='value', full_name='FloatArray.value', index=0,
      number=1, type=1, cpp_type=5, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=311,
  serialized_end=338,
)


_INTARRAY = _descriptor.Descriptor(
  name='IntArray',
  full_name='IntArray',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='value', full_name='IntArray.value', index=0,
      number=1, type=18, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=340,
  serialized_end=365,
)

_WIDGETSTATES.fields_by_name['widgets'].message_type = _WIDGETSTATE
_WIDGETSTATE.fields_by_name['int_array_value'].message_type = _INTARRAY
_WIDGETSTATE.fields_by_name['float_array_value'].message_type = _FLOATARRAY
_WIDGETSTATE.oneofs_by_name['value'].fields.append(
  _WIDGETSTATE.fields_by_name['trigger_value'])
_WIDGETSTATE.fields_by_name['trigger_value'].containing_oneof = _WIDGETSTATE.oneofs_by_name['value']
_WIDGETSTATE.oneofs_by_name['value'].fields.append(
  _WIDGETSTATE.fields_by_name['bool_value'])
_WIDGETSTATE.fields_by_name['bool_value'].containing_oneof = _WIDGETSTATE.oneofs_by_name['value']
_WIDGETSTATE.oneofs_by_name['value'].fields.append(
  _WIDGETSTATE.fields_by_name['float_value'])
_WIDGETSTATE.fields_by_name['float_value'].containing_oneof = _WIDGETSTATE.oneofs_by_name['value']
_WIDGETSTATE.oneofs_by_name['value'].fields.append(
  _WIDGETSTATE.fields_by_name['int_value'])
_WIDGETSTATE.fields_by_name['int_value'].containing_oneof = _WIDGETSTATE.oneofs_by_name['value']
_WIDGETSTATE.oneofs_by_name['value'].fields.append(
  _WIDGETSTATE.fields_by_name['string_value'])
_WIDGETSTATE.fields_by_name['string_value'].containing_oneof = _WIDGETSTATE.oneofs_by_name['value']
_WIDGETSTATE.oneofs_by_name['value'].fields.append(
  _WIDGETSTATE.fields_by_name['int_array_value'])
_WIDGETSTATE.fields_by_name['int_array_value'].containing_oneof = _WIDGETSTATE.oneofs_by_name['value']
_WIDGETSTATE.oneofs_by_name['value'].fields.append(
  _WIDGETSTATE.fields_by_name['float_array_value'])
_WIDGETSTATE.fields_by_name['float_array_value'].containing_oneof = _WIDGETSTATE.oneofs_by_name['value']
DESCRIPTOR.message_types_by_name['WidgetStates'] = _WIDGETSTATES
DESCRIPTOR.message_types_by_name['WidgetState'] = _WIDGETSTATE
DESCRIPTOR.message_types_by_name['FloatArray'] = _FLOATARRAY
DESCRIPTOR.message_types_by_name['IntArray'] = _INTARRAY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

WidgetStates = _reflection.GeneratedProtocolMessageType('WidgetStates', (_message.Message,), {
  'DESCRIPTOR' : _WIDGETSTATES,
  '__module__' : 'huajiweb.proto.Widget_pb2'
  # @@protoc_insertion_point(class_scope:WidgetStates)
  })
_sym_db.RegisterMessage(WidgetStates)

WidgetState = _reflection.GeneratedProtocolMessageType('WidgetState', (_message.Message,), {
  'DESCRIPTOR' : _WIDGETSTATE,
  '__module__' : 'huajiweb.proto.Widget_pb2'
  # @@protoc_insertion_point(class_scope:WidgetState)
  })
_sym_db.RegisterMessage(WidgetState)

FloatArray = _reflection.GeneratedProtocolMessageType('FloatArray', (_message.Message,), {
  'DESCRIPTOR' : _FLOATARRAY,
  '__module__' : 'huajiweb.proto.Widget_pb2'
  # @@protoc_insertion_point(class_scope:FloatArray)
  })
_sym_db.RegisterMessage(FloatArray)

IntArray = _reflection.GeneratedProtocolMessageType('IntArray', (_message.Message,), {
  'DESCRIPTOR' : _INTARRAY,
  '__module__' : 'huajiweb.proto.Widget_pb2'
  # @@protoc_insertion_point(class_scope:IntArray)
  })
_sym_db.RegisterMessage(IntArray)


# @@protoc_insertion_point(module_scope)

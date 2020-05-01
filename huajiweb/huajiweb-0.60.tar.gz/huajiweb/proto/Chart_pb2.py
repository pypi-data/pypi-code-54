# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: huajiweb/proto/Chart.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from huajiweb.proto import DataFrame_pb2 as huajiweb_dot_proto_dot_DataFrame__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='huajiweb/proto/Chart.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=b'\n\x1bhuajiweb/proto/Chart.proto\x1a\x1fhuajiweb/proto/DataFrame.proto\"\x92\x01\n\x05\x43hart\x12\x0c\n\x04type\x18\x01 \x01(\t\x12\x18\n\x04\x64\x61ta\x18\x02 \x01(\x0b\x32\n.DataFrame\x12\r\n\x05width\x18\x03 \x01(\r\x12\x0e\n\x06height\x18\x04 \x01(\r\x12#\n\ncomponents\x18\x05 \x03(\x0b\x32\x0f.ChartComponent\x12\x1d\n\x05props\x18\x06 \x03(\x0b\x32\x0e.ChartProperty\"=\n\x0e\x43hartComponent\x12\x0c\n\x04type\x18\x01 \x01(\t\x12\x1d\n\x05props\x18\x02 \x03(\x0b\x32\x0e.ChartProperty\"+\n\rChartProperty\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\tb\x06proto3'
  ,
  dependencies=[huajiweb_dot_proto_dot_DataFrame__pb2.DESCRIPTOR,])




_CHART = _descriptor.Descriptor(
  name='Chart',
  full_name='Chart',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='Chart.type', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='data', full_name='Chart.data', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='width', full_name='Chart.width', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='height', full_name='Chart.height', index=3,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='components', full_name='Chart.components', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='props', full_name='Chart.props', index=5,
      number=6, type=11, cpp_type=10, label=3,
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
  serialized_start=65,
  serialized_end=211,
)


_CHARTCOMPONENT = _descriptor.Descriptor(
  name='ChartComponent',
  full_name='ChartComponent',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='ChartComponent.type', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='props', full_name='ChartComponent.props', index=1,
      number=2, type=11, cpp_type=10, label=3,
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
  serialized_start=213,
  serialized_end=274,
)


_CHARTPROPERTY = _descriptor.Descriptor(
  name='ChartProperty',
  full_name='ChartProperty',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='ChartProperty.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='ChartProperty.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
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
  serialized_start=276,
  serialized_end=319,
)

_CHART.fields_by_name['data'].message_type = huajiweb_dot_proto_dot_DataFrame__pb2._DATAFRAME
_CHART.fields_by_name['components'].message_type = _CHARTCOMPONENT
_CHART.fields_by_name['props'].message_type = _CHARTPROPERTY
_CHARTCOMPONENT.fields_by_name['props'].message_type = _CHARTPROPERTY
DESCRIPTOR.message_types_by_name['Chart'] = _CHART
DESCRIPTOR.message_types_by_name['ChartComponent'] = _CHARTCOMPONENT
DESCRIPTOR.message_types_by_name['ChartProperty'] = _CHARTPROPERTY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Chart = _reflection.GeneratedProtocolMessageType('Chart', (_message.Message,), {
  'DESCRIPTOR' : _CHART,
  '__module__' : 'huajiweb.proto.Chart_pb2'
  # @@protoc_insertion_point(class_scope:Chart)
  })
_sym_db.RegisterMessage(Chart)

ChartComponent = _reflection.GeneratedProtocolMessageType('ChartComponent', (_message.Message,), {
  'DESCRIPTOR' : _CHARTCOMPONENT,
  '__module__' : 'huajiweb.proto.Chart_pb2'
  # @@protoc_insertion_point(class_scope:ChartComponent)
  })
_sym_db.RegisterMessage(ChartComponent)

ChartProperty = _reflection.GeneratedProtocolMessageType('ChartProperty', (_message.Message,), {
  'DESCRIPTOR' : _CHARTPROPERTY,
  '__module__' : 'huajiweb.proto.Chart_pb2'
  # @@protoc_insertion_point(class_scope:ChartProperty)
  })
_sym_db.RegisterMessage(ChartProperty)


# @@protoc_insertion_point(module_scope)

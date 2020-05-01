# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: huajiweb/proto/Delta.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from huajiweb.proto import Element_pb2 as huajiweb_dot_proto_dot_Element__pb2
from huajiweb.proto import NamedDataSet_pb2 as huajiweb_dot_proto_dot_NamedDataSet__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='huajiweb/proto/Delta.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=b'\n\x1bhuajiweb/proto/Delta.proto\x1a\x1dhuajiweb/proto/Element.proto\x1a\"huajiweb/proto/NamedDataSet.proto\"h\n\x05\x44\x65lta\x12\x1f\n\x0bnew_element\x18\x03 \x01(\x0b\x32\x08.ElementH\x00\x12\x13\n\tnew_block\x18\x04 \x01(\x08H\x00\x12!\n\x08\x61\x64\x64_rows\x18\x05 \x01(\x0b\x32\r.NamedDataSetH\x00\x42\x06\n\x04typeb\x06proto3'
  ,
  dependencies=[huajiweb_dot_proto_dot_Element__pb2.DESCRIPTOR,huajiweb_dot_proto_dot_NamedDataSet__pb2.DESCRIPTOR,])




_DELTA = _descriptor.Descriptor(
  name='Delta',
  full_name='Delta',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='new_element', full_name='Delta.new_element', index=0,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='new_block', full_name='Delta.new_block', index=1,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='add_rows', full_name='Delta.add_rows', index=2,
      number=5, type=11, cpp_type=10, label=1,
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
      name='type', full_name='Delta.type',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=98,
  serialized_end=202,
)

_DELTA.fields_by_name['new_element'].message_type = huajiweb_dot_proto_dot_Element__pb2._ELEMENT
_DELTA.fields_by_name['add_rows'].message_type = huajiweb_dot_proto_dot_NamedDataSet__pb2._NAMEDDATASET
_DELTA.oneofs_by_name['type'].fields.append(
  _DELTA.fields_by_name['new_element'])
_DELTA.fields_by_name['new_element'].containing_oneof = _DELTA.oneofs_by_name['type']
_DELTA.oneofs_by_name['type'].fields.append(
  _DELTA.fields_by_name['new_block'])
_DELTA.fields_by_name['new_block'].containing_oneof = _DELTA.oneofs_by_name['type']
_DELTA.oneofs_by_name['type'].fields.append(
  _DELTA.fields_by_name['add_rows'])
_DELTA.fields_by_name['add_rows'].containing_oneof = _DELTA.oneofs_by_name['type']
DESCRIPTOR.message_types_by_name['Delta'] = _DELTA
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Delta = _reflection.GeneratedProtocolMessageType('Delta', (_message.Message,), {
  'DESCRIPTOR' : _DELTA,
  '__module__' : 'huajiweb.proto.Delta_pb2'
  # @@protoc_insertion_point(class_scope:Delta)
  })
_sym_db.RegisterMessage(Delta)


# @@protoc_insertion_point(module_scope)

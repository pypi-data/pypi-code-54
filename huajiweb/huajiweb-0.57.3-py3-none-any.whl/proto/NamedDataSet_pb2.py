# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: huajiweb/proto/NamedDataSet.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from huajiweb.proto import DataFrame_pb2 as streamlit_dot_proto_dot_DataFrame__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='huajiweb/proto/NamedDataSet.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=b'\n\"huajiweb/proto/NamedDataSet.proto\x1a\x1fstreamlit/proto/DataFrame.proto\"H\n\x0cNamedDataSet\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x10\n\x08has_name\x18\x03 \x01(\x08\x12\x18\n\x04\x64\x61ta\x18\x02 \x01(\x0b\x32\n.DataFrameb\x06proto3'
  ,
  dependencies=[streamlit_dot_proto_dot_DataFrame__pb2.DESCRIPTOR,])




_NAMEDDATASET = _descriptor.Descriptor(
  name='NamedDataSet',
  full_name='NamedDataSet',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='NamedDataSet.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='has_name', full_name='NamedDataSet.has_name', index=1,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='data', full_name='NamedDataSet.data', index=2,
      number=2, type=11, cpp_type=10, label=1,
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
  ],
  serialized_start=71,
  serialized_end=143,
)

_NAMEDDATASET.fields_by_name['data'].message_type = streamlit_dot_proto_dot_DataFrame__pb2._DATAFRAME
DESCRIPTOR.message_types_by_name['NamedDataSet'] = _NAMEDDATASET
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

NamedDataSet = _reflection.GeneratedProtocolMessageType('NamedDataSet', (_message.Message,), {
  'DESCRIPTOR' : _NAMEDDATASET,
  '__module__' : 'huajiweb.proto.NamedDataSet_pb2'
  # @@protoc_insertion_point(class_scope:NamedDataSet)
  })
_sym_db.RegisterMessage(NamedDataSet)


# @@protoc_insertion_point(module_scope)

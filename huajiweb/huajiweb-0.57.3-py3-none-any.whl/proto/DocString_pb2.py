# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: huajiweb/proto/DocString.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='huajiweb/proto/DocString.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=b'\n\x1fstreamlit/proto/DocString.proto\"^\n\tDocString\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0e\n\x06module\x18\x02 \x01(\t\x12\x12\n\ndoc_string\x18\x03 \x01(\t\x12\x0c\n\x04type\x18\x04 \x01(\t\x12\x11\n\tsignature\x18\x05 \x01(\tb\x06proto3'
)




_DOCSTRING = _descriptor.Descriptor(
  name='DocString',
  full_name='DocString',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='DocString.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='module', full_name='DocString.module', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='doc_string', full_name='DocString.doc_string', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type', full_name='DocString.type', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='signature', full_name='DocString.signature', index=4,
      number=5, type=9, cpp_type=9, label=1,
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
  serialized_start=35,
  serialized_end=129,
)

DESCRIPTOR.message_types_by_name['DocString'] = _DOCSTRING
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

DocString = _reflection.GeneratedProtocolMessageType('DocString', (_message.Message,), {
  'DESCRIPTOR' : _DOCSTRING,
  '__module__' : 'huajiweb.proto.DocString_pb2'
  # @@protoc_insertion_point(class_scope:DocString)
  })
_sym_db.RegisterMessage(DocString)


# @@protoc_insertion_point(module_scope)

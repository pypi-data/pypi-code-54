# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: huajiweb/proto/Json.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='huajiweb/proto/Json.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=b'\n\x1ahuajiweb/proto/Json.proto\"\x14\n\x04Json\x12\x0c\n\x04\x62ody\x18\x01 \x01(\tb\x06proto3'
)




_JSON = _descriptor.Descriptor(
  name='Json',
  full_name='Json',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='body', full_name='Json.body', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  serialized_start=30,
  serialized_end=50,
)

DESCRIPTOR.message_types_by_name['Json'] = _JSON
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Json = _reflection.GeneratedProtocolMessageType('Json', (_message.Message,), {
  'DESCRIPTOR' : _JSON,
  '__module__' : 'huajiweb.proto.Json_pb2'
  # @@protoc_insertion_point(class_scope:Json)
  })
_sym_db.RegisterMessage(Json)


# @@protoc_insertion_point(module_scope)

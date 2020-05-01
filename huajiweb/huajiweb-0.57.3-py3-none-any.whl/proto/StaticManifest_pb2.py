# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: huajiweb/proto/StaticManifest.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='huajiweb/proto/StaticManifest.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=b'\n$huajiweb/proto/StaticManifest.proto\"\x9a\x02\n\x0eStaticManifest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x14\n\x0cnum_messages\x18\x02 \x01(\r\x12\x33\n\rserver_status\x18\x03 \x01(\x0e\x32\x1c.StaticManifest.ServerStatus\x12!\n\x19\x63onfigured_server_address\x18\x04 \x01(\t\x12\x1a\n\x12\x65xternal_server_ip\x18\x05 \x01(\t\x12\x1a\n\x12internal_server_ip\x18\x06 \x01(\t\x12\x13\n\x0bserver_port\x18\x07 \x01(\r\x12\x18\n\x10server_base_path\x18\x08 \x01(\t\"%\n\x0cServerStatus\x12\x0b\n\x07RUNNING\x10\x00\x12\x08\n\x04\x44ONE\x10\x01\x62\x06proto3'
)



_STATICMANIFEST_SERVERSTATUS = _descriptor.EnumDescriptor(
  name='ServerStatus',
  full_name='StaticManifest.ServerStatus',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='RUNNING', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DONE', index=1, number=1,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=286,
  serialized_end=323,
)
_sym_db.RegisterEnumDescriptor(_STATICMANIFEST_SERVERSTATUS)


_STATICMANIFEST = _descriptor.Descriptor(
  name='StaticManifest',
  full_name='StaticManifest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='StaticManifest.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='num_messages', full_name='StaticManifest.num_messages', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='server_status', full_name='StaticManifest.server_status', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='configured_server_address', full_name='StaticManifest.configured_server_address', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='external_server_ip', full_name='StaticManifest.external_server_ip', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='internal_server_ip', full_name='StaticManifest.internal_server_ip', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='server_port', full_name='StaticManifest.server_port', index=6,
      number=7, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='server_base_path', full_name='StaticManifest.server_base_path', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _STATICMANIFEST_SERVERSTATUS,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=41,
  serialized_end=323,
)

_STATICMANIFEST.fields_by_name['server_status'].enum_type = _STATICMANIFEST_SERVERSTATUS
_STATICMANIFEST_SERVERSTATUS.containing_type = _STATICMANIFEST
DESCRIPTOR.message_types_by_name['StaticManifest'] = _STATICMANIFEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

StaticManifest = _reflection.GeneratedProtocolMessageType('StaticManifest', (_message.Message,), {
  'DESCRIPTOR' : _STATICMANIFEST,
  '__module__' : 'huajiweb.proto.StaticManifest_pb2'
  # @@protoc_insertion_point(class_scope:StaticManifest)
  })
_sym_db.RegisterMessage(StaticManifest)


# @@protoc_insertion_point(module_scope)

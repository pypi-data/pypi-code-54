# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: feast/core/FeatureSet.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from feast.types import Value_pb2 as feast_dot_types_dot_Value__pb2
from feast.core import Source_pb2 as feast_dot_core_dot_Source__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='feast/core/FeatureSet.proto',
  package='feast.core',
  syntax='proto3',
  serialized_options=_b('\n\nfeast.coreB\017FeatureSetProtoZ/github.com/gojek/feast/sdk/go/protos/feast/core'),
  serialized_pb=_b('\n\x1b\x66\x65\x61st/core/FeatureSet.proto\x12\nfeast.core\x1a\x17\x66\x65\x61st/types/Value.proto\x1a\x17\x66\x65\x61st/core/Source.proto\x1a\x1egoogle/protobuf/duration.proto\"\xd4\x01\n\x0e\x46\x65\x61tureSetSpec\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\x05\x12(\n\x08\x65ntities\x18\x03 \x03(\x0b\x32\x16.feast.core.EntitySpec\x12)\n\x08\x66\x65\x61tures\x18\x04 \x03(\x0b\x32\x17.feast.core.FeatureSpec\x12*\n\x07max_age\x18\x05 \x01(\x0b\x32\x19.google.protobuf.Duration\x12\"\n\x06source\x18\x06 \x01(\x0b\x32\x12.feast.core.Source\"K\n\nEntitySpec\x12\x0c\n\x04name\x18\x01 \x01(\t\x12/\n\nvalue_type\x18\x02 \x01(\x0e\x32\x1b.feast.types.ValueType.Enum\"L\n\x0b\x46\x65\x61tureSpec\x12\x0c\n\x04name\x18\x01 \x01(\t\x12/\n\nvalue_type\x18\x02 \x01(\x0e\x32\x1b.feast.types.ValueType.EnumBN\n\nfeast.coreB\x0f\x46\x65\x61tureSetProtoZ/github.com/gojek/feast/sdk/go/protos/feast/coreb\x06proto3')
  ,
  dependencies=[feast_dot_types_dot_Value__pb2.DESCRIPTOR,feast_dot_core_dot_Source__pb2.DESCRIPTOR,google_dot_protobuf_dot_duration__pb2.DESCRIPTOR,])




_FEATURESETSPEC = _descriptor.Descriptor(
  name='FeatureSetSpec',
  full_name='feast.core.FeatureSetSpec',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='feast.core.FeatureSetSpec.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='version', full_name='feast.core.FeatureSetSpec.version', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='entities', full_name='feast.core.FeatureSetSpec.entities', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='features', full_name='feast.core.FeatureSetSpec.features', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='max_age', full_name='feast.core.FeatureSetSpec.max_age', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='source', full_name='feast.core.FeatureSetSpec.source', index=5,
      number=6, type=11, cpp_type=10, label=1,
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
  serialized_start=126,
  serialized_end=338,
)


_ENTITYSPEC = _descriptor.Descriptor(
  name='EntitySpec',
  full_name='feast.core.EntitySpec',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='feast.core.EntitySpec.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value_type', full_name='feast.core.EntitySpec.value_type', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
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
  serialized_end=415,
)


_FEATURESPEC = _descriptor.Descriptor(
  name='FeatureSpec',
  full_name='feast.core.FeatureSpec',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='feast.core.FeatureSpec.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value_type', full_name='feast.core.FeatureSpec.value_type', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=417,
  serialized_end=493,
)

_FEATURESETSPEC.fields_by_name['entities'].message_type = _ENTITYSPEC
_FEATURESETSPEC.fields_by_name['features'].message_type = _FEATURESPEC
_FEATURESETSPEC.fields_by_name['max_age'].message_type = google_dot_protobuf_dot_duration__pb2._DURATION
_FEATURESETSPEC.fields_by_name['source'].message_type = feast_dot_core_dot_Source__pb2._SOURCE
_ENTITYSPEC.fields_by_name['value_type'].enum_type = feast_dot_types_dot_Value__pb2._VALUETYPE_ENUM
_FEATURESPEC.fields_by_name['value_type'].enum_type = feast_dot_types_dot_Value__pb2._VALUETYPE_ENUM
DESCRIPTOR.message_types_by_name['FeatureSetSpec'] = _FEATURESETSPEC
DESCRIPTOR.message_types_by_name['EntitySpec'] = _ENTITYSPEC
DESCRIPTOR.message_types_by_name['FeatureSpec'] = _FEATURESPEC
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

FeatureSetSpec = _reflection.GeneratedProtocolMessageType('FeatureSetSpec', (_message.Message,), {
  'DESCRIPTOR' : _FEATURESETSPEC,
  '__module__' : 'feast.core.FeatureSet_pb2'
  # @@protoc_insertion_point(class_scope:feast.core.FeatureSetSpec)
  })
_sym_db.RegisterMessage(FeatureSetSpec)

EntitySpec = _reflection.GeneratedProtocolMessageType('EntitySpec', (_message.Message,), {
  'DESCRIPTOR' : _ENTITYSPEC,
  '__module__' : 'feast.core.FeatureSet_pb2'
  # @@protoc_insertion_point(class_scope:feast.core.EntitySpec)
  })
_sym_db.RegisterMessage(EntitySpec)

FeatureSpec = _reflection.GeneratedProtocolMessageType('FeatureSpec', (_message.Message,), {
  'DESCRIPTOR' : _FEATURESPEC,
  '__module__' : 'feast.core.FeatureSet_pb2'
  # @@protoc_insertion_point(class_scope:feast.core.FeatureSpec)
  })
_sym_db.RegisterMessage(FeatureSpec)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)

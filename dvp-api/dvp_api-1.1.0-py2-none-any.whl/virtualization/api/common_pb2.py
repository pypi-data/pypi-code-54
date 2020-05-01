# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: dlpx/virtualization/api/common.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='dlpx/virtualization/api/common.proto',
  package='com.delphix.virtualization.common',
  syntax='proto3',
  serialized_options=_b('P\001'),
  serialized_pb=_b('\n$dlpx/virtualization/api/common.proto\x12!com.delphix.virtualization.common\"\x9a\x01\n\x10RemoteConnection\x12I\n\x0b\x65nvironment\x18\x01 \x01(\x0b\x32\x34.com.delphix.virtualization.common.RemoteEnvironment\x12;\n\x04user\x18\x02 \x01(\x0b\x32-.com.delphix.virtualization.common.RemoteUser\"q\n\x11RemoteEnvironment\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x11\n\treference\x18\x02 \x01(\t\x12;\n\x04host\x18\x03 \x01(\x0b\x32-.com.delphix.virtualization.common.RemoteHost\"X\n\nRemoteHost\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x11\n\treference\x18\x02 \x01(\t\x12\x13\n\x0b\x62inary_path\x18\x03 \x01(\t\x12\x14\n\x0cscratch_path\x18\x04 \x01(\t\"-\n\nRemoteUser\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x11\n\treference\x18\x02 \x01(\t\"h\n\x0cLinkedSource\x12\x0c\n\x04guid\x18\x01 \x01(\t\x12J\n\nparameters\x18\x02 \x01(\x0b\x32\x36.com.delphix.virtualization.common.PluginDefinedObject\"\x9f\x01\n\x0c\x44irectSource\x12G\n\nconnection\x18\x01 \x01(\x0b\x32\x33.com.delphix.virtualization.common.RemoteConnection\x12\x46\n\rlinked_source\x18\x02 \x01(\x0b\x32/.com.delphix.virtualization.common.LinkedSource\"\x8e\x01\n\x11SingleEntireMount\x12P\n\x12remote_environment\x18\x01 \x01(\x0b\x32\x34.com.delphix.virtualization.common.RemoteEnvironment\x12\x12\n\nmount_path\x18\x02 \x01(\t\x12\x13\n\x0bshared_path\x18\x03 \x01(\t\"\x8e\x01\n\x11SingleSubsetMount\x12P\n\x12remote_environment\x18\x01 \x01(\x0b\x32\x34.com.delphix.virtualization.common.RemoteEnvironment\x12\x12\n\nmount_path\x18\x02 \x01(\t\x12\x13\n\x0bshared_path\x18\x03 \x01(\t\"\xc2\x02\n\x0cStagedSource\x12\x46\n\rlinked_source\x18\x01 \x01(\x0b\x32/.com.delphix.virtualization.common.LinkedSource\x12N\n\x11source_connection\x18\x02 \x01(\x0b\x32\x33.com.delphix.virtualization.common.RemoteConnection\x12J\n\x0cstaged_mount\x18\x03 \x01(\x0b\x32\x34.com.delphix.virtualization.common.SingleEntireMount\x12N\n\x11staged_connection\x18\x04 \x01(\x0b\x32\x33.com.delphix.virtualization.common.RemoteConnection\"\xf8\x01\n\rVirtualSource\x12\x0c\n\x04guid\x18\x01 \x01(\t\x12G\n\nconnection\x18\x02 \x01(\x0b\x32\x33.com.delphix.virtualization.common.RemoteConnection\x12\x44\n\x06mounts\x18\x03 \x03(\x0b\x32\x34.com.delphix.virtualization.common.SingleSubsetMount\x12J\n\nparameters\x18\x04 \x01(\x0b\x32\x36.com.delphix.virtualization.common.PluginDefinedObject\"h\n\x0cSourceConfig\x12\x0c\n\x04name\x18\x01 \x01(\t\x12J\n\nparameters\x18\x02 \x01(\x0b\x32\x36.com.delphix.virtualization.common.PluginDefinedObject\"f\n\nRepository\x12\x0c\n\x04name\x18\x01 \x01(\t\x12J\n\nparameters\x18\x02 \x01(\x0b\x32\x36.com.delphix.virtualization.common.PluginDefinedObject\"V\n\x08Snapshot\x12J\n\nparameters\x18\x01 \x01(\x0b\x32\x36.com.delphix.virtualization.common.PluginDefinedObject\"`\n\x12SnapshotParameters\x12J\n\nparameters\x18\x01 \x01(\x0b\x32\x36.com.delphix.virtualization.common.PluginDefinedObject\"#\n\x13PluginDefinedObject\x12\x0c\n\x04json\x18\x01 \x01(\t\")\n\rOwnershipSpec\x12\x0b\n\x03uid\x18\x01 \x01(\x05\x12\x0b\n\x03gid\x18\x02 \x01(\x05\x42\x02P\x01\x62\x06proto3')
)




_REMOTECONNECTION = _descriptor.Descriptor(
  name='RemoteConnection',
  full_name='com.delphix.virtualization.common.RemoteConnection',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='environment', full_name='com.delphix.virtualization.common.RemoteConnection.environment', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='user', full_name='com.delphix.virtualization.common.RemoteConnection.user', index=1,
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
  serialized_start=76,
  serialized_end=230,
)


_REMOTEENVIRONMENT = _descriptor.Descriptor(
  name='RemoteEnvironment',
  full_name='com.delphix.virtualization.common.RemoteEnvironment',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='com.delphix.virtualization.common.RemoteEnvironment.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='reference', full_name='com.delphix.virtualization.common.RemoteEnvironment.reference', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='host', full_name='com.delphix.virtualization.common.RemoteEnvironment.host', index=2,
      number=3, type=11, cpp_type=10, label=1,
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
  serialized_start=232,
  serialized_end=345,
)


_REMOTEHOST = _descriptor.Descriptor(
  name='RemoteHost',
  full_name='com.delphix.virtualization.common.RemoteHost',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='com.delphix.virtualization.common.RemoteHost.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='reference', full_name='com.delphix.virtualization.common.RemoteHost.reference', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='binary_path', full_name='com.delphix.virtualization.common.RemoteHost.binary_path', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='scratch_path', full_name='com.delphix.virtualization.common.RemoteHost.scratch_path', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  serialized_start=347,
  serialized_end=435,
)


_REMOTEUSER = _descriptor.Descriptor(
  name='RemoteUser',
  full_name='com.delphix.virtualization.common.RemoteUser',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='com.delphix.virtualization.common.RemoteUser.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='reference', full_name='com.delphix.virtualization.common.RemoteUser.reference', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  serialized_start=437,
  serialized_end=482,
)


_LINKEDSOURCE = _descriptor.Descriptor(
  name='LinkedSource',
  full_name='com.delphix.virtualization.common.LinkedSource',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='guid', full_name='com.delphix.virtualization.common.LinkedSource.guid', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='parameters', full_name='com.delphix.virtualization.common.LinkedSource.parameters', index=1,
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
  serialized_start=484,
  serialized_end=588,
)


_DIRECTSOURCE = _descriptor.Descriptor(
  name='DirectSource',
  full_name='com.delphix.virtualization.common.DirectSource',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='connection', full_name='com.delphix.virtualization.common.DirectSource.connection', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='linked_source', full_name='com.delphix.virtualization.common.DirectSource.linked_source', index=1,
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
  serialized_start=591,
  serialized_end=750,
)


_SINGLEENTIREMOUNT = _descriptor.Descriptor(
  name='SingleEntireMount',
  full_name='com.delphix.virtualization.common.SingleEntireMount',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='remote_environment', full_name='com.delphix.virtualization.common.SingleEntireMount.remote_environment', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='mount_path', full_name='com.delphix.virtualization.common.SingleEntireMount.mount_path', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='shared_path', full_name='com.delphix.virtualization.common.SingleEntireMount.shared_path', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  serialized_start=753,
  serialized_end=895,
)


_SINGLESUBSETMOUNT = _descriptor.Descriptor(
  name='SingleSubsetMount',
  full_name='com.delphix.virtualization.common.SingleSubsetMount',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='remote_environment', full_name='com.delphix.virtualization.common.SingleSubsetMount.remote_environment', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='mount_path', full_name='com.delphix.virtualization.common.SingleSubsetMount.mount_path', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='shared_path', full_name='com.delphix.virtualization.common.SingleSubsetMount.shared_path', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  serialized_start=898,
  serialized_end=1040,
)


_STAGEDSOURCE = _descriptor.Descriptor(
  name='StagedSource',
  full_name='com.delphix.virtualization.common.StagedSource',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='linked_source', full_name='com.delphix.virtualization.common.StagedSource.linked_source', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='source_connection', full_name='com.delphix.virtualization.common.StagedSource.source_connection', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='staged_mount', full_name='com.delphix.virtualization.common.StagedSource.staged_mount', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='staged_connection', full_name='com.delphix.virtualization.common.StagedSource.staged_connection', index=3,
      number=4, type=11, cpp_type=10, label=1,
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
  serialized_start=1043,
  serialized_end=1365,
)


_VIRTUALSOURCE = _descriptor.Descriptor(
  name='VirtualSource',
  full_name='com.delphix.virtualization.common.VirtualSource',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='guid', full_name='com.delphix.virtualization.common.VirtualSource.guid', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='connection', full_name='com.delphix.virtualization.common.VirtualSource.connection', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='mounts', full_name='com.delphix.virtualization.common.VirtualSource.mounts', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='parameters', full_name='com.delphix.virtualization.common.VirtualSource.parameters', index=3,
      number=4, type=11, cpp_type=10, label=1,
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
  serialized_start=1368,
  serialized_end=1616,
)


_SOURCECONFIG = _descriptor.Descriptor(
  name='SourceConfig',
  full_name='com.delphix.virtualization.common.SourceConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='com.delphix.virtualization.common.SourceConfig.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='parameters', full_name='com.delphix.virtualization.common.SourceConfig.parameters', index=1,
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
  serialized_start=1618,
  serialized_end=1722,
)


_REPOSITORY = _descriptor.Descriptor(
  name='Repository',
  full_name='com.delphix.virtualization.common.Repository',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='com.delphix.virtualization.common.Repository.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='parameters', full_name='com.delphix.virtualization.common.Repository.parameters', index=1,
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
  serialized_start=1724,
  serialized_end=1826,
)


_SNAPSHOT = _descriptor.Descriptor(
  name='Snapshot',
  full_name='com.delphix.virtualization.common.Snapshot',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='parameters', full_name='com.delphix.virtualization.common.Snapshot.parameters', index=0,
      number=1, type=11, cpp_type=10, label=1,
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
  serialized_start=1828,
  serialized_end=1914,
)


_SNAPSHOTPARAMETERS = _descriptor.Descriptor(
  name='SnapshotParameters',
  full_name='com.delphix.virtualization.common.SnapshotParameters',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='parameters', full_name='com.delphix.virtualization.common.SnapshotParameters.parameters', index=0,
      number=1, type=11, cpp_type=10, label=1,
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
  serialized_start=1916,
  serialized_end=2012,
)


_PLUGINDEFINEDOBJECT = _descriptor.Descriptor(
  name='PluginDefinedObject',
  full_name='com.delphix.virtualization.common.PluginDefinedObject',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='json', full_name='com.delphix.virtualization.common.PluginDefinedObject.json', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  serialized_start=2014,
  serialized_end=2049,
)


_OWNERSHIPSPEC = _descriptor.Descriptor(
  name='OwnershipSpec',
  full_name='com.delphix.virtualization.common.OwnershipSpec',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='uid', full_name='com.delphix.virtualization.common.OwnershipSpec.uid', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='gid', full_name='com.delphix.virtualization.common.OwnershipSpec.gid', index=1,
      number=2, type=5, cpp_type=1, label=1,
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
  serialized_start=2051,
  serialized_end=2092,
)

_REMOTECONNECTION.fields_by_name['environment'].message_type = _REMOTEENVIRONMENT
_REMOTECONNECTION.fields_by_name['user'].message_type = _REMOTEUSER
_REMOTEENVIRONMENT.fields_by_name['host'].message_type = _REMOTEHOST
_LINKEDSOURCE.fields_by_name['parameters'].message_type = _PLUGINDEFINEDOBJECT
_DIRECTSOURCE.fields_by_name['connection'].message_type = _REMOTECONNECTION
_DIRECTSOURCE.fields_by_name['linked_source'].message_type = _LINKEDSOURCE
_SINGLEENTIREMOUNT.fields_by_name['remote_environment'].message_type = _REMOTEENVIRONMENT
_SINGLESUBSETMOUNT.fields_by_name['remote_environment'].message_type = _REMOTEENVIRONMENT
_STAGEDSOURCE.fields_by_name['linked_source'].message_type = _LINKEDSOURCE
_STAGEDSOURCE.fields_by_name['source_connection'].message_type = _REMOTECONNECTION
_STAGEDSOURCE.fields_by_name['staged_mount'].message_type = _SINGLEENTIREMOUNT
_STAGEDSOURCE.fields_by_name['staged_connection'].message_type = _REMOTECONNECTION
_VIRTUALSOURCE.fields_by_name['connection'].message_type = _REMOTECONNECTION
_VIRTUALSOURCE.fields_by_name['mounts'].message_type = _SINGLESUBSETMOUNT
_VIRTUALSOURCE.fields_by_name['parameters'].message_type = _PLUGINDEFINEDOBJECT
_SOURCECONFIG.fields_by_name['parameters'].message_type = _PLUGINDEFINEDOBJECT
_REPOSITORY.fields_by_name['parameters'].message_type = _PLUGINDEFINEDOBJECT
_SNAPSHOT.fields_by_name['parameters'].message_type = _PLUGINDEFINEDOBJECT
_SNAPSHOTPARAMETERS.fields_by_name['parameters'].message_type = _PLUGINDEFINEDOBJECT
DESCRIPTOR.message_types_by_name['RemoteConnection'] = _REMOTECONNECTION
DESCRIPTOR.message_types_by_name['RemoteEnvironment'] = _REMOTEENVIRONMENT
DESCRIPTOR.message_types_by_name['RemoteHost'] = _REMOTEHOST
DESCRIPTOR.message_types_by_name['RemoteUser'] = _REMOTEUSER
DESCRIPTOR.message_types_by_name['LinkedSource'] = _LINKEDSOURCE
DESCRIPTOR.message_types_by_name['DirectSource'] = _DIRECTSOURCE
DESCRIPTOR.message_types_by_name['SingleEntireMount'] = _SINGLEENTIREMOUNT
DESCRIPTOR.message_types_by_name['SingleSubsetMount'] = _SINGLESUBSETMOUNT
DESCRIPTOR.message_types_by_name['StagedSource'] = _STAGEDSOURCE
DESCRIPTOR.message_types_by_name['VirtualSource'] = _VIRTUALSOURCE
DESCRIPTOR.message_types_by_name['SourceConfig'] = _SOURCECONFIG
DESCRIPTOR.message_types_by_name['Repository'] = _REPOSITORY
DESCRIPTOR.message_types_by_name['Snapshot'] = _SNAPSHOT
DESCRIPTOR.message_types_by_name['SnapshotParameters'] = _SNAPSHOTPARAMETERS
DESCRIPTOR.message_types_by_name['PluginDefinedObject'] = _PLUGINDEFINEDOBJECT
DESCRIPTOR.message_types_by_name['OwnershipSpec'] = _OWNERSHIPSPEC
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

RemoteConnection = _reflection.GeneratedProtocolMessageType('RemoteConnection', (_message.Message,), dict(
  DESCRIPTOR = _REMOTECONNECTION,
  __module__ = 'dlpx.virtualization.api.common_pb2'
  # @@protoc_insertion_point(class_scope:com.delphix.virtualization.common.RemoteConnection)
  ))
_sym_db.RegisterMessage(RemoteConnection)

RemoteEnvironment = _reflection.GeneratedProtocolMessageType('RemoteEnvironment', (_message.Message,), dict(
  DESCRIPTOR = _REMOTEENVIRONMENT,
  __module__ = 'dlpx.virtualization.api.common_pb2'
  # @@protoc_insertion_point(class_scope:com.delphix.virtualization.common.RemoteEnvironment)
  ))
_sym_db.RegisterMessage(RemoteEnvironment)

RemoteHost = _reflection.GeneratedProtocolMessageType('RemoteHost', (_message.Message,), dict(
  DESCRIPTOR = _REMOTEHOST,
  __module__ = 'dlpx.virtualization.api.common_pb2'
  # @@protoc_insertion_point(class_scope:com.delphix.virtualization.common.RemoteHost)
  ))
_sym_db.RegisterMessage(RemoteHost)

RemoteUser = _reflection.GeneratedProtocolMessageType('RemoteUser', (_message.Message,), dict(
  DESCRIPTOR = _REMOTEUSER,
  __module__ = 'dlpx.virtualization.api.common_pb2'
  # @@protoc_insertion_point(class_scope:com.delphix.virtualization.common.RemoteUser)
  ))
_sym_db.RegisterMessage(RemoteUser)

LinkedSource = _reflection.GeneratedProtocolMessageType('LinkedSource', (_message.Message,), dict(
  DESCRIPTOR = _LINKEDSOURCE,
  __module__ = 'dlpx.virtualization.api.common_pb2'
  # @@protoc_insertion_point(class_scope:com.delphix.virtualization.common.LinkedSource)
  ))
_sym_db.RegisterMessage(LinkedSource)

DirectSource = _reflection.GeneratedProtocolMessageType('DirectSource', (_message.Message,), dict(
  DESCRIPTOR = _DIRECTSOURCE,
  __module__ = 'dlpx.virtualization.api.common_pb2'
  # @@protoc_insertion_point(class_scope:com.delphix.virtualization.common.DirectSource)
  ))
_sym_db.RegisterMessage(DirectSource)

SingleEntireMount = _reflection.GeneratedProtocolMessageType('SingleEntireMount', (_message.Message,), dict(
  DESCRIPTOR = _SINGLEENTIREMOUNT,
  __module__ = 'dlpx.virtualization.api.common_pb2'
  # @@protoc_insertion_point(class_scope:com.delphix.virtualization.common.SingleEntireMount)
  ))
_sym_db.RegisterMessage(SingleEntireMount)

SingleSubsetMount = _reflection.GeneratedProtocolMessageType('SingleSubsetMount', (_message.Message,), dict(
  DESCRIPTOR = _SINGLESUBSETMOUNT,
  __module__ = 'dlpx.virtualization.api.common_pb2'
  # @@protoc_insertion_point(class_scope:com.delphix.virtualization.common.SingleSubsetMount)
  ))
_sym_db.RegisterMessage(SingleSubsetMount)

StagedSource = _reflection.GeneratedProtocolMessageType('StagedSource', (_message.Message,), dict(
  DESCRIPTOR = _STAGEDSOURCE,
  __module__ = 'dlpx.virtualization.api.common_pb2'
  # @@protoc_insertion_point(class_scope:com.delphix.virtualization.common.StagedSource)
  ))
_sym_db.RegisterMessage(StagedSource)

VirtualSource = _reflection.GeneratedProtocolMessageType('VirtualSource', (_message.Message,), dict(
  DESCRIPTOR = _VIRTUALSOURCE,
  __module__ = 'dlpx.virtualization.api.common_pb2'
  # @@protoc_insertion_point(class_scope:com.delphix.virtualization.common.VirtualSource)
  ))
_sym_db.RegisterMessage(VirtualSource)

SourceConfig = _reflection.GeneratedProtocolMessageType('SourceConfig', (_message.Message,), dict(
  DESCRIPTOR = _SOURCECONFIG,
  __module__ = 'dlpx.virtualization.api.common_pb2'
  # @@protoc_insertion_point(class_scope:com.delphix.virtualization.common.SourceConfig)
  ))
_sym_db.RegisterMessage(SourceConfig)

Repository = _reflection.GeneratedProtocolMessageType('Repository', (_message.Message,), dict(
  DESCRIPTOR = _REPOSITORY,
  __module__ = 'dlpx.virtualization.api.common_pb2'
  # @@protoc_insertion_point(class_scope:com.delphix.virtualization.common.Repository)
  ))
_sym_db.RegisterMessage(Repository)

Snapshot = _reflection.GeneratedProtocolMessageType('Snapshot', (_message.Message,), dict(
  DESCRIPTOR = _SNAPSHOT,
  __module__ = 'dlpx.virtualization.api.common_pb2'
  # @@protoc_insertion_point(class_scope:com.delphix.virtualization.common.Snapshot)
  ))
_sym_db.RegisterMessage(Snapshot)

SnapshotParameters = _reflection.GeneratedProtocolMessageType('SnapshotParameters', (_message.Message,), dict(
  DESCRIPTOR = _SNAPSHOTPARAMETERS,
  __module__ = 'dlpx.virtualization.api.common_pb2'
  # @@protoc_insertion_point(class_scope:com.delphix.virtualization.common.SnapshotParameters)
  ))
_sym_db.RegisterMessage(SnapshotParameters)

PluginDefinedObject = _reflection.GeneratedProtocolMessageType('PluginDefinedObject', (_message.Message,), dict(
  DESCRIPTOR = _PLUGINDEFINEDOBJECT,
  __module__ = 'dlpx.virtualization.api.common_pb2'
  # @@protoc_insertion_point(class_scope:com.delphix.virtualization.common.PluginDefinedObject)
  ))
_sym_db.RegisterMessage(PluginDefinedObject)

OwnershipSpec = _reflection.GeneratedProtocolMessageType('OwnershipSpec', (_message.Message,), dict(
  DESCRIPTOR = _OWNERSHIPSPEC,
  __module__ = 'dlpx.virtualization.api.common_pb2'
  # @@protoc_insertion_point(class_scope:com.delphix.virtualization.common.OwnershipSpec)
  ))
_sym_db.RegisterMessage(OwnershipSpec)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)

# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tensorflow_serving/apis/model_service.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from tensorflow_serving.apis import get_model_status_pb2 as tensorflow__serving_dot_apis_dot_get__model__status__pb2
from tensorflow_serving.apis import model_management_pb2 as tensorflow__serving_dot_apis_dot_model__management__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='tensorflow_serving/apis/model_service.proto',
  package='tensorflow.serving',
  syntax='proto3',
  serialized_pb=_b('\n+tensorflow_serving/apis/model_service.proto\x12\x12tensorflow.serving\x1a.tensorflow_serving/apis/get_model_status.proto\x1a.tensorflow_serving/apis/model_management.proto2\xe7\x01\n\x0cModelService\x12g\n\x0eGetModelStatus\x12).tensorflow.serving.GetModelStatusRequest\x1a*.tensorflow.serving.GetModelStatusResponse\x12n\n\x19HandleReloadConfigRequest\x12\'.tensorflow.serving.ReloadConfigRequest\x1a(.tensorflow.serving.ReloadConfigResponseB\x03\xf8\x01\x01\x62\x06proto3')
  ,
  dependencies=[tensorflow__serving_dot_apis_dot_get__model__status__pb2.DESCRIPTOR,tensorflow__serving_dot_apis_dot_model__management__pb2.DESCRIPTOR,])



_sym_db.RegisterFileDescriptor(DESCRIPTOR)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\370\001\001'))

_MODELSERVICE = _descriptor.ServiceDescriptor(
  name='ModelService',
  full_name='tensorflow.serving.ModelService',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=164,
  serialized_end=395,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetModelStatus',
    full_name='tensorflow.serving.ModelService.GetModelStatus',
    index=0,
    containing_service=None,
    input_type=tensorflow__serving_dot_apis_dot_get__model__status__pb2._GETMODELSTATUSREQUEST,
    output_type=tensorflow__serving_dot_apis_dot_get__model__status__pb2._GETMODELSTATUSRESPONSE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='HandleReloadConfigRequest',
    full_name='tensorflow.serving.ModelService.HandleReloadConfigRequest',
    index=1,
    containing_service=None,
    input_type=tensorflow__serving_dot_apis_dot_model__management__pb2._RELOADCONFIGREQUEST,
    output_type=tensorflow__serving_dot_apis_dot_model__management__pb2._RELOADCONFIGRESPONSE,
    options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_MODELSERVICE)

DESCRIPTOR.services_by_name['ModelService'] = _MODELSERVICE

# @@protoc_insertion_point(module_scope)

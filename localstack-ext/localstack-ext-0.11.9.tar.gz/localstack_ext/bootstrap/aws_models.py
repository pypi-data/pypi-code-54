from localstack.utils.aws import aws_models
XNhMt=super
XNhMR=None
XNhMV=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  XNhMt(LambdaLayer,self).__init__(arn)
  self.cwd=XNhMR
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,XNhMV,env=XNhMR):
  XNhMt(RDSDatabase,self).__init__(XNhMV,env=env)
 def name(self):
  return self.XNhMV.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)

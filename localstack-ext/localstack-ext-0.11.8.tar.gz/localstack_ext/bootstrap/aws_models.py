from localstack.utils.aws import aws_models
iOPgo=super
iOPgs=None
iOPgM=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  iOPgo(LambdaLayer,self).__init__(arn)
  self.cwd=iOPgs
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,iOPgM,env=iOPgs):
  iOPgo(RDSDatabase,self).__init__(iOPgM,env=env)
 def name(self):
  return self.iOPgM.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)

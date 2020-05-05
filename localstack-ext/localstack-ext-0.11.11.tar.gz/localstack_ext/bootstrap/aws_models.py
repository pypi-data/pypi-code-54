from localstack.utils.aws import aws_models
HBoQl=super
HBoQE=None
HBoQy=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  HBoQl(LambdaLayer,self).__init__(arn)
  self.cwd=HBoQE
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,HBoQy,env=HBoQE):
  HBoQl(RDSDatabase,self).__init__(HBoQy,env=env)
 def name(self):
  return self.HBoQy.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)

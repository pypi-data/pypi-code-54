import click
import boto3
import json
import time
import os
import copy
import inquirer
import webbrowser
import random
import string
import time
from pprint import pprint
from pyfiglet import Figlet
from colorama import init, Fore, Back, Style
from yaspin import yaspin

__version__ = '0.1.2'

init(autoreset=True)

aws_sm_client = boto3.client('sagemaker')
aws_iam_client = boto3.client('iam')
aws_s3_client = boto3.client('s3')

@click.group()
def main():
  pass
  
@main.command()
def run():
  
  printLogoAndVersion()

  create_sageup_data_file_if_not_exist()

  questions = [
    inquirer.Text('name', message="Notebook instance name"),
    inquirer.List(
      "instance-type",
      message="Notebook instance type",
      choices=["ml.t2.medium", 
                "ml.t2.large",
                "ml.t2.xlarge",
                "ml.t2.2xlarge",
                "ml.t3.medium", 
                "ml.t3.large",
                "ml.t3.xlarge",
                "ml.t3.2xlarge",
                "ml.m5.xlarge",
                "ml.m5.2xlarge",
                "ml.m5.4xlarge",
                "ml.m5.12xlarge",
                "ml.m5.24xlarge",
                "ml.m4.xlarge",
                "ml.m4.2xlarge",
                "ml.m4.4xlarge",
                "ml.m4.10xlarge",
                "ml.m4.16xlarge",
                "ml.c5.xlarge",
                "ml.c5.2xlarge",
                "ml.c5.4xlarge",
                "ml.c5.9xlarge",
                "ml.c5.18xlarge",
                "ml.c4.xlarge",
                "ml.c4.2xlarge",
                "ml.c4.4xlarge",
                "ml.c4.8xlarge",
                "ml.p2.xlarge",
                "ml.p2.8xlarge",
                "ml.p2.16xlarge",
                "ml.p3.2xlarge",
                "ml.p3.8xlarge",
                "ml.p3.16xlarge"
              ],
    ),
    inquirer.List(
      'iam-role-type',
      message="Would like to use a custom IAM role or create a default role (if not exist) with full access to SageMaker and S3?",
      choices=['Default', 'Custom'],
      default="Default"
    )
  ]

  answers = inquirer.prompt(questions)

  notebook_name = answers['name']
  instance_type = answers['instance-type']
  iam_role_type = answers['iam-role-type']

  if iam_role_type == 'Custom':
    questions = [inquirer.Text('iam-role-arn', message="IAM Role ARN")]
    answers = inquirer.prompt(questions)

    iam_role_arn = answers['iam-role-arn']

  questions = [inquirer.Text('session-expiration', message="Notebook session expiration in minutes. [Default 720 minutes (12 hours)]", default="720")]
  answers = inquirer.prompt(questions)

  session_expiration_seconds = int(answers['session-expiration']) * 60

  time.sleep(0.5)
  
  print('')
  print('Instance name:               ' + cyan(notebook_name))
  print('Instance type:               ' + cyan(instance_type))
  if iam_role_type == 'Custom':
    print('Custom IAM role:             ' + cyan(iam_role_arn))
  elif iam_role_type == 'Default':
    print('IAM role:                    ' + cyan(iam_role_type + " (full access to SageMaker and S3)"))
  print('Notebook session expiration: ' + cyan(str(session_expiration_seconds / 60) + " minutes"))
  print('')

  questions = [inquirer.List('proceed', message="Would you like to proceed?", choices=['Yes', 'No'], default="Yes")]
  answers = inquirer.prompt(questions)
  
  proceed = answers['proceed']

  if proceed == "Yes":
    if iam_role_type == 'Default':
      iam_role_arn = create_default_role_if_not_exist()

    create_notebook_response = aws_sm_client.create_notebook_instance(
      NotebookInstanceName = notebook_name,
      InstanceType = instance_type,
      RoleArn = iam_role_arn
    )

    notebook_instance_arn = create_notebook_response['NotebookInstanceArn']

    print('Created notebook instance: ' + cyan(notebook_instance_arn))

    wait_until_in_service(notebook_name)

    print("Notebook is in service now.")

    url = get_notebook_url(notebook_name, session_expiration_seconds)

    print('Notebook signed URL: ' + cyan(url))

    webbrowser.open(url, new = 1)
  else:
    print("Aborted.")

def printLogoAndVersion():
  f = Figlet(font='slant')
  print(f.renderText('SageUp'))
  print("Version: " + Fore.GREEN + __version__)
  print(Style.RESET_ALL)

def cyan(input):
  return Fore.CYAN + input + Style.RESET_ALL

@yaspin(text="Starting notebook instance. This can take few minutes ...")
def wait_until_in_service(notebook_name):
  status = "Pending"
  describe_notebook_response = ""
  url = ""
  while status != "InService":
    time.sleep(3)
    describe_notebook_response = describe_notebook(notebook_name)
    status = describe_notebook_response['NotebookInstanceStatus']
  
  return

def describe_notebook(notebook_name):
  describe_notebook_response = aws_sm_client.describe_notebook_instance(
    NotebookInstanceName = notebook_name
  )
  return describe_notebook_response

def get_notebook_url(notebook_name, session_expiration_seconds):
  url_response = aws_sm_client.create_presigned_notebook_instance_url(
    NotebookInstanceName = notebook_name,
    SessionExpirationDurationInSeconds = session_expiration_seconds
  )
  return url_response['AuthorizedUrl']

def create_default_role_if_not_exist():
  sageup_data = read_sageup_data_object()
  if sageup_data['role'] == '':
    role_name = 'SageMaker-SageUp-Role-' + random_string(20)
    data = {
      'Version': '2012-10-17',
      'Statement': {
        'Effect': 'Allow',
        'Principal': {
          'Service': 'sagemaker.amazonaws.com'
        },
        'Action': 'sts:AssumeRole'
      }
    }
    role_create_response = aws_iam_client.create_role(
      Path='/service-role/',
      RoleName=role_name,
      AssumeRolePolicyDocument=json.dumps(data),
      Description='IAM role used for SageMaker notebook instance.'
    )

    attach_sm_role_response = aws_iam_client.attach_role_policy(
      RoleName=role_name, 
      PolicyArn='arn:aws:iam::aws:policy/AmazonSageMakerFullAccess'
    )

    attach_s3_role_response = aws_iam_client.attach_role_policy(
      RoleName=role_name, 
      PolicyArn='arn:aws:iam::aws:policy/AmazonS3FullAccess'
    )

    print('Created default IAM role: ' + cyan(role_create_response['Role']['Arn']))
    sageup_data['role'] = role_create_response['Role']['Arn']
    update_sageup_data_file(sageup_data)
    return role_create_response['Role']['Arn']
  else:
    return sageup_data['role']

def create_sageup_data_file_if_not_exist():
  
  sageup_path = os.getenv("HOME") + "/.sageup"
  sageup_path_file = os.getenv("HOME") + "/.sageup/data.json"

  if not os.path.exists(sageup_path):
    os.makedirs(sageup_path)

  try:
    file = open(sageup_path_file, 'r')
  except IOError:
    file = open(sageup_path_file, 'w')
    file.write('{"bucket":"","role":""}')
    file.close()

def random_string(length):
  return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def read_sageup_data_object():
  sageup_path_file = os.getenv("HOME") + "/.sageup/data.json"
  file = open(sageup_path_file) 
  return json.load(file) 

def update_sageup_data_file(data_object):
  sageup_path_file = os.getenv("HOME") + "/.sageup/data.json"
  file = open(sageup_path_file, 'w')
  file.write(json.dumps(data_object))
  file.close()

def create_bucket_if_not_exist():
  sageup_data = read_sageup_data_object()
  if sageup_data['bucket'] == '':
    bucket_name = "sageup-bucket-" + random_string(20).lower()
    print(bucket_name)
    bucket_create_response = aws_s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': 'us-west-2'})
    pprint(bucket_create_response)
    sageup_data['bucket'] = bucket_name
    update_sageup_data_file(sageup_data)

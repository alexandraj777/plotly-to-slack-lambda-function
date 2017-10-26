import boto3
import json

from botocore.exceptions import ClientError

class AWSClient(object):
  def __init__(self, client_name, *args, **kwargs):
    self._client = boto3.client(client_name, *args, **kwargs)


class IamClient(AWSClient):
  def __init__(self, *args, **kwargs):
    super(IamClient, self).__init__('iam', *args, **kwargs)
    self._role_name = 'lambda_basic_execution'
    self._role_policy_document_name = 'role_policy_document.json'

  @property
  def role_name(self):
    return self._role_name

  @property
  def role_policy_document_name(self):
    return self._role_policy_document_name

  def _get_role_policy_document(self):
    with open(self.role_policy_document_name, 'r') as f:
      role_policy_document_json = f.read()
    return json.loads(role_policy_document_json)

  def create_role(self):
    return self._client.create_role(
      RoleName=self.role_name,
      AssumeRolePolicyDocument=json.dumps(self._get_role_policy_document()),
    )

  def get_role(self):
    return self._client.get_role(
      RoleName=self.role_name
    )

  def delete_role(self):
    return self._client.delete_role(
      RoleName=self.role_name
    )

  def get_or_create_role(self):
    try:
      return self.get_role()
    except ClientError:
      return self.create_role()


class LambdaClient(AWSClient):
  def __init__(self, *args, **kwargs):
    super(LambdaClient, self).__init__('lambda', *args, **kwargs)
    self._function_name = 'plotlyImageToSlack'
    self._function_code_zip_file_name = 'plotlyImageToSlack.zip'

  @property
  def function_name(self):
    return self._function_name

  @property
  def function_code_zip_file_name(self):
    return self._function_code_zip_file_name

  def invoke(self, plot_url):
    return self._client.invoke(
      FunctionName=self.function_name,
      InvocationType='Event',
      Payload=json.dumps(dict(plot_url=plot_url)),
    )

  def _get_zipped_function_code(self):
    with open(self.function_code_zip_file_name, 'rb') as f:
      code = f.read()
    return code

  def update_function_code(self):
    return self._client.update_function_code(
      FunctionName=self.function_name,
      ZipFile=self._get_zipped_function_code(),
    )

  def create_function(self, role, **env_variables):
    return self._client.create_function(
      FunctionName=self.function_name,
      Runtime='python2.7',
      Role=role['Role']['Arn'],
      Handler='main.handler',
      Code=dict(
        ZipFile=self._get_zipped_function_code(),
      ),
      Description='Downloads Plotly images and sends to Slack',
      Timeout=300,
      Environment=dict(
        Variables=env_variables,
      ),
    )

  def delete_function(self):
    return self._client.delete_function(
      FunctionName=self.function_name,
    )

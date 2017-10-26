import argparse
from aws_clients import LambdaClient, IamClient

# We assume that you have followed the instructions in http://boto3.readthedocs.io/en/latest/guide/configuration.html
# to configure your AWS credentials. If for some reason this does not work for you, passing aws_access_key_id and
# aws_secret_access_key directly as named arguments should work.
lambda_client = LambdaClient()
iam_client = IamClient()

def create_function(**environment_variables):
  role = iam_client.get_or_create_role()
  lambda_client.create_function(
    role=role,
    **environment_variables
  )

def update_function():
  lambda_client.update_function_code()

def invoke_function(plotly_url):
  # Find test urls at https://plot.ly/feed/
  # Try out: https://plot.ly/~matlab_user_guide/436
  lambda_client.invoke(plotly_url)

def delete_all_resources():
  lambda_client.delete_function()
  iam_client.delete_role()

if __name__ == "__main__":
  parser = argparse.ArgumentParser()

  parser.add_argument('--plotly-api-token', type=str, required=True, help="Your Plotly api token")
  parser.add_argument('--plotly-username', type=str, required=True, help="Your Plotly username")
  parser.add_argument('--slack-channel', type=str, required=True, help="A Slack channel that will receive images")
  parser.add_argument('--slack-token', type=str, required=True, help="A Slack token with permissions to post to the slack_channel. recommended: [bot users](https://api.slack.com/bot-users)")

  args = parser.parse_args()

  create_function(
    PLOTLY_API_TOKEN=args.plotly_api_token,
    PLOTLY_USERNAME=args.plotly_username,
    SLACK_CHANNEL=args.slack_channel,
    SLACK_TOKEN=args.slack_token,
  )

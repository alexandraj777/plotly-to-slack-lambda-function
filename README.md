# plotlyImageToSlack

`plotlyImageToSlack` downloads the image of a [Plotly](https://plot.ly/) chart and messages it to you via [Slack](https://slack.com/). `plotlyImageToSlack` is intended to be run as an [AWS Lambda](https://aws.amazon.com/lambda/) function.

This Lambda function was created to help debug machine learning models running on EC2.

## Pre-reqs

 * [boto3](https://boto3.readthedocs.io/en/latest/): We assume that you are familiar with using AWS's `boto3` Python client, and that you have followed AWS's [instructions](http://boto3.readthedocs.io/en/latest/guide/configuration.html) to configure your AWS credentials.

 * [Plotly](https://plot.ly/): You will need a Plotly account and API token. If you are not already a Plotly user you can test this function with graphs from their [public feed](https://plot.ly/feed/)

 * [Slack](https://slack.com/): You will need a Slack channel where you would like to post your Plotly images, and a token that has permissions to post to this channel. We suggest using the token from a [bot user](https://api.slack.com/bot-users).

## Quickstart

Run `pip install -r requirements.txt` to install development requirements. Once you've followed the steps in the previous section, run the following code to create or fetch an [IAM role](http://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html), and create a Lambda function:

```bash
python create_lambda_function.py \
  --plotly-api-token <YOUR PLOTLY API TOKEN> \
  --plotly-username <YOUR PLOTLY USERNAME> \
  --slack-channel <'#channel' or '@username' on SLACK> \
  --slack-token <SLACK BOT TOKEN>
```

You can test your function by running:

```bash
from aws_clients import LambdaClient

lambda_client = LambdaClient()
lambda_client.invoke("https://plot.ly/~matlab_user_guide/436")
```

If the function was configured correctly, you should receive a slack message with a Plotly image.

## Debugging

You can debug, change environment variables, and test via the [AWS Console](console.aws.amazon.com). `test_event.json` is a test event that you can copy-paste into the AWS Lambda console.

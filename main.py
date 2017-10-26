from slackclient import SlackClient
import os
import plotly.plotly as py
import re

plotly_api_token = os.getenv('PLOTLY_API_TOKEN')
plotly_username = os.getenv('PLOTLY_USERNAME')
slack_channel = os.getenv('SLACK_CHANNEL')
slack_token = os.getenv('SLACK_TOKEN')

if plotly_api_token is None:
  raise Exception('Expected to find plotly api token at environment variable PLOTLY_API_TOKEN, found nothing')
if plotly_username is None:
  raise Exception('Expected to find plotly username at environment variable PLOTLY_USERNAME, found nothing')
if slack_channel is None:
  raise Exception('Expected to find slack channel at environment variable SLACK_CHANNEL, found nothing')
if slack_token is None:
  raise Exception('Expected to find slack token at environment variable SLACK_TOKEN, found nothing')


class SlackBot(object):
  def __init__(self, channel):
    self.channel = channel
    self.slackclient = SlackClient(slack_token)

  def upload_file(self, file, filename=None):
    self.slackclient.api_call(
      "files.upload",
      as_user=True,
      channels=self.channel,
      filename=filename,
      file=file,
    )

def handler(event, context):
  plot_username, plot_number = re.search('plot\.ly\/~(\w+)\/(\d+)', event['plot_url']).groups()
  assert plot_username is not None
  assert plot_number is not None
  bot = SlackBot(slack_channel)
  py.sign_in(plotly_username, plotly_api_token)
  fig = py.get_figure(plot_username, plot_number)
  bot.upload_file(file=py.image.get(fig), filename='plotly-{}-{}.png'.format(plot_username, plot_number))

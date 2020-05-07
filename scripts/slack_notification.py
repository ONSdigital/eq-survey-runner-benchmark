import os
import sys
import warnings

import slack
from slack.errors import SlackApiError


def parse_environment_variables():
    slack_auth_token = os.getenv('SLACK_AUTH_TOKEN')
    if not slack_auth_token:
        print("'SLACK_AUTH_TOKEN' environment variable must be provided")
        sys.exit(1)

    slack_channel = os.getenv('SLACK_CHANNEL_NAME')
    if not slack_channel:
        print("'SLACK_CHANNEL_NAME' environment variable must be provided")
        sys.exit(1)

    content = os.getenv('CONTENT')
    attachment_filename = os.getenv('ATTACHMENT_FILENAME')
    if content and attachment_filename:
        print(
            "Only one of 'CONTENT' or 'ATTACHMENT_FILENAME' environment variable can be provided"
        )
        sys.exit(1)

    if not (content or attachment_filename):
        print(
            "Either 'CONTENT' or 'ATTACHMENT_FILENAME' environment variable must be provided"
        )
        sys.exit(1)

    if attachment_filename and not os.path.isfile(attachment_filename):
        print("Attachment file does not exist")
        sys.exit(1)

    initial_comment = os.getenv('INITIAL_COMMENT', '')
    title = os.getenv('TITLE', '')

    return {
        'slack_auth_token': slack_auth_token,
        'slack_channel': slack_channel,
        'content': content,
        'attachment_filename': attachment_filename,
        'initial_comment': initial_comment,
        'title': title,
    }


def post_slack_notification():
    parsed_variables = parse_environment_variables()

    client = slack.WebClient(token=parsed_variables['slack_auth_token'])

    try:
        if parsed_variables['content']:
            response = client.files_upload(
                channels=f'#{parsed_variables["slack_channel"]}',
                content=parsed_variables['content'],
                filetype=os.getenv('FILE_TYPE', 'python'),
                title=parsed_variables['title'],
                initial_comment=parsed_variables['initial_comment'],
            )
        else:
            response = client.files_upload(
                channels=f'#{parsed_variables["slack_channel"]}',
                file=parsed_variables['attachment_filename'],
                title=parsed_variables['title'],
                initial_comment=parsed_variables['initial_comment'],
            )
    except SlackApiError as e:
        print(f'Slack notification errored\nError: {e.response["error"]}')
        sys.exit(2)

    if response.get('ok', False) is False:
        print('Slack notification failed')
        sys.exit(2)

    print('Slack notification posted')


if __name__ == "__main__":
    with warnings.catch_warnings():
        #  https://github.com/slackapi/python-slackclient/issues/622
        warnings.simplefilter('ignore', category=RuntimeWarning)

        post_slack_notification()

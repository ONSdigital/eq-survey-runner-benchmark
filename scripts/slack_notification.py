import os
import sys
import warnings

import slack
from slack.errors import SlackApiError


def post_slack_notification():
    slack_auth_token = os.getenv('SLACK_API_TOKEN')
    if not slack_auth_token:
        print("'SLACK_API_TOKEN' must be provided")
        sys.exit(1)

    slack_channel = os.getenv('SLACK_CHANNEL_NAME')
    if not slack_channel:
        print("'SLACK_CHANNEL_NAME' must be provided")
        sys.exit(2)

    content = os.getenv('CONTENT')
    attachment_file_path = os.getenv('ATTACHMENT_FILE_PATH')
    if content and attachment_file_path:
        print("Only one of 'CONTENT' or 'ATTACHMENT_FILE_PATH' can be provided")
        sys.exit(3)

    if not (content or attachment_file_path):
        print("Either 'CONTENT' or 'ATTACHMENT_FILE_PATH' must be provided")
        sys.exit(4)

    if attachment_file_path and not os.path.isfile(attachment_file_path):
        print("Attachment file does not exist")
        sys.exit(5)

    client = slack.WebClient(token=slack_auth_token)

    initial_comment = os.getenv('INITIAL_COMMENT', '')
    title = os.getenv('TITLE', '')

    try:
        if content:
            response = client.files_upload(
                channels=f'#{slack_channel}',
                content=content,
                filetype=os.getenv('FILE_TYPE', 'python'),
                title=title,
                initial_comment=initial_comment,
            )
        else:
            response = client.files_upload(
                channels=f'#{slack_channel}',
                file=attachment_file_path,
                title=title,
                initial_comment=initial_comment,
            )
    except SlackApiError as e:
        print(f'Slack notification errored\nError: {e.response["error"]}')
        sys.exit(6)

    if response.get('ok', False) is False:
        print('Slack notification failed')
        sys.exit(7)

    print('Slack notification posted')


if __name__ == "__main__":
    with warnings.catch_warnings():
        #  https://github.com/slackapi/python-slackclient/issues/622
        warnings.simplefilter('ignore', category=RuntimeWarning)

        post_slack_notification()

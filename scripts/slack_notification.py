import os
import sys
import warnings

import slack


def main():
    if not os.getenv('SLACK_API_TOKEN'):
        print("Slack API auth token must be provided")
        sys.exit(1)

    if not os.getenv('SLACK_CHANNEL_NAME'):
        print("Slack channel name must be provided")
        sys.exit(2)

    attachment_file_path = os.getenv('ATTACHMENT_FILE_PATH')
    if not attachment_file_path:
        print("Attachment file path must be provided")
        sys.exit(3)

    if not os.path.isfile(attachment_file_path):
        print("Attachment file does not exist")
        sys.exit(4)

    client = slack.WebClient(token=os.getenv('SLACK_API_TOKEN'))

    channel = os.getenv('SLACK_CHANNEL_NAME')
    text_content = os.getenv('TEXT_CONTENT', '')
    text_title = os.getenv('TEXT_TITLE', '')

    if attachment_file_path:
        response = client.files_upload(
            channels=f'#{channel}',
            file=attachment_file_path,
            title=text_title,
            initial_comment=text_content,
        )

        if response.get('ok', False) is False:
            print('Slack notification failed')
            sys.exit(5)

        print('Slack notification posted')

if __name__ == "__main__":
    with warnings.catch_warnings():
        #  https://github.com/slackapi/python-slackclient/issues/622
        warnings.simplefilter('ignore', category=RuntimeWarning)

        main()

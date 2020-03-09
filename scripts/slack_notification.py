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

    file_text_content = os.getenv('FILE_TEXT_CONTENT')
    attachment_file_path = os.getenv('ATTACHMENT_FILE_PATH')
    if file_text_content and attachment_file_path:
        print("Only text content or attachment can be provided")
        sys.exit(3)

    if not (file_text_content or attachment_file_path):
        print("Text content or attachment file path must be provided")
        sys.exit(4)

    if attachment_file_path and not os.path.isfile(attachment_file_path):
        print("Attachment file does not exist")
        sys.exit(5)

    client = slack.WebClient(token=os.getenv('SLACK_API_TOKEN'))

    channel = os.getenv('SLACK_CHANNEL_NAME')

    text_content = os.getenv('TEXT_CONTENT', '')
    text_title = os.getenv('TEXT_TITLE', '')

    if file_text_content:
        response = client.files_upload(
            channels=f'#{channel}',
            content=file_text_content,
            filetype=os.getenv('FILE_TYPE', 'python'),
            title=text_title,
            initial_comment=text_content,
        )

        if response.get('ok', False) is False:
            print('Slack text content notification failed')
            sys.exit(6)

        print('Slack text content notification posted')

    elif attachment_file_path:
        response = client.files_upload(
            channels=f'#{channel}',
            file=attachment_file_path,
            title=text_title,
            initial_comment=text_content,
        )

        if response.get('ok', False) is False:
            print('Slack attachment notification failed')
            sys.exit(7)

        print('Slack attachment notification posted')


if __name__ == "__main__":
    with warnings.catch_warnings():
        #  https://github.com/slackapi/python-slackclient/issues/622
        warnings.simplefilter('ignore', category=RuntimeWarning)

        main()

import os
import sys
import warnings

import slack_sdk as slack
from slack_sdk.errors import SlackApiError


def parse_environment_variables():
    slack_auth_token = os.getenv("SLACK_AUTH_TOKEN")
    if not slack_auth_token:
        print("'SLACK_AUTH_TOKEN' environment variable must be provided")
        sys.exit(1)

    slack_channel_id = os.getenv("SLACK_CHANNEL_ID")
    if not slack_channel_id:
        print("'SLACK_CHANNEL_ID' environment variable must be provided")
        sys.exit(1)

    content = os.getenv("CONTENT")
    attachment_filename = os.getenv("ATTACHMENT_FILENAME")
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

    initial_comment = os.getenv("INITIAL_COMMENT", "")
    title = os.getenv("TITLE", "")
    file_type = os.getenv("FILE_TYPE", "yaml")

    return {
        "slack_auth_token": slack_auth_token,
        "slack_channel_id": slack_channel_id,
        "content": content,
        "attachment_filename": attachment_filename,
        "file_type": file_type,
        "initial_comment": initial_comment,
        "title": title,
    }


def post_slack_notification(
    slack_auth_token,
    content,
    attachment_filename,
    file_type,
    initial_comment,
    title,
    slack_channel_id,
):
    client = slack.WebClient(token=slack_auth_token)

    try:
        if content:
            response = client.files_upload_v2(
                channel=slack_channel_id,
                content=content,
                filetype=file_type,
                title=title,
                initial_comment=initial_comment,
            )

        else:
            response = client.files_upload_v2(
                channel=slack_channel_id,
                file=attachment_filename,
                title=title,
                initial_comment=initial_comment,
            )
    except SlackApiError as e:
        print(f'Slack notification errored\nError: {e.response["error"]}')
        sys.exit(2)

    if response.get("ok", False) is False:
        print("Slack notification failed")
        sys.exit(2)

    print("Slack notification posted")


if __name__ == "__main__":
    with warnings.catch_warnings():
        #  https://github.com/slackapi/python-slackclient/issues/622
        warnings.simplefilter("ignore", category=RuntimeWarning)

        parsed_variables = parse_environment_variables()
        post_slack_notification(**parsed_variables)
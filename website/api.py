import logging

from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from slackclient import SlackClient
from website.models import HomePage, LiveBlog, PendingUpdate

SLACK_VERIFICATION_TOKEN = getattr(settings, 'SLACK_VERIFICATION_TOKEN', None)
SLACK_BOT_USER_TOKEN = getattr(settings, 'SLACK_BOT_USER_TOKEN', None)
Client = SlackClient(SLACK_BOT_USER_TOKEN)


logger = logging.getLogger(__name__)


class Event(APIView):
    def post(self, request, *args, **kwargs):

        slack_message = request.data

        if slack_message.get('token') != SLACK_VERIFICATION_TOKEN:
            return Response(status=status.HTTP_403_FORBIDDEN)

        # TODO: Verify message. https://api.slack.com/docs/verifying-requests-from-slack

        # Verification challenge
        if slack_message.get('type') == 'url_verification':
            return Response(data=slack_message, status=status.HTTP_200_OK)

        logger.debug(slack_message)

        # Handle app event.
        if 'event' in slack_message and 'channel' in slack_message['event']:
            event = slack_message['event']
            action_taken = True  # Assume we are going to do something

            # TODO: This should be a channel2page selection.
            channel = event['channel']
            try:
                live_blog = LiveBlog.objects.get(slack_channel=channel)
            except LiveBlog.DoesNotExist:
                if event['type'] == 'channel_created':
                    live_blog = HomePage.objects.first().add_child(
                        instance=LiveBlog(
                            title=event['channel']['name'],
                            slack_channel=channel['id'],
                            show_in_menus=True,
                        ))
                    live_blog.save_revision().publish()
                else:
                    # Apparently we missed the channel created event...
                    live_blog = HomePage.objects.first().add_child(
                        instance=LiveBlog(
                            title=channel,
                            slack_channel=channel,
                        ))

            if event['type'] == 'message' and 'subtype' not in event:
                PendingUpdate.objects.create(
                    live_blog=live_blog,
                    update_type=PendingUpdate.NEW_MESSAGE,
                    raw_update=slack_message['event']['text'],
                    slack_id=slack_message['event']['client_msg_id'],
                    json=slack_message,
                )
            elif event['type'] == 'message' and bool(event.get('files')):
                PendingUpdate.objects.create(
                    live_blog=live_blog,
                    update_type=PendingUpdate.NEW_MESSAGE,
                    raw_update="raw",
                    slack_id="One",
                    json=slack_message,
                )
            elif event['type'] == 'message' \
                    and event.get('subtype') == 'message_changed':
                PendingUpdate.objects.create(
                    live_blog=live_blog,
                    update_type=PendingUpdate.EDIT,
                    raw_update=slack_message['event']['message']['text'],
                    slack_id=slack_message['event']['message']['client_msg_id'],
                    json=slack_message,
                )
            elif event['type'] == 'message' \
                    and event.get('subtype') == 'message_deleted':
                PendingUpdate.objects.create(
                    live_blog=live_blog,
                    update_type=PendingUpdate.DELETE,
                    raw_update='',
                    slack_id=slack_message['event']['previous_message'][
                        'client_msg_id']
                )
            else:
                # nothing done
                action_taken = False

            if action_taken:
                live_blog.update()

        return Response(status=status.HTTP_200_OK)

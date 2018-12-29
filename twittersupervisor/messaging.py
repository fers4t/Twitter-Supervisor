import logging


class Messaging:

    def __init__(self, api, args):
        self.twitter_api = api
        self.args = args

    def announce_follow_event(self, following, user_ids):
        # TODO i18n of the message ?
        if following:
            pattern = '{0} (@{1}) follows you now.'
        else:
            pattern = '{0} (@{1}) stopped following you.'
        for user_id in user_ids:
            user = self.twitter_api.get_user(user_id)
            if user is not None:
                message = pattern.format(user.name, user.screen_name)
                if self.args.quiet:
                    logging.info(message)
                else:
                    self.twitter_api.send_direct_message(message)

''''
 * An API wrapper for KoGaMa re-written in Python.\n
 * Scripted by: TheNoobPro44 (With the help of: MD & Tokeeto!)\n
 * Originaly Made By: Ars3ne.\n
'''
import requests
import json
import time
import threading
from .exceptions import (
    DisallowedURlInput,
    NotAValidServer,
    FailedLogin,
    TooManyRequests,
    ReasonNotFound,
    TemplateNotFound
)


class KoGaMa:
    """ A wrapper for the kogama website api """

    def __init__(self, server):
        if server.lower() not in ('www', 'br', 'friends'):
            raise NotAValidServer('Not a valid server!')

        self.url = {
            'br': 'https://kogama.com.br',
            'www': 'https://www.kogama.com',
            'friends': 'https://friends.kogama.com',
        }[server.lower()]

        self.session = requests.Session()
        self.user_id = None

        self.show_as_available = False
        ping_thread = threading.Thread(
            target=self._send_ping,
            name='ping',
            deamon=True
        )
        ping_thread.run()

    def login(self, username, password):
        """
        Logs in on a KoGaMa account, given the Username & Password.\n
        Raises an exception if unsuccessful\n

        Parameters:
        ----------
            username : str\n
            >    Users account name.\n
            password : str\n
            >    Users account password.\n
        """
        response = self.session.post(
            f"{self.url}/auth/login/",
            json={"username": username, "password": password}
        )

        if 'error' in response:
            raise FailedLogin('Error in login')
        if 'banned' in response:
            raise FailedLogin('Account is banned')

        if response.status_code != 200:
            raise FailedLogin(f"Please check If your Password or Username is correct and try again.. (Error Code: {response.status_code})")

        self.user_id = response.json()['data']['id']

    def logout(self):
        """
        Logout from the KoGaMa account
        """
        self.session.get(f"{self.url}/auth/logout/")
        self.session.cookies.clear()

    def _post_to_feed(self, feed_url, data):
        response = self.session.post(url, json=data)

        if response.status_code == 429:
            raise TooMuchRequests("Chill, Cowboy! You are doing this too much, wait a little.")

        if response.status_code not in (201, 200):
            raise Exception(f"Failed to post comment. Error Code: {response.status_code}")

        if 'Disallowed' in response.text:
            raise DisallowedURlInput("Please do not put links in your message!")

        if 'Disallowed' in response.text:
            raise DisallowedURlInput("Please do not put links in your message!")

    def post_feed(self, user_id, message):
        """
        Post a message in users Feed.\n

        Parameters:
        -----------
            user_id : str\n
                User's account ID.\n
            message : str\n
                Message that will be sent.\n
        """
        self._post_to_feed(
            f"{self.url}/api/feed/{user_id}/",
            {"status_message": message, "profile_id": user_id, "wait": True}
        )

    def get_post_comments(self, post_id):
        """
        Get comments from a post and return it.\n

        Parameters:
        ----------
        post_id : str\n
            ID of the Post.\n
        """
        response = self.session.get(f'{self.url}/api/feed/{post_id}/comment/')
        return response.json()

    def post_feed_comment(self, feed_id, message):
        """
        Post a comment in a Feed.\n

        Parameters:
        ----------
        feed_id : str\n
            ID of the Feed.\n
        message : str\n
            Message that will be posted.\n
        """
        self._post_to_feed(
            f"{self.url}/api/feed/{feed_id}/comment/",
            {"comment": message}
        )

    def post_game_comment(self, game_id, message):
        """
        Post a comment in a Game.\n

        Parameters:
        ----------
        game_id : str\n
            ID of the Game.\n
        message : str\n
          Message that will be posted.\n
        """
        self._post_to_feed(
            f"{self.url}/game/{game_id}/comment/",
            {"comment": message}
        )

    def post_model_comment(self, model_id, message):
        """
        Post a comment in a Model.\n

        Parameters:
        ----------
        model_id : str\n
            ID of the Model.\n
        message : str\n
            Message that will be posted.\n
        """
        self._post_to_feed(f"{self.url}/model/market/i-{model_id}/comment/", {"comment":message})

    def post_avatar_comment(self, avatar_id, message):
        """
        - Post a comment in a Avatar.\n


        Parameters:
        ----------
        avatar_id : str\n
            ID of the Avatar.\n
        message : str\n
            Message that will be posted.\n
        """
        self._post_to_feed(f"{self.url}/model/market/a-{avatar_id}/comment/", {"comment":message})

    def post_news_comment(self, news_id, message):
        """
        - Post a comment in a News Page.\n

        - Returns True, If the comment has been posted.\n
        - Returns False, If fails to post a comment.\n

        Parameters:
        ----------
        news_id : int / str\n
            ID of the News.\n
        message : str\n
            Message that will be posted.\n
        """
        self._post_to_feed(f"{self.url}/api/news/{news_id}/comment/", {"comment":message})

    def _delete_comment(self, url):
        response = self.session.delete(url)

        if response.status_code != 200:
            raise Exception(f"Failed to delete comment in [Comment ID: {comment_id}].. (Error Code: {response.status_code})")

        if "Unauthorized" in response.text:
            raise Exception("Unauthorized.")

    def delete_game_comment(self, game_id, comment_id):
        """
        Deletes a comment on a Game.\n

        Parameters:
        ----------
        game_id : str\n
            ID of the Game.\n
        comment_id : str\n
            ID of the Comment.\n
        """
        self._delete_comment(f"{self.url}/game/{game_id}/comment/{comment_id}/")

    def delete_feed_comment(self, feed_id, comment_id):
        """
        Deletes a comment in a profile feed.\n

        Parameters:
        ----------
        feed_id : int / str
            ID of the Feed.
        comment_id : int / str
            ID of the Comment.
        """
        self._delete_comment(f"{self.url}/feed/{feed_id}/comment/{feed_id}/")

    def create_game(self, name, description, template='base'):
        """
        Creates a game.\n

        Parameters:
        ----------
        name : str\n
            name of your Game.\n
        description : str\n
            Description of your Game.\n
        template : str\n
            Template of your Game.\n
            Valid values are: ['base', 'city', 'island', 'parkour']\n
        """
        templates = {"base": 3, "city": 4, "island": 5, "parkour": 6}
        if template not in templates:
            raise TemplateNotFound("This template doesn't exist!")

        response = self.session.post(
            f"{self.url}/game/",
            json={
                "name": Name,
                "description": description,
                "proto_id": templates[template]
            }
        )

        if response.status_code != 201:
            raise Exception(f"Failed to create game, [Game Name: {Name}]; [Game Description: {Desc}]; [Template: {Template}]; (Error Code: {response.status_code})")

    def invite_member_to_game(self, game_id, user_id):
        """
        Invites a member to a Project or Game.\n

        Parameters:
        ----------
        game_id : str\n
            ID of the Game.\n
        user_id : str\n
            ID of the User.\n
        """
        response = self.session.post(
            f"{self.url}/game/{game_id}/member/",
            json={"game_id": game_id, "member_user_id":user_id}
        )
        if response.status_code != 201:
            raise Exception(f"Failed to invite [User ID: {user_id}] to a game, [Game ID: {game_id}].. (Error Code: {response.status_code})")

    def send_friend_request(self, friend_id):
        """
        Sends a friend request to a user.\n

        Parameters:
        ----------
        user_id : str\n
            ID of the User.\n
        """
        response = self.session.post(
            f"{self.url}/user/{friend_id}/friend/",
            json={
                "friend_profile_id": friend_id,
                "profile_id": self.user_id,
                "user_id": friend_id
            }
        )

        if response.status_code != 201:
            raise Exception(f"Failed to send friend request to [Friend ID: {friend_id}].. (Error Code: {response.status_code})")

    def cancel_friend_request(self, friend_id):
        """
        Cancels a friend request.\n

        Parameters:
        ----------
        user_id : str\n
            ID of the User.\n
        """
        response = self.session.delete(f"{self.url}/user/{self.user_id}/friend/{friend_id}/")

        if response.status_code != 201:
            raise Exception(f"Failed to cancel friend request, [Friend ID: {friend_id}].. (Error Code: {response.status_code})")

    def purchase_model(self, model_id):
        """
        Purchases a Model from Shop.\n

        Parameters:
        ----------
        model_id : str\n
            ID of the Model.\n
        """
        response = self.session.post(f"{self.url}/model/market/i-{model_id}/purchase/")

        if response.status_code != 201:
            raise Exception(f"Failed to purchase model, [Model ID: {model_id}].. (Error Code: {response.status_code})")

    def purchase_avatar(self, avatar_id):
        """
        Purchases a Avatar from Shop.\n

        Parameters:
        ----------
        avatar_id : str\n
            ID of the Avatar.\n
        """
        response = self.session.post(f"{self.url}/model/market/a-{avatar_id}/purchase/")

        if response.status_code != 201:
            raise Exception(f"Failed to purchase avatar, [Avatar ID: {avatar_id}].. (Error Code: {response.status_code})")

    def claim_elite_gold(self):
        """ Claims daily Elite Gold. """
        response = self.session.post(
            f"{self.url}/user/{self.user_id}/claim-daily-gold/"
        )
        if response.status_code != 200:
            raise Exception(f"Failed to purchase claim elite gold.. (Error Code: {response.status_code})")

    def reedem_coupon(self, coupon):
        """
        Reedems a coupon code.\n

        Parameters:
        ----------
        coupon : str\n
            Coupon Code.\n
        """
        response = self.session.post(
            f"{self.url}/api/coupon/redeem/",
            json={"code": coupon}
        )

        if response.status_code != 201:
            raise Exception(f"Failed to reedem coupon, [Coupon: {coupon}].. (Error Code: {response.status_code})")

    def unlock_badge(self, badge):
        """
        Unlocks a Hidden Badge.\n

        Parameters:
        -----------
        badge : str\n
            Badge ID.\n
        """
        response = self.session.post(f"{self.url}/user/{self.user_id}/badge/{badge}/read/")

        if response.status_code != 201:
            raise Exception(f"Failed to unlock badge, [Badge ID: {badge}].. (Error Code: {response.status_code})")

    def like_game(self, game_id):
        """
        Likes an game.\n

        Parameters:
        ----------
        game_id : str\n
            ID of the game.\n
        """
        response = self.session.post(f"{self.url}/game/{game_id}/like/")

        if response.status_code != 201:
            raise Exception(f"Failed to Like game, [Game ID: {game_id}].. (Error Code: {response.status_code})")

    def like_model(self, model_id):
        """
        Likes an Model.\n

        Parameters:
        ----------
        model_id : str\n
            ID of the model.\n
        """
        response = self.session.post(f"{self.url}/model/market/i-{model_id}/like/")

        if response.status_code != 201:
            raise Exception(f"Failed to Like model, [Model ID: {model_id}].. (Error Code: {response.status_code})")

    def like_avatar(self, avatar_id):
        """
        Likes an avatar.\n

        Parameters:
        ----------
        avatar_id : str\n
            ID of the model.\n
        """
        response = self.session.post(f"{self.url}/model/market/a-{avatar_id}/like/")
        if response.status_code != 201:
            raise Exception(f"Failed to Like avatar, [Avatar ID: {avatar_id}].. (Error Code: {response.status_code})")

    def _send_ping(self):
        """ Notifies the server that the user is available in chat """
        while True:
            if self.user_id and self.show_as_available:
                self.session.post(
                    f"{self.url}/user/{self.user_id}/pulse/",
                    json={
                        "status": "active",
                        "location": 'kogama.py'}
                )
            time.sleep(5)

    def appear_online(self):
        """
        Keep showing as online in the chat.\n
        Turn off again by running appear_offline()
        """
        self.show_as_available = True

    def appear_offline(self):
        self.show_as_available = False


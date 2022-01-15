"""
 * An API-Wrapper for the KoGaMa Website API.\n
 * Made by: TheNoobPro44 [with the help of Tokeeto]\n
 * Originaly Made By: Ars3ne.\n
"""

import requests
from exceptions import (failed_login, disallowed_url_input, too_many_requests, unauthorized_request)

class KoGaMa:
    """KoGaMa.py-Rewrite is an api-wrapper for the KoGaMa Website API."""
    def __init__(self, server : str):
        if server.lower() not in ('www', 'br', 'friends'):
            raise Exception(f'"{server.upper()}" is not a valid server! Valid values are ["www","br", "friends"]')

        self.url = {
            'br': 'https://kogama.com.br',
            'www': 'https://www.kogama.com',
            'friends': 'https://friends.kogama.com',
        }[server.lower()]

        self.session = requests.Session()
        self.user_id = None

    def login(self, username : str, password : str):
        """
        Makes log in on a KoGaMa Account.\n
        You must login first before using commands.

        Parameters:
        -----------
            username (str) : Account Username.
            password (str) : Account Password.
        """

        response = self.session.post(f"{self.url}/auth/login/",json={"username": username,"password": password})

        if response.status_code == 429:
           raise too_many_requests("Chill, Cowboy! You are doing this too much, wait a little. [Status Code: 429]")

        if 'banned' in response:
            raise Exception('Unable to make login: Your account was banned.')
        elif 'error' in response:
            raise failed_login(f'An error happened! [Status Code: {response.status_code}]')
        elif response.status_code != 200:
            raise failed_login(f"Please check If your Username or Password is correct and try again.. [Status Code: {response.status_code}]")

        self.user_id = response.json()['data']['id']

    def logout(self):
        """
        Logout of a KoGama Account.\n
        Deletes the cookies of account, ending the session.

        Note: This isn't always required. It's optional if you wanna clear your cookies.

        """

        self.session.get(f"{self.url}/auth/logout/")
        self.session.cookies.clear()
    
    def _handle_requests(self, method, url, data=None, error_message='Failed to perform action..'):
        """This funcion will handle all requests (DELETE, POST, PUT) and will also handle errors properly.."""

        if method == 'delete':
            response = self.session.delete(url)

            if response.status_code == 429:
                raise too_many_requests("Chill, Cowboy! You are doing this too much, wait a little. [Status Code: 429]")
            elif 'banned' in response.text:
                raise Exception("You can't peform this action since your account was banned..")
            elif "Unauthorized" in response.text:
                raise unauthorized_request("Unauthorized Request. You don't have permission to perform that action. [Status Code: 401]")
            elif response.status_code != 200:
                raise Exception(f"{error_message} [Status Code: {response.status_code}]")
        elif method == 'post':
            response = self.session.post(url, json=data)

            if response.status_code == 429:
                raise too_many_requests("Chill, Cowboy! You are doing this too much, wait a little. [Status Code: 429]")
            elif 'banned' in response.text:
                raise Exception("You can't peform this action since your account was banned..")
            elif "Unauthorized" in response.text:
                raise unauthorized_request("Unauthorized Request. You don't have permission to perform that action. [Status Code: 401]")
            elif 'Disallowed' in response.text:
                raise disallowed_url_input("Please do not put links in your message.")
            elif response.status_code not in (200, 201):
                raise Exception(f"{error_message} [Status Code: {response.status_code}]")
        elif method == 'put':
            response = self.session.put(url, json=data)

            if response.status_code == 429:
                raise too_many_requests("Chill, Cowboy! You are doing this too much, wait a little. [Status Code: 429]")
            elif 'banned' in response.text:
                raise Exception("You can't peform this action since your account was banned..")
            elif "Unauthorized" in response.text:
                raise unauthorized_request("Unauthorized Request. You don't have permission to perform that action. [Status Code: 401]")
            elif response.status_code not in (200, 201):
                raise Exception(f"{error_message} [Status Code: {response.status_code}]")

    def post_feed(self, user_id : str, message : str):
        """
        Posts a message in users Feed.\n

        Parameters:
        ------------
            user_id (str) : ID of the Account.\n
            message (str) : Message to post.\n
        """

        self._handle_requests(method='post', url=f"{self.url}/api/feed/{user_id}/", data={"status_message": message, "profile_id": user_id, "wait": True}, error_message='Failed to post message on the Feed.')

    def post_feed_comment(self, feed_id : str, message : str):
        """
        Posts a comment in a existing Feed.\n

        Parameters:
        ------------
            feed_id (str) : ID of the Feed.\n
            message (str) : Message to post.\n
        """

        self._handle_requests(method='post', url=f"{self.url}/api/feed/{feed_id}/comment/", data={"comment": message}, error_message='Failed to post comment on a Feed.')

    def post_game_comment(self, game_id : str, message : str):
        """ 
        Posts a comment in a game.\n

        Parameters:
        ------------
            game_id (str) : ID of the Game.\n
            message (str) : Message to post.\n
        """

        self._handle_requests(method='post', url=f"{self.url}/game/{game_id}/comment/",data={"comment": message}, error_message='Failed to post comment on the Game.')

    def post_model_comment(self, model_id : str, message : str):
        """
        Posts a comment in a Model.\n

        Parameters:
        ------------
            model_id (str) : ID of the Model.\n
            message (str) : Message to post.\n
        """

        self._handle_requests(method='post', url=f"{self.url}/model/market/i-{model_id}/comment/", data={"comment":message}, error_message='Failed to post comment on the Model.')

    def post_avatar_comment(self, avatar_id : str, message : str):
        """ 
        Posts a comment in a Avatar.\n

        Parameters:
        ------------
            avatar_id (str) : ID of the Avatar.\n
            message (str) : Message to post.\n
        """

        self._handle_requests(method='post', url=f"{self.url}/model/market/a-{avatar_id}/comment/", data={"comment":message}, error_message='Failed to post comment on the Avatar.')

    def post_news_comment(self, news_id : str, message : str):
        """   
        Posts a message in a news post.\n

        Parameters:
        ------------
            news_id (str) : ID of the News Post.\n
            message (str) : Message to post.\n
        """

        self._handle_requests(method='post', url=f"{self.url}/api/news/{news_id}/comment/", data={"comment":message}, error_message='Failed to post comment on the News Post.')

    def delete_game_comment(self, game_id : str, comment_id : str):
        """
        Deletes a Game comment.\n

        Parameters:
        ------------
            game_id (str) : ID of the Game.\n
            comment_id (str) : ID of the comment.\n
        """

        self._handle_requests(method='delete', url=f"{self.url}/game/{game_id}/comment/{comment_id}/", error_message='Failed to delete Game comment.')
    
    def delete_model_comment(self, model_id : str, comment_id : str):
        """
        Deletes a Model comment.\n

        Parameters:
        ------------
            model_id (str) : ID of the Model.\n
            comment_id (str) : ID of the comment.\n
        """

        self._handle_requests(method='delete', url=f"{self.url}/model/market/i-{model_id}/comment/{comment_id}/", error_message='Failed to delete Model comment.')
    
    def delete_avatar_comment(self, avatar_id : str, comment_id : str):
        """
        Deletes a Avatar comment.\n

        Parameters:
        ------------
            avatar_id (str) : ID of the Avatar.\n
            comment_id (str) : ID of the comment.\n
        """

        self._handle_requests(method='delete', url=f"{self.url}/model/market/a-{avatar_id}/comment/{comment_id}/", error_message='Failed to delete Avatar comment.')

    def delete_feed_post(self, user_id : str, feed_id : str):
        """
        Deletes a feed post.\n

        Parameters:
        ------------
            user_id (str) : ID of the user who posted.\n
            comment_id (str) : ID of the comment.\n
        """

        self._handle_requests(method='delete', url=f"{self.url}/api/feed/{user_id}/{feed_id}/", error_message='Failed to delete Feed Post.')

    def delete_feed_comment(self, feed_id : str, comment_id : str):
        """
        Deletes a feed comment.\n

        Parameters:
        ------------
            feed_id (str) : ID of the Feed Comment.\n
            comment_id (str) : ID of the comment.\n
        """

        self._handle_requests(method='delete', url=f"{self.url}/feed/{feed_id}/comment/{comment_id}/", error_message='Failed to delete Feed Comment.')

    def create_game(self, name : str, description='No description provided.', template='base'):
        """
        Creates a game.\n

        By default, the template is 'base' and description is 'No description provided'.\n

        Parameters:
        ------------
            name (str) : Name of the Game.\n
            description (str) : Description of the Game.\n
            template (str) : Template of your Game. Valid values are: ['base', 'city', 'island', 'parkour']\n
        """

        templates = {"base": 3, "city": 4, "island": 5, "parkour": 6}

        if template not in templates:
            raise Exception("This template doesn't exist! Valid values are: ['base', 'city', 'island', 'parkour']")

        response = self.session.post(f"{self.url}/game/",json={"name": name,"description": description,"proto_id": templates[template]})

        if response.status_code == 429:
            raise too_many_requests("Chill, Cowboy! You are doing this too much, wait a little. [Status Code: 429]")
        elif response.status_code != 201:
            raise Exception(f"Failed to create Game. [Status Code: {response.status_code}]")
        elif response.status_code == 201:
            return response.json()

    def invite_member_to_game(self, game_id : str, user_id : str):
        """
        Invites a member to project.\n

        Parameters:
        ------------
            game_id (str) : ID of the Game.\n
            user_id (str) : ID of the User.\n
        """

        self._handle_requests(method='post', url=f"{self.url}/game/{game_id}/member/",data={"game_id": game_id, "member_user_id":user_id}, error_message='Failed to invite member to the Game.')

    def send_friend_request(self, friend_id : str):
        """
        Sends a friend request to a user.\n

        Parameters:
        ----------
            friend_id (str) : ID of the User.\n
        """

        self._handle_requests(method='post', url=f"{self.url}/user/{friend_id}/friend/",data={"friend_profile_id": friend_id,"profile_id": self.user_id,"user_id": friend_id}, error_message='Failed to send friend request.')

    def cancel_friend_request(self, friend_id : str):
        """ 
        Cancels a friend request.\n

        Parameters:
        ----------
            user_id (str) : ID of the User.
        """

        self._handle_requests(method='delete', url=f"{self.url}/user/{self.user_id}/friend/{friend_id}/", error_message='Failed to cancel friend request.')

    def purchase_model(self, model_id : str):
        """
        Purchases a Model from Shop.\n

        Parameters:
        ----------
            model_id (str) : ID of the Model.
        """

        self._handle_requests(method='post', url=f"{self.url}/model/market/i-{model_id}/purchase/", error_message='Failed to purchase Model.')

    def purchase_avatar(self, avatar_id : str):
        """
        Purchases an avatar from the shop.\n

        Parameters:
        ----------
            avatar_id (str) : ID of the Avatar.
        """

        self._handle_requests(method='post', url=f"{self.url}/model/market/a-{avatar_id}/purchase/", error_message='Failed to purchase Avatar.')

    def claim_elite_gold(self):
        """
        Claims daily Elite Gold.

        Returns `Exception` If failed to claim the Gold.
        """

        response = self.session.post(f"{self.url}/user/{self.user_id}/claim-daily-gold/")

        if response.status_code == 429:
            raise too_many_requests("Chill, Cowboy! You are doing this too much, wait a little. [Status Code: 429]")
        elif response.status_code != 200:
            raise Exception(f"Failed to purchase claim elite gold.. [Status Code: {response.status_code}]")

    def reedem_coupon(self, coupon : str):
        """ 
        Reedems a coupon code.\n

        Parameters:
        ----------
            coupon (str) : Coupon.
        """

        self._handle_requests(method='post', url=f"{self.url}/api/coupon/redeem/", data={"code": coupon}, error_message='Failed to reedem coupon.')

    def unlock_badge(self, badge : str):
        """
        Unlocks a Hidden Badge.\n

        Parameters:
        ----------
            badge (str) : Badge ID.
        """

        self._handle_requests(method='post', url=f"{self.url}/user/{self.user_id}/badge/{badge}/read/", error_message='Failed to unlock Hidden Badge.')

    def like_game(self, game_id : str):
        """
        Likes a game.\n

        Parameters:
        ----------
            game_id (str) : Game ID.
        """

        response = self.session.post(f"{self.url}/game/{game_id}/like/")

        if response.status_code == 429:
            raise too_many_requests("Chill, Cowboy! You are doing this too much, wait a little. [Status Code: 429]")
        elif response.status_code != 201:
            raise Exception(f"Failed to like Game. [Status Code: {response.status_code}]")

    def like_model(self, model_id : str):
        """
        Likes a model.\n

        Parameters:
        ----------
            model_id (str) : Model ID.
        """

        response = self.session.post(f"{self.url}/model/market/i-{model_id}/like/")

        if response.status_code == 429:
            raise too_many_requests("Chill, Cowboy! You are doing this too much, wait a little. [Status Code: 429]")
        elif response.status_code != 201:
            raise Exception(f"Failed to like Model. [Status Code: {response.status_code}]")

    def like_avatar(self, avatar_id : str):
        """
        Likes an avatar.\n

        Parameters:
        ----------
            avatar_id (str) : Avatar ID.
        """

        response = self.session.post(f"{self.url}/model/market/a-{avatar_id}/like/")

        if response.status_code == 429:
            raise too_many_requests("Chill, Cowboy! You are doing this too much, wait a little. [Status Code: 429]")
        elif response.status_code != 201:
            raise Exception(f"Failed to like Avatar. [Status Code: {response.status_code}]")

    def change_email(self, email : str):
        """
        Changes the email of your KoGaMa Account.\n

        Parameters:
        ----------
            email (str) : Email of the Account.
        """

        self._handle_requests(method='put', url=f"{self.url}/user/{self.user_id}/email/", data={"email":email}, error_message='Failed to change account email.')
        
    def change_username(self, username : str):
        """
        Changes the name of your KoGaMa Account.\n

        Parameters:
        ----------
            username (str) : Username.
        """

        self._handle_requests(method='put', url=f"{self.url}/user/{self.user_id}/username/", data={"username":username}, error_message='Failed to change account username.')
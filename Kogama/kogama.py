"""
 * An API-Wrapper for the KoGaMa Website API.\n
 * Made by: TheNoobPro44 [with the help of Tokeeto]\n
 * Originaly Made By: Ars3ne.\n
"""

import requests
from exceptions import (failed_login, disallowed_url_input, too_many_requests, unauthorized_request)

class KoGaMa:
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

        response = self.session.post(f"{self.url}/auth/login/", json={"username": username,"password": password})

        if response.status_code == 429:
           raise too_many_requests("Chill, Cowboy! You are doing this too much, wait a little. [Status Code: 429]")

        if 'banned' in response:
            raise failed_login('Unable to make login: Your account was banned.')
        elif response.status_code == 400:
            raise failed_login(f'Wrong username or password! [Status Code: {response.status_code}]')
        elif response.status_code != 200:
            raise failed_login(f"Something went wrong. [Status Code: {response.status_code}]")

        self.user_id = response.json()['data']['id']

    def logout(self):
        """
        Logout of a KoGama Account.\n
        Deletes the cookies of the account, ending the session.

        Note: This isn't always required. It's optional if you wanna clear your cookies and keep the account safe.
        After executing this, you need to log in again to use the commands.
        """

        self.session.get(f"{self.url}/auth/logout/")
        self.session.cookies.clear()
        self.user_id = None
    
    def _handle_requests(self, method, url, data=None, error_message='Something went wrong.'):
        """This function will handle requests."""

        if method == 'GET':
            response = self.session.get(url)

            if response.status_code != 200:
                raise Exception(f"Something went wrong. [Status Code: {response.status_code}]")
            else:
                return response.text
        elif method == 'POST':
            response = self.session.post(url, json=data)

            if response.status_code == 429:
                raise too_many_requests("Chill, Cowboy! You are doing this too much, wait a little. [Status Code: 429]")
            elif "Unauthorized" in response.text:
                raise unauthorized_request("Unauthorized Request. You don't have permission to perform that action. [Status Code: 401]")
            elif response.status_code == 400:
                raise Exception(f"Bad Request. Please check If your level is above 3. [Status Code: 400]")
            elif 'Disallowed' in response.text:
                raise disallowed_url_input("Please do not put links in your message.")
            elif response.status_code not in (200, 201):
                raise Exception(f"Something went wrong! {error_message} [Status Code: {response.status_code}]")
        elif method == 'PUT':
            response = self.session.put(url, json=data)

            if response.status_code == 429:
                raise too_many_requests("Chill, Cowboy! You are doing this too much, wait a little. [Status Code: 429]")
            elif "Unauthorized" in response.text:
                raise unauthorized_request("Unauthorized Request. You don't have permission to perform that action. [Status Code: 401]")
            elif response.status_code == 400:
                raise Exception(f"Bad Request. Please check If your level is above 3. [Status Code: 400]")
            elif 'Disallowed' in response.text:
                raise disallowed_url_input("Please do not put links in your message.")
            elif response.status_code not in (200, 201, 204):
                raise Exception(f"Something went wrong! {error_message} [Status Code: {response.status_code}]")
        elif method == 'DELETE':
            response = self.session.delete(url)

            if response.status_code == 429:
                raise too_many_requests("Chill, Cowboy! You are doing this too much, wait a little. [Status Code: 429]")
            elif "Unauthorized" in response.text:
                raise unauthorized_request("Unauthorized Request. You don't have permission to perform that action. [Status Code: 401]")
            elif response.status_code == 400:
                raise Exception(f"Bad Request. Please check If your level is above 3. [Status Code: 400]")
            elif response.status_code != 200:
                raise Exception(f"Something went wrong! [Status Code: {response.status_code}]")

    def post_feed_message(self, user_id : str, message : str):
        """
        Posts a message in an user's Feed.\n

        Parameters:
        ------------
            user_id (str) : ID of the Account.\n
            message (str) : Message to post.\n
        """

        self._handle_requests(method='POST', url=f"{self.url}/api/feed/{user_id}/", data={"profile_id": user_id, "status_message": message, "wait": True}, error_message=f'Failed to post a feed message. (user_id: {user_id} / message: {message})')

    def post_feed_comment(self, feed_id : str, message : str):
        """
        Posts a comment in an existing Feed.\n

        Parameters:
        ------------
            feed_id (str) : ID of the Feed.\n
            message (str) : Message to post.\n
        """

        self._handle_requests(method='POST', url=f"{self.url}/api/feed/{feed_id}/comment/", data={"comment": message}, error_message=f'Failed to post comment on a Feed. (feed_id: {feed_id} / message: {message})')

    def post_game_comment(self, game_id : str, message : str):
        """ 
        Posts a comment in a Game.\n

        Parameters:
        ------------
            game_id (str) : ID of the Game.\n
            message (str) : Message to post.\n
        """

        self._handle_requests(method='POST', url=f"{self.url}/game/{game_id}/comment/",data={"comment": message}, error_message=f'Failed to post comment on a Game. (game_id: {game_id} / message: {message})')

    def post_model_comment(self, model_id : str, message : str):
        """
        Posts a comment in a Model.\n

        Parameters:
        ------------
            model_id (str) : ID of the Model.\n
            message (str) : Message to post.\n
        """

        self._handle_requests(method='POST', url=f"{self.url}/model/market/i-{model_id}/comment/", data={"comment":message}, error_message=f'Failed to post comment on a Model. (model_id: {model_id} / message: {message})')

    def post_avatar_comment(self, avatar_id : str, message : str):
        """ 
        Posts a comment in an Avatar.\n

        Parameters:
        ------------
            avatar_id (str) : ID of the Avatar.\n
            message (str) : Message to post.\n
        """

        self._handle_requests(method='POST', url=f"{self.url}/model/market/a-{avatar_id}/comment/", data={"comment":message}, error_message=f'Failed to post comment on a avatar. (avatar_id: {avatar_id} / message: {message})')

    def post_news_comment(self, news_id : str, message : str):
        """   
        Posts a message in a News post.\n

        Parameters:
        ------------
            news_id (str) : ID of the News Post.\n
            message (str) : Message to post.\n
        """

        self._handle_requests(method='POST', url=f"{self.url}/api/news/{news_id}/comment/", data={"comment":message}, error_message=f'Failed to post comment on a news post. (news_id: {news_id} / message: {message})')

    def delete_game_comment(self, game_id : str, comment_id : str):
        """
        Deletes a Game comment.\n

        Parameters:
        ------------
            game_id (str) : ID of the Game.\n
            comment_id (str) : ID of the comment.\n
        """

        self._handle_requests(method='DELETE', url=f"{self.url}/game/{game_id}/comment/{comment_id}/", error_message=f'Failed to delete a Game comment. (game_id {game_id} / comment_id: {comment_id})')
    
    def delete_model_comment(self, model_id : str, comment_id : str):
        """
        Deletes a Model comment.\n

        Parameters:
        ------------
            model_id (str) : ID of the Model.\n
            comment_id (str) : ID of the comment.\n
        """

        self._handle_requests(method='DELETE', url=f"{self.url}/model/market/i-{model_id}/comment/{comment_id}/", error_message=f'Failed to delete a Model comment. (model_id: {model_id} / comment_id: {comment_id})')
    
    def delete_avatar_comment(self, avatar_id : str, comment_id : str):
        """
        Deletes an Avatar comment.\n

        Parameters:
        ------------
            avatar_id (str) : ID of the Avatar.\n
            comment_id (str) : ID of the comment.\n
        """

        self._handle_requests(method='DELETE', url=f"{self.url}/model/market/a-{avatar_id}/comment/{comment_id}/", error_message=f'Failed to delete an Avatar comment. (avatar_id: {avatar_id} / comment_id: {comment_id})')

    def delete_feed_post(self, user_id : str, feed_id : str):
        """
        Deletes a Feed post.\n

        Parameters:
        ------------
            user_id (str) : ID of the user who posted.\n
            comment_id (str) : ID of the comment.\n
        """

        self._handle_requests(method='DELETE', url=f"{self.url}/api/feed/{user_id}/{feed_id}/", error_message=f'Failed to delete a Feed post. (user_id: {user_id} / feed_id: {feed_id})')

    def delete_feed_post_comment(self, feed_id : str, comment_id : str):
        """
        Deletes a Feed post comment.\n

        Parameters:
        ------------
            feed_id (str) : ID of the Feed Comment.\n
            comment_id (str) : ID of the comment.\n
        """

        self._handle_requests(method='DELETE', url=f"{self.url}/feed/{feed_id}/comment/{comment_id}/", error_message=f'Failed to delete a Feed comment. (feed_id: {feed_id} / comment_id: {comment_id})')

    def create_game(self, name : str, description='No description provided.', template='base'):
        """
        Creates an game.\n

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
        elif "Unauthorized" in response.text:
            raise unauthorized_request("Unauthorized Request. You don't have permission to perform that action. [Status Code: 401]")
        elif response.status_code == 400:
            raise Exception(f"Bad Request. [Status Code: 400]")
        elif response.status_code != 201:
            raise Exception(f"Something went wrong! [Status Code: {response.status_code}]")
        else:
            return response.json()

    def invite_member_to_game(self, game_id : str, user_id : str):
        """
        Invites a member to project.\n

        Parameters:
        ------------
            game_id (str) : ID of the Game.\n
            user_id (str) : ID of the User.\n
        """

        self._handle_requests(method='POST', url=f"{self.url}/game/{game_id}/member/",data={"game_id": game_id, "member_user_id":user_id}, error_message=f'Failed to invite member to the Game. (game_id: {game_id} / user_id: {user_id})')

    def send_friend_request(self, friend_id : str):
        """
        Sends a friend request to a user.\n

        Parameters:
        ----------
            friend_id (str) : ID of the User.\n
        """

        self._handle_requests(method='POST', url=f"{self.url}/user/{friend_id}/friend/",data={"friend_profile_id": friend_id,"profile_id": self.user_id,"user_id": friend_id}, error_message=f'Failed to send friend request. (friend_id: {friend_id})')

    def cancel_friend_request(self, friend_id : str):
        """ 
        Cancels a friend request.\n

        Parameters:
        ----------
            user_id (str) : ID of the User.
        """

        self._handle_requests(method='DELETE', url=f"{self.url}/user/{self.user_id}/friend/{friend_id}/", error_message=f'Failed to cancel friend request. (friend_id: {friend_id})')

    def purchase_model(self, model_id : str):
        """
        Purchases a Model from Shop.\n

        Parameters:
        ----------
            model_id (str) : ID of the Model.
        """

        self._handle_requests(method='POST', url=f"{self.url}/model/market/i-{model_id}/purchase/", error_message=f'Failed to purchase a Model. (model_id {model_id})')

    def purchase_avatar(self, avatar_id : str):
        """
        Purchases an avatar from the shop.\n

        Parameters:
        ----------
            avatar_id (str) : ID of the Avatar.
        """

        self._handle_requests(method='POST', url=f"{self.url}/model/market/a-{avatar_id}/purchase/", error_message=f'Failed to purchase Avatar. (avatar_id: {avatar_id})')

    def claim_elite_gold(self):
        """
        Claims daily Elite Gold.

        Returns an `Exception` If failed to claim the Gold.
        """

        self._handle_requests(method='POST', url=f"{self.url}/user/{self.user_id}/claim-daily-gold/", error_message=f'Failed to claim Daily Gold.')

    def reedem_coupon(self, coupon : str):
        """ 
        Reedems a coupon code.\n

        Parameters:
        ----------
            coupon (str) : Coupon.
        """

        self._handle_requests(method='POST', url=f"{self.url}/api/coupon/redeem/", data={"code": coupon}, error_message=f'Failed to reedem coupon. (coupon: {coupon})')

    def unlock_badge(self, badge_id : str):
        """
        Unlocks a Hidden Badge.\n

        Parameters:
        ----------
            badge_id (str) : Badge ID.
        """

        self._handle_requests(method='POST', url=f"{self.url}/user/{self.user_id}/badge/{badge_id}/read/", error_message=f'Failed to unlock a Hidden Badge. (badge_id: {badge_id})')

    def like_game(self, game_id : str):
        """
        Likes a Game.\n

        Parameters:
        ----------
            game_id (str) : Game ID.
        """

        self._handle_requests(method='POST', url=f"{self.url}/game/{game_id}/like/", error_message=f'Failed to like a Game. (game_id: {game_id})')

    def like_model(self, model_id : str):
        """
        Likes a Model.\n

        Parameters:
        ----------
            model_id (str) : Model ID.
        """

        self._handle_requests(method='POST', url=f"{self.url}/model/market/i-{model_id}/like/", error_message=f'Failed to like a Model. (model_id: {model_id})')

    def like_avatar(self, avatar_id : str):
        """
        Likes an Avatar.\n

        Parameters:
        ----------
            avatar_id (str) : Avatar ID.
        """

        self._handle_requests(method='POST', url=f"{self.url}/model/market/a-{avatar_id}/like/", error_message=f'Failed to like an Avatar. (avatar_id: {avatar_id})')

    def change_email(self, email : str):
        """
        Changes the email of your KoGaMa Account.\n

        Parameters:
        ----------
            email (str) : Email of the Account.
        """

        self._handle_requests(method='PUT', url=f"{self.url}/user/{self.user_id}/email/", data={"email":email}, error_message=f'Failed to change account email. (email: {email})')
        
    def change_username(self, username : str):
        """
        Changes the name of your KoGaMa Account.\n

        Parameters:
        ----------
            username (str) : Username.
        """

        self._handle_requests(method='PUT', url=f"{self.url}/user/{self.user_id}/username/", data={"username":username}, error_message=f'Failed to change account username. (username: {username})')

    def get_game_comments(self, game_id : str, page='1', count='10'):
        """
        Returns all of the game comments.\n

        Parameters:
        ----------
            game_id (str) : Game ID.
            count (str)   : Number of comments that should return in the response. (Default 10)
            page (str)    : Number of the page. (Default 1)
        """

        return self._handle_requests(method='GET', url=f"{self.url}/game/{game_id}/comment/?page={page}&count={count}", data=None, error_message=f'Failed to get Game comments. (game_id: {game_id} / page: {page} / count: {count})')

    def get_model_comments(self, model_id : str, page='1', count='10'):
        """
        Returns all of the model comments.\n

        Parameters:
        ----------
            model_id (str) : Model ID.\n
            count (str)   : Number of comments that should return in the response. (Default 10)\n
            page (str)    : Number of the page. (Default 1)\n
        """

        return self._handle_requests(method='GET', url=f"{self.url}/model/market/i-{model_id}/comment/?page={page}&count={count}", error_message=f'Failed to get Model comments. (model_id: {model_id} / page: {page} / count: {count})')

    def get_avatar_comments(self, avatar_id : str, page='1', count='10'):
        """
        Returns all of the avatar comments.\n

        Parameters:
        ----------
            avatar_id (str) : Avatar ID.\n
            count (str)   : Number of comments that should return in the response. (Default 10)\n
            page (str)    : Number of the page. (Default 1)\n
        """

        return self._handle_requests(method='GET', url=f"{self.url}/model/market/a-{avatar_id}/comment/?page={page}&count={count}", error_message=f'Failed to get Avatar comments. (avatar_id: {avatar_id} / page: {page} / count: {count})')
    
    def get_user_feed_posts(self, user_id : str, page='1', count='10'):
        """
        Returns all of the user feed posts.\n

        Parameters:
        ----------
            user_id (str) : User ID.\n
            count (str)   : Number of feed posts that should return in the response. (Default 10)\n
            page (str)    : Number of the page. (Default 1)\n
        """

        return self._handle_requests(method='GET', url=f"{self.url}/api/feed/{user_id}/?page={page}&count={count}", error_message=f'Failed to get user feed posts. (user_id: {user_id} / page: {page} / count: {count})')

    def get_feed_post_comments(self, feed_id : str, page='1', count='10'):
        """
        Returns all of the feed post comments.\n

        Parameters:
        ----------
            feed_id (str) : Feed ID.\n
            count (str)   : Number of feed post comments that should return in the response. (Default 10)\n
            page (str)    : Number of the page. (Default 1)\n
        """

        return self._handle_requests(method='GET', url=f"{self.url}/api/feed/{feed_id}/comment/?page={page}&count={count}", error_message=f'Failed to get user feed post comments. (feed_id: {feed_id} / page: {page} / count: {count})')

    def get_news_comments(self, news_id : str, page='1', count='10'):
        """
        Returns all of the news comments.\n

        Parameters:
        ----------
            news_id (str) : News ID.\n
            count (str)   : Number of comments that should return in the response. (Default 10)\n
            page (str)    : Number of the page. (Default 1)\n
        """

        return self._handle_requests(method='GET', url=f"{self.url}/api/news/{news_id}/comment/?page={page}&count={count}", error_message=f'Failed to get news comments. (news_id: {news_id} / page: {page} / count: {count})')
    
    def get_user_badges_ids(self, user_id : str, page='1', count='10'):
        """
        Returns all of the user badges ids.\n

        Parameters:
        ----------
            user_id (str) : User ID.\n
            count (str)   : Number of badges ids that should return in the response. (Default 10)\n
            page (str)    : Number of the page. (Default 1)\n
        """

        return self._handle_requests(method='GET', url=f"{self.url}/user/{user_id}/badge/?page={page}&count={count}", error_message=f'Failed to get user badges ids. (user_id: {user_id} / page: {page} / count: {count})')

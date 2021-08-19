''''
 * An API wrapper for KoGaMa re-written in Python.\n
 * Scripted by: TheNoobPro44 (With the help of: MD & Tokeeto!)\n
 * Originaly Made By: Ars3ne.\n
'''
import requests
import json
import time
from .Exceptions import DisallowedURlInput, NotAValidServer, FailedLogin, TooMuchRequests, ReasonNotFound, TemplateNotFound

class KoGaMa:
    """You're using version 0.5.4!"""
    def __init__(self, server):
      if server.lower() not in ('www', 'br', 'friends'):
          raise NotAValidServer('Not a valid server!')
        
      self.user_id = None
      self.url = {'br': 'https://kogama.com.br',
                  'www': 'https://www.kogama.com',
                  'friends': 'https://friends.kogama.com',
                  }[server.lower()]

      self.session = requests.Session()

    def Login(self, username, password):
        """
        - Makes login in a KoGaMa account, given the Username & Password.\n

        - Returns True, If the user has logged in.\n
        - Returns False, If the user could not login.\n
        
        Parameters:
        ----------
          username : str\n
             User's account name.\n
          password : str\n
             User's account password.\n
        """
        response = self.session.post(f"{self.url}/auth/login/", json={"username": username, "password": password})
        if 'error' or 'banned' not in response:
          return True
        else:
          return False
        if response.status_code != 200:
          raise FailedLogin(f"Please check If your Password or Username is correct and try again.. (Error Code: {response.status_code})")
        else:
          self.user_id = response.json()['data']['id']

    def Logout(self):
      """
      - Logout a user from his KoGaMa account.\n
      - Returns True, If the user has logged out.\n
      
      Parameters:
      ----------
        No Parameters..
      """
      self.session.get(f"{self.url}/auth/logout/")
      self.session.cookies.clear()
      return True

    def PostFeed(self, userID, message):
      """
        - Post a message in user's Feed.\n

        - Returns True, If the message has been sent.\n
        - Returns False, If message fails to send.\n
        
        Parameters:
        -----------
          userID : str\n
             User's account ID.\n
          message : str\n
             Message that will be sent.\n
      """
      response = self.session.post(f"{self.url}/api/feed/{userID}/", json={"status_message": message,"profile_id": userID,"wait": True})
      response2 = response.text
      if response.status_code != 200:
        return False
      else:
        return True
      if response.status_code != 200:
          raise Exception(f"Failed to Post a message in [User ID: {userID}] Feed, make sure he's your friend. (Error Code: {response.status_code})")
      if 'Disallowed' in response2:
        raise DisallowedURlInput("Please do not put links in your message!")

    def GetPostComments(self, postID):
        """
        - Get comments from a post and return it.\n
        
        Parameters:
        ----------
          postID : str\n
            ID of the Post.\n
        """
        response = self.session.get(f'{self.url}/api/feed/{postID}/comment/')
        response2 = json.loads(response.text)
        return response2
    
    def PostFeedComment(self, FeedID, message):
        """
        - Post a comment in a Feed.\n

        - Returns True, If the comment has been posted.\n
        - Returns False, If fails to post a comment.\n
      
        Parameters:
        ----------
          FeedID : str\n
            ID of the Feed.\n
          message : str\n
            Message that will be posted.\n
        """
        response = self.session.post(f"{self.url}/api/feed/{FeedID}/comment/", json={"comment":message})
        response2 = response.text
        if response.status_code == 429:
            raise TooMuchRequests("Chill, Cowboy! You are doing this too much, wait a little.")
        elif response.status_code == 201:
            return True
        else:
            return False
        if response.status_code != 201:
            raise Exception(f"Failed to post comment in [Feed ID: {FeedID}].. (Error Code: {response.status_code})")
        if 'Disallowed' in response2:
          raise DisallowedURlInput("Please do not put links in your message!")

    def PostGameComment(self, GameID, message):
      """
      - Post a comment in a Game.\n

      - Returns True, If the comment has been posted.\n
      - Returns False, If fails to post a comment.\n
      
      Parameters:
      ----------
        GameID : str\n
          ID of the Game.\n
        message : str\n
          Message that will be posted.\n
      """
      response = self.session.post(f"{self.url}/game/{GameID}/comment/", json={"comment":message})
      response2 = response.text
      if response.status_code == 429:
        raise TooMuchRequests("Chill, Cowboy! You are doing this too much, wait a little.")
      if response.status_code == 201:
        return True
      else:
        return False
      if response.status_code != 201:
        raise Exception(f"Failed to post comment in [Game ID: {GameID}].. (Error Code: {response.status_code})")
      if 'Disallowed' in response2:
        raise DisallowedURlInput("Please do not put links in your message!")

    def PostModelComment(self, ModelID, message):
      """
      - Post a comment in a Model.\n

      - Returns True, If the comment has been posted.\n
      - Returns False, If fails to post a comment.\n
      
      Parameters:
      ----------
        ModelID : str\n
          ID of the Model.\n
        message : str\n
          Message that will be posted.\n
      """
      response = self.session.post(f"{self.url}/model/market/i-{ModelID}/comment/", json={"comment":message})
      response2 = response.text
      if response.status_code == 429:
        raise TooMuchRequests("Chill, Cowboy! You are doing this too much, wait a little.")
      if response.status_code == 201:
        return True
      else:
        return False
      if response.status_code != 201:
        raise Exception(f"Failed to post comment in [Model ID: {ModelID}].. (Error Code: {response.status_code})")
      if 'Disallowed' in response2:
        raise DisallowedURlInput("Please do not put links in your message!")
    
    def PostAvatarComment(self, AvatarID, message):
      """
      - Post a comment in a Avatar.\n

      - Returns True, If the comment has been posted.\n
      - Returns False, If fails to post a comment.\n

      Parameters:
      ----------
        AvatarID : str\n
          ID of the Avatar.\n
        message : str\n
          Message that will be posted.\n
      """
      response = self.session.post(f"{self.url}/model/market/a-{AvatarID}/comment/", json={"comment":message})
      response2 = response.text
      if response.status_code == 429:
        raise TooMuchRequests("Chill, Cowboy! You are doing this too much, wait a little.")
      if response.status_code == 201:
        return True
      else:
        return False
      if response.status_code != 201:
        raise Exception(f"Failed to post comment in [Avatar ID: {AvatarID}].. (Error Code: {response.status_code})")
      if 'Disallowed' in response2:
        raise DisallowedURlInput("Please do not put links in your message!")

    def PostNewsComment(self, newsID, message):
        """
        - Post a comment in a News Page.\n

        - Returns True, If the comment has been posted.\n
        - Returns False, If fails to post a comment.\n
        
        Parameters:
        ----------
          newsID : int / str\n
            ID of the News.\n
          message : str\n
            Message that will be posted.\n
        """
        response = self.session.post(f"{self.url}/api/news/{newsID}/comment/", json={"comment":message})
        response2 = response.text
        if response.status_code == 429:
            raise TooMuchRequests("Chill, Cowboy! You are doing this too much, wait a little.")
        if response.status_code == 201:
            return True
        elif response.status_code != 201:
            return False
        if response.status_code != 201:
            raise Exception(f"Failed to post comment in [News ID: {newsID}].. (Error Code: {response.status_code})")
        if 'Disallowed' in response2:
          raise DisallowedURlInput("Please do not put links in your message!")
            
    def DeleteGameComment(self, GameID, CommentID):
        """
        - Deletes a comment in a Game.\n

        - Returns True, If the comment has been deleted.\n
        - Returns False, If fails to delete the comment.\n
        
        Parameters:
        ----------
          GameID : str\n
            ID of the Game.\n
          CommentID : str\n
            ID of the Comment.\n
        """
        url2 = self.url
        response = self.session.delete(f"{url2}/game/{GameID}/comment/{CommentID}/")
        response2 = response.text
        if response.status_code == 200:
            return True
        elif response.status_code != 200:
            return False
        if response.status_code != 200:
            raise Exception(f"Failed to delete comment in [Comment ID: {CommentID}].. (Error Code: {response.status_code})")
        if "Unauthorized" in response2:
            raise Exception("Unauthorized.")
    
    def DeleteFeedComment(self, FeedID, CommentID):
        """
        - Deletes a comment in a Game.\n
        
        Returns True, If the comment has been deleted.\n
        Returns False, If fails to delete the comment.\n
        
        Parameters:
        ----------
        FeedID : int / str
            ID of the Feed.
        CommentID : int / str
            ID of the Comment.
        """
        response = self.session.delete(f"{self.url}/feed/{FeedID}/comment/{FeedID}/")
        response2 = response.text
        if response.status_code == 200:
            return True
        else:
            return False
        if response.status_code != 200:
            raise Exception(f"Failed to delete comment in [Comment ID: {CommentID}].. (Error Code: {response.status_code})")
        elif "Unauthorized" in response2:
            raise Exception("Unauthorized.")
            
    def CreateGame(self, Name, Desc, Template):
      """
      - Creates a game.\n

      - Returns True, If the game has been created.\n
      - Returns False, If fails to create a game.\n
      
      Parameters:
      ----------
        Name : str\n
          Name of your Game.\n
        Desc : str\n
          Description of your Game.\n
        Template : str\n
          Template of your Game.\n
      """
      tmplt = Template.lower()
      tmplt2 = tmplt.replace(" ", "_")
      templates = {"base_template": 3, "city_template": 4, "island_template": 5, "parkour_template": 6}
      try:
        tn = templates[tmplt2]
      except KeyError:
        raise TemplateNotFound("This template doesn't exist!")
      response = self.session.post(f"{self.url}/game/", json={"name":Name,"description":Desc,"proto_id":tn})
      stscd = response.status_code
      if stscd == 201:
        return True
      else:
        return False
      if response.status_code != 201:
        raise Exception(f"Failed to create game, [Game Name: {Name}]; [Game Description: {Desc}]; [Template: {Template}].. (Error Code: {response.status_code})")

    def InviteMemberToGame(self, GameID, UserID):
      """
      - Invites a member to a Project or Game.\n

      - Returns True, If the user has been invited.\n
      - Returns False, If fails to invite a user.\n
      
      Parameters:
      ----------
        GameID : str\n
          ID of the Game.\n
        UserID : str\n
          ID of the User.\n
      """
      response = self.session.post(f"{self.url}/game/{GameID}/member/", json={"game_id":GameID,"member_user_id":UserID})
      stscd = response.status_code
      if stscd == 201:
        return True
      else:
        return False
      if response.status_code != 201:
        raise Exception(f"Failed to invite [User ID: {UserID}] to a game, [Game ID: {GameID}].. (Error Code: {response.status_code})")
    
    def SendFriendRequest(self, friendID):
        """
        - Sends a friend request to a user.\n

        - Returns True, If a friend request has been sent.\n
        - Returns False, If fails to send a friend request.\n
        
        Parameters:
        ----------
          UserID : str\n
            ID of the User.\n
        """
        response = self.session.post(f"{self.url}/user/{friendID}/friend/", json={"friend_profile_id":friendID,"profile_id":self.user_id,"user_id":friendID})
        stscd = response.status_code
        if stscd == 201:
            return True
        elif stscd != 201:
            return False
        if response.status_code != 201:
            raise Exception(f"Failed to send friend request to [Friend ID: {friendID}].. (Error Code: {response.status_code})")
            
    def CancelFriendRequest(self, friendID):
      """
      - Cancels a friend request.\n

      - Returns True, If a friend request has been cancelled.\n
      - Returns False, If fails to cancel a friend request.\n
      
      Parameters:
      ----------
        UserID : str\n
          ID of the User.\n
      """
      response = self.session.delete(f"{self.url}/user/{self.user_id}/friend/{friendID}/")
      stscd = response.status_code
      if stscd == 201:
         return True
      else:
         return False
      if response.status_code != 201:
        raise Exception(f"Failed to cancel friend request, [Friend ID: {friendID}].. (Error Code: {response.status_code})")
                                
    def PurchaseModel(self, modelID):
       """
       - Purchases a Model from Shop.\n
       
       - Returns True, If model has been bought.\n
       - Returns False, If fails to buy model.\n
       
       Parameters:
       ----------
        modelID : str\n
          ID of the Model.\n
       """       
       response = self.session.post(f"{self.url}/model/market/i-{modelID}/purchase/")
       stscd = response.status_code
       if stscd == 201:
         return True
       else:
         return False
       if response.status_code != 201:
          raise Exception(f"Failed to purchase model, [Model ID: {modelID}].. (Error Code: {response.status_code})")
                                     
    def PurchaseAvatar(self, avatarID):
       """
       - Purchases a Avatar from Shop.\n
       
       - Returns True, If avatar has been bought.\n
       - Returns False, If fails to buy avatar.\n
       
       Parameters:
       ----------
          avatarID : str\n
            ID of the Avatar.\n
       """
       response = self.session.post(f"{self.url}/model/market/a-{avatarID}/purchase/")
       stscd = response.status_code
       if stscd == 201:
         return True
       else:
         return False
       if response.status_code != 201:
          raise Exception(f"Failed to purchase avatar, [Avatar ID: {avatarID}].. (Error Code: {response.status_code})")
                                 
    def ClaimEliteGold(self):
       """
       - Claims daily Elite Gold.\n 
       
       - Returns True, If the gold has been collected.\n
       - Returns False, If fails to collect gold.\n
       
       Parameters:
       ----------
        None..\n
       """
       response = self.session.post(f"{self.url}/user/{self.user_id}/claim-daily-gold/")
       stscd = response.status_code
       if stscd == 200:
        return True
       else:
        return False
       if response.status_code != 200:
          raise Exception(f"Failed to purchase claim elite gold.. (Error Code: {response.status_code})")

    def ReedemCoupon(self, coupon):
      """
      - Reedems a coupon code.\n
       
      - Returns True, If the coupon has been reedemed.\n
      - Returns False, If fails to reedem coupon.\n
       
      Parameters:
      ----------
      coupon : str\n
        Coupon Code.\n
      """
      response = self.session.post(f"{self.url}/api/coupon/redeem/", json={"code": coupon})
      stscd = response.status_code
      if stscd == 201:
        return True
      else:
         return False
      if response.status_code != 201:
        raise Exception(f"Failed to reedem coupon, [Coupon: {coupon}].. (Error Code: {response.status_code})")

    def UnlockBadge(self, badge):
       """
       - Unlocks a Hidden Badge.\n
       
       - Returns True, If the badge has been unlocked.\n
       - Returns False, If fails to unlock badge.\n
       
       Parameters:
       -----------
        badge : str\n
          Badge ID.\n
      
       Note:
       ----------
        This feature is still in development and will likely be finished in future versions..\n
       """
       response = self.session.post(f"{self.url}/user/{self.user_id}/badge/{badge}/read/")
       stscd = response.status_code
       if stscd == 201:
        return True
       else:
        return False
       if response.status_code != 201:
          raise Exception(f"Failed to unlock badge, [Badge ID: {badge}].. (Error Code: {response.status_code})")
    
    def LikeGame(self, GameID):
      """
       - Likes an game.\n
       
       - Returns True, If the the game has been liked.\n
       - Returns False, If fails to like the game.\n
       
       Parameters:
       ----------
        GameID : str\n
          ID of the game.\n
      """
      response = self.session.post(f"{self.url}/game/{GameID}/like/")
      stscd = response.status_code
      if stscd == 201:
        return True
      else:
        return False
      if response.status_code != 201:
        raise Exception(f"Failed to Like game, [Game ID: {GameID}].. (Error Code: {response.status_code})")
      
    def LikeModel(self, ModelID):
      """
       - Likes an Model.\n
       
       - Returns True, If the the model has been liked.\n
       - Returns False, If fails to like the model.\n
       
       Parameters:
       ----------
        ModelID : str\n
          ID of the model.\n
      """
      response = self.session.post(f"{self.url}/model/market/i-{ModelID}/like/")
      stscd = response.status_code
      if stscd == 201:
        return True
      else:
        return False
      if response.status_code != 201:
        raise Exception(f"Failed to Like model, [Model ID: {ModelID}].. (Error Code: {response.status_code})")
    
    def LikeAvatar(self, AvatarID):
      """
       - Likes an avatar.\n
       
       - Returns True, If the the avatar has been liked.\n
       - Returns False, If fails to like the avatar.\n
       
       Parameters:
       ----------
        AvatarID : str\n
          ID of the model.\n
      """
      response = self.session.post(f"{self.url}/model/market/a-{AvatarID}/like/")
      stscd = response.status_code
      if stscd == 201:
        return True
      else:
        return False
      if response.status_code != 201:
        raise Exception(f"Failed to Like avatar, [Avatar ID: {AvatarID}].. (Error Code: {response.status_code})")
    
    def run(self):
       """
       - Keeps the player alive.\n 
       
       Parameters:
       ----------
        None..\n
        
       Note:
       ----------
        This feature is still in development, and might not work..\n
       """
       j = f"/profile/{self.user_id}/"
       while True:
         self.session.post(f"{self.url}/user/{self.user_id}/pulse/", json={"status":"active","location": j})
         time.sleep(21)

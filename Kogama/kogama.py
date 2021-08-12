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

        Returns True, If the user has logged in.\n
        Returns False, If the user could not login.\n

        Parameters:
        ----------
          username : str
             User's account name.
          password : str
             User's account password.
        """
        data = {"username": username, "password": password}
        response = self.session.post(f"{self.url}/auth/login/", json=data)
        if 'error' or 'banned' not in response:
          return True
        elif 'error' or 'banned' in response:
          return False
        if response.status_code != 200:
          raise FailedLogin(f"Please check If your Password / Username is correct and try again.. (Error Code: {response.status_code})")
        else:
          self.user_id = response.json()['data']['id']

    def Logout(self):
      """
      - Logout a user from his KoGaMa account.\n

      Returns True, If the user has logged out.\n
      
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

        Returns True, If the message has been sent.\n
        Returns False, If message fails to send.\n
        
        Parameters:
        ----------
          userID : int / str
             ID of the user.
          message : str
             Message that will be posted.
        """
        url2 = self.url
        uid = userID
        data = {"status_message": message,"profile_id": userID,"wait": True}
        response = self.session.post(f"{url2}/api/feed/{uid}/", json=data)
        response2 = response.text
        if response.status_code != 200:
          return False
        if response.status_code != 200:
            raise Exception(f"Failed to Post a message in [User ID: {userID}] feed, make sure he's your friend. (Error Code: {response.status_code})")
        if response.status_code == 200:
          return True
        if 'Disallowed' in response2:
          raise DisallowedURlInput("Please do not put links in your message!")

    def ReportUser(self, userID, reason):
      """
      - Feature has been removed.

      Notes:
      ----------
        Due to developers planning to remove this feature, we'll deactivate it..
      """
      raise Exception("Hey! Due to developers planning removing the report button in the future, we'll deactivate this function.. We hope you understand!")

    # Comments Category..
    
    def GetPostComments(self, postID):
        """
        - Get comments from a post and return it.\n
        
        Parameters:
        ----------
          postID : int / str
             ID of the Post.
        """
        url2 = self.url
        response = self.session.get(f'{url2}/api/feed/{postID}/comment/')
        response2 = json.loads(response.text)
        gfc = response2["data"][0]["_data"]
        gfc2 = json.loads(gfc)
        gfc3 = gfc2["data"]
        return gfc3
    
    def PostFeedComment(self, message, FeedID):
        """
        - Post a comment in a Feed.\n

        Returns True, If the comment has been posted.\n
        Returns False, If fails to post a comment.\n
      
        Parameters:
        ----------
            FeedID : int / str
                ID of the Feed.
            message : str
                Message that will be posted.
        """
        url2 = self.url
        data = {"comment":message}
        response = self.session.post(f"{url2}/api/feed/{FeedID}/comment/", json=data)
        if response.status_code == 429:
            raise TooMuchRequests("Chill, Cowboy! You are doing this too much, wait a little.")
        if response.status_code == 201:
            return True
        elif response.status_code != 201:
            return False
        if response.status_code != 201:
            raise Exception(f"Failed to post comment in [Feed ID: {FeedID}].. (Error Code: {response.status_code})")

    def PostGameComment(self, GameID, message):
      """
      - Post a comment in a Game.\n

      Returns True, If the comment has been posted.\n
      Returns False, If fails to post a comment.\n
      
      Parameters:
      ----------
        GameID : int / str
            ID of the Game.
        message : str
            Message that will be posted.
      """
      url2 = self.url
      data = {"comment":message}
      response = self.session.post(f"{url2}/game/{GameID}/comment/", json=data)
      response2 = response.text
      if response.status_code == 429:
        raise TooMuchRequests("Chill, Cowboy! You are doing this too much, wait a little.")
      if response.status_code == 201:
        return True
      elif response.status_code != 201:
        return False
      if response.status_code != 201:
        raise Exception(f"Failed to post comment in [Game ID: {GameID}].. (Error Code: {response.status_code})")

    def PostModelComment(self, ModelID, message):
      """
      - Post a comment in a Model.\n

      Returns True, If the comment has been posted.\n
      Returns False, If fails to post a comment.\n
      
      Parameters:
      ----------
        ModelID : int / str
            ID of the Model.
        message : str
            Message that will be posted.
      """
      url2 = self.url
      data = {"comment":message}
      response = self.session.post(f"{url2}/model/market/i-{ModelID}/comment/", json=data)
      response2 = response.text
      if response.status_code == 429:
        raise TooMuchRequests("Chill, Cowboy! You are doing this too much, wait a little.")
      if response.status_code == 201:
        return True
      elif response.status_code != 201:
        return False
      if response.status_code != 201:
        raise Exception(f"Failed to post comment in [Model ID: {ModelID}].. (Error Code: {response.status_code})")
    
    def PostAvatarComment(self, AvatarID, message):
      """
      - Post a comment in a Avatar.\n

      Returns True, If the comment has been posted.\n
      Returns False, If fails to post a comment.\n

      Parameters:
      ----------
        AvatarID : int / str
            ID of the Avatar.
        message : str
            Message that will be posted.

      """
      url2 = self.url
      data = {"comment": message}
      response = self.session.post(f"{url2}/model/market/a-{AvatarID}/comment/", json=data)
      response2 = response.text
      if response.status_code == 429:
        raise TooMuchRequests("Chill, Cowboy! You are doing this too much, wait a little.")
      if response.status_code == 201:
        return True
      elif response.status_code != 201:
        return False
      if response.status_code != 201:
        raise Exception(f"Failed to post comment in [Avatar ID: {AvatarID}].. (Error Code: {response.status_code})")

    def PostNewsComment(self, newsID, message):
        """
        - Post a comment in a News Page.\n
        
        Returns True, If the comment has been posted.\n
        Returns False, If fails to post a comment.\n
        
        Parameters:
        ----------
        newsID : int / str
            ID of the News.
        message : str
            Message that will be posted.
        """
        url2 = self.url
        data = {"comment":message}
        response = self.session.post(f"{url2}/api/news/{newsID}/comment/", json=data)
        response2 = response.text
        if response.status_code == 429:
            raise TooMuchRequests("Chill, Cowboy! You are doing this too much, wait a little.")
        if response.status_code == 201:
            return True
        elif response.status_code != 201:
            return False
        if response.status_code != 201:
            raise Exception(f"Failed to post comment in [News ID: {newsID}].. (Error Code: {response.status_code})") 
            
    def DeleteGameComment(self, GameID, CommentID):
        """
        - Deletes a comment in a Game.\n
        
        Returns True, If the comment has been deleted.\n
        Returns False, If fails to delete the comment.\n
        
        Parameters:
        ----------
        GameID : int / str
            ID of the Game.
        CommentID : int / str
            ID of the Comment.
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
        elif "Unauthorized" in response2:
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
        url2 = self.url
        response = self.session.delete(f"{url2}/feed/{FeedID}/comment/{FeedID}/")
        response2 = response.text
        if response.status_code == 200:
            return True
        elif response.status_code != 200:
            return False
        if response.status_code != 200:
            raise Exception(f"Failed to delete comment in [Comment ID: {CommentID}].. (Error Code: {response.status_code})")
        elif "Unauthorized" in response2:
            raise Exception("Unauthorized.")
            
    # Game Category..
    
    def CreateGame(self, Name, Desc, Template):
      """
      - Creates a game.\n

      Returns True, If the game has been created.\n
      Returns False, If fails to create a game.\n
      
      Parameters:
      ----------
        Name : str
            Name of your Game.
        Desc : str
            Description of your Game.
        Template : str
            Template of your Game.
      """
      url2 = self.url
      tmplt = Template.lower()
      tmplt2 = tmplt.replace(" ", "_")
      templates = {"base_template": 3, "city_template": 4, "island_template": 5, "parkour_template": 6}
      try:
        tpl = templates[tmplt2]
      except KeyError:
        raise TemplateNotFound("This template doesn't exist!")
      tn = templates[tmplt2]
      data = {"name":Name,"description":Desc,"proto_id":tn}
      response = self.session.post(f"{url2}/game/", json=data)
      stscd = response.status_code
      if stscd == 201:
        return True
      if stscd != 201:
        return False
      if response.status_code != 201:
            raise Exception(f"Failed to create game, [Game Name: {Name}]; [Game Description: {Desc}]; [Template: {Template}].. (Error Code: {response.status_code})")

    def InviteMemberToGame(self, GameID, UserID):
      """
      - Invites a member to a Project or Game.\n

      Returns True, If the user has been invited.\n
      Returns False, If fails to invite a user.\n
      
      Parameters:
      ----------
        GameID : int / str
            ID of the Game.
        UserID : int / str
            ID of the User.
      """
      url2 = self.url
      data = {"game_id":GameID,"member_user_id":UserID}
      response = self.session.post(f"{url2}/game/{GameID}/member/", json=data)
      stscd = response.status_code
      if stscd == 201:
        return True
      if stscd != 201:
        return False
      if response.status_code != 201:
            raise Exception(f"Failed to invite [User ID: {UserID}] to a game, [Game ID: {GameID}].. (Error Code: {response.status_code})")
    
    # Friend Category..
    def SendFriendRequest(self, friendID):
        """
        - Sends a friend request to a user.\n

        Returns True, If a friend request has been sent.\n
        Returns False, If fails to send a friend request.\n
        
        Parameters:
        ----------
          UserID : int / str
             ID of the User.
        """
        url2 = self.url
        uid = self.user_id
        data = {"friend_profile_id":friendID,"profile_id":uid,"user_id":friendID}
        response = self.session.post(f"{url2}/user/{friendID}/friend/", json=data)
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

      Returns True, If a friend request has been cancelled.\n
      Returns False, If fails to cancel a friend request.\n
      
      Parameters:
      ----------
        UserID : int / str
            ID of the User.
      """
      url2 = self.url
      uid = self.user_id
      response = self.session.delete(f"{url2}/user/{uid}/friend/{friendID}/")
      stscd = response.status_code
      if stscd == 201:
         return True
      elif stscd != 201:
         return False
      if response.status_code != 201:
            raise Exception(f"Failed to cancel friend request, [Friend ID: {friendID}].. (Error Code: {response.status_code})")
        
    # Buy Category..
                                 
    def PurchaseModel(self, modelID):
       """
       - Purchases a Model from Shop.\n
       
       Returns True, If model has been bought.\n
       Returns False, If fails to buy model.\n
       
       Parameters:
       ----------
        modelID : int / str
            ID of the Model.
       """       
       url2 = self.url
       response = self.session.post(f"{url2}/model/market/i-{modelID}/purchase/")
       stscd = response.status_code
       if stscd == 201:
         return True
       elif stscd != 201:
         return False
       if response.status_code != 201:
            raise Exception(f"Failed to purchase model, [Model ID: {modelID}].. (Error Code: {response.status_code})")
                                     
    def PurchaseAvatar(self, avatarID):
       """
       - Purchases a Avatar from Shop.\n
       
       Returns True, If avatar has been bought.\n
       Returns False, If fails to buy avatar.\n
       
       Parameters:
       ----------
          avatarID : int / str
             ID of the Avatar.
       """
       url2 = self.url
       response = self.session.post(f"{url2}/model/market/a-{avatarID}/purchase/")
       stscd = response.status_code
       if stscd == 201:
         return True
       elif stscd != 201:
         return False
       if response.status_code != 201:
            raise Exception(f"Failed to purchase avatar, [Avatar ID: {avatarID}].. (Error Code: {response.status_code})")
    
    # Elite Category
                                     
    def ClaimEliteGold(self):
       """
        - Claims daily Elite Gold.\n 
       
       Returns True, If the gold has been collected.\n
       Returns False, If fails to collect gold.\n
       
       Parameters:
       ----------
         None..
       """
       url2 = self.url
       uid = self.user_id
       response = self.session.post(f"{url2}/user/{uid}/claim-daily-gold/")
       stscd = response.status_code
       if stscd == 200:
        return True
       elif stscd != 200:
        return False
       if response.status_code != 200:
            raise Exception(f"Failed to purchase claim elite gold.. (Error Code: {response.status_code})")
    # Badges Category
    
    def ReedemCoupon(self, coupon):
      """
      Reedems a coupon code.\n
       
      Returns True, If the coupon has been reedemed.\n
      Returns False, If fails to reedem coupon.\n
       
      Parameters:
      ----------
      coupon : str
          Coupon Code.
      """
      data = {"code": coupon}
      url2 = self.url
      response = self.session.post(f"{url2}/api/coupon/redeem/", json=data)
      stscd = response.status_code
      if stscd == 201:
        return True
      elif stscd != 201:
         return False
      if response.status_code != 201:
            raise Exception(f"Failed to reedem coupon, [Coupon: {coupon}].. (Error Code: {response.status_code})")

    def UnlockBadge(self, badge):
       """
       Unlocks a Hidden Badge.\n
       
       Returns True, If the badge has been unlocked.\n
       Returns False, If fails to unlock badge.\n
       
       Parameters:
       ----------
        badge : str / int
            Badge Number.
        
       Notes:
       ----------
        This feature is still in development and will likely be finished in future versions..
       """
       url2 = self.url
       uid = self.user_id
       response = self.session.post(f"{url2}/user/{uid}/badge/{badge}/read/")
       stscd = response.status_code
       if stscd == 201:
        return True
       elif stscd != 201:
        return False
       if response.status_code != 201:
            raise Exception(f"Failed to unlock badge, [Badge ID: {badge}].. (Error Code: {response.status_code})")
    
    def run(self):
       """
        - Keeps the player alive.\n 
       
       Parameters:
       ----------
        None..\n
        
       Notes:
       ----------
        This feature is still in development, and might not work..\n
       """
       userID = self.user_id
       url2 = self.url
       j = f"/profile/{userID}/"
       data = {"status":"active","location": j}
       while True:
         self.session.post(f"{url2}/user/{userID}/pulse/")
         time.sleep(21)

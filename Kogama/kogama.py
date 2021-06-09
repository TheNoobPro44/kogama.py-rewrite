''''
 * An API wrapper for KoGaMa re-written in Python. 
 * Scripted by: TheNoobPro44 (With the help of: MD & Tokeeto!)
 * Originaly Made By: Ars3ne.
'''
import os
import requests
import time
import json
from requests.sessions import Session, session
from .Exceptions import DisallowedURlInput, NotAValidServer, InvalidInformation, FailedLogin, FeedError, TooMuchRequests, ReasonNotFound, TemplateNotFound, FieldIsRequired

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
        Makes login in a KoGaMa account, given the Username & Password.

        Returns True, If the user has logged in.
        Returns False, If the user could not login.
        
        **Parameters**
        ----------
        username : str
            User's account name.
        password : str
            User's account password.
        """
        if username or password == " ":
            raise FieldIsRequired("Hey. This field is required, please input your username and password!")
        data = {"username": username, "password": password}
        response = self.session.post(f"{self.url}/auth/login/", json=data)
        if 'error' not in response:
          return True
        elif 'error' in response:
          return False
        
        if response.status_code != 200:
          raise FailedLogin("Please check If your Password / Username is correct and try again..")
        else:
          self.user_id = response.json()['data']['id']

    def Logout(self):
      """
      Logout a user from his KoGaMa account.

      Returns True, If the user has logged out.
      
      **Parameters**
      ----------
      No Parameters..
      """
      self.session.get(f"{self.url}/auth/logout/")
      self.session.cookies.clear()
      return True

    def PostFeed(self, userID, message):
        """
        Post a message in user's Feed.

        Returns True, If the message has been sent.
        Returns False, If message fails to send.
        
        **Parameters**
        ----------
        userID : int
            ID of the user.
        message : str
            Message that will be posted.
        """
        if message or userID == " ":
            raise FieldIsRequired("Hey. This field is required, please input your Message!")
        url2 = self.url
        uid = userID
        data = {"status_message": message,"profile_id": userID,"wait": True}
        response = self.session.post(f"{url2}/api/feed/{uid}/", json=data)
        response2 = response.text
        if response.status_code != 200:
          return False
        if response.status_code != 200:
          raise FeedError("An error ocurred while trying to post a message in your Feed!")
        if response.status_code == 200:
          return True
        if 'Disallowed' in response2:
          raise DisallowedURlInput("Please do not put links in your message!")

    def ReportUser(self, userID, reason):
      """
      Reports a users..

      Returns True, If the user has been reported.
      Returns False, If fails to report a user.
      **Parameters**
        ----------
        userID : int
            The ID of the user being reported.
        reason : str
            Reason of report.
      """
      if userID or reason == " ":
        raise FieldIsRequired("Hey. This field is required, please input the user ID or the Report Reason!")
      reports={"sharing_personal_information":1, "sharing_password": 2, "use_of_profanity": 3, "sexual_content_or_behaviour": 4, "violent_content": 5, "chain_messages": 6, "pretend_to_be_admin": 7, "personal_threats": 8, "cheats & hacking": 9, "other": 10, "using_cheat_tool": 11}
      url2 = self.url
      rl = reason.lower()
      rl2 = rl.replace(" ", "_")
      try:
        rl3 = reports[rl2]
      except KeyError:
        raise ReasonNotFound("This report reason is invalid!")
      rn = reports[rl2]
      response = self.session.post(f"{url2}/api/report/profile/{userID}/{rn}/")
      sc = response.status_code
      if sc == 429:
        raise TooMuchRequests("Chill Cowboy! You're sending alot of reports!")
      if sc != 201:
        return False

    # Comments Category..
    
    def GetPostComments(self, postID):
        """
        Get comments from a post and return it.
        
        **Parameters**
        ----------
        postID : int
            ID of the Post.
        """
        if postID == " ":
            raise FieldIsRequired("Hey. This field is required, please input your Post ID!")
        url2 = self.url
        response = self.session.get(f'{url2}/api/feed/{postID}/comment/')
        response2 = json.loads(response.text)
        gfc = response2["data"][0]["_data"]
        gfc2 = json.loads(gfc)
        gfc3 = gfc2["data"]
        return gfc3

    def PostGameComment(self, GameID, message):
      """
      Post a comment in a Game.

      Returns True, If the comment has been posted.
      Returns False, If fails to post a comment.
      
      **Parameters**
        ----------
        GameID : int
            ID of the Game.
        message : str
            Message that will be posted.
      """
      if GameID or message == " ":
          raise FieldIsRequired("Hey. This field is required, please input your Message or Game ID!")
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

    def PostModelComment(self, ModelID, message):
      """
      Post a comment in a Model.

      Returns True, If the comment has been posted.
      Returns False, If fails to post a comment.
      
      **Parameters**
        ----------
        ModelID : int
            ID of the Model.
        message : str
            Message that will be posted.
      """
      if message or ModelID == " ":
            raise FieldIsRequired("Hey. This field is required, please input your Message or Model ID!")
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
    
    def PostAvatarComment(self, AvatarID, message):
      """
      Post a comment in a Avatar.

      Returns True, If the comment has been posted.
      Returns False, If fails to post a comment.
      """
      if message or AvatarID == " ":
          raise FieldIsRequired("Hey. This field is required, please input your message or Avatar ID!")
      url2 = self.url
      data = {"comment":message}
      response = self.session.post(f"{url2}/model/market/a-{AvatarID}/comment/")
      response2 = response.text
      if response.status_code == 429:
        raise TooMuchRequests("Chill, Cowboy! You are doing this too much, wait a little.")
      if response.status_code == 201:
        return True
      elif response.status_code != 201:
        return False

    def PostNewsComment(self, newsID, message):
        """
        Post a comment in a News Page.
        
        Returns True, If the comment has been posted.
        Returns False, If fails to post a comment.
        
        **Parameters**
        ----------
        newsID : int
            ID of the News.
        message : str
            Message that will be posted.
        """
        if newsID or message == " ":
            raise FieldIsRequired("Hey. This field is required, please input your message or News ID!")
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
    # Game Category..
    
    def CreateGame(self, Name, Desc, Template):
      """
      Creates a game.

      Returns True, If the game has been created.
      Returns False, If fails to create a game.
      
      **Parameters**
        ----------
        Name : str
            Name of your Game.
        Desc : str
            Description of your Game.
        Template : str
            Template of your Game.
      """
      if Name == " ":
          raise FieldIsRequired("Hey. This field is required, please input your Game Name!")
      if Desc == " ":
          raise FieldIsRequired("Hey. This field is required, please input your Game Description!")
      if Template == " ":
          raise FieldIsRequired("Hey. This field is required, please input your Game Template!")
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

    def InviteMemberToGame(self, GameID, UserID):
      """
      Invites a member to a Project or Game.

      Returns True, If the user has been invited.
      Returns False, If fails to invite a user.
      
      **Parameters**
        ----------
        GameID : int
            ID of the Game.
        UserID : int
            ID of the User.
      """
      if GameID or UserID == " ":
          raise FieldIsRequired("Hey. This field is required, please input your Game ID or User ID!")
      url2 = self.url
      data = {"game_id":GameID,"member_user_id":UserID}
      response = self.session.post(f"{url2}/game/{GameID}/member/", json=data)
      stscd = response.status_code
      if stscd == 201:
        return True
      if stscd != 201:
        return False
    
    # Friend Category..
    def SendFriendRequest(self, friendID):
        """
        Sends a friend request to a user.

        Returns True, If a friend request has been sent.
        Returns False, If fails to send a friend request.
        
        **Parameters**
        ----------
        UserID : int
            ID of the User.
        """
        if friendID == " ":
            raise FieldIsRequired("Hey. This field is required, please input your friend's Profile ID!")
        url2 = self.url
        uid = self.user_id
        data = {"friend_profile_id":friendID,"profile_id":uid,"user_id":friendID}
        response = self.session.post(f"{url2}/user/{friendID}/friend/", json=data)
        stscd = response.status_code
        if stscd == 201:
            return True
        elif stscd != 201:
            return False
    def CancelFriendRequest(self, friendID):
      """
      Cancels a friend request.

      Returns True, If a friend request has been cancelled.
      Returns False, If fails to cancel a friend request.
      
      **Parameters**
        ----------
        UserID : int
            ID of the User.
      """
      if friendID == " ":
        raise FieldIsRequired("Hey. This field is required, please input your friend's Profile ID!")
      url2 = self.url
      uid = self.user_id
      response = self.session.delete(f"{url2}/user/{uid}/friend/{friendID}/")
      stscd = response.status_code
      if stscd == 201:
         return True
      elif stscd != 201:
         return False
        
    # Buy Category..
                                 
    def PurchaseModel(self, modelID):
       """
       Purchases a Model from Shop.
       
       Returns True, If model has been bought.
       Returns False, If fails to buy model.
       
       **Parameters**
        ----------
        modelID : int
            ID of the Model.
       """       
       if modelID == " ":
            raise FieldIsRequired("Hey. This field is required, please input the Model ID!")
       url2 = self.url
       response = self.session.post(f"{url2}/model/market/i-{modelID}/purchase/")
       stscd = response.status_code
       if stscd == 201:
         return True
       elif stscd != 201:
         return False
                                     
    def PurchaseAvatar(self, avatarID):
       """
       Purchases a Avatar from Shop.
       
       Returns True, If avatar has been bought.
       Returns False, If fails to buy avatar.
       
       **Parameters**
        ----------
        avatarID : int
            ID of the Avatar.
       """
       url2 = self.url
       if avatarID == " ":
            raise FieldIsRequired("Hey. This field is required, please input the Avatar ID!")
       response = self.session.post(f"{url2}/model/market/a-{avatarID}/purchase/")
       stscd = response.status_code
       if stscd == 201:
         return True
       elif stscd != 201:
         return False    
    
    # Elite Category                                
    def ClaimEliteGold(self):
       """
       Claims daily Elite Gold.
       
       Returns True, If the gold has been collected.
       Returns False, If fails to collect gold.
       
       **Parameters**
        ----------
        None
       """
       url2 = self.url
       uid = self.user_id
       response = self.session.post(f"{url2}/user/{uid}/claim-daily-gold/")
       stscd = response.status_code
       if stscd == 200:
        return True
       elif stscd != 200:
        return False
    
    # Badges Category
    def ReedemCoupon(self, coupon):
      """
      Reedems a coupon code.
       
      Returns True, If the coupon has been reedemed.
      Returns False, If fails to reedem coupon.
       
      **Parameters**
      ----------
      coupon : str
          Coupon Code.
      """
      if coupon == " ":
        raise FieldIsRequired("Hey. This field is required, please input the Coupon Code!")
      data = {"code": coupon}
      url2 = self.url
      response = self.session.post(f"{url2}/api/coupon/redeem/", json=data)
      stscd = response.status_code
      if stscd == 201:
        return True
      elif stscd != 201:
         return False                          

    def UnlockBadge(self, badge):
       """
       Unlocks a Hidden Badge.
       
       Returns True, If the badge has been unlocked.
       Returns False, If fails to unlock badge.
       
       **Parameters**
        ----------
        badge : str
            Badge Name.
        
        **Notes**
        ----------
        This feature is still in development and will likely be finished in future versions..
       """
       if badge == " ":
           raise FieldIsRequired("Hey. This field is required, please input the Badge Name!")
       bdg = badge.lower()
       bdg2 = bdg.replace(" ", "_")
       url2 = self.url
       uid = self.user_id
       badges = {"follow_instagram_kogama_official": 110, "follow_instagram": 110, "ifollowinstagram": 110}
       try:
          bdg3 = badges[bdg2]
       except KeyError:
           raise Exception("Badge Not Found!")
       bdg3 = badges[bdg2]
       response = self.session.post(f"{url2}/user/{uid}/badge/{bdg3}/read/")
       stscd = response.status_code
       if stscd == 201:
        return True
       elif stscd != 201:
        return False
    
    # Account Settings
    
    def AddEmail(self, email):
      """
      Adds email to account.
       
      Returns True, If the email has been changed.
      Returns False, If fails to change email.
       
      **Parameters**
      ----------
      email : str
          Account Email.
      """
      if email == " ":
          raise FieldIsRequired("Hey. This field is required, please input your Email!")
      data = {"email": email}
      url2 = self.url
      uid = self.user_id
      response = self.session.post(f"{url2}/user/{uid}/email/", json=data)
      stscd = response.status_code
      if stscd == 200:
        return True
      elif stscd != 200:
        return False

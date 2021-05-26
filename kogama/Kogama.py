''''
/*
 * An API wrapper for KoGaMa re-written in Python. 
 * Scripted by: TheNoobPro44 (With the help of: MD & Tokeeto)
 * Originaly Made By: Ars3ne
*/
'''
import os
import requests
import time
import json
from requests.sessions import Session, session
from Exceptions import DisallowedURlInput, NotAValidServer, InvalidInformation, FailedLogin, FeedError, TooMuchRequests, ReasonNotFound, TemplateNotFound

class KoGaMa:
    def __init__(self, server):
        if server.lower() not in ('www', 'br', 'friends'):
            raise Exception('Not a valid server')
        
        self.haslogged = False
        self.user_id = None
        self.url = {
            'br': 'https://kogama.com.br',
            'www': 'https://www.kogama.com',
            'friends': 'https://friends.kogama.com',
        }[server.lower()]

        self.session = requests.Session()

    def Login(self, username, password):
        """
        Makes login in a KoGaMa account, given the Username & Password.

        Returns True, If the user has logged in.
        Returns False, If the user could not login.
        """
        data = {"username": username, "password": password}
        response = self.session.post(f"{self.url}/auth/login", json=data)
        if 'error' not in response:
          return True
        elif 'error' in response:
          return False
        
        if response.status_code != 200:
          raise FailedLogin("Please check if your password / username is correct and try again..")
        else:
          self.haslogged = True
          self.user_id = response.json()['data']['id']

    def Logout(self):
      """
      Logout a user from his KoGaMa account.

      Returns True, If the user has logged out.
      """
      self.session.get(f"{self.url}/auth/logout/")
      self.session.cookies.clear()
      return True

    def PostFeed(self, message):
        data = {
            "status_message": message,
            "profile_id": self.user_id,
            "wait": True,
        }
        response = self.session.post(f"{self.url}/api/feed/{self.user_id}", json=data)
        response2 = response.text
        if response.status_code != 200:
          print(response.text)
        if 'Disallowed' in response2:
          raise DisallowedURlInput("Please do not put links in your message!")

    def ReportUser(self, userID, reason):
      rl = reason.lower()
      rl2 = rl.replace(" ", "_")
      reports={"sharing_personal_information":1, "sharing_password": 2, "use_of_profanity": 3, "sexual_content_or_behaviour": 4, "violent_content": 5, "chain_messages": 6, "pretend_to_be_admin": 7, "personal_threats": 8, "cheats & hacking": 9, "other": 10, "using_cheat_tool": 11}
      if not rl2 in reports:
        return False
      if not rl2 in reports:
        raise ReasonNotFound("This report reason is invalid!")
      else:
        return True
        rn = reports[rl2]
        response = self.session.post(f"{self.url}/api/report/profile/{self.userID}/{self.rn}/")
        sc = response.status_code
        if sc == 429:
          raise TooMuchRequests("Chill Cowboy! You're sending alot of reports!")
      
    def PostGameComment(self, GameID, message):
      data = {
        "comment":message
      }
      response = self.session.post(f"{self.url}/game/{self.GameID}/comment/", json=data)
      response2 = response.text
      if response.status_code == 429:
        raise TooMuchRequests("Chill, Cowboy! You are doing this too much, wait a little.")
      if response.status_code == 201:
        return True
      elif response.status_code != 201:
        return False
    
    def PostModelComment(self, ModelID, message):
      data = {
        "comment":message
      }
      response = self.session.post(f"{self.url}/model/market/i-{ModelID}/comment/", json=data)
      response2 = response.text
      if response.status_code == 429:
        raise TooMuchRequests("Chill, Cowboy! You are doing this too much, wait a little.")
      if response.status_code == 200:
        return True
      elif response.status_code != 200:
        return False

    def GetPostComments(self, postID):
        response = self.session.get(f'{self.url}/api/feed/{postID}/comment/')
        response2 = json.loads(response.text)
        gfc = response2["data"][0]["_data"]
        gfc2 = json.loads(gfc)
        gfc3 = gfc2["data"]
        print(gfc3)

    def PostAvatarComment(self, AvatarID, message):
      data = {
        "comment":message
      }
      response = self.session.post(f"{self.url}/model/market/a-{AvatarID}/comment/")
      response2 = response.text
      if response.status_code == 429:
        raise TooMuchRequests("Chill, Cowboy! You are doing this too much, wait a little.")
      if response.status_code == 201:
        return True
      elif response.status_code != 201:
        return False

    def CreateGame(self, Name, Desc, Template):
      tmplt = Template.lower()
      tmplt2 = tmplt.replace(" ", "_")
      templates = {"base_template": 3, "city_template": 4, "island_template": 5, "parkour_template": 6}
      if not tmplt2 in templates:
        raise TemplateNotFound("This template doesn't exist!")
      else:
        tn = templates[tmplt2]
        data = {
          "name":{self.Name},
          "description":{self.Desc},
          "proto_id":{self.tn}
        }
        response = self.session.post(f"{self.url}/game/", json=data)
        stscd = response.status_code
        if stscd == 201:
          return True
        if stscd != 201:
          return False

    def InviteMemberToGame(self, GameID, UserID):
      data = {
        "game_id":{self.GameID},
        "member_user_id":{self.UserID}
      }
      response = self.session.post(f"{self.url}/game/{self.GameID}/member/", json=data
    )
      stscd = response.status_code
      if stscd == 201:
        return True
      if stscd != 201:
        return False



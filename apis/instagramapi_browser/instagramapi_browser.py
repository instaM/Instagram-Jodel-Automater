#!/usr/bin/env python
# -*- coding: utf-8 -*-

import atexit
import datetime
import itertools
import json
import logging
import random
import signal
import sys
import os
if 'threading' in sys.modules:
    del sys.modules['threading']
import time
import requests



class InstagramAPI:
   
    url = 'https://www.instagram.com/'
    url_tag = 'https://www.instagram.com/explore/tags/%s/?__a=1'
    url_likes = 'https://www.instagram.com/web/likes/%s/like/'
    url_unlike = 'https://www.instagram.com/web/likes/%s/unlike/'
    url_comment = 'https://www.instagram.com/web/comments/%s/add/'
    url_follow = 'https://www.instagram.com/web/friendships/%s/follow/'
    url_unfollow = 'https://www.instagram.com/web/friendships/%s/unfollow/'
    url_login = 'https://www.instagram.com/accounts/login/ajax/'
    url_logout = 'https://www.instagram.com/accounts/logout/'
    url_media_detail = 'https://www.instagram.com/p/%s/?__a=1'
    url_user_detail = 'https://www.instagram.com/%s/?__a=1'

    user_agent = ("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36")
    accept_language = 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'
    get_header = header = {'Upgrade-Insecure-Requests' : '1',
'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding' : 'gzip, deflate, br',
'Accept-Language' : 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7'}
    # If instagram ban you - query return 400 error.
    error_400 = 0
    # If you have 3 400 error in row - looks like you banned.
    error_400_to_ban = 3
    # If InstaBot think you are banned - going to sleep.
    ban_sleep_time = 2 * 60 * 60

    
    def __init__(self,login,password):
                 
        self.s = requests.Session()
        self.user_login = login.lower()
        self.user_password = password
        self.media_by_tag = []
        self.media_on_feed = []
        self.media_by_user = []

    def login(self):
        log_string = 'Trying to login as %s...\n' % (self.user_login)
        print(log_string)
        self.s.cookies.update({
            'sessionid': '',
            'mid': '',
            'ig_pr': '1',
            'ig_vw': '1920',
            'csrftoken': '',
            's_network': '',
            'ds_user_id': ''
        })
        self.login_post = {
            'username': self.user_login,
            'password': self.user_password
        }
        self.s.headers.update({
            'Upgrade-Insecure-Requests' : '1',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': self.accept_language,
            'Connection': 'keep-alive',
            'Content-Length': '0',
            'Host': 'www.instagram.com',
            'Origin': 'https://www.instagram.com',
            'Referer': 'https://www.instagram.com/',
            'User-Agent': self.user_agent,
            'X-Instagram-AJAX': '1',
            'X-Requested-With': 'XMLHttpRequest'
        })
        r = self.s.get(self.url)
        self.s.headers.update({'X-CSRFToken': r.cookies['csrftoken']})
        time.sleep(5 * random.random())
        login = self.s.post(
            self.url_login, data=self.login_post, allow_redirects=True)
        self.s.headers.update({'X-CSRFToken': login.cookies['csrftoken']})
           # self.s.cookies.update({'mid': login.cookies['mid']})
        self.csrftoken = login.cookies['csrftoken']
        time.sleep(5 * random.random())
        print(login.text)
        if login.status_code == 200:
            r = self.s.get('https://www.instagram.com/')
            finder = r.text.find(self.user_login)
            if finder != -1:
               
                self.login_status = True
                log_string = '%s login success!' % (self.user_login)
                print(log_string)
            else:
                self.login_status = False
                print('Login error! Check your login data!')
        else:
            print('Login error! Connection error!')

    def logout(self):
        try:
            logout_post = {'csrfmiddlewaretoken': self.csrftoken}
            logout = self.s.post(self.url_logout, data=logout_post)
            print("Logout success!")
            self.login_status = False
        except:
            print("Logout error!")
    def getMediaInfo(self,media_short):
        info = {}
        if self.login_status:
            
            if self.login_status == 1:
                
                try:
                   
                        
                    url_det = self.url_media_detail % (media_short)
                        
                    r = self.s.get(url_det)
                    all_data = json.loads(r.text)
                    
                   
                    return all_data
                except:
                    
                    print("Except on get_media!")
                    
                    return None
            else:
                return None
    def getUserInfo(self,user_id,username=None):
        info = {}
        if self.login_status:
            
            if self.login_status == 1:
                
                try:
                    if(username==None):
                        url_follow = self.url_follow % (user_id)
                        username = requests.get(url_follow,headers=self.get_header, cookies=self.s.cookies.get_dict(),allow_redirects=True)
                        url_det = username.url+"?__a=1"
                        
                    else:
                        
                        url_det = self.url_user_detail % (username)
                        
                    r = self.s.get(url_det)
                    all_data = json.loads(r.text)
                    
                   
                    return all_data
                except:
                    
                    print("Except on getUserInfo!")
                    
                    return None
            else:
                return None
    def getHashtagFeed(self, tag,max):
        """ Get media ID set, by your hashtag """
        feed = []
        next_id = None
        if (self.login_status):
            for x in range(0,max):    
                if self.login_status == 1:
                    if(next_id == None):
                        url_tag = self.url_tag % (tag)
                    else:
                        url_tag = self.url_tag % (tag)+"&max_id="+next_id   
                    try:
                        
                        r = self.s.get(url_tag)
                       # print(r.text)
                        
                        all_data = json.loads(r.text)
                        if(all_data["graphql"]["hashtag"]["edge_hashtag_to_media"]["page_info"]["has_next_page"] == False):
                            for post in all_data["graphql"]["hashtag"]["edge_hashtag_to_media"]["edges"]:
                                feed.append(post)
                            return feed
                        else:
                            next_id = all_data["graphql"]["hashtag"]["edge_hashtag_to_media"]["page_info"]["end_cursor"] 
                            
                        for post in all_data["graphql"]["hashtag"]["edge_hashtag_to_media"]["edges"]:
                            feed.append(post)
                        
                    except:
                        return []
                        
              
        return feed

    def like(self, media_id):
        """ Send http request to like media by ID """
        if self.login_status:
            url_likes = self.url_likes % (media_id)
            try:
                like = self.s.post(url_likes)
                print(like.status_code)
                last_liked_media_id = media_id
            except:
                
                like = 0
        return like

    def unlike(self, media_id):
        """ Send http request to unlike media by ID """
        if self.login_status:
            url_unlike = self.url_unlike % (media_id)
            try:
                unlike = self.s.post(url_unlike)
            except:
               
                unlike = 0
        return unlike

    def comment(self, media_id, comment_text):
        """ Send http request to comment """
        if self.login_status:
            comment_post = {'comment_text': comment_text}
            url_comment = self.url_comment % (media_id)
            try:
                comment = self.s.post(url_comment, data=comment_post)
               
                return comment
            except:
                print("Comment failed")
        return False

    def follow(self, user_id):
        """ Send http request to follow """
        if self.login_status:
            url_follow = self.url_follow % (user_id)
            try: 
                follow = self.s.post(url_follow)
                
                print(follow.status_code)
                
                return follow
            except:
                print("Follow failed")
        return False

    def unfollow(self, user_id):
        """ Send http request to unfollow """
        if self.login_status:
            url_unfollow = self.url_unfollow % (user_id)
            try:
                unfollow = self.s.post(url_unfollow)
                  
                return unfollow
            except:
               print("Unfollow failed")
        return False

    
    def likeRandomUserMedia(self,user_id,username=None):
        
        media = self.getUserInfo(user_id,username)
        if(media == None):
            return False
        media_length = len(media["user"]["media"]["nodes"])
        if(len == 0):
            return False
        rnd_media = random.choice(media["user"]["media"]["nodes"])
        #print(rnd_media["id"])
        time.sleep(random.randint(1,10))
        self.like(rnd_media["id"])
        return True
    
    
    def getTimeline(self):
        if self.login_status:
            now_time = datetime.datetime.now()
            log_string = "%s : Get media id on recent feed" % (self.user_login)
            print(log_string)
            if self.login_status == 1:
                url_tag = 'https://www.instagram.com/?__a=1'
                try:
                    r = self.s.get(url_tag)
                    all_data = json.loads(r.text)
                    #print(r.text)    
                    return list(
                        all_data['graphql']['user']['edge_web_feed_timeline'][
                            'edges'])

                    
                except:
                    self.media_on_feed = []
                    print("Except on get_media!")
                    time.sleep(20)
                    return 0
            else:
                return 0

  
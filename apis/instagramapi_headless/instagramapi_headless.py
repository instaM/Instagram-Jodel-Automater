# -*- coding: utf-8 -*-
import time
import random
import os
from selenium import webdriver

from selenium.webdriver.common.keys import Keys

from selenium.webdriver.chrome.options import Options
  
from selenium.webdriver.common.action_chains import ActionChains

class InstagramAPI:
    base_url = 'https://www.instagram.com/'
    login_url = 'http://www.instagram.com/accounts/login'
    logout_url = 'http://www.instagram.com/accounts/logout'
    user_detail_url = 'https://www.instagram.com/%s/'
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    def __init__(
            self,
            username,
            password,
            chromedriver_path 
            ):
        self.username = username
        self.password = password
        self.chromedriver_path = chromedriver_path
        self.driver = None
        
        self.failCounter = 0
    def login (self):
       
        options = Options()
        options.add_argument('headless')

        options.add_argument('user-agent={%s}' % (self.user_agent))
        options.add_argument("no-sandbox")
        options.add_argument("disable-setuid-sandbox")
        options.add_argument("lang=en")
        
        self.driver = webdriver.Chrome(executable_path=self.chromedriver_path,chrome_options=options)
        
        self.driver.get(self.login_url);
        login_name=self.driver.find_element_by_name("username")
        login_pw=self.driver.find_element_by_name("password")
        login_name.send_keys(self.username)
        login_pw.send_keys(self.password)
        login_pw.send_keys(Keys.ENTER)
        time.sleep(3)
        self.driver.get(self.base_url)
        return True
    
    def logout(self):
        self.driver.get(self.logout_url)
        self.driver.quit()
        return True
    
    def follow(self,username):
        url = self.user_detail_url % (username)
        if(url != self.driver.current_url):
            self.driver.get(url)
            time.sleep(5)
            
        follow_button = self.driver.find_elements_by_xpath("//button[.//text()='Follow']")
        if(len(follow_button) == 0):
            return False
        try:
            follow_button[0].click()
        except Exception as e:
            print(e)
            return False
        
        return True
    def unfollow(self,username):
        url = self.user_detail_url % (username)
        if(url != self.driver.current_url):
            self.driver.get(url)
            time.sleep(5)
            
        follow_button = self.driver.find_elements_by_xpath("//button[.//text()='Following']")
        if(len(follow_button) == 0):
            return False
         try:
            follow_button[0].click()
        except Exception as e:
            print(e)
            return False
        
        return True
    def likeRandomUserMedia(self,username):
        
        url = self.user_detail_url % (username)
        
        if(url != self.driver.current_url):
            self.driver.get(url)
            time.sleep(5)
        post = self.driver.find_elements_by_xpath("//a[div[div[img]]]")
       # post = self.driver.find_elements_by_tag_name('img')
       
        if(len(post) == 0):
            return False
       # picture = (((random.choice(post).find_element_by_xpath('..')
        #   .find_element_by_xpath('..')))
       #    .find_element_by_xpath('..'))
        picture= random.choice(post)
        picture.click()
        time.sleep(3)
        try:
            like = picture.find_elements_by_xpath("//a[@role='button']/span[text()='Like']/..")
            if(len(like) == 0):
                return False
            like[0].click()
        except Exception as e:
            self.failCounter += 1
            print("#%i Failed" %(self.failCounter))
            print(e)
            
            return False   
        print("#%i Failed" %(self.failCounter))
        return True
         
    def likeNewsFeedMedia(self):
        try:
          if(self.driver.current_url != self.base_url):
              
              self.driver.get(self.base_url)
              time.sleep(5)
          
          like = self.driver.find_elements_by_xpath("//a[@role='button']/span[text()='Like']/..")
          if(len(like) == 0):
              return False
          to_like = random.choice(like)
          actions = ActionChains(self.driver)
          actions.move_to_element(to_like).perform()
         
          self.driver.execute_script("window.scrollBy(0, 200)") 
          time.sleep(2)
          to_like.click()
        except:
          return False
        return True
    
    
    
    
    
    
    
    
    
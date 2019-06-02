# -*- coding: utf-8 -*-
import time
import random
import os
import sys
import datetime
import logging
import json

from selenium import webdriver

from selenium.webdriver.common.keys import Keys

from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

class InstagramAPI:
    base_url = 'https://www.instagram.com/'
    login_url = 'http://www.instagram.com/accounts/login'
    logout_url = 'http://www.instagram.com/accounts/logout'
    user_detail_url = 'https://www.instagram.com/%s/'
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    logger = logging.getLogger("instalog.api_headless")
    WINDOW_SIZE = "1920,1080"
    time_format = "%d_%m_%y__%H_%M.png"
    screenshot_path = "../log/"
    def __init__(
            self,
            username,
            password,
            chromedriver_path = "/usr/lib/chromium-browser/chromedriver"
            ):
        self.username = username
        self.password = password
        self.chromedriver_path = chromedriver_path
        self.driver = None
        
        self.failCounter = 0
    def login (self):
       
        options = Options()
        #options.add_argument('headless')

        options.add_argument('user-agent={%s}' % (self.user_agent))
        options.add_argument("no-sandbox")
        options.add_argument("disable-setuid-sandbox")
        options.add_argument("lang=en")
        options.add_experimental_option('prefs', {'intl.accept_languages':'en_EN'})
        options.add_argument("--window-size=%s" % self.WINDOW_SIZE)
        self.driver = webdriver.Chrome(executable_path=self.chromedriver_path,chrome_options=options)
        
        self.driver.get(self.login_url);
        time.sleep(2)
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
        try:
          url = self.user_detail_url % (username)
          if(url != self.driver.current_url):
              self.driver.get(url)
              time.sleep(5)
              
          follow_button = self.driver.find_elements_by_xpath("//button[.//text()='Follow']")
          if(len(follow_button) == 0):
              return False
          self.driver.execute_script("window.scrollTo(0, 0)") 
          follow_button[0].click()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
        
            self.logger.error(str(exc_type)+" - "+ str(exc_obj.message)+" - "+ str(exc_tb.tb_lineno))
            self.driver.save_screenshot(self.screenshot_path+datetime.datetime.now().strftime(self.time_format))
            return False
        
        return True
    def unfollow(self,username):
        try:
          url = self.user_detail_url % (username)
          if(url != self.driver.current_url):
              self.driver.get(url)
              time.sleep(5)
              
          follow_button = self.driver.find_elements_by_xpath("//button[.//text()='Following']")
          if(len(follow_button) == 0):
              
              return False

          self.driver.execute_script("window.scrollTo(0, 0)") 
          follow_button[0].click()
          time.sleep(1)
          unfollow = self.driver.find_elements_by_xpath("//button[.//text()='Unfollow']")
          unfollow[0].click()
        except Exception as e:
            self.logger.error(e.message)
            self.driver.save_screenshot(self.screenshot_path+datetime.datetime.now().strftime(self.time_format))
            return None
        
        return True
    def likeRandomUserMedia(self,username):
        self.logger.info("Liking user " + username)
        try:
            url = self.user_detail_url % (username)
             
            if(url != self.driver.current_url):
                self.driver.get(url)
                time.sleep(5)
            post = self.driver.find_elements_by_xpath("//a[div[div[img]]]")
           # post = self.driver.find_elements_by_tag_name('img')
           
            if(len(post) == 0):
                self.logger.info("Did not find any pictures")
                return False
           # picture = (((random.choice(post).find_element_by_xpath('..')
            #   .find_element_by_xpath('..')))
           #    .find_element_by_xpath('..'))
            picture= random.choice(post)
            picture.click()
            time.sleep(3)
       
            like = picture.find_elements_by_xpath("//section/span[1]/button")
            if(len(like) == 0):
                return False
            like[0].click()
        except Exception as e:
            self.failCounter += 1
            self.logger.info("#%i Failed" %(self.failCounter))
            exc_type, exc_obj, exc_tb = sys.exc_info()
        
            self.logger.error(str(exc_type)+" - "+ str(exc_obj.message)+" - "+ str(exc_tb.tb_lineno))
            self.driver.save_screenshot(self.screenshot_path+datetime.datetime.now().strftime(self.time_format))
            return False   
        
        return True
         
    def likeNewsFeedMedia(self):
        try:
          if(self.driver.current_url != self.base_url):
              
              self.driver.get(self.base_url)
              time.sleep(5)
          
          like = self.driver.find_elements_by_xpath("//button[contains(@class,'coreSpriteHeartOpen')]")
          if(len(like) == 0):
              return False
          to_like = random.choice(like)
          actions = ActionChains(self.driver)
          actions.move_to_element(to_like).perform()
         
          self.driver.execute_script("window.scrollBy(0, 200)") 
          time.sleep(2)
          to_like.click()
        except Exception as e:
          exc_type, exc_obj, exc_tb = sys.exc_info()
        
          self.logger.error(str(exc_type)+" - "+ str(exc_obj.message)+" - "+ str(exc_tb.tb_lineno))
          self.driver.save_screenshot(self.screenshot_path+datetime.datetime.now().strftime(self.time_format))
          return False
        return True
    def test(self):
        try:
          print(8/0)
        except Exception as e:
          exc_type, exc_obj, exc_tb = sys.exc_info()
        
          self.logger.error(str(exc_type)+" - "+ str(exc_obj.message)+" - "+ str(exc_tb.tb_lineno))
          self.driver.save_screenshot(self.screenshot_path+datetime.datetime.now().strftime(self.time_format))
          return False
        return True

    def getFollowing(self,
                      username,
                      grab):
        """ Get entire list of followers using graphql queries. """
        relationship_data = {}
        relationship_data.update(
            {username: {"all_following": [], "all_followers": []}})


        url = self.user_detail_url % (username)
        try:
            if (url != self.driver.current_url):
                self.driver.get(url)
            # Get followers count
            followers_count = 0

            if grab != "full" and grab > followers_count:
                self.logger.info(
                    "You have requested higher amount than existing followers count "
                    " ~gonna grab all available")
                grab = followers_count





            # if there has been prior graphql query, use that existing data to speed
            # up querying time
            all_prior_followers = None

            user_data = {}


            graphql_endpoint = 'https://www.instagram.com/graphql/query/'

            graphql_followers = (
                    graphql_endpoint + '?query_hash=58712303d941c6855d4e888c5f0cd22f')

            all_followers = []

            variables = {}
            user_data['id'] = self.driver.execute_script(
                "return window._sharedData.entry_data.ProfilePage[0]."
                "graphql.user.id")

            variables['id'] = user_data['id']
            variables['first'] = 50

            # get follower and user loop

            sc_rolled = 0
            local_read_failure = False
            passed_time = "time loop"
        except Exception as exc:
            return []
        try:
            has_next_data = True

            url = (
                '{}&variables={}'
                    .format(graphql_followers, str(json.dumps(variables)))
            )
            self.driver.get(url)

            """ Get stored graphql queries data to be used """
            try:
                filename = 'graphql_queries.json'

                query_date = datetime.datetime.today().strftime('%d-%m-%Y')

                if not os.path.isfile(filename):
                    with open(filename, 'w') as graphql_queries_file:
                        json.dump({username: {query_date: {"sc_rolled": 0}}},
                                  graphql_queries_file)
                        graphql_queries_file.close()

                # load the existing graphql queries data
                with open(filename) as graphql_queries_file:
                    graphql_queries = json.load(graphql_queries_file)
                    stored_usernames = list(
                        name for name, date in graphql_queries.items())

                    if username not in stored_usernames:
                        graphql_queries[username] = {query_date: {"sc_rolled": 0}}
                    stored_query_dates = list(
                        date for date, score in graphql_queries[username].items())

                    if query_date not in stored_query_dates:
                        graphql_queries[username][query_date] = {"sc_rolled": 0}
            except Exception as exc:
                self.logger.info(
                    "Error occurred while getting `scroll` data from "
                    "graphql_queries.json\n{}\n".format(
                        str(exc).encode("utf-8")))
                local_read_failure = True


            while has_next_data:
                try:
                    pre = self.driver.find_element_by_tag_name("pre").text
                except NoSuchElementException as exc:
                    self.logger.info("Encountered an error to find `pre` in page!"
                                "\t~grabbed {} usernames \n\t{}"
                                .format(len(set(all_followers)),
                                        str(exc).encode("utf-8")))
                    return all_followers

                data = json.loads(pre)['data']

                # get followers
                page_info = (
                    data['user']['edge_follow']['page_info'])
                edges = data['user']['edge_follow']['edges']
                for user in edges:
                    entry = {"id": user["node"]["id"], "username": user["node"]["username"],"full_name": user["node"]["full_name"]}
                    all_followers.append(entry)

                grabbed = len(all_followers)

                if grab != "full" and grabbed >= grab:
                    self.logger.info('\n')
                    self.logger.info(
                        "Grabbed {} usernames from `Followers` as requested at {}".format(
                            grabbed, passed_time))

                    break

                has_next_data = page_info['has_next_page']
                if has_next_data:
                    variables['after'] = page_info['end_cursor']

                    url = (
                        '{}&variables={}'
                            .format(
                            graphql_followers, str(json.dumps(variables)))
                    )

                    self.driver.get( url)
                    sc_rolled += 1

                    # dump the current graphql queries data
                    if local_read_failure is not True:
                        try:

                            with open(filename, 'w') as graphql_queries_file:
                                graphql_queries[username][query_date][
                                    "sc_rolled"] += 1
                                json.dump(graphql_queries,
                                          graphql_queries_file)
                        except Exception as exc:
                            self.logger.info('\n')
                            self.logger.info(
                                "Error occurred while writing `scroll` data to "
                                "graphql_queries.json\n{}\n"
                                    .format(str(exc).encode("utf-8")))

                    # take breaks gradually
                    if sc_rolled > 91:
                        self.logger.info('\n')
                        self.logger.info("Queried too much! ~ sleeping a bit :>")
                        time.sleep(600)
                        sc_rolled = 0

        except BaseException as exc:
            self.logger.info('\n')
            self.logger.info("Unable to get `Followers` data:\n\t{}\n".format(
                str(exc).encode("utf-8")))

        # remove possible duplicates
        all_followers = [i for n, i in enumerate(all_followers) if i not in all_followers[n + 1:]]
        return all_followers

    def getFollowers(self,
                      username,
                      grab):
        """ Get entire list of followers using graphql queries. """
        relationship_data = {}
        relationship_data.update(
            {username: {"all_following": [], "all_followers": []}})

        try:

            url = self.user_detail_url % (username)

            if (url != self.driver.current_url):
                self.driver.get(url)
            # Get followers count
            followers_count = 0

            if grab != "full" and grab > followers_count:
                self.logger.info(
                    "You have requested higher amount than existing followers count "
                    " ~gonna grab all available")

                grab = followers_count





            # if there has been prior graphql query, use that existing data to speed
            # up querying time
            all_prior_followers = None

            user_data = {}


            graphql_endpoint = 'https://www.instagram.com/graphql/query/'

            graphql_followers = (
                    graphql_endpoint + '?query_hash=37479f2b8209594dde7facb0d904896a')

            all_followers = []

            variables = {}
            user_data['id'] = self.driver.execute_script(
                "return window._sharedData.entry_data.ProfilePage[0]."
                "graphql.user.id")

            variables['id'] = user_data['id']
            variables['first'] = 50

            # get follower and user loop

            sc_rolled = 0
            local_read_failure = False
            passed_time = "time loop"
        except Exception as exc:
            return []
        try:
            has_next_data = True

            url = (
                '{}&variables={}'
                    .format(graphql_followers, str(json.dumps(variables)))
            )
            self.driver.get(url)

            """ Get stored graphql queries data to be used """
            try:
                filename = 'graphql_queries.json'

                query_date = datetime.datetime.today().strftime('%d-%m-%Y')

                if not os.path.isfile(filename):
                    with open(filename, 'w') as graphql_queries_file:
                        json.dump({username: {query_date: {"sc_rolled": 0}}},
                                  graphql_queries_file)
                        graphql_queries_file.close()

                # load the existing graphql queries data
                with open(filename) as graphql_queries_file:
                    graphql_queries = json.load(graphql_queries_file)
                    stored_usernames = list(
                        name for name, date in graphql_queries.items())

                    if username not in stored_usernames:
                        graphql_queries[username] = {query_date: {"sc_rolled": 0}}
                    stored_query_dates = list(
                        date for date, score in graphql_queries[username].items())

                    if query_date not in stored_query_dates:
                        graphql_queries[username][query_date] = {"sc_rolled": 0}
            except Exception as exc:
                self.logger.info(
                    "Error occurred while getting `scroll` data from "
                    "graphql_queries.json\n{}\n".format(
                        str(exc).encode("utf-8")))
                local_read_failure = True


            while has_next_data:
                try:
                    pre = self.driver.find_element_by_tag_name("pre").text
                except NoSuchElementException as exc:
                    self.logger.info("Encountered an error to find `pre` in page!"
                                "\t~grabbed {} usernames \n\t{}"
                                .format(len(set(all_followers)),
                                        str(exc).encode("utf-8")))
                    return all_followers

                data = json.loads(pre)['data']

                # get followers
                page_info = (
                    data['user']['edge_followed_by']['page_info'])
                edges = data['user']['edge_followed_by']['edges']
                for user in edges:
                    if(user["node"]["followed_by_viewer"] == False and user["node"]["requested_by_viewer"] == False):
                        entry = {"id": user["node"]["id"], "username": user["node"]["username"],"full_name": user["node"]["full_name"]}
                        all_followers.append(entry)

                grabbed = len(all_followers)

                if grab != "full" and grabbed >= grab:
                    print('\n')
                    self.logger.info(
                        "Grabbed {} usernames from `Followers` as requested at {}".format(
                            grabbed, passed_time))

                    break

                has_next_data = page_info['has_next_page']
                if has_next_data:
                    variables['after'] = page_info['end_cursor']

                    url = (
                        '{}&variables={}'
                            .format(
                            graphql_followers, str(json.dumps(variables)))
                    )

                    self.driver.get( url)
                    sc_rolled += 1

                    # dump the current graphql queries data
                    if local_read_failure is not True:
                        try:

                            with open(filename, 'w') as graphql_queries_file:
                                graphql_queries[username][query_date][
                                    "sc_rolled"] += 1
                                json.dump(graphql_queries,
                                          graphql_queries_file)
                        except Exception as exc:
                            print('\n')
                            self.logger.info(
                                "Error occurred while writing `scroll` data to "
                                "graphql_queries.json\n{}\n"
                                    .format(str(exc).encode("utf-8")))

                    # take breaks gradually
                    if sc_rolled > 91:
                        print('\n')
                        self.logger.info("Queried too much! ~ sleeping a bit :>")
                        time.sleep(600)
                        sc_rolled = 0

        except BaseException as exc:
            print('\n')
            self.logger.info("Unable to get `Followers` data:\n\t{}\n".format(
                str(exc).encode("utf-8")))

        # remove possible duplicates
        all_followers = [i for n, i in enumerate(all_followers) if i not in all_followers[n + 1:]]
        return all_followers

    def getCommonUsers(self,username):
        followers =self.getFollowers(username,"full")
        following = self.getFollowing(username,"full")

        common_followers = [i for i in followers for j in following if i['id'] == j['id']]
        return common_followers
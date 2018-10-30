# -*- coding: utf-8 -*-
# Model: I-O DATA MiCAP 3323C & 3340C
# Function1: Login to UI
# Function2: Change5G channel
# Function3: Check if DFS is actioning or not
# Function4: Get WLAN client status
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re, sys, os, inspect

class Test(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_ip = "192.168.0.1"
        self.username = "admin"
        self.password = "1234"
        self.waittime = 70
        self.base_url = "http://"+ self.base_ip
        self.verificationErrors = []
        self.accept_next_alert = True
        self.wlan_client_table = "table2"
        self.Channel_2G = ['1', '2', '3', '4', '5','6', '7', '8', '9', '10','11', '12', '13', '自動' ]
        self.Channel_5G = ['36', '40', '44', '48', '52' ]
        self.Channel_5G_dfs =['56', '60','64','100','104','108','112','116','120','124','128','自動']
        
        
    def test_(self):
        driver = self.driver
        driver.get("http://"+self.username+":"+self.password+"@"+self.base_ip)
        #time.sleep(1)
        #driver.switch_to_alert()
        self.close_alert_and_get_its_text()
        #print (self.close_alert_and_get_its_text())
        #Selenium-WebDriver Java Code for entering Username & Password as below:
        #driver.find_element_by_id("使用者名稱:").send_keys("admin")
        #driver.find_element_by_id(By.id("密碼:")).send_keys("1234")
        #driver.switch_to_alert.accept()
        global i
        for i in range(1000):
            print("\r\n")
            #self.set_5g_channel()
            #self.disable_ssid1_broadcast_hidden()
            #self.set_ssid2_broadcast_hidden("enable")
            self.set_2g_channel()
            #self.enable_ssid1_broadcast_hidden()
            #self.set_ssid2_broadcast_hidden("disable")
            #self.set_5g_channel()



    def set_2g_channel(self):
        print("---------------------------")
        print("2.4G Run",i, "rounds. ", "Totoal",  i*len(self.Channel_2G), "times")
        print("---------------------------")
        global Channels_2G
        for Channels_2G in self.Channel_2G:
            #self.get_channel_status()
            self.driver.get(self.base_url + "/cgi-bin/luci/content/wireless_settings/2g_settings")
            Select(self.driver.find_element_by_id("2g_channel")).select_by_visible_text(Channels_2G)
            self.driver.find_element_by_css_selector("input[type=\"button\"]").click()
            print("=Config 2.4G channel as",Channels_2G)
            time.sleep(60)
            self.get_channel_status()
            self.wlan_client_tables()
            #self.driver.get(self.base_url + "/cgi-bin/luci/content/wireless_settings/client_list")
            #for element in self.driver.find_elements_by_class_name('table2'):
                #print ("WLAN Client table:\r\n" ,element.text)
                #print (element.tag_name)

            
            
    def set_5g_channel(self):
        print("---------------------------")
        print("5G Run", i, "rounds. ", "Totoal", i*(len(self.Channel_5G)+len(self.Channel_5G_dfs)), "times")
        print("---------------------------")    
        global Channels_5G
        Channel_5G_dfs=self.Channel_5G_dfs
        Channel_5G=self.Channel_5G
        Channel_all=Channel_5G+Channel_5G_dfs
        for Channels_5G in Channel_all:
            self.driver.get(self.base_url + "/cgi-bin/luci/content/wireless_settings/5g_settings")
            Select(self.driver.find_element_by_id("5g_channel")).select_by_visible_text(Channels_5G)
            self.driver.find_element_by_css_selector("input[type=\"button\"]").click()
            print("Config 5G channel as",Channels_5G)
            #print ("wait 70 sec")
            time.sleep(self.waittime)
            self.check_dfs_status()
            self.get_channel_status()
            self.check_5g_channel()       
            self.wlan_client_tables()             
                    
    def check_dfs_status(self):
       #Check if DFS is actioning or not
       for element in self.driver.find_elements_by_id('dfs_msg'):
            if element.text == "DFS動作中です。しばらくお待ちください。":
                print (element.text)
                time.sleep(70)
        
    def check_5g_channel(self):
        #Check 5G channel
        self.driver.get(self.base_url + "/cgi-bin/luci/menu/status")
        for element in self.driver.find_elements_by_xpath('/html/body/blockquote/p/table[3]/tbody/tr[3]/td[2]'):
            print ("Current channel is ",element.text)
            if element.text != Channels_5G:
                print ("******Channel Missmatch!*******")
                time.sleep(60)
            else:
                print ("Channel Match !")
    def get_channel_status(self):
        #Get channel from status page
        print("=Current channel in status page=")
        self.driver.get(self.base_url + "/cgi-bin/luci/menu/status")
        for i, j, k in ((i, j, k) for i in range(3,4) for j in range(2,4) for k in range(1,3)):
            b='/html/body/blockquote/p/table['+str(i)+']/tbody/tr['+str(j)+']/td['+str(k)+']'
            #print(b)
            #self.driver.implicitly_wait(0)
            for element in self.driver.find_elements_by_xpath(b):
                print(element.text,end="  ")
        print()        
             
    def wlan_client_tables(self):
        #Show client list table
        wlan_client_table=self.wlan_client_table
        self.driver.get(self.base_url + "/cgi-bin/luci/content/wireless_settings/client_list")
        print("---WLAN Client table:---")
        for element in self.driver.find_elements_by_class_name(wlan_client_table):
            no_client='ルーターにクライアントが接続されていません'
            if element.text == no_client:
                time.sleep(60)
                self.driver.find_element_by_css_selector("input[type=\"button\"]").click()
                for element in self.driver.find_elements_by_class_name('table2'):
                    if element.text == no_client:
                        print (element.text)
                        print ("No WLAN client connected; continue to test next channel !")
                        #driver.quit()
                        #break
            else:
                print (element.text)
                

    def disable_ssid1_broadcast_hidden(self):
        print(inspect.stack()[0][3])
        self.driver.get(self.base_url + "/cgi-bin/luci/content/wireless_settings/2g_settings")
        Select(self.driver.find_element_by_id("ssid1_broadcast_hidden")).select_by_visible_text("無効")
        self.driver.find_element_by_css_selector("input[type=\"button\"]").click()
        time.sleep(60)
    def set_ssid2_broadcast_hidden(self,a):
        print(inspect.stack()[0][3])
        if a == "enable":
            b="有効"
        elif a == "disable":
            b="無効"
        self.driver.get(self.base_url + "/cgi-bin/luci/content/wireless_settings/5g_settings")
        Select(self.driver.find_element_by_id("ssid2_broadcast_hidden")).select_by_visible_text(b)
        self.driver.find_element_by_css_selector("input[type=\"button\"]").click()
        self.close_alert()
        time.sleep(60)
    def enable_ssid1_broadcast_hidden(self):
        print(inspect.stack()[0][3])
        self.driver.get(self.base_url + "/cgi-bin/luci/content/wireless_settings/2g_settings")
        Select(self.driver.find_element_by_id("ssid1_broadcast_hidden")).select_by_visible_text("有効")
        self.driver.find_element_by_css_selector("input[type=\"button\"]").click()
        time.sleep(60)        

    def wfile(self,a):
        print=os.path.splitext(__fclose_alertile__)[0]+".txt"
        self.f = open(print, 'a', encoding = 'UTF-8')
        f=self.f
        with f as g:
            print(a, end=" ")
            #print(end="\r\n ", file=g)                       
            print(a, end=" ", file=g)
        f.close()


    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    def close_alert(self):
        try:
            time.sleep(1)
            alert = self.driver.switch_to_alert()
            alert.accept()
        except:
            print ("no alert")    
    def tearDown(self):
        time.sleep(1)
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main(exit=False)



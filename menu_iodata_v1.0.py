# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time, re, sys, os, subprocess,inspect
from my_tool import *
import tkinter as tk

driver = webdriver.Firefox()
driver.implicitly_wait(30)
base_ip = "192.168.0.1"
username = "admin"
password = "1234"
waittime = 150
ping_check_host = "192.168.0.1"
base_url = "http://"+ base_ip
Channel_5G = ['36', '40', '44', '48', '52' ]
Channel_5G_dfs =['56', '60','64','100','104','108','112','116','120','124','128','自動']
selection= 4

def main():
    case_select = {
        0: iodata_reboot,
        1: iodata_get_status_test,
        2: iodata_set_5G_channel,
        3: iodata_config_wizard,
        4: iodata_4,
        #5: iodata_5
    }
    #Create menu base on tkinter
    base = tk.Tk()
    radio_value = tk.IntVar()
    radio_value.set(0)
    base.title("I-O DATA GUI Test")
    tk.Label(text="----version 1.0 by Frank Wen----").pack() 
    tk.Label(text="Login IP: "+base_ip).pack() 
    tk.Label(text="Login Username: "+username).pack() 
    tk.Label(text="Login Password: "+password).pack() 
    tk.Label(text="--------------------------------").pack() 
    
    for i in range(len(case_select)):
        tk.Radiobutton(text = case_select[i].__name__, variable = radio_value, value = i).pack()

    def run():
        value = radio_value.get()
        case_select[value]()
    tk.Button(base, text='Run', command=run).pack()
    base.mainloop()

def iodata_reboot():
    #driver = webdriver.Firefox()
    #driver.implicitly_wait(30)
    #login UI
    driver.get("http://"+username+":"+password+"@"+base_ip)
    #Check if alert raise and close it
    close_alert()
    time.sleep(5)
    iodata_get_status()
    iodata_get_status_wan()
    driver.implicitly_wait(10)
    i = j = 0
    write_file("\r\n",current_time(),"reboot times is ")
    #loop to reboot
    while i <= 10000:
        ping_fail=is_ping_fail(ping_check_host)
        if ping_fail :
            j += 1
            print(ping_check_host,"Ping Fail",j,"times")
            print(current_time())
            iodata_get_status()
            iodata_get_status_wan()
            break
        #Print status page
        driver.get(base_url + "/cgi-bin/luci/menu/status")    
        iodata_get_channel_status()

        #Enter reboot page    
        driver.get(base_url + "/cgi-bin/luci/content/system_settings/initialization")
        driver.find_element_by_xpath(u"//input[@type='button' and @value='再起動']").click()
        close_alert()
        close_alert()
        i += 1
        write_file(str(i))
        write_file(", ")
        time.sleep(waittime)
    

def iodata_get_status_test():
    print(inspect.stack()[0][3])  
    #driver = webdriver.Firefox()
    #driver.implicitly_wait(30)
    #login UI
    driver.get("http://"+username+":"+password+"@"+base_ip)
    #Check if alert raise and close it
    close_alert()
    try:
        time.sleep(1)
        alert = driver.switch_to_alert()
        alert.accept()
    except:
        print ("no alert")
    time.sleep(1)
    driver.get(base_url + "/cgi-bin/luci/menu/status")   
    N=5
    for i, j, k in ((i, j, k) for i in range(1,2) for j in range(1,N) for k in range(1,N)):
        b='/html/body/blockquote/p/table['+str(i)+']/tbody/tr['+str(j)+']/td['+str(k)+']'
        #print(b)
        driver.implicitly_wait(0)
        try:
            element = webdriverWait(driver, 0,0.1).until(EC.presence_of_element_located((By.ID, "wan_information")))
            for element in driver.find_elements_by_xpath(b):
                write_file(element.text)
        except:
            pass
            #print (i,j,k, "not exist")
    for l,m in ((l,m) for l in range(2,4) for m in range(1,4)):
        c='/html/body/blockquote/p/span/table/tbody/tr['+str(l)+']/td['+str(m)+']'
        #print(c)
        for element in driver.find_elements_by_xpath(c):
            write_file(element.text)
    driver.quit()
def iodata_set_5G_channel():
    print(inspect.stack()[0][3])  
    #login UI
    driver.get("http://"+username+":"+password+"@"+base_ip)
    #Check if alert raise and close it
    close_alert()
    #Config 5G channel setting
    driver.get(base_url + "/cgi-bin/luci/content/wireless_settings/5g_settings")
    Select(driver.find_element_by_id("5g_channel")).select_by_visible_text('自動')
    driver.find_element_by_css_selector("input[type=\"button\"]").click()
    #Get current cahnnel from status page
    time.sleep(50)
    #Get channel number
    iodata_get_status(3,3,2,3,1,2)
    time.sleep(180)
    driver.quit()
    
def iodata_config_wizard():
    print("Function name is :", inspect.stack()[0][3])
    #open UI
    driver.get("http://"+base_ip)
    #Config Wizard seeting
    driver.find_element_by_id("username").clear()
    driver.find_element_by_id("username").send_keys("admin")
    driver.find_element_by_id("new_passwd_1").clear()
    driver.find_element_by_id("new_passwd_1").send_keys("1234")
    driver.find_element_by_id("new_passwd_2").clear()
    driver.find_element_by_id("new_passwd_2").send_keys("1234")
    driver.find_element_by_name("next").click()
    driver.find_element_by_name("disable_administrator").click()
    driver.find_element_by_name("disable_netfilter").click()
    driver.find_element_by_name("submit").click()   
    driver.quit()

    
def iodata_4():
    print("Function name is :", inspect.stack()[0][3])
def iodata_5():
    pass
    
def iodata_get_status(Mstart=1,Mend=1,Nstart=1,Nend=4,Ostart=1,Oend=4):
    driver.get(base_url + "/cgi-bin/luci/menu/status")   
    #default range is (1,1)(1,4)(1,4) 
    for i, j, k in ((i, j, k) for i in range(Mstart,Mend+1) for j in range(Nstart,Nend+1) for k in range(Ostart,Oend+1)):
        b='/html/body/blockquote/p/table['+str(i)+']/tbody/tr['+str(j)+']/td['+str(k)+']'
        #print(b)
        driver.implicitly_wait(0)
        try:
            element = webdriverWait(driver, 0,0.1).until(EC.presence_of_element_located((By.ID, "wan_information")))
            for element in driver.find_elements_by_xpath(b):
                write_file(element.text)
        except:
            pass
            #print (i,j,k, "not exist")
def iodata_get_channel_status():
    #Get channel from status page
    print("=Current channel in status page=")
    driver.get(base_url + "/cgi-bin/luci/menu/status")
    for i, j, k in ((i, j, k) for i in range(3,4) for j in range(2,4) for k in range(1,3)):
        b='/html/body/blockquote/p/table['+str(i)+']/tbody/tr['+str(j)+']/td['+str(k)+']'
        #print(b)
        #driver.implicitly_wait(0)
        for element in driver.find_elements_by_xpath(b):
            print(element.text,end="  ")
    print()        
                      
            
def iodata_get_status_wan():            
    for l,m in ((l,m) for l in range(2,4) for m in range(1,4)):
        c='/html/body/blockquote/p/span/table/tbody/tr['+str(l)+']/td['+str(m)+']'
        #print(c)
        for element in driver.find_elements_by_xpath(c):
            write_file(element.text)
                
def close_alert():
    try:
        time.sleep(1)
        alert = driver.switch_to_alert()
        alert.accept()
    except:
        print ("no alert")



if __name__ == "__main__":
    main()
























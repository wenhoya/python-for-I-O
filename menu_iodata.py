# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time, re, sys, os, subprocess,inspect
from my_tool import *
import tkinter as tk

#driver = webdriver.Firefox()
#driver.implicitly_wait(30)
base_ip = "192.168.0.1"
username = "admin"
password = "1234"
waittime = 120
pppoewan_sleep = 120
ping_check_host = "192.168.0.1"
base_url = "http://"+ base_ip
firmwareurl = "D:\\Documents\\work\\_Project\\_SmartGW\\IO-DATA\\ras1.bin"
Channel_5G = ['36', '40', '44', '48', '52' ]
Channel_5G_dfs =['56', '60','64','100','104','108','112','116','120','124','128','自動']
selection= 4

def main():
    case_select = {
        0: iodata_reboot,
        1: iodata_get_status_test,
        2: iodata_set_5G_channel,
        3: iodata_apply_PPPoE_wan,
        4: iodata_restore_default_wizard,
        5: iodata_fw_upgrade,
        6: test_6

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
    tk.Label(text="Ping check IP: "+ping_check_host).pack() 
    tk.Label(text="FW upgrade URL: "+firmwareurl).pack() 
    tk.Label(text="--------------------------------").pack() 
    
    for i in range(len(case_select)):
        tk.Radiobutton(text = case_select[i].__name__, variable = radio_value, value = i).pack(anchor=tk.W)

    def run():
        value = radio_value.get()
        case_select[value]()
    tk.Button(base, text='Run', command=run).pack()
    base.mainloop()

def iodata_reboot():
    #case_select 0
    global driver
    driver = webdriver.Firefox()
    driver.implicitly_wait(30)
    #login UI
    driver.get("http://"+username+":"+password+"@"+base_ip)
    #Check if alert raise and close it
    close_alert()
    time.sleep(5)
    driver.get(base_url + "/cgi-bin/luci/menu/status")    
    iodata_get_status_new()
    driver.implicitly_wait(10)
    i = j = k = 0
    write_file("\r\n",current_time())
    #loop to reboot
    while i <= 10000:
        ping_fail=is_ping_fail(ping_check_host)
        subprocess.Popen("ping "+ ping_check_host)
        if ping_fail :
            j += 1
            print(ping_check_host,"Ping Fail",j,"times")
            print(current_time())
            iodata_get_status_wan()
            #break
        else:
            k +=1
            print("Reboot",i,"times.","Ping Pass",k,"times.","Ping Fail",j,"times.")
            

        #Print status page
        driver.get(base_url + "/cgi-bin/luci/menu/status")    
        iodata_get_status_wan()
        iodata_get_channel_status()

        #Enter reboot page    
        driver.get(base_url + "/cgi-bin/luci/content/system_settings/initialization")
        driver.find_element_by_xpath(u"//input[@type='button' and @value='再起動']").click()
        close_alert()
        close_alert()
        i += 1
        #write_file(str(i))
        #write_file(", ")
        time.sleep(waittime)
    

def iodata_get_status_test():
    #case_select 1
    print(inspect.stack()[0][3]) 
    global driver
    driver = webdriver.Firefox()
    driver.implicitly_wait(30)
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
    driver.get(base_url + "/cgi-bin/luci/menu/status")
    driver.implicitly_wait(0)
    #Print Internet status
    for l,m in ((l,m) for l in range(2,4) for m in range(1,4)):
        c='/html/body/blockquote/p/span/table/tbody/tr['+str(l)+']/td['+str(m)+']'
        print(c)
        for element in driver.find_elements_by_xpath(c):
            write_file(element.text)
    #Print System status
    for l,m in ((l,m) for l in range(2,4) for m in range(1,4)):
        c='/html/body/blockquote/p/table[1]/tbody/tr['+str(l)+']/td['+str(m)+']'
        print(c)
        for element in driver.find_elements_by_xpath(c):
            write_file(element.text)
    #Print notice content         
    d='//*[@id="wan_information"]/table/tbody/tr/td'
    for element in driver.find_elements_by_xpath(d):
        print("\r\n","==Notice content==\r\n",element.text)
    driver.quit()
def iodata_set_5G_channel():
    #case_select 2
    print(inspect.stack()[0][3])  
    global driver
    driver = webdriver.Firefox()
    driver.implicitly_wait(30)
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
    
def iodata_apply_PPPoE_wan():
    #case_select 3
    print("Function name is :", inspect.stack()[0][3])
    global driver
    driver = webdriver.Firefox()
    driver.implicitly_wait(30)
    #login UI
    driver.get("http://"+username+":"+password+"@"+base_ip)
    #Check if alert raise and close it
    close_alert()
    time.sleep(5)
    driver.get(base_url + "/cgi-bin/luci/menu/status")    
    iodata_get_status_new()
    #loop
    i = j = k = 0
    while i <= 10000:
        os.system("ipconfig/flushdns ")
        ping_fail=is_ping_fail(ping_check_host)
        #Output ping result to shell
        p = subprocess.Popen("ping "+ ping_check_host, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        print (output.decode("unicode_escape"))
        if ping_fail :
            j += 1
            print(ping_check_host,"Ping Fail",j,"times")
            print(current_time())
            iodata_get_status_wan()
            #break
        else:
            k +=1
            print("Test",i+1,"times.","Ping Pass",k,"times.","Ping Fail",j,"times.")
            
        #Select and apply PPPoE WAN seeting
        driver.get(base_url + "/cgi-bin/luci/content/internet")
        driver.find_element_by_id("pppoe_radio").click()
        #html: <input value="設定" id="apply_pppoe" width="105" type="button">
        driver.find_element_by_id("apply_pppoe").click()
        i += 1
        time.sleep(pppoewan_sleep)
  
def iodata_restore_default_wizard():
    #case_select 4
    print("Function name is :", inspect.stack()[0][3])
    global driver
    driver = webdriver.Firefox()
    driver.implicitly_wait(30)
    #login UI
    driver.get("http://"+username+":"+password+"@"+base_ip)
    #Check if alert raise and close it
    close_alert()
    time.sleep(5)
    driver.implicitly_wait(10)
    write_file("\r\n",current_time())
    #Restore default    
    driver.get(base_url + "/cgi-bin/luci/content/system_settings/initialization")
    driver.find_element_by_xpath(u"//input[@type='button' and @value='出荷時設定']").click()
    close_alert()
    close_alert()
    time.sleep(80)
    #Config Wizard seeting
    print ("Config Wizard setting")
    driver.find_element_by_id("username").clear()
    driver.find_element_by_id("username").send_keys("admin")
    driver.find_element_by_id("new_passwd_1").clear()
    driver.find_element_by_id("new_passwd_1").send_keys("1234")
    driver.find_element_by_id("new_passwd_2").clear()
    driver.find_element_by_id("new_passwd_2").send_keys("1234")
    driver.find_element_by_name("next").click()
    time.sleep(3)
    driver.find_element_by_name("disable_administrator").click()
    time.sleep(3)
    driver.find_element_by_name("disable_netfilter").click()
    time.sleep(3)
    driver.find_element_by_name("submit").click()
    time.sleep(120)

def iodata_fw_upgrade():
    #case_select 5
    print("Function name is :", inspect.stack()[0][3])
    global driver
    driver = webdriver.Firefox()
    driver.implicitly_wait(30)
    #login UI
    driver.get("http://"+username+":"+password+"@"+base_ip)
    #Check if alert raise and close it
    close_alert()
    time.sleep(5)
    #Get model name & firmware version
    driver.get(base_url + "/cgi-bin/luci/menu/status")    
    iodata_get_status_new()
    driver.implicitly_wait(10)
    #print("\r\n",current_time(),"upgrade times is ")
    write_file("\r\n",current_time(),"upgrade times is ")
    #fw upgrade   
    for i in range(1000):
        driver.get(base_url + "/cgi-bin/luci/content/system_settings/firmware")
        driver.find_element_by_name("filePath").clear()
        driver.find_element_by_name("filePath").send_keys(firmwareurl)
        driver.find_element_by_css_selector("input[type=\"button\"]").click()
        close_alert()
        close_alert()
        i += 1
        #print(str(i),", ")   
        write_file(str(i),", ")        
        time.sleep(100)
    #driver.quit()    
    
    
def test_6():
    #case_test 6
    print(inspect.stack()[0][3]) 
    global driver
    driver = webdriver.Firefox()
    driver.implicitly_wait(30)
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
    driver.get(base_url + "/cgi-bin/luci/menu/status")
    driver.implicitly_wait(0)
    #test new function
    iodata_get_status_new()
    iodata_get_status_wan()
    driver.quit()    
    pass
    
def iodata_get_status(Mstart=1,Mend=4,Nstart=1,Nend=4,Ostart=1,Oend=4):
    #The function does not work, need debugging
    driver.get(base_url + "/cgi-bin/luci/menu/status")   
    #default range is (1,4)(1,4)(1,4) 
    for i, j, k in ((i, j, k) for i in range(Mstart,Mend+1) for j in range(Nstart,Nend+1) for k in range(Ostart,Oend+1)):
        b='/html/body/blockquote/p/table['+str(i)+']/tbody/tr['+str(j)+']/td['+str(k)+']'
        #print(b)
        #driver.implicitly_wait(0)
        try:
        #    element = webdriverWait(driver, 0,0.1).until(EC.presence_of_element_located((By.ID, "wan_information")))
            for element in driver.find_elements_by_xpath(b):
                write_file(element.text)
        except:
            pass
            print (i,j,k, "not exist")
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

            
def iodata_get_status_new():            
    driver.implicitly_wait(0)
    #Get and print notice content         
    d='//*[@id="wan_information"]/table/tbody/tr/td'
    for element in driver.find_elements_by_xpath(d):
        print("\r\n","==Notice content==\r\n",element.text)
    #Get and print System status
    print("\r\n","==System status==")
    for l,m in ((l,m) for l in range(2,6) for m in range(1,4)):
        c='/html/body/blockquote/p/table[1]/tbody/tr['+str(l)+']/td['+str(m)+']'
        for element in driver.find_elements_by_xpath(c):
            print(element.text,end="  ")
    #Get and print Internet status
    print("\r\n","==Internet status==")
    for l,m in ((l,m) for l in range(2,8) for m in range(1,4)):
        c='/html/body/blockquote/p/span/table/tbody/tr['+str(l)+']/td['+str(m)+']'
        for element in driver.find_elements_by_xpath(c):
            print(element.text,end="  ")
    print()        
            
def iodata_get_status_wan():
    driver.implicitly_wait(0)
    #Get and print notice content         
    d='//*[@id="wan_information"]/table/tbody/tr/td'
    for element in driver.find_elements_by_xpath(d):
        print("\r\n","==Notice content==\r\n",element.text)            
    #Get and print Internet status
    print("\r\n","==Internet status==")
    for l,m in ((l,m) for l in range(2,8) for m in range(1,4)):
        c='/html/body/blockquote/p/span/table/tbody/tr['+str(l)+']/td['+str(m)+']'
        for element in driver.find_elements_by_xpath(c):
            print(element.text,end="  ")
    print()        
                
def close_alert():
    try:
        time.sleep(1)
        alert = driver.switch_to_alert()
        alert.accept()
    except:
        print ("no alert")



if __name__ == "__main__":
    main()
























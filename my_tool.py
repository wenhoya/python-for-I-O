import __main__
import os,time,subprocess
def is_ping_fail(a):
    hostname = a
    response = os.system("ping -n 2 " + hostname)
    # and then check the response...
    #if response == 0:
    #    pingstatus = "Network Active"
        #active+=1
    #else:
    #    pingstatus = "Network Error"
        #inactive+=1
    #print(pingstatus)
    #return pingstatus
    return response
def is_ping_fail_new(a):
    hostname = a
    p = subprocess.Popen("ping "+ hostname)
    # Linux Version p = subprocess.Popen(['ping','127.0.0.1','-c','1',"-W","2"])
    # The -c means that the ping will stop afer 1 package is replied 
    # and the -W 2 is the timelimit
    p.wait()
    return p.poll()
    
def write_file_old(b):
    file_name=os.path.splitext(__file__)[0]+".txt"
    f = open(file_name, 'a', encoding = 'UTF-8')
    with f as g:
        print(b, end=" ")
        #print(end="\r\n ", file=g)                       
        print(b, end=" ", file=g)
    f.close()
def write_file(b,b1=None,b2=None):
    file_name=os.path.splitext(__main__.__file__)[0]+".txt"
    f = open(file_name, 'a', encoding = 'UTF-8')
    with f as g:
        if b1==None:
            print(b, end=" ")
            print(b, end=" ", file=g)          
        elif b2==None:
            print(b,b1, end=" ")
            print(b,b1, end=" ", file=g)
        else:
            print(b,b1,b2, end=" ")
            print(b,b1,b2, end=" ", file=g)
    f.close()    
#print(ping_check("192.168.1.1"))
#wfile("abc")
def current_time():
    now = time.strftime("%c")
    now1 = "Current date & time : " + now +"\r\n"
    return now1
	
def abc():
    pass
if __name__ == "__main__":
    c=write_file_new("123","456","789")
    d=write_file_new("123")    
    e=write_file_new("b1","b2")        
    print(__main__.__file__)
    #time.sleep(10)
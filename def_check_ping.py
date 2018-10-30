import unittest, time, re, sys, os
class Test(unittest.TestCase):
    def setUp(self):
        self.ping_check_host = "192.168.111.1"
    def test_(self):
            ping=self.check_ping()
            if ping == "Network Error":
                print("Network Error", end=" ")
            else :    
                print("Network Active", end=" ")

    
    def check_ping(self):
        hostname = self.ping_check_host
        response = os.system("ping -n 2 " + hostname)
        # and then check the response...
        if response == 0:
            pingstatus = "Network Active"
            #active+=1
        else:
            pingstatus = "Network Error"
            #inactive+=1
        
        print(pingstatus)
        return pingstatus

if __name__ == "__main__":
    unittest.main(exit=False)        
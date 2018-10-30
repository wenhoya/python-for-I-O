import unittest, time, re, sys, os
class Test(unittest.TestCase):
    def test_(self):
        #self.current_time()
        print(self.current_time())
    
    def current_time(self):
        now = time.strftime("%c")
        now1 = "Current date & time : " + now
        #print(now1)
        return now1

if __name__ == "__main__":
    unittest.main(exit=False)        
import tkinter as tk
base = tk.Tk()
radio_value = tk.IntVar()
radio_value.set(0)
base_ip = "192.168.0.1"
username = "admin"
password = "1234"

def main():
    lunch = {
        0: aa,
        1: a,
        2: b,
        3: c,
        4: d,
        }
    tk.Label(text="Login IP: "+base_ip).pack() 
    tk.Label(text="Login Username: "+username).pack() 
    tk.Label(text="Login Password: "+password).pack() 
    
    for i in range(len(lunch)):
        #lunch[i] = tk.StringVar()
        #print(lunch[i])
        tk.Radiobutton(text = lunch[i].__name__, variable = radio_value, value = i).pack()

    def run():
        value = radio_value.get()
        lunch[value]()


    tk.Button(base, text='Run', command=run).pack()
    base.mainloop()

def aa():
    print("aa")
    
def a():
    pass
            
def b():
    pass
            
def c():
    pass
            
def d():
    pass
        
if __name__ == "__main__":
    main()        
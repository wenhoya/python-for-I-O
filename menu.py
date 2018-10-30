import tkinter as tk
base = tk.Tk()
radio_value = tk.IntVar()
radio_value.set(0)

def main():
    lunch = {
        0: a,
        1: a,
        2: b,
        3: c,
        4: d,
        }

    for i in range(len(lunch)):
        tk.Radiobutton(text = lunch[i].__name__, variable = radio_value, value = i).pack(anchor=tk.W)

    def run():
        value = radio_value.get()
        lunch[value]()

    tk.Button(base, text='Run', command=run).pack()
    base.mainloop()

def a():
    print("a")
    text = "Test text"
    output = tk.Tk()
    tk.Scrollbar(output).pack()
    for i in range(100):
        # How to save lable or copy the text ?
        tk.Label(output,text="Test text: "+text).pack() 
            
def b():
    pass
            
def c():
    pass
            
def d():
    pass
        
if __name__ == "__main__":
    main()        
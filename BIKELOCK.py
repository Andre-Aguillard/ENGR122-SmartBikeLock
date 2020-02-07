import RPi.GPIO as GPIO
import serial
from Tkinter import *       ### This is to set up a GUI for the lock.
from time import sleep, time
### GUI for the Lock:
class GUI4Lock(Frame):
    def __init__(self, master):
        Frame.__init__(self,master) ### This sets up the main window of the GUI
        self.master = master     ### in order to build widgets on to top it.
        self.images = []
        
    # image getter   
    @property
    def images(self):
        return self._images        
    # image getter
    @images.setter
    def images(self, value):
        self._images = value
      
    def setupGUI(self):
        #organize the GUI
        # this function works fine, as long as you have the images as actual GIFs
        self.pack(fill=BOTH, expand=1)

        # setup text at top of the GUI
        # first, place frame where the text will be displayed
        text_frame = Frame(self, width=WIDTH, height=HEIGHT/3)
        # widget - same deal as above
        # disable by default
        # don't let it control frame's size 
        GUI4Lock.text = Text(text_frame, bg="lightgrey", state=DISABLED)
        GUI4Lock.text.pack(fill=Y, expand=1)
        text_frame.pack(side=TOP, fill=X, expand=1)
        text_frame.pack_propagate(False)
        
        # setup image to the left of the GUI
        # widget is a Tkinter label
        # don't let image control width's size
        img = None
        GUI4Lock.image = Label(self, width=WIDTH/2, height=HEIGHT/2, image = img)
        GUI4Lock.image.image = img
        GUI4Lock.image.pack(side= LEFT, fill=Y, expand=1)
        GUI4Lock.image.pack_propagate(False)
        
        ##Frame to hold the buttons, Yes Andre figured out how to do this himself.
        button_frame = LabelFrame(self,text="Buttons for user input" ,width= WIDTH/2, height=HEIGHT, relief =RAISED)
        ##Define what each button looks like and does. 
        GUI4Lock.button1= Button(button_frame, text="1", padx=10, pady=10, width=10,command= lambda: inputNumber(1))
        GUI4Lock.button2= Button(button_frame, text="2", padx=10, pady=10, width=10,command= lambda: inputNumber(2))
        GUI4Lock.button3= Button(button_frame, text="3", padx=10, pady=10, width=10,command= lambda: inputNumber(3))
        GUI4Lock.button4= Button(button_frame, text="4", padx=10, pady=10, width=10,command= lambda: inputNumber(4))
        GUI4Lock.button5= Button(button_frame, text="5", padx=10, pady=10, width=10,command= lambda: inputNumber(5))
        GUI4Lock.button6= Button(button_frame, text="6", padx=10, pady=10, width=10,command= lambda: inputNumber(6))
        GUI4Lock.button7= Button(button_frame, text="7", padx=10, pady=10, width=10,command= lambda: inputNumber(7))
        GUI4Lock.button8= Button(button_frame, text="8", padx=10, pady=10, width=10,command= lambda: inputNumber(8))
        GUI4Lock.button9= Button(button_frame, text="9", padx=10, pady=10, width=10,command= lambda: inputNumber(9))
        GUI4Lock.button0= Button(button_frame, text="0", padx=10, pady=10, width=10,command= lambda: inputNumber(0))
        GUI4Lock.buttonPOUND= Button(button_frame, text="#", padx=10, pady=10, width=10,command= lambda: inputNumber("#"))
        GUI4Lock.buttonRFID= Button(button_frame, text="RFID", padx=10, pady=10, width=10, command= RFID_tag)
        GUI4Lock.buttonY= Button(button_frame, text="YES", padx=10, pady=10, width=10,command=  inputYES)
        GUI4Lock.buttonN= Button(button_frame, text="NO", padx=10, pady=10, width=10,command= inputNO) 
        ##place the buttons in a grid within the button frame.
        GUI4Lock.button1.grid(row=0, column=0)
        GUI4Lock.button2.grid(row=0, column=1)
        GUI4Lock.button3.grid(row=0, column=2)
        GUI4Lock.button4.grid(row=1, column=0)
        GUI4Lock.button5.grid(row=1, column=1)
        GUI4Lock.button6.grid(row=1, column=2)
        GUI4Lock.button7.grid(row=2, column=0)
        GUI4Lock.button8.grid(row=2, column=1)
        GUI4Lock.button9.grid(row=2, column=2)
        GUI4Lock.button0.grid(row=3, column=1)
        GUI4Lock.buttonRFID.grid(row=4, column=1)
        GUI4Lock.buttonY.grid(row=5, column=0)
        GUI4Lock.buttonN.grid(row=5, column=2)
        GUI4Lock.buttonPOUND.grid(row=5, column=1)
        # initalize the button-frame, and don't let it control the frame's size
        ## Place it on the right side and let it be full sized.         
        button_frame.pack(side=RIGHT, fill=X, expand=1)
        button_frame.pack_propagate(False)
           
    def start(self):
        self.setupGUI()
        self.setLogoImage()
        setup()
        displayHome()
 
    def setLogoImage(self):
        GUI4Lock.original =PhotoImage(file="bikelock.gif")
        #resize the image to fit. 
        GUI4Lock.img = GUI4Lock.original.subsample(5,5)
        # display image to left
        GUI4Lock.image.config(image=GUI4Lock.img)
        GUI4Lock.image.image = GUI4Lock.img
def RFID_tag():
    # This takes the time the function was called, and converts it to Milliseconds
    startTime = int(time() * 1000)
    while (int(time()*1000) < startTime + 5 *1000):
        response = "Entering RFID mode. \n\nPlease scan your RFID card now."
        display(response)
        data = ser.read(12)
        # Attempt to validate the data we just read.
        code = validate_rfid(data)
        if (code in locks) :
            #If code is in locks, then the person is unlocking their lock so open the lock
            openLock(code)
            #Since this is the second time the code is scanned, that lock is now free, and empty
            emptyLocks.append (locks[code])
            # And it also is no longer associated with a code. 
            del locks[code]
            # Set the response. 
            ## The response will be display on the GUI once that is finished
            response = "Thank you for using a better bike lock, \n" \
                    +"We appreciate your business. Have a great day!"
            display(response)
            sleep(4)
            displayHome()
            break
        elif(code):
            #If its a new code, check to see if there are any open locks
            response = "Checking for open locks..."
            display(response)
            checkLocks(code)
            display("Thank you for using a better bike lock, \n" \
                    +"We appreciate your business. Have a great day!")
            sleep(2)
            displayHome()
            break
    else:        
        response = "The RFID scanner has timed out. \nPlease press the button again or enter " \
                "a manual code by pressing the buttons. \n\nThank You. "
        display(response)
        sleep(2)
        displayHome()

def validate_rfid(code):
    # A valid code will be 12 characters long with the first char being
    # a line feed and the last char being a carriage return.
    s = code.decode("ascii")

    if (len(s) == 12) and (s[0] == "\n") and (s[11] == "\r"):
        # We matched a valid code.  Strip off the "\n" and "\r" and just
        # return the RFID code.
        return s[1:-1]
    else:
        # We didn't match a valid code, so return False.
        return False
    
def setup():
    # Initialize the Raspberry Pi by quashing any warnings and telling it
    # we're going to use the BCM pin numbering scheme.
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    # This pin corresponds to GPIO18, which we'll use to turn the RFID
    # reader on and off with.
    GPIO.setup(ENABLE_PIN, GPIO.OUT)
    
    # Next we'll create a list generated from the number of locks in the
    # system, and use that to link them to GPIO pins from a list of available ones. 
    pins = [21,20,16,12,26,19,13,6,5,25,24,23]
    global locksWithPins
    locksWithPins = {} # A dictionary to keep track of which pins are associated with
                       # which locks
    for x in range (1,NUMBER_OF_LOCKS+1):
      locksWithPins[x] = pins[0]
      GPIO.setup(pins[0], GPIO.OUT)
      del pins[0]
      
      
    # Setting the pin to LOW will turn the reader on.  You should notice
    # the green LED light on the reader turn red if successfully enabled.

    display("Enabling RFID reader...\n")
    GPIO.output(ENABLE_PIN, GPIO.LOW)
    # Set ser as a global so it can be accessed later in the program. 
    global ser
    # Set up the serial port as per the Parallax reader's datasheet.
    ser = serial.Serial(baudrate = 2400,
                      bytesize = serial.EIGHTBITS,
                      parity   = serial.PARITY_NONE,
                      port     = SERIAL_PORT,
                      stopbits = serial.STOPBITS_ONE,
                      timeout  = 1)
        
    # Create a dictionary that associates the bike lock number with a code -Aguillard
    global locks
    locks = {}
    # Create a list of empty locks based initially off the number of locks -Aguillard
    # in the system
    global emptyLocks
    emptyLocks = [x for x in range (1,(NUMBER_OF_LOCKS + 1))]

# Assigns a code to a lock
def assignLock(code):
    ## The code for the lock is the key in the dictionary and the empty lock number
    ## becomes the value paired with it.
    locks[code] = emptyLocks[0]
    # If we assign a lock, we must then open that lock for the user to use.
    openLock(code)
    #And since that lock is full, remove it from the list of open locks
    del emptyLocks[0]

# Checks to see if there are any open locks
def checkLocks(code):
    # If there are no empty locks, then there's nothing else to do.
    if (emptyLocks == []):
        response = "Sorry there are no empty locks at this time, \
                    please try again later."
        display(response)
        sleep(2)
    # If there are emptylocks, then assign a lock
    else:
        response = "Assigning you a lock..."
        display(response)
        sleep(2)
        assignLock(code)

# Unlocks a lock and adds a that lock back to the list of empty locks
def openLock(code):
    # Opens the locks
    global locksWithPins
    response =("You have {} seconds to access your lock").format(OPEN_TIME)
    display(response)
    window.update
    sleep(2)
    x = locks[code]
    response = ("You have {} seconds to access your lock \n\nOpening lock... ").format(OPEN_TIME)
    display(response)
    window.update
    GPIO.output(locksWithPins[x], GPIO.HIGH)
    sleep(OPEN_TIME)
    display("Closing lock...")
    sleep(2)
    GPIO.output(locksWithPins[x], GPIO.LOW)

def inputNumber(number):
        #Turns the input number into a string
        number = str(number)
        #accesses the global list ManCode
        global ManCode
        if (len(ManCode)== 10):
            GUI4Lock.button0.config(state=DISABLED)
            GUI4Lock.button1.config(state=DISABLED)
            GUI4Lock.button2.config(state=DISABLED)
            GUI4Lock.button3.config(state=DISABLED)
            GUI4Lock.button4.config(state=DISABLED)
            GUI4Lock.button5.config(state=DISABLED)
            GUI4Lock.button6.config(state=DISABLED)
            GUI4Lock.button7.config(state=DISABLED)
            GUI4Lock.button8.config(state=DISABLED)
            GUI4Lock.button9.config(state=DISABLED)
            #Redefine global variable mCode to the code that is manually entered.
            global mCode
            mCode = "".join(ManCode)
            display("Your Bike Lock Code is: " + mCode + "\n\nIt is recommended that you" \
                            + " write down\nyour code, or take a picture of it \nwith your phone." + \
                            "\n\nAre you satisfied with your code? \nPress YES or NO to the left to \nconfirm.")
            ## Waites for manual input and clears the list ManCode, then enables all the number buttons again.
            del ManCode [:]
            GUI4Lock.button0.config(state=NORMAL)
            GUI4Lock.button1.config(state=NORMAL)
            GUI4Lock.button2.config(state=NORMAL)
            GUI4Lock.button3.config(state=NORMAL)
            GUI4Lock.button4.config(state=NORMAL)
            GUI4Lock.button5.config(state=NORMAL)
            GUI4Lock.button6.config(state=NORMAL)
            GUI4Lock.button7.config(state=NORMAL)
            GUI4Lock.button8.config(state=NORMAL)
            GUI4Lock.button9.config(state=NORMAL)
        else :
            #Appends the number to ManCode list
            #Special exception for # sign
            if (number==('#')):
                if(len(ManCode)<10):
                    response = "Pound sign (#) should only be pressed at the end of your code, please input a different number"
                    display(response)
                    window.update
                    sleep(3)
                else:
                    pass
            elif(number != ("#")):        
                ManCode.append(number)
                codeCount = len(ManCode)
                GUI4Lock.text.config(state=NORMAL)
                GUI4Lock.text.delete("1.0", END)
                GUI4Lock.text.insert(END, "You've entered manual code mode. \n\n" + \
                                     "Please input a 10-digit code using \nthe number pad below and " +\
                                     "press the pound sign (#) once you're done. \n \nYour current code is: " + str(codeCount) \
                                      + " character(s)")
                GUI4Lock.text.config(state=DISABLED)

def inputYES():
    global mCode
    if (len(mCode)==10):
        response = "Fantastic! Proceeding to Locking Method..."
        display(response)
        sleep(2)
        manualCode(mCode)
        mCode = ""
    else:
        response = "Please use the keypad >>>" +"\nto input a manual code."
        display(response)
    
def inputNO():
    if (len(mCode)==10):
        displayHome()
    else:
        response = "Please use the keypad >>>" +"\nto input a manual code."
        display(response)      
            
def manualCode(mCode):
    if (mCode in locks) :
        #If code is in locks, then the person is unlocking their lock so open the lock
        display("Code accepted! Accessing Lock Now...")
        window.update
        openLock(mCode)
        #Since this is the second time the code is scanned, that lock is now free, and empty
        emptyLocks.append (locks[mCode])
        # And it also is no longer associated with a code. 
        del locks[mCode]
        # Set the response. 
        ## The response will be display on the GUI once that is finished
        response = "Thank you for using a better bike lock, \n" \
                +"We appreciate your business. Have a great day!"
        display(response)
        sleep(3)
        displayHome()
    #If its a new code, check to see if there are any open locks
    else:
        response = "Checking for open locks..."
        display(response)
        sleep(2)
        checkLocks(mCode)
        display("Thank you for using a better bike lock, \n" \
                +"We appreciate your business. Have a great day!")
        sleep(2)
        displayHome()
                
def display(response):
    GUI4Lock.text.config(state=NORMAL)
    GUI4Lock.text.delete("1.0", END)
    # Display the desired text on the screen.
    GUI4Lock.text.insert(END, response)
    print (response)
    GUI4Lock.text.config(state=DISABLED)
    window.update()
    
def displayHome():
    GUI4Lock.text.config(state=NORMAL)
    GUI4Lock.text.delete("1.0", END)
    # Display the desired text on the screen.
    GUI4Lock.text.insert(END, "Welcome to a Better Bike Lock Home screen.\n\nTo begin, please hit the " \
                + "RFID button to scan a compatable RFID card \nor hit a number to enter a manual code." \
                + "\n\nTo unlock your bike, either scan your RFID card again, \nor re-enter your manual code.")
    print (displayHome)
    GUI4Lock.text.config(state=DISABLED)
    window.update()


#Used to define the height and width of the GUI
WIDTH = 950 
HEIGHT= 440
##Variables to use if the code is inputed manually.
ManCode = []
global mCode

window = Tk()
window.title("Better Bike Lock Home")

ENABLE_PIN  = 18              # The BCM pin number corresponding to GPIO18
SERIAL_PORT = '/dev/ttyAMA0'  # The location of our serial port.  This may
                              # vary depending on OS version.
  
NUMBER_OF_LOCKS = 2           #set the number of locks
OPEN_TIME = 10                ### Time that lock is open for

t = GUI4Lock(window)
#Starts the program
t.start()
window.mainloop()

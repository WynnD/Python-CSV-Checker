# Monitor Pilot.csv for file changes, do other cool stuff

'''feature ideas:
'''

from urllib import request
from time import sleep
#from tkinter import messagebox
from tkinter import *
from smtplib import *
from tkinter import messagebox
from email.mime.text import MIMEText

class PilotCSVReader(Frame):
    


    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.pack()

        #how to change tkinter frame title?
        
        #make Label that updates number (v) of weekly new users
        self.v = StringVar()
        self.v.set("0")
        self.label = Label(self, textvariable=self.v)
        
        
        #make Update button
        button = Button(self,
                        text='Update',
                        command=lambda:self.check(True))
        
        #make label that says "users"
        users = Label(self, text='Users')
        
        #pack elements
        self.label.pack()
        users.pack(side=TOP)
        button.pack(side=BOTTOM)
        
        self.check(False)
        
        self.mainloop()



    def check(self, once):
        'check if americanwx file is changed'
        try:
            #get userlists
            
            #from americanwx
            infile = request.urlopen('http://www.americanwx.com/models/pilot.csv')
            self.userlistwx = infile.readlines()
            self.v.set(str(len(self.userlistwx)))
            infile.close()

            #local (google drive) file
            infile = open('pilot.csv')
            userlistloc = infile.readlines()
            infile.close()

            #find number of lines to isolate
            self.newusers = len(self.userlistwx)-len(userlistloc)

            if self.newusers > 0:
                if self.newusers == 1:
                    messagebox.showinfo("New user!","1 new user!")
                else:
                    messagebox.showinfo("New users!","{} new users!".format(self.newusers))
                self.edit()
        except:
            self.after(2000, lambda:self.check(True))
            
        #repeat every 15 seconds
        if once == False:
            self.after(900000, lambda:self.check(False))



    def edit(self):
        'edits local file to add names'

        #isolate lines to add
        self.addlst = self.userlistwx[(len(self.userlistwx)-self.newusers):]

        #open local pilot.csv to edit
        editfile = open('pilot.csv','a')

        #add names to local pilot.csv
        for i in range(len(self.addlst)):
            self.addlst[i] = self.addlst[i].decode("utf-8")
            if self.addlst[i][-1] == "\n":
                self.addlst[i] = self.addlst[i][:-1]
            editfile.write("\n"+(self.addlst[i]))

        #send emails
        self.email()
        editfile.close()



    def email(self):
        'sends email notification'

        #log in to gmail
        email = SMTP_SSL('smtp.gmail.com',465)
        email.login('wynnd5595@gmail.com','Time2pretend')

        #add new subscribers' information
        sublist = '\n'.join(self.addlst)
        sublist = sublist.split('\n')

        info = 'New User Information:\n\n'

        for i in range(0,len(sublist)):
            line = sublist[i]
            elements = line.split(',')
            info += 'Username: '+elements[1]+'\n'+\
                    'Email: '+elements[2]+'\n\n'
        
        
        
        #create new messagebody
        if self.newusers == 1:
            subject = 'Woo hoo! We have a new pilotwx user!'
            messagebody = 'Dear Pilot Safety 1,\n\n'+'Good news! We have a new pilotwx user!\n\n\n'+info+'\nFull list of users here: '\
                      'https://drive.google.com/file/d/0By9p3-olIy0YN1dSUHBNRmJlQjA/edit?usp=sharing'+'\n\nSincerely,\nPS1Bot'
        else:
            subject = 'Woo hoo! We have {} new pilotwx users!'.format(self.newusers)
            messagebody = 'Dear Pilot Safety 1,\n\n'+'Good news! We have {} new pilotwx users!\n\n\n'.format(self.newusers)+info+'\nFull list of users here: '\
                      +'https://drive.google.com/file/d/0By9p3-olIy0YN1dSUHBNRmJlQjA/edit?usp=sharing'+'\n\nSincerely,\nPS1Bot'

        #build email object
        msg = MIMEText(messagebody)

        msg['Subject'] = subject
        msg['From'] = 'PS1bot@pilotsafety1.com'
        msg['To'] = 'wynnd5595@gmail.com, pilotsafety1@gmail.com'
        
        
        
        email.sendmail('wynnd5595@gmail.com','wynnd5595@gmail.com',msg.as_string())
        email.sendmail('wynnd5595@gmail.com','pilotsafety1@gmail.com',msg.as_string())


        email.quit()


s = PilotCSVReader()

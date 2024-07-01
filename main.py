import os
!pip install setuptools
import io
import tempfile
import sys
import subprocess
import pkg_resources
import webbrowser
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

import base64
from tkinter import Tk,PhotoImage
from PIL import Image,ImageTk

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

requiredPackages= ['pycryptodomex','pillow','cryptography']
for packages in requiredPackages:
    try:
        pkg_resources.get_distribution(packages)
    except pkg_resources.DistributionNotFound:
        print(f"{packages} is not installed,installing...")
        subprocess.check_call(['pip','install',packages])


from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad,unpad
from Cryptodome.Random import get_random_bytes
from cryptography.fernet import Fernet



#creating a main window


root=tk.Tk()
root.title("Folder encryption software")
root.geometry("600x500")
window_width=600
window_height=500
screen_width=root.winfo_screenwidth()
screen_height=root.winfo_screenheight()
x=int((screen_width/2)-(window_width/2))
y=int((screen_height/2)-(window_height/2))
root.geometry(f"{window_width}x{window_height}+{x}+{y}")
root.configure(bg='black')



def button1_click():
    global folder_window
    folder_window=tk.Toplevel(root)
    folder_window.geometry("560x200")
    folder_window.title("encryption")

    folderPath_label=tk.Label(folder_window,text="folder path")
    email_label=tk.Label(folder_window,text="sender mail")
    smtp_label=tk.Label(folder_window,text="smtp password")
    receiver_label=tk.Label(folder_window,text="receiver mail")

    folderPath_entry=tk.Entry(folder_window,width=60)
    email_entry=tk.Entry(folder_window,width=60)
    smtp_entry=tk.Entry(folder_window,width=60,show="*")
    receiver_entry=tk.Entry(folder_window,width=60)


    def browse_folder():
        inital_directory='/'
        folder_path = filedialog.askdirectory(initialdir=inital_directory)
        folderPath_entry.delete(0,tk.END)
        folderPath_entry.insert(0,folder_path)

    browse_button=tk.Button(folder_window,text="Browse",font=("Arial", 10, "bold"), padx=10, pady=10,command=browse_folder)

    
    def encrypt_folder():
        
        folder_path =folderPath_entry.get()
        sender_mail=email_entry.get()
        reciver_mail=receiver_entry.get()
        smtp_password=smtp_entry.get()
        if folder_path =='':
            messagebox.showerror("error","please select a folder")
            return
        if not os.path.exists(folder_path):
            messagebox.showerror("error","Invalid folder path")
            return
        Key=Fernet.generate_key()
        fernet=Fernet(Key)
        # pass_path='F:\enc\pass.txt'
        # with open(pass_path,'wb') as file:
        #     file.write(Key)

        sender_mail=sender_mail
        reciver_mail=reciver_mail
        subject='The key for ecrypted folder'
        message='the key for encrypted folder'+folder_path+'is \n'+str(Key)

        smtp_server="smtp.gmail.com"
        smtp_port=587
        smtp_username=sender_mail
        smtp_password=smtp_password

        msg=MIMEMultipart()
        msg['From']=sender_mail
        msg['To']=reciver_mail
        msg['Subject']=subject

        msg.attach(MIMEText(message,'plain'))

        server = smtplib.SMTP(smtp_server,smtp_port)
        server.starttls()
        server.login(smtp_username,smtp_password)

        server.send_message(msg)
        server.quit()
        messagebox.showinfo("Info","check mail")

        for filename in os.listdir(folder_path):
            filepath = os.path.join(folder_path,filename)
            if os.path.isfile(filepath):
                with open(filepath,'rb') as file:
                    data = file.read()
                encrypted_data=fernet.encrypt(data)
                with open(filepath,'wb') as file:
                    file.write(encrypted_data)


    
    encrypt_button=tk.Button(folder_window,text="ENCRYPT",font=("Arial", 10, "bold"),bg="red",fg="white",command=encrypt_folder)

    folderPath_label.grid(row=0,column=0,pady=5)
    email_label.grid(row=1,column=0,pady=5)
    browse_button.grid(row=0,column=2,padx=12)
    smtp_label.grid(row=2,column=0,pady=5)
    receiver_label.grid(row=3,column=0,pady=5)

    folderPath_entry.grid(row=0,column=1,pady=5)
    email_entry.grid(row=1,column=1,pady=5)
    smtp_entry.grid(row=2,column=1,pady=5)
    receiver_entry.grid(row=3,column=1,pady=5)
    encrypt_button.grid(row=5,column=1,pady=10)


def button2_click():
    global folder_window
    folder_window=tk.Toplevel(root)
    folder_window.geometry("560x150")
    folder_window.title("decryption")

    folderPath_label=tk.Label(folder_window,text="folder path")
    password_label=tk.Label(folder_window,text="password")

    folderPath_entry=tk.Entry(folder_window,width=60)
    password_entry=tk.Entry(folder_window,width=60)

    def browse_folder():
        inital_directory='/'
        folder_path = filedialog.askdirectory(initialdir=inital_directory)
        folderPath_entry.delete(0,tk.END)
        folderPath_entry.insert(0,folder_path)

    browse_button=tk.Button(folder_window,text="Browse",font=("Arial", 10, "bold"), padx=10, pady=10,command=browse_folder)

    def decrypt_folder():
        folder_path =folderPath_entry.get()
        password=password_entry.get()
        if folder_path =='':
            messagebox.showerror("error","please select a folder")
            return
        if not os.path.exists(folder_path):
            messagebox.showerror("error","Invalid folder path")
            return
        if password=='':
            messagebox.showerror("error","no password entered")
            return
        
        try:
            Key = bytes(password.encode())
            Key=Key[2:-1]
            try:
                fernet=Fernet(Key)
                for filename in os.listdir(folder_path):
                    filepath = os.path.join(folder_path,filename)
                    if os.path.isfile(filepath):
                        with open(filepath,'rb') as file:
                            encrypted_data = file.read()
                        decrypted_data=fernet.decrypt(encrypted_data)
                        print(f"the decrypted data is {decrypted_data}")
                        with open(filepath,'wb') as file:
                            file.write(decrypted_data)
                messagebox.showinfo("Info","decrypted successfully")
            except :
                messagebox.showerror("Error","invalid keys")
                return
        except:
            messagebox.showinfo("Info","Already decrypted")
            return
        
    decrypt_button=tk.Button(folder_window,text="DECRYPT",font=("Arial", 10, "bold"),bg="red",fg="white",command=decrypt_folder)

    folderPath_label.grid(row=0,column=0)
    password_label.grid(row=1,column=0)
    
    browse_button.grid(row=0,column=2,padx=12)

    folderPath_entry.grid(row=0,column=1)
    password_entry.grid(row=1,column=1)


    decrypt_button.grid(row=2,column=1,pady=10)

def button3_click():
    global folder_window
    folder_window=tk.Toplevel(root)
    folder_window.geometry("300x100")
    folder_window.title("file")

    folderPath_label=tk.Label(folder_window,text="folder path")
    folderPath_entry=tk.Entry(folder_window)
    

    def browse_folder():
        inital_directory='/'
        folder_path = filedialog.askdirectory(initialdir=inital_directory)
        folderPath_entry.delete(0,tk.END)
        folderPath_entry.insert(0,folder_path)

    browse_button=tk.Button(folder_window,text="Browse",font=("Arial", 10, "bold"), padx=10, pady=10,command=browse_folder)

    def hide_folder():
        folder_path=folderPath_entry.get()
        if folder_path =='':
            messagebox.showerror("error","please select a folder")
            return
        if not os.path.exists(folder_path):
            messagebox.showerror("error","Invalid folder path")
            return
        result=subprocess.run(["attrib", "+h", folder_path], capture_output=True, text=True)
        if result.returncode==0:
            messagebox.showinfo("info",f"folder has been hidden, the path is {folder_path}")
            return
        else:
            messagebox.showerror("error","the file is  not hidden")
    
    def unhide_folder():
        folder_path=folderPath_entry.get()
        if folder_path =='':
            messagebox.showerror("error","please enter the folder path")
            return
        if not os.path.exists(folder_path):
            messagebox.showerror("error","Invalid folder path")
            return
        result=subprocess.run(["attrib", "-h", folder_path], capture_output=True, text=True)
        if result.returncode==0:
            messagebox.showinfo("info",f"folder has been unhidden, the path is {folder_path}")
            return
        else:
            messagebox.showerror("error","the file is still hidden")
        

    hide_button=tk.Button(folder_window,text="HIDE",font=("Arial", 10, "bold"),bg="red",fg="white",command=hide_folder)
    unhide_button=tk.Button(folder_window,text="UNHIDE",font=("Arial", 10, "bold"),bg="red",fg="white",command=unhide_folder)

    folderPath_label.grid(row=0,column=0)
    browse_button.grid(row=0,column=2,padx=12)
    folderPath_entry.grid(row=0,column=1)
    hide_button.grid(row=1,column=0,pady=10)
    unhide_button.grid(row=1,column=1,pady=10)




button_frame=tk.Frame(root, bg='grey',width=x/2,height=y)
button_frame.pack(expand=True)

button1 = tk.Button(button_frame, text="ENCRYPT FOLDER", font=("Arial", 14, "bold"), padx=10, pady=5,command=button1_click)
button2 = tk.Button(button_frame, text="DECRYPT FOLDER", font=("Arial", 14, "bold"), padx=10, pady=5,command=button2_click)
button3=tk.Button(button_frame, text="HIDE FOLDER", font=("Arial", 14, "bold"), padx=10, pady=5,command=button3_click)

button1.grid(row=0,column=0,padx=10,pady=10)
button2.grid(row=1,column=0,padx=10,pady=10)
button3.grid(row=2,column=0,padx=10,pady=10)


root.mainloop()


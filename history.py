import tkinter as tk
from tkinter import *
from tkinter import messagebox, ttk
import os
import string
import time
import sqlite3

def main_app():
    db_table = "downloads"
    db_table_primary = "id"
    db_column1 = "name"
    db_column2 = "type_and_time"
    db_column3 = "url"

    mydb = sqlite3.connect ("downloads.db")

    top =tk.Tk()
    top.title("Database Table Editing Tool")
    top.geometry("500x500")


    def table_contents():
      newWindow = Toplevel(top)
      newWindow.title("Users List")

      # The Restart Function

      def restart():
        newWindow.destroy()
        table_contents()

        # New Connection To Refresh The Database

      mydb = sqlite3.connect ("downloads.db")

        # sets the geometry of toplevel
      newWindow.geometry("840x600")

        # The SQL To Fetch The Rows
      sql_id = "SELECT {} FROM `{}` ".format(db_table_primary, db_table)
      cursor_id = mydb.cursor()
      cursor_id.execute(sql_id)
      result_id = cursor_id.fetchall()

      sql_username = "SELECT {} FROM `{}` ".format(db_column1, db_table)
      cursor_username = mydb.cursor()
      cursor_username.execute(sql_username)
      result_username = cursor_username.fetchall()

      sql_userid = "SELECT {} FROM `{}` ".format(db_column2, db_table)
      cursor_userid = mydb.cursor()
      cursor_userid.execute(sql_userid)
      result_userid = cursor_userid.fetchall()

      sql_msg = "SELECT {} FROM `{}` ".format(db_column3, db_table)
      cursor_msg = mydb.cursor()
      cursor_msg.execute(sql_msg)
      result_msg = cursor_msg.fetchall()

      #
      # The ID Label, Table, And Delete Button
      #

      id_lb = Label(newWindow, text="{}".format(db_table_primary))
      id_lb.grid(row=0, column=0)

      id = Listbox(newWindow, height = 10, width = 16, bg = "white", activestyle = 'dotbox', font = "Helvetica", fg = "Black")
      for thelist in result_id:
        id.insert(1, thelist)
        id.grid(row=1, column=0)

       # To Get A Selected Entry In The Listbox

      def id_delete():
        for i in id.curselection():
            item = str(id.get(i))
            cleanitem = item.translate(str.maketrans('', '', string.punctuation))
            sql_delete = """ DELETE FROM `{}` WHERE `{}` = '{}' """.format(db_table,db_table_primary, cleanitem)
            mydb.execute(sql_delete)
            mydb.commit()
            #Label(newWindow, text="Row : {} Was Deleted Succesfully".format(cleanitem)).grid(row=5, column=2)
            restart()
        # The Delete Button
      Button(newWindow, text="Delete", command=id_delete ,activebackground="grey", activeforeground="grey").grid(row=2, column=0)

      # CONFIRMATION BUTTON

      def confirm_delete_all():
        delete_all = Toplevel(top)
        delete_all.title("Delete All Confirmation")
        delete_all.geometry("300x300")
        Button(delete_all, text="CONFIRM DELETE ALL", command=delete_all_func, activebackground="grey", activeforeground="grey", pady=10).place(relx=0.5, rely=0.5, anchor=CENTER)
        global close_confirmation
        def close_confirmation():
          delete_all.destroy()

      # THE DELETE ALL FUNCTION
      def delete_all_func():
        for contents in result_id:
          item = str(contents)
          cleanitem = item.translate(str.maketrans('', '', string.punctuation))
          sql_delete_all = """ DELETE FROM `{}` WHERE `{}` = '{}' """.format(db_table, db_table_primary, cleanitem)
          mydb.execute(sql_delete_all)
          mydb.commit()
        restart()
        close_confirmation()



      # THE DELETE ALL BUTTON

      Button(newWindow, text="Delete All", command=confirm_delete_all, activebackground="grey", activeforeground="grey").grid(row=4, column=0)

      #
      # The Username Label, Table
      #

      uname_lb = Label(newWindow, text="{}".format(db_column1))
      uname_lb.grid(row=0, column=1)

      uname = Listbox(newWindow, height = 10, width = 16, bg = "white", activestyle = 'dotbox', font = "Helvetica", fg = "Black")
      for thelist in result_username:
        uname.insert(1, thelist)
        uname.grid(row=1, column=1)


      #
      # The UserId Label, Table
      #

      uid_lb = Label(newWindow, text="{}".format(db_column2))
      uid_lb.grid(row=0, column=2)

      uid = Listbox(newWindow, height = 10, width = 16, bg = "white", activestyle = 'dotbox', font = "Helvetica", fg = "Black")
      for thelist in result_userid:
        uid.insert(1, thelist)
        uid.grid(row=1, column=2)

      # The Message Content Label, Table

      msg_lb = Label(newWindow, text="{}".format(db_column3))
      msg_lb.grid(row=0, column=3)

      msg_content = Listbox(newWindow, height = 10, width = 25, bg = "white", activestyle = 'dotbox', font = "Helvetica", fg = "Black")
      for thelist in result_msg:
       msg_content.insert(1, thelist)
       msg_content.grid(row=1, column=3)


      ###
      Label(newWindow, text="").grid(row=3, column=0)

      # Refresh Button
      refresh = Button(newWindow, text="Refresh", command=restart, activebackground='grey', activeforeground='grey', pady=10)
      refresh.grid(row=4, column=2)

      ## Reset ID To Zero

      Label(newWindow, text="").grid(row=7, column=0)

      def reset_primary():
        sql_reset_id = """UPDATE sqlite_sequence SET seq = 0 WHERE name = '{}';""".format(db_table)
        Label(newWindow, text="The Table Must Be Empty For This To Work").grid(row=7, column=2)
        mydb.execute(sql_reset_id)
        mydb.commit()

      reset = Button(newWindow, text="Reset {} To Zero".format(db_table_primary), command=reset_primary, activebackground='grey', activeforeground='grey', pady=10)
      reset.grid(row=9, column=2)

      # TextBox Creation
    empty_space = tk.Label(top, text="")
    empty_space.pack()

    mylist = Button(top, text="Download History", command= table_contents, activebackground="blue", activeforeground="magenta", pady=10)
    mylist.pack()
    lbl = tk.Label(top, text = "Made By MortexAG")
    lbl.pack(side="bottom")

    top.mainloop()
#main_app()
#except Exception as e:
#  print(e)


from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from sqlite3 import *
import matplotlib.pyplot as plt
import requests
import bs4

def f1():
	add_window.deiconify()
	main_window.withdraw()

def f2():
	main_window.deiconify()
	add_window.withdraw()

def f3():
	view_window.deiconify()
	main_window.withdraw()
	vw_st_data.delete(1.0, END)
	info=""
	con = None
	try:
		con = connect("dfp.db")
		cursor = con.cursor()
		sql = "select * from employee"
		cursor.execute(sql)
		data = cursor.fetchall()
		for d in data:
			info = info + "id:" + str(d[0]) + "name" + str(d[1]) + "salary" + str(d[2]) + "\n"
		vw_st_data.insert(INSERT,info)
	except Exception as e:
		showerror("Isuue", e)
	finally:
		if con is not None:
			con.close()

def f4():
	main_window.deiconify()
	view_window.withdraw()

def f5():
	update_window.deiconify()
	main_window.withdraw()

def f6():
	main_window.deiconify()
	update_window.withdraw()

def f7():
	delete_window.deiconify()
	main_window.withdraw()

def f8():
	main_window.deiconify()
	delete_window.withdraw()

def f9():
	charts_window.deiconify()
	main_window.withdraw()
	con = None
	try:
		con = connect("dfp.db")
		cursor = con.cursor()
		sql = " select name, salary from employee "
		cursor.execute(sql)
		name = []
		salary = []
		data = cursor.fetchall()
		for d in data:
			name.append(d[0])
			salary.append(d[1])
		salary.sort()
		salary.reverse()
		salary = salary[0:5]
		name = name[0:5]
		plt.bar(name, salary)
		plt.xlabel("Name")
		plt.ylabel("Salary")
		plt.title("Employee With Salaries")
		plt.show()
	except Exception as e:
		showerror("issue ", e)
		con.rollback()
	finally:
		if con is not None:
			con.close()

def f10():
	main_window.deiconify()
	charts_window.withdraw()

def f11():
	con = None
	try:
		con = connect("dfp.db")
		cursor = con.cursor()
		sql = "insert into employee values('%s','%s','%s')"
		id = aw_ent_id.get()
		name = aw_ent_name.get()
		salary = aw_ent_salary.get()
		lc = 0
		for s in name:
			if s.isalpha() is False:
					showinfo("Name","Enter only alphabets")
			else:
					lc = lc + 1
		if lc < 2:
				showinfo("Name","Enter min. 2 alphabets")
		elif id.isnumeric() is False:
				showinfo("Id","Enter Positive Integers Only")
		elif int(id) <= 0:
				showinfo("Id","Enter Positive integers only")
		elif salary.isnumeric() is False:
				showinfo("Salary","Enter integers only")
		elif int(salary) < 8000:
				showinfo("Salary","Salary should be min of 8k")
		else:
				cursor.execute(sql%(id,name,salary))
				con.commit()
				showinfo("Success","record added")
	except Exception as e:
		showerror("issue", e)
		con.rollback()
	finally:
		aw_ent_id.delete(0, END)
		aw_ent_name.delete(0, END)
		aw_ent_salary.delete(0, END)
		if con is not None:
			con.close()

def f12():
	con = None
	try:
		con = connect("dfp.db")
		cursor = con.cursor()
		sql = "update employee set name = '%s',salary = '%s' where id = '%s' "
		id = uw_ent_id.get()
		name = uw_ent_name.get()
		salary = uw_ent_salary.get()
		lc = 0
		for s in name:
			if s.isalpha() is False:
				showinfo("Name","Enter only alphabets")
			else:
				lc = lc + 1
		if lc < 2:
			showinfo("Name","Enter min. 2 alphabets")
		elif id.isnumeric() is False:
			showinfo("Id","Enter Positive Integers Only")
		elif int(id) <= 0:
			showinfo("Id","Enter Positive integers only")
		elif salary.isnumeric() is False:
			showinfo("Salary","Enter integers only")
		elif int(salary) < 8000:
			showinfo("Salary","Salary should be min of 8k")
		else:
			cursor.execute(sql%(name,salary,id ))
			if cursor.rowcount == 1:
				con.commit()
				showinfo("Success","record updated")
			else:
				showinfo(id, " does not exists")
	except Exception as e:
		showerror("issue ", e)
		con.rollback()
	finally:
		uw_ent_id.delete(0, END)
		uw_ent_name.delete(0, END)
		uw_ent_salary.delete(0, END)
		if con is not None:
			con.close()

def f13():
	con = None
	try:
		con = connect("dfp.db")
		cursor = con.cursor()
		sql = "delete from employee where id = '%s' "
		id = dw_ent_id.get()
		if id.isnumeric() is False:
			showinfo("Id","Enter Positive Integers Only")
		else:
			cursor.execute(sql%(id))
			if cursor.rowcount == 1:
				con.commit()
				showinfo("Success","record deleted")
			else:
				showinfo(id, " does not exists")
	except Exception as e:
		showerror("issue ", e)
		con.rollback()
	finally:
		dw_ent_id.delete(0, END)
		if con is not None:
			con.close()

def f14():
	wa = "https://www.brainyquote.com/quote_of_the_day"
	res = requests.get(wa)
	
	data = bs4.BeautifulSoup(res.text, "html.parser")  
	
	info = data.find("img", {"class":"p-qotd"})

	quote = info["alt"]
	msg = Label(main_window, text=quote, font=f17)
	msg.place(x=10, y=500)
		
				 
main_window = Tk()
main_window.title("E.M.S.")
main_window.geometry("550x550+100+100")

topFrame = Frame(main_window, bd=10, relief=RIDGE)
topFrame.pack(side=TOP)

label_title = Label(topFrame, text="Employee Management System", font=('arial',20,'bold'))
label_title.grid(row=0,column=0)

f = ("Arial", 20, "bold")
f17 = ("Arial", 10, "bold")
mw_btn_add = Button(main_window, text="Add", font=f, width=10, command=f1)
mw_btn_view = Button(main_window, text="View", font=f, width=10, command=f3)
mw_btn_update = Button(main_window, text="Update", font=f, width=10, command=f5)
mw_btn_delete = Button(main_window, text="Delete", font=f, width=10, command=f7)
mw_btn_charts = Button(main_window, text="Charts", font=f, width=10, command=f9)
mw_lbl_quote = Label(main_window, text="QOTD:", font=f)
mw_lbl_QOTD = Label(main_window, text=f14(), font=f)
mw_btn_add.pack(pady=10)
mw_btn_view.pack(pady=10)
mw_btn_update.pack(pady=10)
mw_btn_delete.pack(pady=10)
mw_btn_charts.pack(pady=10)
mw_lbl_quote.pack(pady=10)
mw_lbl_QOTD.pack(pady=10)

add_window = Toplevel(main_window)
add_window.title("Add Emp")
add_window.geometry("500x500+100+100")

aw_lbl_id = Label(add_window, text="enter id", font=f)
aw_ent_id = Entry(add_window, bd=4, font=f)
aw_lbl_name = Label(add_window, text="enter name:", font=f)
aw_ent_name = Entry(add_window, bd=4, font=f)
aw_lbl_salary = Label(add_window, text="enter salary:", font=f)
aw_ent_salary = Entry(add_window, bd=4, font=f)
aw_btn_save = Button(add_window, text="Save", font=f, command=f11)
aw_btn_back = Button(add_window, text="Back", font=f, command=f2)

aw_lbl_id.pack(pady=10)
aw_ent_id.pack(pady=10)
aw_lbl_name.pack(pady=10)
aw_ent_name.pack(pady=10)
aw_lbl_salary.pack(pady=10)
aw_ent_salary.pack(pady=10)
aw_btn_save.pack(pady=10)
aw_btn_back.pack(pady=10)

add_window.withdraw()

view_window = Toplevel(main_window)
view_window.title("View Employee")
view_window.geometry("500x500+100+100")

vw_st_data = ScrolledText(view_window, width=30, height=10, font=f)
vw_btn_back = Button(view_window, text="Back", font=f, command=f4)

vw_st_data.pack(pady=10)
vw_btn_back.pack(pady=10)

view_window.withdraw()

update_window = Toplevel(main_window)
update_window.title("Update Employee")
update_window.geometry("500x500+100+100")

uw_lbl_id = Label(update_window, text="enter id", font=f)
uw_ent_id = Entry(update_window, bd=4, font=f)
uw_lbl_name = Label(update_window, text="enter name:", font=f)
uw_ent_name = Entry(update_window, bd=4, font=f)
uw_lbl_salary = Label(update_window, text="enter salary:", font=f)
uw_ent_salary = Entry(update_window, bd=4, font=f)
uw_btn_save = Button(update_window, text="Save", font=f, command=f12)
uw_btn_back = Button(update_window, text="Back", font=f, command=f6)

uw_lbl_id.pack(pady=10)
uw_ent_id.pack(pady=10)
uw_lbl_name.pack(pady=10)
uw_ent_name.pack(pady=10)
uw_lbl_salary.pack(pady=10)
uw_ent_salary.pack(pady=10)
uw_btn_save.pack(pady=10)
uw_btn_back.pack(pady=10)

update_window.withdraw()

delete_window = Toplevel(main_window)
delete_window.title("Delete Employee")
delete_window.geometry("500x500+100+100")

dw_lbl_id = Label(delete_window, text="enter id", font=f)
dw_ent_id = Entry(delete_window, bd=4, font=f)
dw_btn_delete = Button(delete_window, text="Delete", font=f, command=f13)
dw_btn_back = Button(delete_window, text="Back", font=f, command=f8)

dw_lbl_id.pack(pady=10)
dw_ent_id.pack(pady=10)
dw_btn_delete.pack(pady=10)
dw_btn_back.pack(pady=10)

delete_window.withdraw()

charts_window = Toplevel(main_window)
charts_window.title("Top 5 Employee")
charts_window.geometry("500x500+100+100")

cw_st_data = ScrolledText(charts_window, width=30, height=10, font=f)
cw_btn_back = Button(charts_window, text="Back", font=f, command=f10)

cw_st_data.pack(pady=10)
cw_btn_back.pack(pady=10)

charts_window.withdraw()


main_window.mainloop()




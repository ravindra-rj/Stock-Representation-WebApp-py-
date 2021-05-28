import streamlit as st
import pandas as pd
from streamlit import caching
import psycopg2
from StockWebApp import *
# Security
# passlib,hashlib,bcrypt,scrypt

import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False

# DB Management
conn = psycopg2.connect(
   database="StocksUserDB", user='postgres', password='ravindra@089', host='localhost', port= '5432'
)

c = conn.cursor()
# DB  Functions

# def create_usertable():
# 	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
	query = """insert into useraccount(email,password) values(%s,%s)"""
	data = (username,password)
	try:
		c.execute(query,data)
		st.success("You have successfully created a valid Account")
		st.info("Go to Login Menu to login")
	except:
		st.error("user already exist.")
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM useraccount WHERE email=%s and password=%s', (username, password))
	data = c.fetchall()
	return data


def view_all_users():
	c.execute('SELECT * FROM useraccount')
	data = c.fetchall()
	return data




st.title("Welcome to Stocks-Web App")
image = Image.open("D:/python project/Stock-Representation-WebApp-py-/Asserts/StMaWebApp.jpg")
st.image(image, use_column_width=True)
menu = ["Login","SignUp"]
choice = st.sidebar.selectbox("Menu",menu)

if choice == "Login":

	username =st.sidebar.text_input("User Name")
	password = st.sidebar.text_input("Password",type='password')

	if st.sidebar.checkbox("Login"):
		if len(username)>0 and len(password)>0:
				# if password == '12345':
			hashed_pswd = make_hashes(password)
			result = login_user(username,check_hashes(password,hashed_pswd))
			if result:
				st.sidebar.success("Logged In as {}".format(username))

				startup()
			else:
				st.warning("Incorrect Username/Password")
		else:
			st.error("UserName or Password is required!")


elif choice == "SignUp":
	st.subheader("Create New Account")
	new_user = st.text_input("Username")
	new_password = st.text_input("Password",type='password')

	if st.button("Signup"):
		if len(new_password)>0 and len(new_password)>0:
			add_userdata(new_user,make_hashes(new_password))
		else:
			st.error("UserName or Password is required!")

# if __name__ == '__main__':
# 	main()
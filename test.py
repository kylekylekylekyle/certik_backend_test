import psycopg2
from config import config

def create_tables():
	"""create transactions/peers tables for distributedTransactions database """
	commands = (
		"""
		CREATE TABLE transactions(
			sender_id VARCHAR(255) NOT NULL,
			recipient_id VARCHAR(255) NOT NULL,
			value INTEGER NOT NULL,
			transaction_time TIMESTAMP DEFAULT Now(),
		)
		""",
		"""
		CREATE TABLE users(
			username VARCHAR(255) NOT NULL,
			password VARCHAR(255) NOT NULL,
			balance INTEGER NOT NULL,
			peers_id INTEGER [],
		)
		""")
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(* *params)
		cur = conn.cursor()
		for command in commands:
			cur.execute(command)
		cur.close()
		conn.commit()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()

def insert_transaction(sender, recipient, val):
	""" insert the the details of transaction to transactions table """
	sql = """INSERT INTO transactions(sender_id, recipient_id, value)
			VALUES(%s, %s, %d)"""
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(* * params)
		cur = conn.cursor()
		cur.execute(sql, (sender, recipient, val))
		conn.commit()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()

def new_user(username, starting_bal):
	""" setup a new user id and add this user's peers and receive user id"""
	sql = """INSERT INTO users(username, balance, peers_id)
			VALUES(%s, %d, %s)"""
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(* * params)
		cur = conn.cursor()

		balance = starting_bal
		peers_id = []

		cur.execute(sql, (username, balance, peers_id))
		conn.commit()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()
	return

def add_peers(user, peers):
	"""add up to 5 peers for a new user"""
	sql = """UPDATE users
			SET peers = %s
			WHERE username = %s"""
	conn = None
	updated_rows = 0
	try:
		params = config()
		conn = psycopg2.connect(* * params)
		cur = conn.cursor()
		cur.execute(sql, (peers, user))
		updated_rows = cur.rowcount
		conn.commit()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()
	return updated_rows

def update_balance(user, new_balance):
	""" add/subtract funds to current balance"""
	sql = """UPDATE users
			SET balance = %d
			WHERE username = %s"""
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(* *params)
		cur = conn.cursor()
		cur.execute(sql, (new_balance, user))
		conn.commit()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()
	return

def balance_check(user):
	"""checks how much money is in a user's balance"""
	conn = None
	balance = 0
	try:
		params = config()
		conn = psycopg2.connect(* * params)
		cur = conn.cursor()
		cur.execute("SELECT balance FROM users WHERE username = %s", (user))
		if cur is not None:
			balance = cur.fetchone()[0]
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()
	return balance

def num_users():
	"""checks how many users are in the db, only used to see if there are >2 users for most functions to work"""
	conn = None
	total_users = 0
	try:
		params = config()
		conn = psycopg2.connect(* * params)
		cur = conn.cursor()
		cur.execute("SELECT username FROM users")
		row = cur.fetchone()
		while row is not None:
			total_users = total_users + 1
			row = cur.fetchone()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()
	return total_users

def user_check(user):
	""" checks if user exists"""
	conn = None
	exists = 0;
	try:
		params = config()
		conn = psycopg2.connect(* * params)
		cur = conn.cursor()
		cur.execute("SELECT username FROM users WHERE username = %s", (user))
		if cur is not None:
			exists = 1
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()
	return exists

def sender_check(user):
	""" checks if user exists"""
	conn = None
	exists = 0;
	try:
		params = config()
		conn = psycopg2.connect(* * params)
		cur = conn.cursor()
		cur.execute("SELECT sender_id FROM transactions WHERE sender_id = %s", (user))
		if cur is not None:
			exists = 1
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()
	return exists

def recipient_check(user):
	""" checks if user exists"""
	conn = None
	exists = 0;
	try:
		params = config()
		conn = psycopg2.connect(* * params)
		cur = conn.cursor()
		cur.execute("SELECT recipient_id FROM transactions WHERE recipient_id = %s", (user))
		if cur is not None:
			exists = 1
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()
	return exists

def delete_user(user):
	"""deletes specified user then changes all instances of that name in transactions
	to DELETED"""
	sql0 = """UPDATE transactions
			SET sender_id = %s
			WHERE sender_id = %s"""
	sql1 = """UPDATE transactions
			SET recipient_id = %s
			WHERE recipient_id = %s"""
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(* *params)
		cur = conn.cursor()
		cur.execute("DELETE FROM users WHERE username = %s", (user))
		cur.execute(sql0, ("DELETED_ACCOUNT", user))
		cur.execute(sql1, ("DELETED_ACCOUNT", user))
		conn.commit()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()
	return

if __name__ == '__main__':
	create_tables()

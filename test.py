import psycopg2
from config import config

def create_tables():
	"""create transactions/peers tables for distributedTransactions database """
	commands = (
		"""
		CREATE TABLE transactions(
			sender_id INTEGER NOT NULL,
			recipient_id INTEGER NOT NULL,
			value INTEGER NOT NULL,
			transaction_time TIMESTAMP DEFAULT Now(),
		)
		""",
		"""
		CREATE TABLE users(
			user_id INTEGER PRIMARY KEY,
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
			VALUES(%d, %d, %d)"""
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

def new_user(username):
	""" setup a new user id and add this user's peers and receive user id"""
	sql = """INSERT INTO users(username, balance, peers_id)
			VALUES(%s, %d, %s) RETURNING user_id;"""
	conn = None
	user_id = None
	try:
		params = config()
		conn = psycopg2.connect(* * params)
		cur = conn.cursor()

		balance = 0
		peers_id = []

		cur.execute(sql, (username, balance, peers_id,))
		user_id = cur.fetchone()[0]
		conn.commit()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()
	return user_id

def add_peers(user, peers):
	"""add up to 5 peers for a new user"""
	sql = """UPDATE users
			SET peers = %s
			WHERE user_id = %s"""
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
			WHERE user_id = %s"""
	conn = None
	updated_rows = 0
	try:
		params = config()
		conn = psycopg2.connect(* *params)
		cur = conn.cursor()
		cur.execute(sql, (new_balance, user))
		updated_rows = cur.rowcount
		conn.commit()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()
	return updated_rows

def balance_check(user):
	"""checks how much money is in a user's balance"""
	conn = None
	balance = 0
	try:
		params = config()
		conn = psycopg2.connect(* * params)
		cur = conn.cursor()
		cur.execute("SELECT balance FROM users WHERE user_id = %s", user)
		if cur is not None:
			balance = cur.fetchone()[0]
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()
	return balance


if __name__ == '__main__':
	create_tables()
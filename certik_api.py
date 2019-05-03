from flask import Flask
from flask_restful import Api, Resource, reqparse
from test import insert_transaction, new_user, add_peers, update_balance, balance_check, num_users, user_check, sender_check, recipient_check, delete_user 
import psycopg2
from config import config

app = Flask(__name__)
api = Api(app)



class User(Resource):
	def get(self, name):
		#ask for every bit of info in transactions, if empty search don't query it
		parser = reqparse.RequestParser()
		parser.add_argument("sender")
		parser.add_argument("recipient")
		args = parser.parse_args()

		sql = "SELECT * FROM transactions"
		num_concat = 0;
		if not args["sender"]:
			if (sender_check(args["sender"]) == 0):
				return "Sender doesn't exist", 400
			send_concat = " WHERE sender_id = %s" % (args["sender"])
			num_concat = 1
			sql = sql + send_concat
		if not args["recipient"]:
			if (recipient_check(args["recipient"]) == 0):
				return "Recipient doesn't exist", 400
			send_concat = " WHERE recipient_id = %s" % (args["recipient"])
			if (num_concat == 0):
				sql = sql + send_concat
				num_concat = 1
			else:
				sql = sql + " AND" + send_concat
		# CHANGE USER_CHECK TO A NEW FUNCTION THAT CHECKS FOR USER IN TRANSACTIONS

		conn = None
		try:
			params = config()
			conn = psycopg2.connect(* *params)
			cur = conn.cursor()
			cur.execute(sql)
			rows = cur.fetchall()
			cur.close()
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)
		finally:
			if conn is not None:
				conn.close()
		return rows, 200


	def post(self, name):
		parser = reqparse.RequestParser()
		parser.add_argument("balance")
		args = parser.parse_args()

		if (args["balance"] < 0):
			return "Balance can't be lower than 0", 400

		if (user_check(name) == 1):
			return "User with name {} already exists".format(name), 400

		new_user(name, args["balance"])
		return 201

	def put(self, name):
		parser = reqparse.RequestParser()
		parser.add_argument("recipient")
		parser.add_argument("amount")
		args = parser.parse_args()

		if (user_check(name) == 0):
			return "This username doesn't exist", 400

		if (user_check(args["recipient"]) == 0):
			return "The recipient doesn't exist", 400


		user_balance = balance_check(name)
		recipient_balance = balance_check(args["recipient"])

		if (user = args["recipient"]):
			user_balance = user_balance + args["amount"]
			update_balance(name, user_balance)
			insert_transaction(name, name, args["amount"])
			return 200

		if (user_balance < amount):
			return "Insufficient balance", 400

		user_balance = user_balance - args["amount"]
		recipient_balance = recipient_balance + args["amount"]
		update_balance(name, user_balance)
		update_balance(args["recipient"], recipient_balance)
		insert_transaction(name, args["recipient"], args["amount"])
		return 200

	def delete(self, name):
		if (user_check(name) == 0):
			return "User doesn't exist", 400
		
		###delete user from users, change instances of user to "deleted" in transactions
		delete_user(name)
		return 200

api.add_resource(User, "/user/<string:name>")
app.run(debug=True)

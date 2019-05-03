from flask import Flask
from flask_restful import Api, Resource, reqparse
from test import insert_transaction, new_user, add_peers, update_balance, balance_check, num_users, user_check 

app = Flask(__name__)
api = Api(app)



class User(Resource):
	def get(self, name):
		#ask for every bit of info in transactions, if empty search don't query it
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
		parser = reqparse.RequestParser()
		parser.add_argument("user")

		if (user_check(args["user"]) == 0):
			return "User doesn't exist", 400
		###delete user from users, change instances of user to "deleted" in transactions

api.add_resource(User, "/user/<string:name>")
app.run(debug=True)
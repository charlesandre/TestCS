from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask.ext.jsonpify import jsonify
import csv

db_connect = create_engine('sqlite:///test.db')
app = Flask(__name__)
api = Api(app)


class SpecificUsers(Resource):
    def get(self, user_id):
        conn = db_connect.connect()
        query = conn.execute("select * from Users where id =%d "  %int(user_id))
        query2 = conn.execute("select ipv4 from Users where id =%d "  %int(user_id))
        user_ip = query2.fetchone()[0]
        country = "NA"
        geoip = csv.reader(open("geoip.csv"), delimiter=",")
        for row in geoip:
            if row[0].split('.')[0] == user_ip.split('.')[0] or row[0].split('.')[0]=="*":
                if row[0].split('.')[1] == user_ip.split('.')[1] or row[0].split('.')[1]=="*":
                    if row[0].split('.')[2] == user_ip.split('.')[2] or row[0].split('.')[2]=="*":
                        if row[0].split('.')[3] == user_ip.split('.')[3] or row[0].split('.')[3]=="*":
                            country = row[1]
        result = {'Country': country, 'User': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        query = conn.execute("select * from Users where id =%d "  %int(user_id))
        if len(list(query)) == 0:   #USER DOESN'T EXIST --> CREATE
            return {'Error' : "Missing User" }
        return jsonify(result)

class NewUser(Resource):
    def get(self):
        conn = db_connect.connect()
        uid = request.args['id']
        if uid: #ID IS MANDATORY
            last = request.args['lastname']
            if last: #LASTNAME IS MANDATORY
                ip = request.args['ip']
                if ip: #IP IS MANDATORY
                    first = request.args['firstname'] #OPTIONNAL
                    if not first:
                        first = "-1"
                    age = request.args['age'] #OPTIONNAL
                    if not age:
                        age=-1;
                    query = conn.execute("select * from Users where id =%d "  %int(uid))

                    if len(list(query)) == 0:   #USER DOESN'T EXIST --> CREATE
                        if age == -1 and first == "-1":
                            query = conn.execute("insert into Users values (%d, '%s', '%s');"  %(int(uid), last, ip))
                        elif age == -1:
                            query = conn.execute("insert into Users values (%d, '%s', '%s', '%s');"  %(int(uid), last, ip, first))
                        elif first == "-1":
                            query = conn.execute("insert into Users values (%d, '%s', '%s', %d);"  %(int(uid), last, ip, int(age)))
                        else:
                            query = conn.execute("insert into Users values (%d, '%s', '%s', '%s', %d);"  %(int(uid), last, ip, first, int(age)))
                        print("User inserted")

                    else: #USER EXIST --> UPDATE
                        if age == -1 and first == "-1":
                            query = conn.execute("update Users set lastname = '%s', ipv4 = '%s' where id = %d;"  %(last, ip, int(uid)))
                        elif age == -1:
                            query = conn.execute("update Users set lastname = '%s', ipv4 = '%s', firstname = '%s' where id = %d;"  %(last, ip, first, int(uid)))
                        elif first == "-1":
                            query = conn.execute("update Users set lastname = '%s', ipv4 = '%s', age = %d where id = %d;"  %(last, ip, int(age), int(uid)))
                        else:
                            query = conn.execute("update Users set lastname = '%s', ipv4 = '%s', firstname = '%s', age = %d where id = %d;"  %(last, ip, first, int(age), int(uid)))
                        print("User updated")
                else:
                    return {'Error' : "Missing IP" }
            else:
                return {'Error' : "Missing LastName" }
        else:
            return {'Error' : "Missing IP" }


api.add_resource(SpecificUsers, '/users/<user_id>') # Route_2
api.add_resource(NewUser, '/add') # Route_3

if __name__ == '__main__':
     app.run(port='8000')

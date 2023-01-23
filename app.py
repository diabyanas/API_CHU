from flask import Flask, jsonify, request
from flaskext.mysql import MySQL
from flask_restful import Resource, Api

#Create an instance of Flask
app = Flask(__name__)

#Create an instance of MySQL
mysql = MySQL()

#Create an instance of Flask RESTful API
api = Api(app)

#Set database credentials in config.
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'example'
app.config['MYSQL_DATABASE_DB'] = 'API_CHU_CAEN'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3307

#Initialize the MySQL extension
mysql.init_app(app)


#Get All animals or flowers, or Create new one
class Lechu(Resource):
    def get(self,table):
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(f"""select * from {table}""")
            rows = cursor.fetchall()
            return jsonify(rows)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    def post(self,table):

        if table == "employe":
            try:
                conn = mysql.connect()
                cursor = conn.cursor()
                nom = request.get_json()['nom']
                prenom = request.get_json()['prenom']
                age = request.get_json()['age']
                profession = request.get_json()['profession']
                insert_employe = f"""INSERT INTO {table} (nom, prenom, age, profession)
                                    VALUES(%s, %s, %s, %s)"""
                cursor.execute(insert_employe, (nom, prenom, age, profession))
                conn.commit()
                response = jsonify(message='Base mise à jour avec succès.', id=cursor.lastrowid)
                #response.data = cursor.lastrowid
                response.status_code = 200


            except Exception as e:
                print(e)
                response = jsonify('Impossible de mettre la base à jour.')         
                response.status_code = 400 
            finally:
                cursor.close()
                conn.close()
                return(response)

        else:
            try:
                nom_du_produit = request.get_json()['nom_du_produit']
                dimension = request.get_json()['dimension']
                etat = request.get_json()['etat']
                insert_materiel = f"""INSERT INTO {table} (nom_du_produit, dimension, etat)
                                    VALUES(%s, %s, %s)"""
                cursor.execute(insert_materiel, (nom_du_produit, dimension, etat))
                conn.commit()
                response = jsonify(message='Base mise à jour avec succès.', id=cursor.lastrowid)
                #response.data = cursor.lastrowid
                response.status_code = 200


            except Exception as e:
                print(e)
                response = jsonify('Impossible de mettre la base à jour.')         
                response.status_code = 400 
            finally:
                cursor.close()
                conn.close()
             
            
#Get a user by id, update or delete user
class Chu(Resource):
    def get(self, table, id):
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(f"""SELECT * FROM {table} where id = "{id}";""")
            rows = cursor.fetchall()
            return jsonify(rows)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    def put(self, table, id):
        if table == "employe":
            try:
                conn = mysql.connect()
                cursor = conn.cursor()
                nom = request.get_json()['nom']
                prenom = request.get_json()['prenom']
                age = request.get_json()['age']
                profession = request.get_json()['profession']
                update_employe = f"""update {table} 
                                    set nom=%s, prenom=%s, age=%s, profession=%s
                                    where id=%s"""
                cursor.execute(update_employe, (nom, prenom, age, profession, id))
                conn.commit()
                response = jsonify('Base  mise à jour avec succès..')
                response.status_code = 200
            except Exception as e:
                print(e)
                response = jsonify('Impossible de mettre à jour la base de données.')         
                response.status_code = 400
            finally:
                cursor.close()
                conn.close()    
            return(response)       

        else:
            try:
                nom_du_produit = request.get_json()['nom_du_produit']
                dimension = request.get_json()['dimension']
                etat = request.get_json()['etat']
                update_employe = f"""update {table} 
                                    set nom_du_produit=%s, dimension=%s, etat=%s
                                    where id=%s"""
                cursor.execute(update_employe, (nom_du_produit, dimension, etat, id))
                conn.commit()
                response = jsonify('Base  mise à jour avec succès..')
                response.status_code = 200
            except Exception as e:
                print(e)
                response = jsonify('Impossible de mettre à jour la base de données.')         
                response.status_code = 400
            finally:
                cursor.close()
                conn.close()    
            return(response)  

    def delete(self, table, id):
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(f'delete from {table} where id = %s',{id})
            conn.commit()
            response  = jsonify('Base de données mise à jour avec succès.')
            response.status_code = 200
        except Exception as e:
            print(e)
            response = jsonify('Impossible de mettre à jour la base de données.')         
            response.status_code = 400
        finally:
             cursor.close()
             conn.close()    
        return(response)       

#API resource routes

"""
Route pour POST :           http://127.0.0.1:5000/lechu/employe
Route pour selectionner par identifiant, DELETE, PUT : http://127.0.0.1:5000/chu/employe

"""

api.add_resource(Lechu, '/lechu/<string:table>', endpoint='lechu')
api.add_resource(Chu, '/chu/<string:table>/<int:id>', endpoint='chu')

if __name__ == "__main__":
    app.run(debug=True)

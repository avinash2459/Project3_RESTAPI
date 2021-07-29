import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)


mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'oscarData'
mysql.init_app(app)


@app.route('/api/v1/oscar', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblOscarImport')
    result = cursor.fetchall()
    json_result = json.dumps(result)
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/oscars/<int:oscar_id>', methods=['GET'])
def api_retrieve(oscar_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblOscarImport WHERE id=%s', oscar_id)
    result = cursor.fetchall()
    json_result = json.dumps(result)
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/oscars', methods=['POST'])
def api_add() -> str:
    content = request.json
    cursor = mysql.get_db().cursor()
    inputData = (content['actorName'], content['movieName'], content['sex'],
                 content['age'], content['year'])
    sql_insert_query = """INSERT INTO tblOscarImport (actorName,movieName,sex,age,year) VALUES (%s, %s,%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    cursor.execute('SELECT * FROM tblOscarImport ORDER BY id DESC LIMIT 1')
    result = cursor.fetchall()
    json_result = json.dumps(result)
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/oscars/<int:oscar_id>', methods=['PUT'])
def api_edit(oscar_id) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['actorName'], content['movieName'], content['sex'],
                 content['age'], content['year'],oscar_id)
    sql_update_query = """UPDATE tblOscarImport t SET t.actorName = %s, t.movieName = %s, t.sex = %s, t.age =
        %s, t.year = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    query = """SELECT * FROM tblOscarImport WHERE id = %s """
    cursor.execute(query, oscar_id)
    result = cursor.fetchall()
    json_result = json.dumps(result)
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/oscars/<int:oscar_id>', methods=['DELETE'])
def api_delete(oscar_id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblOscarImport WHERE id = %s """
    cursor.execute(sql_delete_query, oscar_id)
    mysql.get_db().commit()
    cursor.execute('SELECT * FROM tblOscarImport')
    result = cursor.fetchall()
    json_result = json.dumps(result)
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
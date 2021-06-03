import pymysql
from flask import Flask,render_template,request

app=Flask(__name__)

@app.route('/search')
def search():
    wanted=request.args.get("wanted",type=str)
    if wanted == None:
        wanted='pineapple'

    db=pymysql.connect(host='localhost',user='root',passwd="z1012194891",db="DataVisual",charset="utf8")
    cursor=db.cursor()
    try:
        sql="SELECT * FROM DataVisual.map_enword where english like '%"+wanted+"%'"
        cursor.execute(sql)
        rs=cursor.fetchall()
        rs=list(rs)
        print(rs)
    except:
        rs='db-error'
        print('py-db-error')

    db.close()
    return render_template('english.html',rs=rs)

if __name__=='__main__':
    app.run(debug=True)
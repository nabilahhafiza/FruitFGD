import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask,redirect,url_for,render_template,request
from pymongo import MongoClient
from bson import ObjectId

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app=Flask(__name__)

#/ --> dashboard
@app.route('/',methods=['GET','POST'])
def home():
  fruit = list(db.Fruit.find())
  return render_template('dashboard.html', fruit=fruit)

#/ --> index 
@app.route('/fruit',methods=['GET','POST'])
def fruit():
  fruit = list(db.Fruit.find({}))
  return render_template('fruit.html', fruit=fruit)

#/ --> addfruit
@app.route('/addFruit',methods=['GET','POST'])
def addfruit():
  if request.method == 'POST':
    name = request.form['name']
    price = request.form['price']
    desc = request.form['desc']
    image = request.files['image']
    
    if image:
      file_name = image.filename
      fix_name = file_name.split('/')[-1]
      file_path = f'static/assets/imgFruit/{fix_name}'
      image.save(file_path)
    else:
      image = None
      
    doc = {
      'name': name,
      'price': price,
      'desc': desc,
      'image': fix_name,
    }
    
    db.Fruit.insert_one(doc)
    return redirect(url_for('fruit'))
  return render_template('AddFruit.html')

#/ --> editfruit
@app.route('/editFruit/<_id>',methods=['GET','POST'])
def editfruit(_id):
  if request.method == 'POST':
    id = request.form['id']
    name = request.form['name']
    price = request.form['price']
    desc = request.form['desc']
    image = request.files['image']
    
    doc = {
      'name': name,
      'price': price,
      'desc': desc,
    }
    
    if image:
      file_name = image.filename
      fix_name = file_name.split('/')[-1]
      file_path = f'static/assets/imgFruit/{fix_name}'
      image.save(file_path)
      doc['image'] = fix_name
    else:
      image = None
      
    db.Fruit.update_one({'_id': ObjectId(id)},{'$set': doc})
    return redirect(url_for('fruit'))

  id = ObjectId(_id)
  data = list(db.Fruit.find({'_id': id}))
  print(data)
  return render_template('EditFruit.html', data=data)

#/ --> deletefruit
@app.route('/deleteFruit/<_id>',methods=['GET','POST'])
def deletefruit(_id):
  db.Fruit.delete_one({'_id': ObjectId(_id)})
  return redirect(url_for('fruit'))


if __name__ == '__main__':
  #DEBUG is SET to TRUE. CHANGE FOR PROD
  app.run('0.0.0.0',port=5000,debug=True)
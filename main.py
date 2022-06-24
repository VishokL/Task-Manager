from flask import Flask,render_template,redirect,request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app=Flask(__name__)
app.config['MONGO_URI']="mongodb+srv://Vishok:PT7vRLyaFYJG5U3@vishoks-cluster.ogocs.mongodb.net/messaging_system?retryWrites=true&w=majority"
mongo=PyMongo(app)

@app.route("/",methods=['GET','POST'])
def index():
    if request.method=='POST':
        data=request.form.to_dict()
        mongo.db.tasks.insert_one(data)
        return redirect("/")
    else:
        tasks=mongo.db.tasks.find()
        completed_tasks=mongo.db.completed_tasks.find()
        return render_template("home.html",tasks=tasks,completed_tasks=completed_tasks)

@app.route("/complete_task/<task_id>",methods=['GET','POST'])
def complete_task(task_id):
    task=mongo.db.tasks.find_one({'_id':ObjectId(task_id)})
    mongo.db.tasks.delete_one({'_id':ObjectId(task_id)})
    mongo.db.completed_tasks.insert_one(task)
    return redirect("/")

if __name__=="__main__":
    app.run(debug=True)
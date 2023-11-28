from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from bson.json_util import dumps
from . import db

mydb=db.myclient["crud_operation"]
mycol=mydb["employees"]

def home(request):
    return HttpResponse("Api is working")

@csrf_exempt
def addEmployee(request):
    if(request.method=="POST"):
        body_unicode=request.body.decode('utf-8')
        body=json.loads(body_unicode)
        employee=mycol.insert_one(body)
        # print(body)
        return HttpResponse("Employee added",employee.inserted_id)
    return HttpResponse("Sorry method doesn't exist")

def employees(request):
    employees=mycol.find()
    list_curr=list(employees)
    body=dumps(list_curr)
    data=json.dumps(body)
    result=json.loads(data)
    return HttpResponse(result)

@csrf_exempt
def employee(request,name):
    query={"name":name}
    if(request.method=="PUT"):
        body_unicode=request.body.decode("utf-8")
        body=json.loads(body_unicode)
        newValues={"$set":body}
        mycol.update_one(query,newValues)
        employee=mycol.find(query)
        list_curr=list(employee)
        body=dumps(list_curr)
        result=json.dumps(body)
        js=json.loads(result)
        return HttpResponse(js)
        return HttpResponse("Data updated")
    if(request.method=="DELETE"):
        mycol.delete_one(query)
        return HttpResponse("Deleted Successfully")

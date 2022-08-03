from courses import models
from user.models import Person
from rest_framework import exceptions, permissions
from school.models import School
from rest_framework.serializers import ValidationError
permissions_list = {
    1: {
        "post": [2, 3, 4, 5, 6, 7, 8,9,10],
        "put": [2, 3, 4, 5, 6, 7, 8,9,10],
        "patch": [2, 3, 4, 5, 6, 7, 8,9,10],
        "get": [2, 3, 4, 5, 6, 7, 8,9,10],
        "delete": [2, 3, 4, 5, 6, 7, 8,9,10]
    },
    2: {
        "post": [3, 4, 5, 6, 7, 8,9,10],
        "put": [2, 3, 4, 5, 6, 7, 8,9,10],
        "patch": [2, 3, 4, 5, 6, 7, 8,9,10],
        "get": [3, 4, 5, 6, 7, 8,9,10],
        "delete": [3, 4, 5, 6, 7, 8,9,10]
    },
    3: {
        "post": [3],
        "put": [3],
        "patch": [3],
        "get": [4],
        "delete": []
    },
    4: {
        "post": [4],
        "put": [4],
        "patch": [4],
        "get": [4],
        "delete": []
    },
    5: {
        "post": [6, 7, 8,10],
        "put": [5, 6, 7, 8,10],
        "patch": [5, 6, 7, 8,10],
        "get": [6, 7, 8],
        "delete": [6, 7, 8,10]
    },
    6: {
        "post": [7, 8,10],
        "put": [6, 7, 8,10],
        "patch": [6, 7, 8,10],
        "get": [7, 8],
        "delete": [7, 8,10]

    },
    7: {
        "post": [],
        "put": [7],
        "patch": [7],
        "get": [7, 8],
        "delete": []
    },
    8: {
        "post": [8],
        "put": [8],
        "patch": [8],
        "get": [8],
        "delete": []
    },
    9: {
        "post": [3,4],
        "put": [3],
        "patch": [3],
        "get": [4],
        "delete": []
    },
    10: {
        "post": [],
        "put": [7],
        "patch": [7],
        "get": [7, 8],
        "delete": []
    },
}

'''
if role_id in permissions_list:
            self.permissions = permissions_list[role_id][request.method.lower()]
            return self.permissions
'''


class AdminGlobalPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            try:
                if int(request.data.get('role_id')) == 4 and view.__class__.__name__.lower() == 'studentviewset':
                    return True
            except:
                raise ValidationError({'role_id':"Invalid role_id"})
        method = request.method
        model = view.model
        request.auth = request.auth
        person = Person.objects.filter(school_code=request.user["school_code"])
        school_code = person.first().school_code
        school = School.objects.filter(school_code=school_code)
        school = school.first()
        if request.auth in permissions_list:
            self.permissions = permissions_list[request.auth][method.lower()]
            if method == "POST":
                if request.data["role_id"] in self.permissions:
            
                    if request.auth in [5,6,7,8,10] and request.data["role_id"] in [5,6,7,8,10] and request.data["school_id"] == str(school.id):
                        return True
                    elif request.auth in [1,2,3,4,10]:
                        return True
            elif method == "GET":
                if view.__class__.__name__.lower() == "adminviewset":
                    if request.auth in [1,2,5,6]:
                        return True
                elif view.__class__.__name__.lower() == 'tutorviewset':
                    if request.auth in [1,2,5,6,3,7]:
                        return True
                elif view.__class__.__name__.lower() == 'studentviewset':
                    if request.auth in [1,2,3,5,6,7,4,8,9,10]:
                        return True
                elif view.__class__.__name__.lower() == 'contentmanagerviewset':
                    if request.auth in [1,2,5,6,9,10]:
                        return True
                
            elif method in ["PUT","PATCH"]:
                requests = request.path.split("/")
                id = requests[-2]
                if requestd_person := Person.objects.filter(id=id).first():
                    role_id = requestd_person.role_id.role_id
                    if role_id in self.permissions:
                        if request.auth in [3,4,5,6,7,8,9,10]: 
                            if id == str(request.user["id"]):
                                return True
                        elif request.auth in [1,2]:
                            return True
                        if request.auth in [5,6] and requestd_person.school_code == request.user["school_code"]:
                            return True
            elif method == "DELETE":
                requests = request.path.split("/")
                id = requests[-2]
                if (requestd_person := Person.objects.filter(id=id)).exists():
                    role_id = requestd_person.first().role_id.role_id
                    if role_id in self.permissions:
                        return True
        else:  
            return False
    



class ContentPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            if request.auth in [1,2]:
                return True
            if request.auth in [9,10]:
                ...
                # if view.__class__.__name__.lower() == standard
                # if request.data.get('standard_name')

        elif request.method == 'GET':
            if request.auth in [1,2]:
                return True
            elif request.auth in [5,6]:
                ...



class SchoolPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        
        if request.method == 'POST':
            if request.auth in [1,2]:
                return True
        if request.method in ['PUT','PATCH']:
            requests = request.path.split("/")
            id = requests[-2]
            if request.auth in [1,2]:
                return True
            else:
                if school:=models.School.objects.filter(id=id).first():
                    school_code = school.school_code
                    if models.Person.objects.filter(request.user['school_code']).exists():
                        return True
        if request.method == 'DELETE':
            if request.auth in [1,2]:
                return True
        if request.method == 'GET':
            return True
        return False
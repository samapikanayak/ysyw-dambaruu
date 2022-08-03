from rest_framework import filters,exceptions 
import coreapi 
import json  
from courses import models


class CustomFilter(filters.BaseFilterBackend):     
    def get_schema_fields(self, view):
        return [coreapi.Field(name='filters',location='query',required=False,type='string')]   

    def filter_queryset(self, request, queryset, view):
        try:             
            if filters := request.GET.get("filters"):  
                filters = json.loads(filters)                 
                filter2 ={}
                fields = view.filter_fields             
                for i in filters:                    
                    if i in fields:  
                        if i == "role_id" or 'id' in i:
                            if filters[i] not in ["",0,"0"," "]:
                                filter2[i] = filters[i]                  
                        else:
                            filter2[i + "__icontains"] = filters[i] 

                queryset = queryset.filter(**filter2)             
            return queryset                 
        except json.JSONDecodeError:           
            raise exceptions.NotFound({"status":"failed","message":"invalid query-params"})
        except AttributeError:
            return queryset

class CustomFilter2(filters.BaseFilterBackend):     
    def get_schema_fields(self, view):
        return [coreapi.Field(name='meta',location='query',required=False,type='string')]   

    def filter_queryset(self, request, queryset, view):
        return queryset

from rest_framework import pagination, response,exceptions 
import json 
from django.conf import settings


class CustomLimitOffsetPagination(pagination.LimitOffsetPagination):
    '''
    limit=page_size
    offset=index
    example :- http://127.0.0.1:8000/admins/?limit=10&offset=10
    '''
    max_limit = 100

    def paginate_queryset(self, queryset, request, view=None):

        '''
        paginating the queryset
        Parameters :- 
            self :- current object,
            queryset :- Model queryset
            request :- Enduser request
         Returns :-
            paginated queryset
        '''
        try:             
            meta = json.loads(request.GET.get("meta"))         
        except (json.JSONDecodeError,ValueError):             
            raise exceptions.NotFound({"status":"failed","message":"invalid query param","data":None})         
        except TypeError:             
            meta = {"limit":settings.REST_FRAMEWORK['PAGE_SIZE'],"offset":0}
        #count no of records in queryset
        self.count = self.get_count(queryset)
        try:
            #limit value from request queryparam
            self.limit = int(meta.get('limit', settings.REST_FRAMEWORK['PAGE_SIZE']))
            #index value from request queryparam of records 
            self.offset = int(meta.get('offset', 0))
        except ValueError:
            raise exceptions.NotFound({"status":"failed","message":"invalid query param","data":None})         
        if self.limit is None:
            return None

        self.request = request
        if self.count > self.limit and self.template is not None:
            self.display_page_controls = True

        if self.count == 0 or self.offset > self.count:
            return []
        return list(queryset[self.offset : self.offset + self.limit])

    def get_paginated_response(self, data):

        '''
        returns customized response to client
        Parameters :- 
            self :- current object,
            data :- data from paginate_queryset()
        Returns :- 
            {dict} response
        '''
        return response.Response(
            {
                "status": "success",
                "message": "",
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "count": self.count,
                "data": data,
            }
        )



from rest_framework.permissions import BasePermission,SAFE_METHODS
from ly3000projApp.models import UserDesignation
from .serializers import UserDesignationSerializer, IssueSerializer



class UserDesignationPermission(BasePermission):

    def has_permission(self,request,view):
        designation = UserDesignation.objects.all()
        all_designations = UserDesignationSerializer(designation,many = True)
        designation_dict = all_designations.data
        for user in designation_dict:
            user_dict = dict(user)
            if user_dict.get('user') == request.user.id:
                if user_dict.get('designation') == 'EMP' or user_dict.get('designation') == 'MANAGER':
                    if request.method in SAFE_METHODS:
                        return True
                    else:
                        return False
                elif user_dict.get('designation') == 'ADMIN':
                    return True
        if request.method in SAFE_METHODS:
            return True
        return False



class IssuePermission(BasePermission):

    def has_permission(self, request, view):
        designation = UserDesignation.objects.all()
        all_designations = UserDesignationSerializer(designation,many = True)
        designation_dict = all_designations.data
        for user in designation_dict:
            user_dict = dict(user)

            if user_dict.get('designation') == 'EMP':

                if request.method in ['PUT','PATCH','DELETE']:
                    issues = Issue.objects.all()
                    iobj = IssueSerializer(issues)
                    iobj_dict = iobj.data

                    if iobj_dict.get('assignee') == request.user.id or iobj_dict.get('reporter') == request.user.id:
                        return True
                    else:
                        return False

                return True
            else:
                return True

class SprintPermission(BasePermission):
    def has_permission(self, request, view):
        try:
            designations = UserDesignation.objects.get(user= request.user.id)
            sobj = UserDesignationSerializer(designations)
            dobj = sobj.data
            if request.method not in SAFE_METHODS:
                if dobj.get('designation') == 'ADMIN' or dobj.get('designation') == 'MANAGER':
                    if dobj.get('user') == request.user.id:
                        return True
                    else:
                        return False
                else:
                    return False

            return True
        except:
            return False

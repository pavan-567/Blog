from Auth.models import User
from Profile.serializers import ProfileSerializer
from Profile.models import Profile
import json

class BreadCrumbMiddleware : 
    def __init__(self, get_response) :
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs) : 
        request.session['breadcrumb'] = request.path_info.split('/')[1 : -1]
        # request.session['users'] = User.objects.all()
        response = self.get_response(request)
        return response
    
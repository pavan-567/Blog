
from django.http import HttpResponse
from django.shortcuts import render


def AuthMiddleware(get_response) : 
    def Auth_Check(request) : 
        response = get_response(request)
        if (request.user.is_authenticated) :
        # or ((request.path_info in ['/Auth/login', '/Auth/register']) or (request.path_info.startswith("/Auth/activate"))) : 
            if request.user.profile.profileverification.is_email_verified : 
                return response
            else : 
                # return HttpResponse(f"Dear - {request.user.username}, Kindly Verify Your Email!")
                return render(request, 'Auth/email-resender.html')
        return response
    return Auth_Check

from django.http import HttpResponseRedirect

def redirect_to_salzinnes(request):
    return HttpResponseRedirect('/manuscript/123723/')
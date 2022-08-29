from urllib import request
from django.shortcuts import render, HttpResponse
import json

# Create your views here.

def login(request):
    return render(request, "login.html")

def login_result(request):
    if (request.method == "POST"):
        print(request.GET)
        username = request.POST.get("username")
        passwd = request.POST.get("passwd")
        
        with open("./userPortal/static/json/userinfo.json", "r") as json_file:
            userinfos:list = json.load(json_file)
            print(userinfos[0])
        for i in userinfos:
            if (i["username"] == username):
                if (i["passwd"] == passwd):
                    state = "success"
                    return render(request, "login_result.html", {"username": username, "passwd": passwd, "state":state})
                else:
                    state = "error-passwd"
                    return render(request, "login_result.html", {"username": username, "passwd": passwd, "state":state})
            else:
                pass
        state = "error-username"
        return render(request, "login_result.html", {"username": username, "passwd": passwd, "state":state})
        
    else:
        HttpResponse("Unknown Request from Login Page!")
        
def adminProcontrol(respond):
    with open("./userPortal/static/json/userinfo.json", "r") as json_file:
        user_data:list = json.load(json_file)
        
    
    return render(respond, "adminProcontrol.html", {"user_data":user_data})

def accountProgress(respond):
    target_user = respond.GET.get("username")
    progress_type = respond.GET.get("type")
    return render(respond, "accountProgress.html", {"username": target_user, "type":progress_type})

def progressResult(respond):
    with open("./userPortal/static/json/userinfo.json", "r") as json_file:
        user_data:list = json.load(json_file)
        
    print(user_data)
    
    if (respond.method == "GET"):
        if (respond.GET.get("type") == "delete"):
            username = respond.GET.get("username")
            print(username)
            for i in user_data:
                if (i["username"] == username):
                    user_data.remove(i)
                    with open("./userPortal/static/json/userinfo.json", "w") as json_file:
                        json.dump(user_data, json_file)
                    state = "success"
                    print(user_data)
                    return render(respond, "progressResult.html", {"state":state})
                else:

                    pass
            state = "error-notExist"
            return render(respond, "progressResult.html", {"state":state})
        else:
            state = "error-unknownRequest"
            return render(respond, "progressResult.html", {"state":state})
    else:
        print(respond.POST.get("type"))
        username = respond.POST.get("origin_username")
        new_username = respond.POST.get("username")
        password = respond.POST.get("passwd")
        print(username)
        print(new_username)
        print(password)
        for i in user_data:
            print(i)
            if (i["username"] == username):
                if (username == "admin"):
                    pass
                else:
                    i["username"] = new_username
                i["passwd"] = password
                with open("./userPortal/static/json/userinfo.json", "w") as json_file:
                    json.dump(user_data, json_file)
                state = "success"
                return render(respond, "progressResult.html", {"state":state})
                pass
            else:
                pass
        state = "error-notExist"
        return render(respond, "progressResult.html", {"state":state})
            
    return render(respond, "progressResult.html", {"state":state})

def signup_page(respond):
    return render(respond, "signupPage.html")

def signup_result(respond):
    new_username = respond.POST.get("username")
    new_passwd = respond.POST.get("passwd")
    
    # check whether there is a same name user in the database
    with open("./userPortal/static/json/userinfo.json", "r") as json_file:
        user_data:list = json.load(json_file)
        
    for i in user_data:
        if (i["username"] == new_username):
            state = "error-exist"
            return render(respond, "signinResult.html", {"state":state})
        else:
            pass
        
    new_user_data:dict = {
        "username": new_username,
        "passwd": new_passwd
    }
    
    user_data.append(new_user_data)
    
    with open("./userPortal/static/json/userinfo.json", "w") as json_file:
        user_data:list = json.dump(user_data, json_file)
        
    state = "success"
    return render(respond, "signinResult.html", {"state":state})
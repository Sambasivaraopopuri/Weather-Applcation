from asyncio.windows_events import NULL
import re
from unicodedata import name
from django.shortcuts import redirect, render
import plotly
import requests
from .models import Register
from plotly.offline import plot
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.graph_objs import Scatter
import plotly.offline as opy
import pandas as pd
# from datetime import datetime
import plotly.express as px
import random
import smtplib
import os
# from flask
data={"data":[{"rh":45.1875,"pod":"d","lon":80.3097,"pres":997,"timezone":"Asia\/Kolkata","ob_time":"2022-06-28 08:47","country_code":"IN","clouds":94,"ts":1656406066,"solar_rad":299.3,"state_code":"02","city_name":"Phirangipuram","wind_spd":5.27587,"wind_cdir_full":"west","wind_cdir":"W","slp":1002.5,"vis":16,"h_angle":12.9,"sunset":"13:13","dni":888.78,"dewpt":20,"snow":0,"uv":2.84887,"precip":0,"wind_dir":280,"sunrise":"00:07","ghi":850.73,"dhi":116.09,"aqi":27,"lat":16.2123,"weather":{"icon":"c04d","code":804,"description":"Overcast clouds"},"datetime":"2022-06-28:08","temp":33.3,"station":"VOBZ","elev_angle":56.63,"app_temp":35.5}],"count":1}
# Create your views here.
def register(request):
    if request.method=="POST":
        if  request.POST["name"]!="" and request.POST["email"]!="" and request.POST["country"]!="" and request.POST["city"]!="" and request.POST["zipcode"]!="" and request.POST["address"]!="":
            data=Register.objects.all()
            for i in data:
                if i.email==request.POST["email"] :
                    msg="Email Alredy Registerd"
                    return render(request,"register.html",{"msg1":msg})
            code=['1','2','3','4','5','6','7','8','9','0','Q','W','E','R','T','Y','U','I','O','P','A','S','D','F','G','H','J','K','L','Z','X','C','V','B','N','M','a','s','d','f','g','h','j','k','l','q','w','e','r','t','y','u','i','o','p','z','x','c','v','b','n','m']
            email_code=""
            for i in range(5):
                email_code+=random.choice(code)
            obj=Register.objects.create(name=request.POST["name"].lower(),email=request.POST["email"],country=request.POST["country"].lower(),city=request.POST["city"].lower(),zipcode=request.POST["zipcode"].lower(),address=request.POST["address"].lower(),verification_code=email_code,status="0")
            obj.save()
            value=0
            for i in data:
                value=i.id
            user=request.POST["name"].lower()
            send_email=request.POST["email"]
            # message=(f"OTP:- {email_code}, Welcome to Weather Application.")
            message="""Welcome to Weather Application.
                            Hi,
                            {0}.
                        Verification Code:
                                '{1}'
                        """.format(user,email_code)
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login("email", "password")
            s.sendmail('&&&&&&&&&&&', send_email, message)
            msg="Done"
            
                
            return render(request,"register.html",{"msg2":msg,"link":"verifiy/"+str(value+1)})
    return render(request,"register.html",{})

def verifiy(request,id):
    register = Register.objects.get(id = id)
    if request.method=="POST":
        if request.POST["verify"]!="":
            if request.POST["verify"]==register.verification_code:
                if register.status!="1":
                    register.status="1"
                    register.save()
                    message="""Welcome to Weather Application.
                            Hi,
                            {0}.
                        Email Verified...
                                '{1}'
                        click to login..
                        {2}
                        """.format(register.name,register.email,"Weather Application/login")
                    s = smtplib.SMTP('smtp.gmail.com', 587)
                    s.starttls()
                    s.login("email", "password")
                    s.sendmail('&&&&&&&&&&&', register.email, message)
                    return render(request,"verify.html",{"msg1":" Next..","name":register.name})
                else:
                    return render(request,"verify.html",{"msg2":"Verified","name":register.name})
                    
            else:
                return render(request,"verify.html",{"msg3":"Roung Address","name":register.name})
        else:
            return render(request,"verify.html",{"msg4":"Enter Verification code","name":register.name})
    return render(request,"verify.html",{"name":register.name})
def login(request):
    if request.method=="POST":
        if  request.POST["name"]!="" and request.POST["email"]!=""  and request.POST["zipcode"]!="" :
            data=Register.objects.all()
            for i in data:
                if i.status=="1":
                    if i.name==request.POST["name"].lower() and i.email==request.POST["email"] and i.zipcode==request.POST["zipcode"].lower():
                        request.session['name'] = request.POST["name"].lower()
                        request.session['email']=request.POST["email"]
                        request.session['zipcode']=request.POST["zipcode"].lower()
                        request.session["country"]=i.country
                        request.session['city']=i.city
                        return redirect('home')
                    
            return render(request,"login.html",{"":"Your not verify Email"})
    return render(request,"login.html",{})

def logout(request):
    try:
        if  request.session['name']!="":
            print("test")
            del request.session['name'] 
            del request.session['email']
            del request.session['zipcode']
            del request.session["country"]
            del request.session['city']
            return redirect("login")
        else:
            
            return redirect("login")
    except :
        return redirect("login")
    

def home(request):
    try:
        if request.session['name']:
            name=request.session['name']
            email=request.session['email']
            zipcode=request.session['zipcode']
            country=request.session["country"]
            city=request.session['city']
            # data={"data":[{"rh":45.1875,"pod":"d","lon":80.3097,"pres":997,"timezone":"Asia\/Kolkata","ob_time":"2022-06-28 08:47","country_code":"IN","clouds":94,"ts":1656406066,"solar_rad":299.3,"state_code":"02","city_name":"Phirangipuram","wind_spd":5.27587,"wind_cdir_full":"west","wind_cdir":"W","slp":1002.5,"vis":16,"h_angle":12.9,"sunset":"13:13","dni":888.78,"dewpt":20,"snow":0,"uv":2.84887,"precip":0,"wind_dir":280,"sunrise":"00:07","ghi":850.73,"dhi":116.09,"aqi":27,"lat":16.2123,"weather":{"icon":"c04d","code":804,"description":"Overcast clouds"},"datetime":"2022-06-28:08","temp":33.3,"station":"VOBZ","elev_angle":56.63,"app_temp":35.5}],"count":1}
            # list_data.append(123)
            json_data=requests.get("api_url")
            data=json_data.json()
            # print(data["data"])
            temp=[] 
            time=[]
            local_time=[]
            filter_local_time=[]
            hour=[]
        
            # print(data["minutely"])
            for i in data["minutely"]:
                for j,k in i.items():
                    if j=="temp":
                        temp.append(round(k-273.15, 2))
                    elif j=="timestamp_local":
                        time.append(k)
            for o in time:
                local_time.append(o.split(":"))
            for g in local_time:
                hour.append(g[0].split("T"))
            for p,h in zip(local_time,hour):
                filter_local_time.append(h[1]+":"+p[1]+":"+p[2])
            # Main Data
            data=data["data"]
            
            data_frame=pd.DataFrame({'filter_local_time' :filter_local_time,'temp' : temp,},columns=['filter_local_time','temp'])
            fig=px.line(x=data_frame["filter_local_time"],y=data_frame["temp"],title="After 1-Hour temperature",labels={"x":"Time","y":"Temperature"})
            fig.update_layout(
                title={
                    "font_size":22,
                    "xanchor":"center",
                    "x":0.5
                }
            )
            chart=fig.to_html()
            if request.method=="POST" :
                if request.POST["zip"]!="" and request.POST["zip"]!=NULL:
                    try:
                        
                        zip_data=requests.get("https://api.weatherbit.io/v2.0/current?postal_code="+request.POST['zip']+"&include=minutely&marine=t&units=S&key=2b61f7e5834547f7bbbd59c7805b2dfc")
                        if (zip_data.status_code==200):
                            zip_data=zip_data.json()
                            data1=zip_data["data"]
                            minutely=zip_data["minutely"]
                            temp=[] 
                            time=[]
                            local_time=[]
                            filter_local_time=[]
                            hour=[]
                            for i in zip_data["minutely"]:
                                for j,k in i.items():
                                    if j=="temp":
                                        temp.append(round(k-273.15, 2))
                                    elif j=="timestamp_local":
                                        time.append(k)
                            for o in time:
                                local_time.append(o.split(":"))
                            for g in local_time:
                                hour.append(g[0].split("T"))
                            for p,h in zip(local_time,hour):
                                filter_local_time.append(h[1]+":"+p[1]+":"+p[2])
                            data_frame=pd.DataFrame({'filter_local_time' :filter_local_time,'temp' : temp,},columns=['filter_local_time','temp'])
                            fig=px.line(x=data_frame["filter_local_time"],y=data_frame["temp"],title="After 1-Hour temperature",labels={"x":"Time","y":"Temperature"})
                            fig.update_layout(
                                title={
                                    "font_size":22,
                                    "xanchor":"center",
                                    "x":0.5
                                }
                            )
                            chart=fig.to_html()
                            return render(request,"home.html",{"name":name,"zipcode":zipcode,"email":email,"country":country,"city":city,"data":data1,"data_frame":chart})  
                    except :
                        return render(request,"home.html",{"name":name,"zipcode":zipcode,"email":email,"country":country,"city":city,"data":data,"msg":"check Zip Code"})
                else:
                    zip_msg="Enyter The Zipcode"
                    return render(request,"home.html",{"name":name,"zipcode":zipcode,"email":email,"country":country,"city":city,"data":data,"zip_msg":zip_msg})
    except:
        return render(request,"login.html",{"msg2":"Check login Email"})
    return render(request,"home.html",{"name":name,"zipcode":zipcode,"email":email,"country":country,"city":city,"data":data,"data_frame":chart})
    # return render(request,"home.html",{"data":data})
         

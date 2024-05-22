from django.shortcuts import render,redirect
from django.http import HttpResponse
import openai, os, requests
from  dotenv import load_dotenv
from django.core.files.base import ContentFile
from .models import Mindeye
from .models import FormDataForm
from django.contrib import messages







load_dotenv()
api_key = os.getenv("OPENAI_KEY", None)
openai.api_key= api_key




def generate_image(request):
    obj=None
    session_id= request.session.get('uid')
    if session_id:
     print("uid success")
     user = FormDataForm.objects.get(uid=session_id)
     print(user.email)
    if api_key is not None and request.method=="POST":
        user_input = request.POST.get('user_input')
        client = openai.Client(api_key=api_key)
        response = client.images.generate(
            model="dall-e-2",
            prompt=user_input,
            size="1024x1024",
            quality="standard",
            n=1,
        )
    
        img_url = response.data[0].url

        response = requests.get(img_url)
        img_file=ContentFile(response.content)

        count= Mindeye.objects.count() + 1
        fname=f"image-{count}.jpg"
        obj= Mindeye(prompt=user_input)
        obj.ai_image.save(fname , img_file)
        obj.save()
        return render (request ,"homepage.html" , {"object":obj})

    
    return render (request ,"homepage.html" , {})

def signUpPage(request):
    return render(request,'signup.html')

def saveform(request):
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        print(name, email, password)
        if (len(name)<1 and len(email)<1 and len(password)<1) :
            print("null form")
            messages.error(request,"PLEASE FILL THE FORM!")
            return render(request,"signup.html")
        elif (len(name)<5):
            print("invalid name")
            messages.error(request,"ENTER FULLNAME!!!")
            return render(request,"signup.html")
        elif (len(password)<5):
            print("invalid name")
            messages.error(request,"PASSWORD IS TOO SHORT!")
            return render(request,"signup.html")
        else:
          data=FormDataForm(name=name,email=email,password=password, usertype='user')
          data.save()
          return render(request,'login.html',{})
    else:
        return render(request,"signup.html")


def loginPage(request):
    print('login page')
    return render(request,'login.html')


def loginSubmit(request):
    if request.method=='POST':
        useremail=request.POST.get('email')
        userpassword=request.POST.get('password')
        print(useremail,userpassword)
        if (len(useremail)<1 and len(userpassword)<1):
            print("form incomplete")
            messages.error(request,"Please fill the form")
            return render (request,"login.html")
        elif(len(useremail)<1):
            print("invalid email")
            messages.error(request,"Enter  a valid email.")
            return render (request,"login.html")

        loginuser=FormDataForm.objects.filter(email=useremail)
        print(loginuser)
        useremail1 = loginuser[0].email
        userpassword1 = loginuser[0].password

        
        print(useremail,useremail1,userpassword, userpassword1)

        if useremail==useremail1 and userpassword==userpassword1:
            
            print("success")
            if(loginuser[0].usertype =='admin'):
               return render(request,'admin.html')
            else:
                 return render(request,'homepage.html')
        
        

        else:
            print("invalid")
            messages.error(request,"Login unsuccessfull!")
            return render(request,"login.html")
        
    return HttpResponse("login")

def indexpage(request):
    return render(request,"indexpage.html")
       
        
def home(request):
    return render(request,"indexpage.html")


def login(request):
    return render (request,"login.html")

def signup(request):
    return render (request,"signup.html")

def admin(request):
    prompts = Mindeye.objects.select_related('uid').all();

    data = []

    for prompt in prompts:
        print(prompt.uid.name,prompt.prompt)
        data.append({
            'id': prompt.id,
            'user': prompt.uid.name,
            'prompt': prompt.prompt, 
            'img': prompt.ai_image
            })

    return render (request,"admin.html", { 'data': data })

    


        
        

    
 




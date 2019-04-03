from .models import Question,CustomUser,Event
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, get_object_or_404,render ,redirect
from .forms import SignUpForm,ReplyForm
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login

#from django.http import HttpResponseRedirect

from django.utils import timezone
import datetime
from django.utils.timezone import utc

# for email activation link
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .forms import SignUpForm
from .tokens import account_activation_token
from django.core.mail import send_mail
from django.utils.encoding import force_text
from trivio import settings as sett
from django.utils.http import urlsafe_base64_decode

# class SignUp(generic.CreateView):
#     form_class = SignUpForm
#     success_url = reverse_lazy('login')
#     template_name = 'signup.html'

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            e=request.POST.get('email')
            current_site = get_current_site(request)
            subject = 'Activate Your Trivio Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            #user.email_user(subject, message)
            send_mail(subject,message,sett.EMAIL_HOST_USER, [e, ], fail_silently=False)
            return redirect('account_activation_sent')
        else:
            return HttpResponse("Time Expired, Try again")
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def activate(request, uidb64, token):
    uid = urlsafe_base64_decode(uidb64).decode()
    if len(uid)>len(CustomUser.objects.all()):
        return HttpResponse("Time Expired, Try again")
    user = CustomUser.objects.get(id=int(uid))

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_confirmed = True
        user.save()
        return HttpResponse("Authentication success go to login")
        #login(request, user)
        return redirect('home')
        
    else:
        return HttpResponse(str(user)+str(account_activation_token.check_token(user, token)))
        return render(request, 'account_activation_invalid.html')

def account_activation_sent(request):
    if request.user.is_anonymous:
        return HttpResponse('Check your Email')


def question(request):
    if request.user.is_anonymous:
        return redirect('home')
    event=Event.objects.get(id=1)
    timenow=((datetime.datetime.now()).strftime('%Y:%m:%d:%H:%M:%S'))
    timenow=datetime.datetime.strptime(timenow,'%Y:%m:%d:%H:%M:%S')
    eventtime=(event.event_start) + datetime.timedelta(hours=5.5)
    eventtime=datetime.datetime.strptime((eventtime.strftime('%Y:%m:%d:%H:%M:%S')),'%Y:%m:%d:%H:%M:%S')
    quiztime=float((len(Question.objects.all())*(event.interval)))+5
    t=int(request.user.id)
    user=CustomUser.objects.get(id=t)
    if user.status<1:
        return redirect('home')
    if (user.status>len(Question.objects.all()) or timenow>(eventtime+ datetime.timedelta(seconds=quiztime))):
        #return HttpResponse(str(eventtime+ datetime.timedelta(seconds=quiztime)))
        user.status=0
        user.save()
        user.publish()
        return redirect('leaderboard')
        #return HttpResponse(str(timenow)+"----"+str(eventtime+datetime.timedelta(seconds=quiztime))+" ----"+str(user.status)+str(len(Question.objects.all())))
    if request.method == "POST":
        score=(request.user.score)
        question = get_object_or_404(Question, pk=str(user.status))
        user_answer=request.POST.get('answer')
        user.flag=0
        if(str(user_answer)==str(question.answer)):
            user.score+=1
            user.flag=1
        (user.status)+=1
        user.save()
        user.publish()
        return redirect('')
    else:
        form=ReplyForm()
        score=user.score
        if int(user.flag)==1:
            message="Correct! "
        else:
            message="Wrong :( "
        if user.status==1:
            message="Hello! welcome to Trivio"
        question = get_object_or_404(Question, pk=str(user.status))
        sec=(timenow-eventtime).total_seconds()
        timeleft=10000
        return render(request,'question.html',{'message':message,'question': question,'form':form,'timeleft':timeleft,'sec':sec,})


def home(request):
    timenow = datetime.datetime.now() #.strftime('%H:%M:%S') #.strftime('%d %b %Y %H:%M:%S')
    event=Event.objects.get(id=1)
    eventtime=(event.event_start) + datetime.timedelta(hours=5.5)
    eventtime=(eventtime.strftime('%Y:%m:%d:%H:%M:%S'))
    eventtime=datetime.datetime.strptime(eventtime,'%Y:%m:%d:%H:%M:%S')
    timenow=(timenow.strftime('%Y:%m:%d:%H:%M:%S'))
    timenow=datetime.datetime.strptime(timenow,'%Y:%m:%d:%H:%M:%S')
    timeleft=eventtime-timenow
    if timeleft >datetime.timedelta(seconds=5):
        timeleft=timeleft.total_seconds()
        return render(request, 'welcome.html', {'timeleft':timeleft},)
    elif (timeleft <datetime.timedelta(seconds=5) and timeleft >datetime.timedelta(seconds=-2)):
        t=int(request.user.id)
        user=CustomUser.objects.get(id=t)
        user.status=1
        user.save()
        user.publish()
        return redirect('')
    else:
        return HttpResponse("the event has already started try next game")



def leaderboard(request,pk):
    limit = CustomUser.objects.all().count()
    limit=int(limit/50)+1
    if int(pk)>=limit:
        return redirect('../0/')
    pos=(int(pk))*50
    p=int(pk)-1
    l=int(pk)+1
    if l==limit:
        l=-1
    if not request.user.is_anonymous:
        user = CustomUser.objects.filter(id=(request.user.id))
        rank = CustomUser.objects.filter(score__gte=request.user.score).count()
        participants = CustomUser.objects.filter().order_by('-score')[pos+1:pos+51]
        return render(request, 'leaderboard.html', {'participants': participants,'rank':rank,'user':user,'position':pos,'p':p,'l':l},)
    
    participants = CustomUser.objects.filter().order_by('-score')[pos+1:pos+11]
    
    return render(request, 'leaderboard.html', {'participants': participants,'position':pos,'p':p,'l':l},)



def profile(request):
    return render(request,'profile.html')

def contact(request):
    return render(request,'contact.html')

def test(request):
    participants = CustomUser.objects.filter().order_by('-score')
    return render(request, 'ques.html', {'participants': participants},)

def test2(request):
    form=ReplyForm()
    message="hello"
    question="Where are you?"
    return render(request,'question.html',{'message':message,'question': question,'form':form,})
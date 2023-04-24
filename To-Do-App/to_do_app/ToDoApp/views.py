from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate, login, logout
from .sendemail import To_Do_email_notification
from datetime import date,datetime
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,DeleteView,UpdateView,FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
import datetime



# Create your views here.
def landingpage(request):
    return render(request,'ToDoApp/landingpage.html',{})

class TaskListView (LoginRequiredMixin,ListView):
    model = Task
    template_name = 'ToDoApp/TaskListView.html'
    context_object_name = 'task_list'
    queryset = Task.objects.order_by('starting_time')

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks_list']= context['task_list'].filter(user = self.request.user)
        return context

class Home(LoginRequiredMixin,ListView):
    model = Task
    template_name = 'ToDoApp/home.html'
    context_object_name = 'task_list'
    queryset = Task.objects.order_by('starting_time')
    
    # sending email if task list is time reminder time has reached 
    tasklist = Task.objects.all()
    if tasklist:
        for task in tasklist:
            task_reminder_time = task.reminder_time.date()
            now_duration = datetime.datetime.now().date()
            duration_diff = task_reminder_time - now_duration

            time_now = datetime.datetime.now().time().replace(second=0,microsecond=0)
            reminder_time = task.reminder_time.time().replace(second=0,microsecond=0)

            print(time_now,reminder_time, duration_diff)
            

            if (duration_diff.days == 0) :
                if (time_now == reminder_time):
                    subject = task.title
                    To_Do_email_notification(task.user.email,f'Hello <b>{task.user.first_name}</b>,<br>This is just a simple notification about your to do activity titled "{task.title}" that is scheduled to start on {task.starting_time}<br>Click here to view task: <a href="https://todo-production-df7e.up.railway.app/{task.pk}/"><b>{task.title}</b></a><br>With regards<br>Calvin<br>To-do-admin',subject)
                else:pass
            else:pass

    # tasklismenu = Task.objects.filter('user_id')
    # queryset = Task.objects.filter('user')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks_list'] = context['task_list'].filter(user = self.request.user).order_by('starting_time')
        context['count'] = context['task_list'].filter(status = 'Un attempted').count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks_list'] = context['tasks_list'].filter(title__contains=search_input)
        context['search_input'] = search_input
      
        return context

# def home(request):
#     task_list = Task.objects.all
#     return render(request,'ToDoApp/home.html',{'task_list':task_list})


class addTask(LoginRequiredMixin,CreateView):
    model = Task
    fields = ('title','activity','starting_time','reminder_time','status')
    template_name = 'ToDoApp/taskform.html'
    success_url = reverse_lazy('ToDoApp:home')

    # def post(self, request):
    #     form = self.form_class(request.POST)
    #     title = request.POST['title']
    #     activity = request.POST['activity']
    #     starting_time = request.POST['starting_time']
    #     reminder_time = request.POST['reminder_time']
    #     status = request.POST['status']

    #     return reverse_lazy('ToDoApp:home')
        
        # return super(addTask, self).render_to_response(context={})
    
    def form_valid(self, form):
        form.instance.user = self.request.user
    
        # querying the date if its not beyond 7 days
        startingtask = form.instance.starting_time.date()
        duration = datetime.datetime.now().date()
        date_diff = startingtask-duration
        if (date_diff.days)>(7):
            form.add_error('starting_time','Task should not be set for a period beyond a week')
            return self.form_invalid(form)
        else:
            return super(addTask,self).form_valid(form)
        # return super(addTask,self).form_valid(form)
    
   


# @login_required
# def addTask(request):
#     task_form = TaskForm(request.POST or None)
#     if request.method =='POST':
#         tast_form = TaskForm(data = request.POST)
#         # user = User_Form.objects.filter()
#         if tast_form.is_valid():
#             task_form
#             tast_form.save()
#             return HttpResponseRedirect('home')
#         else:
#             print(User_Form.errors)
#     else:
#         task_form = TaskForm()

#     return render(request,'ToDoApp/taskform.html',{'task_form':task_form})


# class register(FormView):
#     template_name = 'ToDoApp/register.html'
#     form_class = UserCreationForm
#     redirect_authenticated_user = True
#     success_url = reverse_lazy('ToDoApp:home')

#     def form_valid(self, form):
#         user = form.save()
#         if user is not None:
#             login(self.request, user)
#         return super(register, self).form_valid(form)

#     def get(self, *args, **kwargs):
#         if self.request.user.is_authenticated:
#             return redirect('tasks')
#         return super(register, self).get(*args, **kwargs)


def register(request):

    registered = False

    if request.method == "POST":
        user_form = User_Form(data= request.POST)
        user_profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and user_profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            subject = 'Account Creation'
            To_Do_email_notification(user.email,f'Hello <b>{user.first_name}</b><br>You have successfully created an account with us.<br> With regards<br>To Do Team <br>',subject)

            # profile = user_profile_form.save(commit = False)
            # profile.user = user

            # if 'profile_picture' in request.FILES:
            #      profile.profile_picture = request.FILES['profile_picture']

            # profile.save()

            registered = True

        else:
             print(user_form.errors,user_profile_form.errors)
    else:
        user_form = User_Form()
        user_profile_form = UserProfileForm()

    return render(request,'ToDoApp/register.html',{
        'user_form':user_form,
        'user_profile_form':user_profile_form,
        'registered':registered,
    })

class user_login(LoginView):
    template_name = 'ToDoApp/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('ToDoApp:home')

# def user_login(request):

#     if request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(username = username,password = password)

#         if user:
#             if user.is_active:
#                 login(request,user)
#                 return HttpResponseRedirect(reverse('home'))
#             else:
#                 return HttpResponseRedirect("ACCOUNT NOT ACTIVE")
#         else:
#             print('someone tried loging in ')
#             return HttpResponse('invalid login details supplied')
#     else:
#         return render(request,'ToDoApp/login.html')
    

@login_required
def  user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('landingpage'))

# sending email at the time of reminder of the task
# def reminder_email(request):
#     task = Task.objects.all

# detail vieew

class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    template_name = 'ToDoApp/taskdetail.html'
    context_object_name = 'task'


# def taskdetail(request,id):
#     # if request.method == 'GET':
#         taskss = Task.objects.get(id = id)
#         return render(request,'ToDoApp/taskdetail.html',{'taskss':taskss})
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields =('title','activity','starting_time','reminder_time','status')
    template_name = 'ToDoApp/edit.html'
    success_url = reverse_lazy('ToDoApp:home')


class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'ToDoApp/delete.html'
    success_url = reverse_lazy('ToDoApp:home')

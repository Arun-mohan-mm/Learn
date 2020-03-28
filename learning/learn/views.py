from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import *
from django.contrib import messages
import requests
from learn.forms import LoginForm
import pandas as pd
from bs4 import BeautifulSoup
import time
import datetime
import re
from datetime import date
from django.core import serializers
import json
from django.core.files.storage import FileSystemStorage


def home(request):
    return render(request,'home.html')
def admin_home(request):
    return render(request,'admin_home.html')

def register_st(request):
    if request.method == 'POST':
        x = datetime.datetime.now()
        y = x.strftime("%Y-%m-%d")
        typ = request.POST.get('student')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        psw = request.POST.get('psw')
        log = Login()
        log.Email = email
        log.Password = psw
        log.User_role = typ
        log.save()
        reg = Student_registration()
        reg.First_name = first_name
        reg.Last_name = last_name
        reg.Email = email
        reg.Password = psw
        reg.user_category = typ
        reg.Registration_date = y
        reg.Log_id = log
        reg.save()
        messages.success(request, 'You have successfully registered')
        return render(request, 'home.html')
    else:
        return render(request, 'register.html')

def register_tr(request):
    if request.method == 'POST':
        x = datetime.datetime.now()
        y = x.strftime("%Y-%m-%d")
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        psw = request.POST.get('psw')
        qual = request.POST.get('qual')
        intro = request.POST.get('intro')
        photo = request.FILES['photo']
        enrol = request.POST.get('enrol')
        avg_rev = request.POST.get('avg_rev')
        tot_rev = request.POST.get('tot_rev')
        teach = request.POST.get('teacher')
        log = Login()
        log1 = Login.objects.all()
        for i in log1:
            if i.Email == email:
                messages.success(request, 'User already exists')
                return render(request, 'home.html')
        log.Email = email
        log.Password = psw
        log.User_role = teach
        log.save()
        t = Teacher_registration()
        t.First_name = first_name
        t.Last_name = last_name
        t.Email = email
        t.Password = psw
        t.Registration_date = y
        t.Qualification = qual
        t.Introduction_brief = intro
        t.Image = photo
        t.Num_of_enrolled_students = enrol
        t.Average_review_rating = avg_rev
        t.Num_of_reviews = tot_rev
        t.Log_id = log
        t.save()
        messages.success(request, 'You have successfully registered')
        return render(request, 'home.html')
    else:
        return render(request, 'register_teacher.html')
def admin_rg(request):
    if request.method == 'POST':
        lk = Login.objects.all()
        for t in lk:
            if t.User_role == 'admin':
                messages.success(request, 'You are not allowed to be registered as admin')
                return render(request, 'home.html')
        x = datetime.datetime.now()
        z = x.strftime("%Y-%m-%d")
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        psw = request.POST.get('psw')
        admin = request.POST.get('adminn1')
        log = Login()
        log1 = Login.objects.all()
        for i in log1:
            if i.Email == email:
                messages.success(request, 'User already exists')
                return render(request, 'home.html')
        log.Email = email
        log.Password = psw
        log.User_role = admin
        log.save()
        t = Admin_registration()
        t.First_name = first_name
        t.Last_name = last_name
        t.Email = email
        t.Password = psw
        t.Registration_date = z
        t.Log_id = log
        t.save()
        messages.success(request, 'You have successfully registered')
        return render(request, 'home.html')
    else:
        return render(request, 'register_admin.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get("email")
        password = request.POST.get("pword")
        if (Login.objects.filter(Email=username, Password=password).exists()):
            logs = Login.objects.filter(Email=username, Password=password)

            for value in logs:
                user_id = value.id
                usertype  = value.User_role
                if usertype == 'admin':
                    request.session['logg'] = user_id
                    return render(request, "admin_home.html")

                elif usertype == 'teacher':
                    request.session['logg'] = user_id
                    return render(request, 'teacher_home.html')

                elif usertype == 'student':
                    request.session['logg'] = user_id
                    return render(request, 'student_home.html')
        else:
            messages.success(request, 'Email or password entered is incorrect')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

def chapter_tr(request):
    dm = Subject.objects.all()
    dd = Course_chapter.objects.all()
    return render(request, 'chap_tr.html', {'dd': dd,'dm':dm})

def student_home(request):
    return render(request, "student_home.html")

def teacher_home(request):
    return render(request, 'teacher_home.html')

def admin_prof(request):
    gtt = Login.objects.filter(User_role='admin')
    gtt1 = Admin_registration.objects.all()
    return render(request, 'adm_prof.html', {'gtt': gtt, 'gtt1': gtt1})

def del_admin(request, id):
    Login.objects.get(id = id).delete()
    messages.success(request, 'You have successfully resigned from administration')
    return render(request, 'home.html')

def edit_admin(request):
    bb1 = Admin_registration.objects.all()
    return render(request, 'update_admin.html',{'bb1':bb1})

def bnb(request):
    if request.method == 'POST':
        first = request.POST.get('first')
        last = request.POST.get('last')
        em = request.POST.get('em')
        psw = request.POST.get('psw')
        dcd = Login.objects.get(User_role = 'admin')
        dcd.Email = em
        dcd.Password = psw
        dcd.save()
        dcd1 = Admin_registration.objects.get(Log_id = request.session['logg'])
        dcd1.First_name = first
        dcd1.Last_name = last
        dcd1.Email = em
        dcd1.Password = psw
        dcd1.save()
        messages.success(request, 'You have successfully updated your profile')
        return render(request, 'admin_home.html')
    else:
        return render(request, 'admin_home.html')

def edit_chapter(request, id):
    dm = Subject.objects.all()
    gh = Course_chapter.objects.get(id = id)
    dd = Course_chapter.objects.all()
    if request.method == 'POST':
        sub = request.POST.get('sub')
        cou = request.POST.get('cou')
        c_tt = request.POST.get('c_tt')
        n_s = request.POST.get('n_s')
        vid = request.POST.get('vid')
        imag = request.POST.get('imag')
        prgg = request.POST.get('prgg')
        gh.Subject_title = sub
        gh.Course_name = cou
        gh.Chapter_title = c_tt
        gh.Num_of_assignments = n_s
        if vid != '':
            gh.Num_of_videos  = vid
        if imag != '':
            gh.Num_of_images  = imag
        if prgg != '':
            gh.Num_of_paragraphs  = prgg
        gh.save()
        messages.success(request, 'Chapter edited successfully')
        return render(request, 'chap_tr.html',{'dd':dd,'dm':dm})
    return render(request,'edit_chapter.html',{'gh':gh})

def ch_co_tr(request):
    dd = Course_chapter_content.objects.all()
    return render(request, 'cont_tr.html', {'dd': dd})

def edit_content(request, id):
    gh = Course_chapter_content.objects.get(id=id)
    dd = Course_chapter_content.objects.all()
    if request.method == 'POST':
        sub = request.POST.get('sub')
        cou = request.POST.get('cou')
        c_n1 = request.POST.get('c_n')
        s = request.POST.get('s')
        time = request.POST.get('time')
        s1 = request.POST.get('s1')
        cont_typ = request.POST.get('cont_typ')
        gh.Subject_title = sub
        gh.Course_name = cou
        gh.Course_chapter_name = c_n1
        if cont_typ == 1:
            gh.Content_type = 'Image'
        if cont_typ == 2:
            gh.Content_type = 'Text'
        if cont_typ == 3:
            gh.Content_type = 'Video'
        gh.Is_mandatory  = s
        gh.Time_required_in_sec  = time
        gh.Is_open_for_free  = s1
        gh.save()
        messages.success(request, 'Chapter content edited successfully')
        return render(request, 'cont_tr.html', {'dd': dd})
    return render(request, 'edit_content.html', {'gh': gh})

def delete_content(request, id):
    Course_chapter_content.objects.get(id = id).delete()
    dd = Course_chapter_content.objects.all()
    messages.success(request, 'Chapter content deleted successfully')
    return render(request, 'cont_tr.html',{'dd':dd})

def add_ch_con(request):
    dd = Course_chapter_content.objects.all()
    kk = Subject.objects.all()
    if request.method == 'POST':
        sub_tit = request.session['subj_nn']
        sel_c = request.POST.get('sel_c')
        ch_tit1 = request.POST.get('ch_tit1')
        dt = Course_chapter.objects.get(Course_name=sel_c, Chapter_title= ch_tit1)
        up_c = request.FILES['up_c']
        fs = FileSystemStorage()
        fs.save(up_c.name, up_c)
        s1 = request.POST.get('s1')
        s = request.POST.get('s')
        cont_typ = request.POST.get('cont_typ')
        cdt = Course_chapter_content()
        cv = int(cont_typ)
        if cv == 1:
            cdt.Content_type = 'Image'
        if cv == 2:
            cdt.Content_type = 'Text'
        if cv == 3:
            cdt.Content_type = 'Video'
        time = request.POST.get('time')
        cdt.Subject_title = sub_tit
        cdt.Course_name = sel_c
        cdt.Course_chapter_name  = ch_tit1
        cdt.Content_name  = up_c
        cdt.Is_mandatory = s
        cdt.Time_required_in_sec = time
        cdt.Is_open_for_free = s1
        cdt.Chapt = dt
        cdt.save()
        messages.success(request, 'Chapter content added successfully')
        return render(request, 'cont_tr.html', {'dd': dd})
    return render(request,'add_chapter_content.html',{'kk':kk})

def add_chapter_c1(request):
    gg = request.POST.get('subj')
    bb1 = Course_chapter.objects.all()
    bk = []
    for i in bb1:
        if i.Course_name not in bk:
            bk.append(i.Course_name)
    bb = []
    for i in bb1:
        if i.Chapter_title not in bb:
            bb.append(i.Chapter_title)
    request.session['subj_nn'] = gg
    return render(request, 'add_chapter_c2.html', {'gg': gg,'bb':bb,'bk':bk})

def sub(request):
    if request.method == 'POST':
        sub_name = request.POST.get('sub_name')
        sub_top = request.POST.get('sub_top')
        top_dr=request.POST.get('top_dr')
        dat = request.POST.get('date')
        subject = Subject_details()
        subject.sub_name = sub_name
        subject.sub_topic = sub_top
        subject.topic_dr = top_dr
        subject.Date = dat
        subject.save()
        return render(request,'admin_home.html')
    return render(request, 'subject.html')

def update_pr_tr(request):
    bb = Teacher_registration.objects.get(Log_id=request.session['logg'])
    if request.method == 'POST':
        f_name = request.POST.get('first_name')
        l_name = request.POST.get('last_name')
        email = request.POST.get('email')
        pasw = request.POST.get('psw')
        qual = request.POST.get('qual')
        intro = request.POST.get('intro')
        try:
            imgg1 = request.FILES['imgg1']
            fs = FileSystemStorage()
            fs.save(imgg1.name,imgg1)
            enrol = request.POST.get('enrol')
            log = Login.objects.get(id=request.session['logg'])
            log.Email = email
            log.Password = pasw
            log.save()
            bb.First_name = f_name
            bb.Last_name = l_name
            bb.Email = email
            bb.Password = pasw
            bb.Qualification = qual
            bb.Introduction_brief  = pasw
            bb.Introduction_brief = intro
            bb.Image = imgg1
            bb.Num_of_enrolled_students = enrol
            bb.save()
            messages.success(request, 'Updated successfully')
            return render(request, 'teacher_home.html')
        except:
            imgg2 = request.POST.get('imgg2')
            enrol = request.POST.get('enrol')
            log = Login.objects.get(id=request.session['logg'])
            log.Email = email
            log.Password = pasw
            log.save()
            bb.First_name = f_name
            bb.Last_name = l_name
            bb.Email = email
            bb.Password = pasw
            bb.Qualification = qual
            bb.Introduction_brief = pasw
            bb.Introduction_brief = intro
            bb.Image = imgg2
            bb.Num_of_enrolled_students = enrol
            bb.save()
            messages.success(request, 'Updated successfully')
            return render(request, 'teacher_home.html')
    return render(request, 'update_pr_tr.html', {'bb': bb})

def logout(request):
    if 'logg' in request.session:
        del request.session['logg']
        return render(request,'home.html')
    return render(request, 'home.html')
def update_pr_st(request):
    bb = Student_registration.objects.get(Log_id=request.session['logg'])
    if request.method == 'POST':
        f_name = request.POST.get('first_name')
        l_name = request.POST.get('last_name')
        email = request.POST.get('email')
        pasw = request.POST.get('psw')
        enrol = request.POST.get('enrol')
        log = Login.objects.get(id=request.session['logg'])
        log.Email = email
        log.Password = pasw
        log.save()
        bb.First_name = f_name
        bb.Last_name = l_name
        bb.Email = email
        bb.Password = pasw
        bb.Num_of_courses_enrolled = enrol
        bb.save()
        messages.success(request, 'Updated successfully')
        return render(request, 'student_home.html')
    return render(request, 'update_pr_st.html', {'bb': bb})

def subject_tr(request):
   dd = Subject.objects.all()
   return render(request,'sub_tr.html',{'dd':dd})

def add_chapter(request):
    dm = Subject.objects.all()
    dd = Course_chapter.objects.all()
    kk = []
    for i in dm:
        if i.Subject_title not in kk:
            kk.append(i.Subject_title)
    if request.method == 'POST':
        cou_tit = request.POST.get('cou_tit1')
        ss = Subject.objects.get(Subject_title = request.session['subj_n'], Course_title = cou_tit)
        sub_tit = request.session['subj_n']
        ch_tit1 = request.POST.get('ch_tit1')
        assi = request.POST.get('assi')
        vdd = request.POST.get('vdd')
        im = request.POST.get('im')
        parg = request.POST.get('parg')
        cdt = Course_chapter()
        cdt.Subject_title = sub_tit
        cdt.Course_name = cou_tit
        cdt.Chapter_title  = ch_tit1
        cdt.Num_of_assignments = assi
        cdt.Num_of_videos = vdd
        cdt.Num_of_images = im
        cdt.Num_of_paragraphs = parg
        cdt.Sub_id = ss.id
        cdt.save()
        messages.success(request, 'Chapter added successfully')
        return render(request, 'chap_tr.html', {'dd': dd,'dm':dm})
    return render(request,'add_chapter.html',{'kk':kk})

def delete_chapter(request, id):
    Course_chapter.objects.get(id = id).delete()
    dm = Subject.objects.all()
    dd = Course_chapter.objects.all()
    messages.success(request, 'Chapter deleted successfully')
    return render(request, 'chap_tr.html',{'dd':dd,'dm':dm})

def subject_tr1(request):
   dd = Subject.objects.all()
   return render(request,'sub_tr1.html',{'dd':dd})

def add_chapter1(request):
    gg = request.POST.get('subj')
    gg1 = Subject.objects.all()
    request.session['subj_n'] = gg
    return render(request, 'add_chapter2.html', {'gg1': gg1})

def edit_subject(request, id):
    gh = Subject.objects.get(id = id)
    dd = Subject.objects.all()
    if request.method == 'POST':
        sub = request.POST.get('sub')
        cou = request.POST.get('cou')
        c_b = request.POST.get('c_b')
        c_d = request.POST.get('c_d')
        n_c = request.POST.get('n_c')
        c_f = request.POST.get('c_f')
        lan = request.POST.get('lan')
        gh.Subject_title = sub
        gh.Course_title = cou
        gh.Course_brief = c_b
        gh.Course_duration = c_d
        gh.Num_of_chapters = n_c
        gh.Course_fee  = c_f
        gh.Language  = lan
        gh.save()
        messages.success(request, 'Subject edited successfully')
        return render(request, 'sub_tr.html',{'dd':dd})
    return render(request,'edit_subject.html',{'gh':gh})
def delete_subject(request, id):
    Subject.objects.get(id = id).delete()
    dd = Subject.objects.all()
    messages.success(request, 'Deleted subject successfully')
    return render(request, 'sub_tr.html',{'dd':dd})
def add_subject(request):
    dd = Subject.objects.all()
    if request.method == 'POST':
        sub_tit = request.POST.get('sub_tit')
        cou_tit = request.POST.get('cou_tit')
        c_b1 = request.POST.get('c_b1')
        c_d1 = request.POST.get('c_d1')
        n_c1 = request.POST.get('n_c1')
        c_f1 = request.POST.get('c_f1')
        lang = request.POST.get('lang')
        cdt = Subject()
        cdt.Subject_title = sub_tit
        cdt.Course_title = cou_tit
        cdt.Course_brief = c_b1
        cdt.Course_duration = c_d1
        cdt.Num_of_chapters = n_c1
        cdt.Course_fee = c_f1
        cdt.Language = lang
        cdt.save()
        messages.success(request, 'Added subject successfully')
        return render(request, 'sub_tr.html', {'dd': dd})
    return render(request,'add_subject.html')

def stu_sub_selnew(request):
    sne = Subject.objects.all()
    snew = []
    for i in sne:
        if i.Subject_title not in snew:
            snew.append(i.Subject_title)
    return render(request, 'st_sub_selnew1.html',{'snew':snew})
def st_sub_selnew2(request):
    d = request.POST.get('subj')
    request.session['sub_n'] = d
    snew1 = Subject.objects.filter(Subject_title = d)
    return render(request, 'st_sub_selnew2.html', {'snew1': snew1})

def disp_teach(request):
    couu = request.POST.get('cou')
    request.session['course'] = couu
    drt = Subject.objects.filter(Subject_title = request.session['sub_n'], Course_title = couu)
    return render(request,'st_sub_selnew.html',{'drt':drt})
def stu_buk_teacher(request):
    dh = Student_registration.objects.get(Log_id = request.session['logg'])
    gg = Subject.objects.get(Course_title = request.session['course'], Subject_title = request.session['sub_n'])
    spp = Enrollment()
    spp.Student_name = dh.First_name
    spp.Student_email = dh.Email
    spp.Subject_name = request.session['sub_n']
    spp.Course_name = request.session['course']
    spp.Attendance = 0
    spp.Pending_days = 0
    spp.Teacher_response = 'To be expected'
    if gg.Course_fee > 0:
        spp.Is_paid_subscription = 'True'
    else:
        spp.Is_paid_subscription = 'False'
    spp.save()
    messages.success(request, 'You have successfully booked a course')
    return render(request,'student_home.html')

def upl_cer(request):
    ss = Student_registration.objects.all()
    if request.method == 'POST':
        try:
            cert = request.FILES['cert']
            fs = FileSystemStorage()
            fs.save(cert.name,cert)
            stu_id = request.POST.get('stu_id')
            try:
                djk = Student_registration.objects.get(id = stu_id)
            except:
                messages.success(request, 'Please select a student')
                return render(request,'upload_cert.html',{'ss':ss})
            cc = Certificates()
            cc.Student_name = djk.First_name
            cc.Student_email = djk.Email
            cc.Certificate = cert
            cc.save()
            messages.success(request, 'Certificate uploaded successfully')
            return render(request, 'admin_home.html')
        except:
            cert = request.POST.get('cert')
            stu_id = request.POST.get('stu_id')
            djk = Student_registration.objects.get(id = stu_id)
            cc = Certificates()
            cc.Student_name = djk.First_name
            cc.Student_email = djk.Email
            cc.Certificate = cert
            cc.save()
            messages.success(request, 'Certificate uploaded successfully')
            return render(request, 'admin_home.html')
    return render(request,'upload_cert.html',{'ss':ss})

def do_cer(request):
    dd = Student_registration.objects.get(Log_id = request.session['logg'])
    try:
        sr = Certificates.objects.filter(Student_name = dd.First_name, Student_email = dd.Email)
    except:
        messages.success(request, 'No certificate available')
        return render(request, 'student_home.html')
    return render(request,'do_cer.html',{'sr':sr})

def about(request):
    tt = Teacher_registration.objects.all()
    return render (request,'about.html',{'tt':tt})



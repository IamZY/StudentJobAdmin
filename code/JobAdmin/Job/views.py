from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import json
from .models import Job,User,Teacher,Student,Admin,StudentJobEducation,\
    Education,JobInfo,Notice,ReadNotice,Resume,Business,BusinessPerson,BusinessAndStudent,College,Subject
from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
import time
# Create your views here.
def hello(request):
    # resp = {'errorcode': 100, 'detail': 'Get success'}
    jobs = Job.objects.all()
    jobs_json = serializers.serialize('json',jobs)
    # print(type(jobs_json))
    return HttpResponse(jobs_json, "application/json")
    # return HttpResponse(json.dumps(resp), content_type="application/json")

def login(request):
    # 只有请求header中的'Content-Type'：'application/x-www-form-urlencoded'才会填充request.POST
    # print(request.body)
    if request.method == 'POST' and request.body:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        # content = body['content']
        # name = request.body['username']
        # print(body['params']['username'])
        name = body['params']['username']
        passwd = body['params']['password']
        # passwd = request.body['password']
        u = User.objects.get(uname=name, upasswd=passwd)
        if not u is None:
            # json_u = serializers.serialize('json', u)
            # msg, code, user
            # return HttpResponse(json.dumps({'msg':'success','code':'200','user': u}), "application/json")
            name = u.uname
            passwd = u.upasswd
            id = u.uid
            utype = u.utype
            fkno = u.fkno
            data = {
                'msg': 'success',
                'code': 200,
                # 'user': json.loads(json_u)
                # 'username': name,
                # 'password': passwd
                # 'user': json.loads(u)
                'user' : {
                    'uid': id,
                    'username': name,
                    'password': passwd,
                    'utype': utype,
                    'fkno': fkno
                }
            }
            # return JsonResponse(data=data,safe=False)
            return JsonResponse(data=data,safe=False)
            # return u
        else:
            data = {
                'msg': 'error',
                'code': 500,
            }
            # return HttpResponse(json.dumps({'msg': 'error', 'code': 500, 'user': None}), "application/json")
            return JsonResponse(data=data,safe=False)
    else:
        data = {
            'msg': 'error',
            'code': 500,
        }
        return JsonResponse(data=data,safe=False)

def allJob(request):
    # print(request)
    if request.method == "GET":
        # print(request.GET['page'])
        # print(request.GET['pageSize'])
        utype = request.GET.get('utype')
        print(utype)
        page = request.GET.get('page')
        pageSize = request.GET.get('pageSize')

        businessName= request.GET.get('businessName')
        location= request.GET.get('location')
        jobName= request.GET.get('jobName')
        businessYear= request.GET.get('businessYear')
        education= request.GET.get('education')
        businessType= request.GET.get('businessType')
        money= request.GET.get('money')
        pubTime= request.GET.get('pubTime')
        url= request.GET.get('url')
        # print(jobName)
        jobs = []
        if utype == '3':
            bid = request.GET.get('bid')
            business = BusinessPerson.objects.get(id=bid).bid
            jobs = Job.objects.filter(bid=business)
        else:
            # print('else')
            jobs = Job.objects.all()
        # print(jobs)
        if len(businessName) != 0:
            # print('---')
            jobs = jobs.filter(businessName__icontains=businessName)
        if len(location) != 0:
            # print('---')
            jobs = jobs.filter(location__icontains=location)
        if len(jobName) != 0:
            # print('---')
            jobs = jobs.filter(jobName__icontains=jobName)
        if len(businessYear) != 0:
            # print('---')
            jobs = jobs.filter(businessYear__icontains=businessYear)
        if len(education) != 0:
            # print('---')
            jobs = jobs.filter(education__icontains=education)
        if len(businessType) != 0:
            # print('---')
            jobs = jobs.filter(businessType__icontains=businessType)
        if len(money) != 0:
            # print('---')
            jobs = jobs.filter(money__icontains=money)
        if len(pubTime) != 0:
            # print('---')
            jobs = jobs.filter(pubTime__icontains=pubTime)



        count = len(jobs)
        # print(type(jobs))
        # for job in jobs:
        # 将数据按照规定每页显示 10 条, 进行分割
        paginator = Paginator(jobs, pageSize)
        try:
            jobs = paginator.page(page)
            # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            jobs = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            jobs = paginator.page(paginator.num_pages)

        # jsonJobs = json.loads(serializers.serialize('json', jobs))
        jobList = []
        for job in jobs:
            jobList.append({
                'jid' : job.jid,
                'businessName': job.businessName,
                'location' : job.location,
                'jobName' :  job.jobName,
                'businessYear':  job.businessYear,
                'education':  job.education,
                'businessType':  job.businessType,
                'money' :  job.money,
                'pubTime' :  job.pubTime,
                'url' :  job.url,
                'bid': job.bid
            })
        # print(jobList)
        data = {
            'total': count,
            'jobs': jobList
        }

        return JsonResponse(data=data,safe=False)

    else:
        data = {
            'msg': 'error',
            'code': 500,
        }
        return JsonResponse(data=data, safe=False)


def getUser(request):
    if request.method == 'GET':
        uid = request.GET.get('id')
        # print(uid)
        user = User.objects.get(uid=uid)
        # print(user)
        data = {}
        if user.utype == "0":
            # 管理员
            admin = Admin.objects.get(aid=user.fkno)
            data = {
                'id': admin.aid,
                'utype': user.utype,
                'username': admin.aname,
                'phone': admin.phone,
                'collage': admin.collage,
                'university': admin.university
            }
        elif user.utype == "1":
            # 学生
            stu = Student.objects.get(sid=user.fkno)
            data = {
                'utype': user.utype,
                'sid' : stu.sid,
                'sno' : stu.sno,
                'name' : stu.name,
                'age' : stu.age,
                'clazz' : stu.clazz,
                'gender' : stu.gender,
                'phone' : stu.phone,
                'collage' : stu.collage,
                'university' : stu.university,
                'email': stu.email,
                'major': stu.major,
            }
        elif user.utype == "3":
            # 企业用户
            bus = BusinessPerson.objects.get(id=user.fkno)
            data = {
                'utype': user.utype,
                'id' : bus.id,
                'no' : bus.bno,
                'name' : bus.name,
                'phone' : bus.phone,
                'dept' : bus.dept,
                'bid': bus.bid,
                'businessName' : Business.objects.get(id=bus.bid).businessName,
                'businessPerson': Business.objects.get(id=bus.bid).businessPerson,
                'businessType': Business.objects.get(id=bus.bid).businessType,
                'location': Business.objects.get(id=bus.bid).location,
            }
        else:
            # 老师
            teacher = Teacher.objects.get(tid=user.fkno)
            data = {
                'utype': user.utype,
                'tid' : teacher.tid,
                'tno' : teacher.tno,
                'name' : teacher.name,
                'age' : teacher.age,
                'clazz' : teacher.clazz,
                'gender': teacher.gender,
                'phone': teacher.phone,
                'subject' : teacher.subject,
                'collage' : teacher.collage,
                'university' : teacher.university,
            }
        return JsonResponse(data=data, safe=False)
    else:
        data = {
            'msg': 'error',
            'code': 500,
        }
        return JsonResponse(data=data, safe=False)

def editUser(request):
    if request.method == 'GET':
        utype=request.GET.get('utype')
        print(utype)
        if utype == '0':
            id=request.GET.get('id')
            username=request.GET.get('username')
            phone=request.GET.get('phone')
            collage=request.GET.get('collage')
            university=request.GET.get('university')
            admin = Admin.objects.get(aid=id)
            admin.aname = username
            admin.phone = phone
            admin.collage = collage
            admin.university = university
            admin.save()
        elif utype == '1':
            id=request.GET.get('id')
            print(id)
            sno= request.GET.get('no')
            name= request.GET.get('username')
            age= request.GET.get('age')
            clazz= request.GET.get('clazz')
            gender= request.GET.get('gender')
            phone= request.GET.get('phone')
            collage= request.GET.get('collage')
            university= request.GET.get('university')
            email = request.GET.get('email')
            major = request.GET.get('major')
            stu = Student.objects.get(sid=id)
            stu.sno = sno
            stu.name = name
            stu.age = age
            stu.clazz = clazz
            stu.gender = gender
            stu.phone = phone
            stu.collage = collage
            stu.university = university
            stu.email = email
            stu.major = major
            stu.save()
        elif utype == '3':
            id=request.GET.get('id')
            print(id)
            sno= request.GET.get('no')
            name= request.GET.get('username')
            phone= request.GET.get('phone')
            bus = BusinessPerson.objects.get(id=id)
            bus.name = name
            bus.phone = phone
            bus.save()
        else:
            id = request.GET.get('id')
            print(id)
            tno = request.GET.get('no')
            name = request.GET.get('username')
            age = request.GET.get('age')
            clazz = request.GET.get('clazz')
            gender = request.GET.get('gender')
            phone = request.GET.get('phone')
            collage = request.GET.get('collage')
            university = request.GET.get('university')
            subject = request.GET.get('subject')
            teacher = Teacher.objects.get(tid=id)
            teacher.tno = tno
            teacher.name = name
            teacher.age = age
            teacher.clazz = clazz
            teacher.gender = gender
            teacher.phone = phone
            teacher.collage = collage
            teacher.university = university
            teacher.subject = subject
            teacher.save()
        data = {
            'msg': 'success',
        }
        return JsonResponse(data=data, safe=False)
    else:
        data = {
            'msg': 'error',
            'code': 500,
        }
        return JsonResponse(data=data, safe=False)

def allUsers(request):
    # print(request)
    if request.method == "GET":
        # print(request.GET['page'])
        # print(request.GET['pageSize'])
        page = request.GET.get('page')
        pageSize = request.GET.get('pageSize')
        name = request.GET.get('name')
        utype = request.GET.get('utype')

        user = User.objects.all()

        if len(name):
            user = user.filter(uname__icontains=name)

        if len(utype):
            user = user.filter(utype=utype)

        userList = []
        for u in user:
            if u.utype == '0':
                admin = Admin.objects.get(aid=u.fkno)
                userList.append({
                    'uid':  u.uid,
                    'uname': u.uname,
                    'upassword': u.upasswd,
                    'utype': u.utype,
                    'aid': admin.aid,
                    'username': admin.aname,
                    'phone': admin.phone,
                    'collage': admin.collage,
                    'university': admin.university
                })
            elif u.utype == '1':
                stu = Student.objects.get(sid=u.fkno)
                userList.append({
                    'uid': u.uid,
                    'uname': u.uname,
                    'upassword': u.upasswd,
                    'utype': u.utype,
                    'sid': stu.sid,
                    'sno': stu.sno,
                    'username': stu.name,
                    'age': stu.age,
                    'clazz': stu.clazz,
                    'gender': stu.gender,
                    'phone': stu.phone,
                    'collage': stu.collage,
                    'university': stu.university
                })
            elif u.utype == '3':
                bus = BusinessPerson.objects.get(id=u.fkno)
                userList.append({
                    'uid': u.uid,
                    'uname': u.uname,
                    'upassword': u.upasswd,
                    'utype': u.utype,
                    'bid': bus.id,
                    'bno': bus.bno,
                    'phone' : bus.phone,
                    'dept' : bus.dept,
                    'username': bus.name,
                    'businessName' : Business.objects.get(id=bus.bid).businessName,
                    'businessPerson': Business.objects.get(id=bus.bid).businessPerson,
                    'businessType': Business.objects.get(id=bus.bid).businessType,
                    'location': Business.objects.get(id=bus.bid).location,
                })
            else:
                t = Teacher.objects.get(tid=u.fkno)
                userList.append({
                    'uid': u.uid,
                    'uname': u.uname,
                    'upassword': u.upasswd,
                    'utype': u.utype,
                    'tid': t.tid,
                    'tno': t.tno,
                    'username': t.name,
                    'age': t.age,
                    'clazz': t.clazz,
                    'gender': t.gender,
                    'phone': t.phone,
                    'subject':t.subject,
                    'collage': t.collage,
                    'university': t.university
                })

        count = len(userList)
        # print(type(jobs))
        # for job in jobs:
        # 将数据按照规定每页显示 10 条, 进行分割
        paginator = Paginator(userList, pageSize)
        try:
            jobs = paginator.page(page)
            # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            jobs = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            jobs = paginator.page(paginator.num_pages)


        data = {
            'total': count,
            'users': userList
        }

        return JsonResponse(data=data, safe=False)

    else:
        data = {
            'msg': 'error',
            'code': 500,
        }
        return JsonResponse(data=data, safe=False)


def addJob(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        businessName = body['params']['businessName']
        # print(businessName)
        location = body['params']['location']
        jobName = body['params']['jobName']
        businessYear = body['params']['businessYear']
        education = body['params']['education']
        businessType = body['params']['businessType']
        money = body['params']['money']
        pubTime = body['params']['pubTime']
        url = body['params']['url']
        utype = body['params']['utype']

        if utype == '3':
            bid = body['params']['bid']
            business = BusinessPerson.objects.get(id=bid).bid

            job = Job()
            job.businessName = Business.objects.get(id=business).businessName
            job.location = Business.objects.get(id=business).location
            job.jobName = jobName
            job.businessYear = businessYear
            job.education = education
            job.businessType = Business.objects.get(id=business).businessType
            job.money = money
            job.pubTime = pubTime
            job.url = url
            job.pubTime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            job.bid = business
            job.save()

        else:
            job = Job()
            job.businessName = businessName
            job.location = location
            job.jobName = jobName
            job.businessYear = businessYear
            job.education = education
            job.businessType = businessType
            job.money = money
            job.pubTime = pubTime
            job.url = url
            job.pubTime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            job.save()



        data = {
            'msg': 'success',
        }
        return JsonResponse(data=data, safe=False)
    else:
        data = {
            'msg': 'error',
        }
        return JsonResponse(data=data, safe=False)

def removeJob(request):
    if request.method == 'GET':
        jid = request.GET.get('id')

        job = Job.objects.get(jid=jid)
        job.delete()
        data = {
            'msg': 'success',
        }
        return JsonResponse(data=data, safe=False)
    else:
        data = {
            'msg': 'error',
        }
        return JsonResponse(data=data, safe=False)

def editJob(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        jid = body['params']['jid']
        businessName = body['params']['businessName']
        location = body['params']['location']
        jobName = body['params']['jobName']
        businessYear = body['params']['businessYear']
        education = body['params']['education']
        businessType = body['params']['businessType']
        money = body['params']['money']
        pubTime = body['params']['pubTime']
        url = body['params']['url']

        job = Job.objects.get(jid=jid)
        job.businessName = businessName
        job.location = location
        job.jobName = jobName
        job.businessYear = businessYear
        job.education = education
        job.businessType = businessType
        job.money = money
        job.pubTime = pubTime
        job.url = url
        job.pubTime = time.strftime('%Y-%m-%d',time.localtime(time.time()))

        job.save()
        data = {
            'msg': 'success',
        }
        return JsonResponse(data=data, safe=False)
    else:
        data = {
            'msg': 'error',
        }
        return JsonResponse(data=data, safe=False)

def editAuth(request):
    if request.method == 'GET':
        utype = request.GET.get('utype')
        uid = request.GET.get('uid')
        uname = request.GET.get('uname')
        upassword = request.GET.get('upassword')
        aid = request.GET.get('aid')
        sid = request.GET.get('sid')
        tid = request.GET.get('tid')
        bid = request.GET.get('bid')
        sno = request.GET.get('sno')
        tno = request.GET.get('tno')
        username = request.GET.get('username')
        age = request.GET.get('age')
        clazz = request.GET.get('clazz')
        gender = request.GET.get('gender')
        phone = request.GET.get('phone')
        subject = request.GET.get('subject')
        collage = request.GET.get('collage')
        university = request.GET.get('university')

        dept = request.GET.get('dept')

        businessName= request.GET.get('businessName')
        businessType= request.GET.get('businessType')
        businessPerson= request.GET.get('businessPerson')
        location= request.GET.get('location')

        if utype == '0':
            admin = Admin.objects.get(aid=aid)
            admin.aname = username
            admin.phone = phone
            admin.collage = collage
            admin.university = university
            admin.save()
            user = User.objects.get(uid=uid)
            user.uname = uname
            user.upasswd = upassword
            user.save()
        elif utype == '1':
            user = User.objects.get(uid=uid)
            user.uname = uname
            user.upasswd = upassword
            user.save()
            stu = Student.objects.get(sid=sid)
            stu.sno = sno
            stu.name = username
            stu.age = age
            stu.clazz = clazz
            stu.gender = gender
            stu.phone = phone
            stu.collage = collage
            stu.university = university
            stu.save()
        elif utype == '3':
            user = User.objects.get(uid=uid)
            user.uname = uname
            user.upasswd = upassword
            user.save()
            bp = BusinessPerson.objects.get(id=bid)
            bp.name = username
            bp.phone = phone
            bp.dept = dept
            bp.save()
            bus = Business.objects.get(id=bp.bid)
            bus.businessName = businessName
            bus.businessType = businessType
            bus.businessPerson = businessPerson
            bus.location = location
            bus.save()
        else:
            user = User.objects.get(uid=uid)
            user.uname = uname
            user.upasswd = upassword
            user.save()
            teacher = Teacher.objects.get(tid=tid)
            teacher.tno = tno
            teacher.name = username
            teacher.age = age
            teacher.clazz = clazz
            teacher.gender = gender
            teacher.phone = phone
            teacher.collage = collage
            teacher.university = university
            teacher.subject = subject
            teacher.save()
        data = {
            'msg': 'success',
        }
        return JsonResponse(data=data, safe=False)
    else:
        data = {
            'msg': 'error',
        }
        return JsonResponse(data=data, safe=False)


def removeAuth(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        utype = request.GET.get('utype')
        if utype == '0':
            user = User.objects.get(uid=id)
            admin = Admin.objects.get(aid=user.fkno)
            admin.delete()
            user.delete()
        elif utype == '1':
            user = User.objects.get(uid=id)
            stu = Student.objects.get(sid=user.fkno)
            stu.delete()
            user.delete()
        else:
            user = User.objects.get(uid=id)
            t = Teacher.objects.get(tid=user.fkno)
            t.delete()
            user.delete()
        data = {
            'msg': 'success',
        }
        return JsonResponse(data=data, safe=False)
    else:
        data = {
            'msg': 'error',
        }
        return JsonResponse(data=data, safe=False)

def addAuth(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        # print(body)
        utype = body['params']['utype']
        if utype == '0':
            uname = body['params']['uname']
            upassword= body['params']['upassword']
            utype= body['params']['utype']
            username= body['params']['username']
            phone= body['params']['phone']
            collage= body['params']['collage']
            university= body['params']['university']

            admin = Admin()
            admin.aname = username
            admin.phone = phone
            admin.collage = collage
            admin.university = university
            admin.save()
            # print(admin.aid)
            user = User()
            user.uname = uname
            user.upasswd = upassword
            user.utype = utype
            user.fkno = admin.aid
            user.save()
        elif utype == '1':
            uname = body['params']['uname']
            upassword = body['params']['upassword']
            utype = body['params']['utype']
            sno = body['params']['sno']
            username = body['params']['username']
            age = body['params']['age']
            clazz = body['params']['clazz']
            gender = body['params']['gender']
            phone = body['params']['phone']
            collage = body['params']['collage']
            university = body['params']['university']
            email = body['params']['email']
            major = body['params']['major']

            stu = Student()
            stu.sno = sno
            stu.name = username
            stu.age = age
            stu.clazz = clazz
            stu.gender = gender
            stu.phone = phone
            stu.collage = collage
            stu.university = university
            stu.email = email
            stu.major = major
            stu.save()

            user = User()
            user.uname = uname
            user.upasswd = upassword
            user.utype = utype
            user.fkno = stu.sid
            user.save()

        else:
            uname = body['params']['uname']
            upassword = body['params']['upassword']
            utype = body['params']['utype']
            tno = body['params']['tno']
            username = body['params']['username']
            age = body['params']['age']
            clazz = body['params']['clazz']
            gender = body['params']['gender']
            phone = body['params']['phone']
            subject = body['params']['subject']
            collage = body['params']['collage']
            university = body['params']['university']

            t = Teacher()
            t.sno = tno
            t.name = username
            t.age = age
            t.clazz = clazz
            t.gender = gender
            t.phone = phone
            t.collage = collage
            t.university = university
            t.subject = subject
            t.save()

            user = User()
            user.uname = uname
            user.upasswd = upassword
            user.utype = utype
            user.fkno = t.tid
            user.save()

        data = {
            'msg': 'success',
        }
        return JsonResponse(data=data, safe=False)
    else:
        data = {
            'msg': 'error',
        }
        return JsonResponse(data=data, safe=False)

def allStudents(request):
    # print(request)
    if request.method == "GET":
        # print(request.GET['page'])
        # print(request.GET['pageSize'])
        page = request.GET.get('page')
        pageSize = request.GET.get('pageSize')
        name = request.GET.get('name')
        utype = request.GET.get('utype')
        fkno = request.GET.get('fkno')

        if utype == '1':
            data = {
                'msg': '无权限',
                'code': 500,
            }

            return JsonResponse(data=data, safe=False)


        if utype == '0':
            # 管理员 查看所有学生信息
            stu = Student.objects.all()

            stuList = []
            businessName = ''
            location = ''
            jobName = ''
            businessType = ''
            fuuniversity = ''
            education = ''
            major = ''
            for s in stu:
                stuJE = StudentJobEducation.objects.get(sid=s.sid)
                if stuJE.jid is None:
                    jid = ''
                else:
                    jid = stuJE.jid
                    businessName = JobInfo.objects.get(id=jid).businessName
                    location = JobInfo.objects.get(id=jid).location
                    jobName = JobInfo.objects.get(id=jid).jobName
                    businessType = JobInfo.objects.get(id=jid).businessType

                if stuJE.eid is None:
                    eid = ''
                else:
                    eid = stuJE.eid
                    fuuniversity = Education.objects.get(eid=eid).university
                    education = Education.objects.get(eid=eid).education
                    major = Education.objects.get(eid=eid).major

                stuList.append({
                    'sid': s.sid,
                    'sno': s.sno,
                    'username': s.name,
                    'age': s.age,
                    'clazz': s.clazz,
                    'gender': s.gender,
                    'phone': s.phone,
                    'collage': s.collage,
                    'university': s.university,
                    'jid': jid,
                    'businessName': businessName,
                    'location': location,
                    'jobName': jobName,
                    'businessType': businessType,
                    'eid': eid,
                    'fuuniversity': fuuniversity,
                    'education': education,
                    'major': major,
                })

            count = len(stuList)
            # print(type(jobs))
            # for job in jobs:
            # 将数据按照规定每页显示 10 条, 进行分割
            paginator = Paginator(stuList, pageSize)
            try:
                stuList = paginator.page(page)
                # todo: 注意捕获异常
            except PageNotAnInteger:
                # 如果请求的页数不是整数, 返回第一页。
                stuList = paginator.page(1)
            except InvalidPage:
                # 如果请求的页数不存在, 重定向页面
                return HttpResponse('找不到页面的内容')
            except EmptyPage:
                # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
                stuList = paginator.page(paginator.num_pages)

            # print(type(stuList))
            students=[]
            for s in stuList:
                # print(type(s))
                # print(s)
                students.append({
                    'sid': s['sid'],
                    'sno': s['sno'],
                    'username': s['username'],
                    'age': s['age'],
                    'clazz': s['clazz'],
                    'gender': s['gender'],
                    'phone': s['phone'],
                    'collage': s['collage'],
                    'university': s['university'],
                    'jid': s['jid'],
                    'businessName': s['businessName'],
                    'location': s['location'],
                    'jobName': s['jobName'],
                    'businessType': s['businessType'],
                    'eid': s['eid'],
                    'fuuniversity': s['fuuniversity'],
                    'education': s['education'],
                    'major': s['major'],
                })


            data = {
                'total': count,
                # 'students': stuList,
                'students': students,
                'code': 200
            }

            return JsonResponse(data=data, safe=False)
        if utype == '2':
            # 教师查看本班级学生信息
            t = Teacher.objects.get(tid=fkno)

            stu = Student.objects.filter(clazz=t.clazz)

            stuList = []
            businessName = ''
            location = ''
            jobName = ''
            businessType = ''
            fuuniversity = ''
            education = ''
            major = ''
            for s in stu:
                stuJE = StudentJobEducation.objects.get(sid=s.sid)
                if stuJE.jid is None:
                    jid = ''
                else:
                    jid = stuJE.jid
                    businessName = JobInfo.objects.get(id=jid).businessName
                    location = JobInfo.objects.get(id=jid).location
                    jobName = JobInfo.objects.get(id=jid).jobName
                    businessType = JobInfo.objects.get(id=jid).businessType

                if stuJE.eid is None:
                    eid = ''
                else:
                    eid = stuJE.eid
                    fuuniversity = Education.objects.get(eid=eid).university
                    education = Education.objects.get(eid=eid).education
                    major = Education.objects.get(eid=eid).major

                stuList.append({
                    'sid': s.sid,
                    'sno': s.sno,
                    'username': s.name,
                    'age': s.age,
                    'clazz': s.clazz,
                    'gender': s.gender,
                    'phone': s.phone,
                    'collage': s.collage,
                    'university': s.university,
                    'jid': jid,
                    'businessName': businessName,
                    'location' : location,
                    'jobName' : jobName,
                    'businessType' : businessType,
                    'eid': eid,
                    'fuuniversity': fuuniversity,
                    'education': education,
                    'major': major,
                })

            count = len(stuList)
            # print(type(jobs))
            # for job in jobs:
            # 将数据按照规定每页显示 10 条, 进行分割
            paginator = Paginator(stuList, pageSize)
            try:
                stuList = paginator.page(page)
                # todo: 注意捕获异常
            except PageNotAnInteger:
                # 如果请求的页数不是整数, 返回第一页。
                stuList = paginator.page(1)
            except InvalidPage:
                # 如果请求的页数不存在, 重定向页面
                return HttpResponse('找不到页面的内容')
            except EmptyPage:
                # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
                stuList = paginator.page(paginator.num_pages)

            students = []
            for s in stuList:
                # print(type(s))
                # print(s)
                students.append({
                    'sid': s['sid'],
                    'sno': s['sno'],
                    'username': s['username'],
                    'age': s['age'],
                    'clazz': s['clazz'],
                    'gender': s['gender'],
                    'phone': s['phone'],
                    'collage': s['collage'],
                    'university': s['university'],
                    'jid': s['jid'],
                    'businessName': s['businessName'],
                    'location': s['location'],
                    'jobName': s['jobName'],
                    'businessType': s['businessType'],
                    'eid': s['eid'],
                    'fuuniversity': s['fuuniversity'],
                    'education': s['education'],
                    'major': s['major'],
                })




            data = {
                'total': count,
                'students': students,
                'code': 200
            }

            return JsonResponse(data=data, safe=False)


    else:
        data = {
            'msg': 'error',
            'code': 500,
        }
        return JsonResponse(data=data, safe=False)

def addJobInfo(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        sid = body['params']['sid']
        businessName= body['params']['businessName']
        location = body['params']['location']
        jobName = body['params']['jobName']
        businessType= body['params']['businessType']

        obj = StudentJobEducation.objects.filter(sid=sid)

        # list = [StudentJobEducation.objects.all()]

        if len(obj) == 0:
            job = JobInfo()
            job.businessName = businessName
            job.location = location
            job.jobName = jobName
            job.businessType = businessType
            job.save()
            par = StudentJobEducation()
            par.sid = sid
            par.jid = job.id
            par.save()
            data = {
                'msg': 'success',
                'code': 200,
            }
            return JsonResponse(data=data, safe=False)
        else:
            if obj[0].eid is None:
                job = JobInfo()
                job.businessName = businessName
                job.location = location
                job.jobName = jobName
                job.businessType = businessType
                job.save()
                par = StudentJobEducation()
                par.sid = sid
                par.jid = job.id
                par.save()
                data = {
                    'msg': 'success',
                    'code': 200,
                }
                return JsonResponse(data=data, safe=False)
            else:
                data = {
                    'msg': '已登记升学',
                    'code': 500,
                }
                return JsonResponse(data=data, safe=False)
    else:
        data = {
            'msg': 'error',
            'code': 500,
        }
        return JsonResponse(data=data, safe=False)

def addEduInfo(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        sid = body['params']['sid']
        education= body['params']['education']
        major = body['params']['major']
        university = body['params']['university']

        obj = StudentJobEducation.objects.filter(sid=sid)
        if len(obj) == 0:
            edu = Education()
            edu.education = education
            edu.major = major
            edu.university = university
            edu.save()
            par = StudentJobEducation()
            par.sid = sid
            par.eid = edu.eid
            par.save()
            data = {
                'msg': 'success',
                'code': 200,
            }
            return JsonResponse(data=data, safe=False)
        else:
            if obj[0].jid is None:
                edu = Education()
                edu.education = education
                edu.major = major
                edu.university = university
                edu.save()
                par = StudentJobEducation()
                par.sid = sid
                par.eid = edu.eid
                par.save()
                data = {
                    'msg': 'success',
                    'code': 200,
                }
                return JsonResponse(data=data, safe=False)
            else:
                data = {
                    'msg': '已登记就业',
                    'code': 500,
                }
                return JsonResponse(data=data, safe=False)
    else:
        data = {
            'msg': 'error',
            'code': 500,
        }
        return JsonResponse(data=data, safe=False)

def getOnesJob(request):
    if request.method == 'GET':
        sid = request.GET.get('sid')
        obj = StudentJobEducation.objects.filter(sid=sid)
        if len(obj) != 0 and obj[0].jid is not None:
            # print('-----')
            job = JobInfo.objects.get(id=obj[0].jid)
            data = {
                'id': job.id,
                'businessName': job.businessName,
                'location': job.location,
                'jobName': job.jobName,
                'businessType': job.businessType,
            }
            return JsonResponse(data=data, safe=False)
        else:
            data = {
                'msg': 'error',
                'code': 500,
            }
            return JsonResponse(data=data, safe=False)

    else:
        data = {
            'msg': 'error',
            'code': 500,
        }
        return JsonResponse(data=data, safe=False)


def getOnesEdu(request):
    if request.method == 'GET':
        sid = request.GET.get('sid')
        obj = StudentJobEducation.objects.filter(sid=sid)
        if len(obj) != 0 and obj[0].eid is not None:
            # print('-----')
            edu = Education.objects.get(eid=obj[0].eid)
            data = {
                'id': edu.eid,
                'education': edu.education,
                'major': edu.major,
                'university': edu.university,
            }
            return JsonResponse(data=data, safe=False)
        else:
            data = {
                'msg': 'error',
                'code': 500,
            }
            return JsonResponse(data=data, safe=False)

    else:
        data = {
            'msg': 'error',
            'code': 500,
        }
        return JsonResponse(data=data, safe=False)


def editJobInfo(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        businessName= request.GET.get('businessName')
        location= request.GET.get('location')
        jobName= request.GET.get('jobName')
        businessType= request.GET.get('businessType')

        job = JobInfo.objects.get(id=id)
        job.businessName = businessName
        job.location = location
        job.jobName = jobName
        job.businessType = businessType
        job.save()
        data = {
            'msg': 'success',
            'code': 200,
        }
        return JsonResponse(data=data, safe=False)


    else:
        data = {
            'msg': 'error',
            'code': 500,
        }
        return JsonResponse(data=data, safe=False)

def editEduInfo(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        education = request.GET.get('education')
        major = request.GET.get('major')
        university = request.GET.get('university')

        edu = Education.objects.get(eid=id)
        edu.education = education
        edu.major = major
        edu.university = university
        edu.save()
        data = {
            'msg': 'success',
            'code': 200,
        }
        return JsonResponse(data=data, safe=False)


    else:
        data = {
            'msg': 'error',
            'code': 500,
        }
        return JsonResponse(data=data, safe=False)

def editStudentInfo(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        sid = body['params']['sid']
        sno = body['params']['sno']
        username = body['params']['username']
        age = body['params']['age']
        clazz = body['params']['clazz']
        gender = body['params']['gender']
        phone = body['params']['phone']
        collage = body['params']['collage']
        university = body['params']['university']
        jid= body['params']['jid']
        businessName = body['params']['businessName']
        location = body['params']['location']
        jobName = body['params']['jobName']
        businessType = body['params']['businessType']
        eid= body['params']['eid']
        fuuniversity = body['params']['fuuniversity']
        education = body['params']['education']
        major = body['params']['major']

        if jid != '':
            stu = Student.objects.get(sid=sid)
            stu.sno = sno
            stu.name = username
            stu.age = age
            stu.clazz = clazz
            stu.gender = gender
            stu.phone = phone
            stu.collage = collage
            stu.university = university
            stu.save()
            job = JobInfo.objects.get(id=jid)
            job.businessName = businessName
            job.location = location
            job.jobName = jobName
            job.businessType = businessType
            job.save()

        if eid != '':
            stu = Student.objects.get(sid=sid)
            stu.sno = sno
            stu.name = username
            stu.age = age
            stu.clazz = clazz
            stu.gender = gender
            stu.phone = phone
            stu.collage = collage
            stu.university = university
            stu.save()
            edu = Education.objects.get(eid=eid)
            edu.education = education
            edu.major = major
            edu.university = fuuniversity
            edu.save()

        data = {
            'msg': 'success',
            'code': 200,
        }
        return JsonResponse(data=data, safe=False)
    else:
        data = {
            'msg': 'error',
            'code': 500,
        }
        return JsonResponse(data=data, safe=False)

def removeStu(request):
    if request.method == 'GET':
        sid = request.GET.get('sid')
        jid = request.GET.get('jid')
        eid = request.GET.get('eid')

        if jid != '':
            job = JobInfo.objects.get(id=jid)
            job.delete()

        if eid != '':
            edu = Education.objects.get(eid=eid)
            edu.delete()


        stu = Student.objects.get(sid=sid)
        stu.delete()

        stuJobEdu = StudentJobEducation.objects.get(sid=sid)
        stuJobEdu.delete()

        data = {
            'msg': 'success',
            'code': 200,
        }
        return JsonResponse(data=data, safe=False)


    else:
        data = {
            'msg': 'error',
            'code': 500,
        }
        return JsonResponse(data=data, safe=False)


def removeJobInfo(request):
    if request.method == 'GET':
        sid = request.GET.get('sid')
        jid = request.GET.get('jid')

        job = JobInfo.objects.get(id=jid)
        job.delete()

        stuJobEdu = StudentJobEducation.objects.get(sid=sid)
        stuJobEdu.delete()

        data = {
            'msg': 'success',
            'code': 200,
        }
        return JsonResponse(data=data, safe=False)


    else:
        data = {
            'msg': 'error',
            'code': 500,
        }
        return JsonResponse(data=data, safe=False)


def removeEduInfo(request):
    if request.method == 'GET':
        sid = request.GET.get('sid')
        eid = request.GET.get('eid')

        edu = Education.objects.get(eid=eid)
        edu.delete()

        stuJobEdu = StudentJobEducation.objects.get(sid=sid)
        stuJobEdu.delete()

        data = {
            'msg': 'success',
            'code': 200,
        }
        return JsonResponse(data=data, safe=False)


    else:
        data = {
            'msg': 'error',
            'code': 500,
        }
        return JsonResponse(data=data, safe=False)

def addNotice(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        tid = body['params']['tid']
        title = body['params']['title']
        date1 = body['params']['date1']
        desc = body['params']['desc']

        notice = Notice()
        notice.tid = tid
        notice.title = title
        # notice.pubTime = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        notice.pubTime = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        notice.desc = desc
        notice.save()
        data = {
            'msg': 'success',
            'code': 200,
        }
        return JsonResponse(data=data, safe=False)

    else:
        data = {
            'msg': 'error',
            'code': 500,
        }
        return JsonResponse(data=data, safe=False)

def allNotices(request):
    if request.method == 'GET':
        page = request.GET.get('page')
        pageSize = request.GET.get('pageSize')

        notices = Notice.objects.all()
        count = len(notices)
        # 将数据按照规定每页显示 10 条, 进行分割
        paginator = Paginator(notices, pageSize)
        try:
            notices = paginator.page(page)
            # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            notices = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            notices = paginator.page(paginator.num_pages)

        noticeList = []

        for n in notices:
            noticeList.append({
                'nid': n.nid,
                'pubTime': n.pubTime,
                'title':n.title,
                'desc':n.desc,
                'tid':n.tid,
                'pubPerson': Teacher.objects.get(tid=n.tid).name
            })

        data = {
            'total': count,
            'notices': noticeList
        }

        return JsonResponse(data=data, safe=False)
    else:
        data = {
            'msg': 'error',
            'code': 500,
        }
        return JsonResponse(data=data, safe=False)


def editNotice(request):
    if request.method == 'GET':
        tid = request.GET.get('tid')
        nid = request.GET.get('nid')
        title = request.GET.get('title')
        desc = request.GET.get('desc')

        notice = Notice.objects.get(nid=nid)
        notice.title = title
        notice.desc = desc
        notice.save()
        data = {
            'msg': 'success',
            'code': 200,
        }
        return JsonResponse(data=data, safe=False)
    else:
        data = {
            'msg': 'error',
            'code': 500,
        }
        return JsonResponse(data=data, safe=False)

def removeNotice(request):
    if request.method == 'GET':
        nid = request.GET.get('nid')

        notice = Notice.objects.get(nid=nid)
        notice.delete()
        data = {
            'msg': 'success',
            'code': 200,
        }
        return JsonResponse(data=data, safe=False)
    else:
        data = {
            'msg': 'error',
            'code': 500,
        }
        return JsonResponse(data=data, safe=False)

def getStuNoticeState(request):
    if request.method == 'GET':
        sid = request.GET.get('sid')
        # stuNotices = ReadNotice.objects.filter(sid=sid)
        notices = Notice.objects.all()
        readNotice = []
        notReadNum = 0
        for n in notices:
            parms = {
                'sid': sid,
                'nid': n.nid
            }
            if len(ReadNotice.objects.filter(**parms)) == 0:
                notReadNum+=1
                readNotice.append({
                    'nid': n.nid,
                    'pubTime': n.pubTime,
                    'title': n.title,
                    'desc': n.desc,
                    'tid': n.tid,
                    'pubPerson': Teacher.objects.get(tid=n.tid).name,
                    'state': '0'
                })
            else:
                readNotice.append({
                    'nid': n.nid,
                    'pubTime': n.pubTime,
                    'title': n.title,
                    'desc': n.desc,
                    'tid': n.tid,
                    'pubPerson': Teacher.objects.get(tid=n.tid).name,
                    'state': '1'
                })

        data = {
            'msg': 'success',
            'code': 200,
            'readNotice': readNotice,
            'notReadNum': notReadNum
        }
        return JsonResponse(data=data, safe=False)

    else:
        data = {
            'msg': 'error',
            'code': 500,
        }
        return JsonResponse(data=data, safe=False)

def makeAllNoticeReaded(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        utype = request.GET.get('utype')

        if utype == '1':
            # 判断已读表中没有该数据 防止重复插入
            notices = Notice.objects.all()
            for n in notices:
                parms = {
                    'sid': id,
                    'nid': n.nid
                }
                if len(ReadNotice.objects.filter(**parms)) == 0:
                    note = ReadNotice()
                    note.sid = id
                    note.nid = n.nid
                    note.save()
        data = {
            'msg': 'success',
            'code': 200,
        }
        return JsonResponse(data=data, safe=False)

    else:
        data = {
            'msg': 'error',
            'code': 500,
        }
        return JsonResponse(data=data, safe=False)

def getSutdentInfo(request):
    if request.method == 'GET':
        sid = request.GET.get('sid')

        s = Student.objects.get(sid=sid)
        jid = StudentJobEducation.objects.get(sid=sid).jid
        job = JobInfo.objects.get(id=jid)
        data = {
            'sid': s.sid,
            'sno': s.sno,
            'username': s.name,
            'age': s.age,
            'clazz': s.clazz,
            'gender': s.gender,
            'phone': s.phone,
            'collage': s.collage,
            'university': s.university,
            'businessName': job.businessName,
            'location': job.location,
            'jobName': job.jobName,
            'businessType': job.businessType,
        }
        return JsonResponse(data=data, safe=False)
    else:
        data = {
            'msg': 'error',
            'code': 500,
        }
        return JsonResponse(data=data, safe=False)


def addResume(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        sid= body['params']['sid']
        skill= body['params']['skill']
        evaluate= body['params']['evaluate']
        reward= body['params']['reward']
        name = body['params']['name']
        practice = body['params']['practice']
        resume = Resume()
        resume.skill = skill
        resume.evaluate = evaluate
        resume.reward = reward
        resume.practice = practice
        resume.name = name
        resume.sid = sid
        resume.time = time.strftime('%Y%m%d',time.localtime(time.time()))
        resume.save()
        data = {
            'msg': 'success',
            'code': 200,
        }
        return JsonResponse(data=data, safe=False)

    else:
        data = {
            'msg': 'error',
            'code': 500,
        }
        return JsonResponse(data=data, safe=False)

def allResumes(request):
    if request.method == 'GET':
        page = request.GET.get('page')
        pageSize = request.GET.get('pageSize')
        id = request.GET.get('id')
        name = request.GET.get('name')
        utype = request.GET.get('utype')
        # print(name)
        resumes = []

        # 学生查看自己的简历
        if utype == '1':
            if name != '':
                dic = {
                    'sid': id,
                    'name': name,
                }
                resumes = Resume.objects.filter(**dic)
            else:
                resumes = Resume.objects.filter(sid=id)

            count = len(resumes)
            # 将数据按照规定每页显示 10 条, 进行分割
            paginator = Paginator(resumes, pageSize)
            try:
                notices = paginator.page(page)
                # todo: 注意捕获异常
            except PageNotAnInteger:
                # 如果请求的页数不是整数, 返回第一页。
                notices = paginator.page(1)
            except InvalidPage:
                # 如果请求的页数不存在, 重定向页面
                return HttpResponse('找不到页面的内容')
            except EmptyPage:
                # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
                notices = paginator.page(paginator.num_pages)

            resumeList = []

            for n in resumes:
                resumeList.append({
                    'id': n.id,
                    'pubTime': n.time,
                    'skill': n.skill,
                    'evaluate': n.evaluate,
                    'practice': n.practice,
                    'reward': n.reward,
                    'name': n.name,
                    'sid': n.sid,
                    'pubPerson': Student.objects.get(sid=n.sid).name,
                    'username': Student.objects.get(sid=n.sid).name,
                    'age': Student.objects.get(sid=n.sid).age,
                    'gender': Student.objects.get(sid=n.sid).gender,
                    'phone': Student.objects.get(sid=n.sid).phone,
                    'collage': Student.objects.get(sid=n.sid).collage,
                    'university': Student.objects.get(sid=n.sid).university,
                    'email': Student.objects.get(sid=n.sid).email,
                    'major': Student.objects.get(sid=n.sid).major,
                    # 'jobName':
                })

            data = {
                'total': count,
                'resumes': resumeList
            }

            return JsonResponse(data=data, safe=False)

        else:
            # 企业查看简历
            print('else')
            print(id)
            bid = BusinessPerson.objects.get(id=id).bid
            print(bid)
            bas = BusinessAndStudent.objects.filter(bid=bid)
            for bp in bas:
                # res = Resume.objects.get(sid=bp.rid)
                resumes.append({
                    'id': Resume.objects.get(sid=bp.rid).id,
                    'time': Resume.objects.get(sid=bp.rid).time,
                    'skill': Resume.objects.get(sid=bp.rid).skill,
                    'evaluate': Resume.objects.get(sid=bp.rid).evaluate,
                    'reward': Resume.objects.get(sid=bp.rid).reward,
                    'name': Resume.objects.get(sid=bp.rid).name,
                    'sid': Resume.objects.get(sid=bp.rid).sid,
                    'practice': Resume.objects.get(sid=bp.rid).practice,
                    'jobName': Job.objects.get(jid=bp.jid).jobName,
                })

            count = len(resumes)
            # 将数据按照规定每页显示 10 条, 进行分割
            paginator = Paginator(resumes, pageSize)
            try:
                notices = paginator.page(page)
                # todo: 注意捕获异常
            except PageNotAnInteger:
                # 如果请求的页数不是整数, 返回第一页。
                notices = paginator.page(1)
            except InvalidPage:
                # 如果请求的页数不存在, 重定向页面
                return HttpResponse('找不到页面的内容')
            except EmptyPage:
                # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
                notices = paginator.page(paginator.num_pages)

            resumeList = []
            print(resumes)

            for n in resumes:
                resumeList.append({
                    'id': n.get('id'),
                    'pubTime':n.get('time'),
                    'skill': n.get('skill'),
                    'evaluate': n.get('evaluate'),
                    'reward': n.get('reward'),
                    'name': n.get('name'),
                    'sid': n.get('sid'),
                    'practice': n.get('practice'),
                    'pubPerson': Student.objects.get(sid=n.get('sid')).name,
                    'username': Student.objects.get(sid=n.get('sid')).name,
                    'age': Student.objects.get(sid=n.get('sid')).age,
                    'gender': Student.objects.get(sid=n.get('sid')).gender,
                    'phone': Student.objects.get(sid=n.get('sid')).phone,
                    'collage': Student.objects.get(sid=n.get('sid')).collage,
                    'university': Student.objects.get(sid=n.get('sid')).university,
                    'email': Student.objects.get(sid=n.get('sid')).email,
                    'major': Student.objects.get(sid=n.get('sid')).major,
                    'jobName': n.get('jobName'),
                })

            data = {
                'total': count,
                'resumes': resumeList
            }

            return JsonResponse(data=data, safe=False)




    else:
        data = {
            'msg': 'error',
            'code': 500,
        }
        return JsonResponse(data=data, safe=False)


def editResume(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        skill = request.GET.get('skill')
        evaluate = request.GET.get('evaluate')
        reward = request.GET.get('reward')
        practice = request.GET.get('practice')

        resume = Resume.objects.get(id=id)
        resume.skill = skill
        resume.evaluate = evaluate
        resume.reward = reward
        reward.practice = practice
        resume.save()
        data = {
            'msg': 'success',
            'code': 200,
        }
        return JsonResponse(data=data, safe=False)
    else:
        data = {
            'msg': 'error',
            'code': 500,
        }
        return JsonResponse(data=data, safe=False)

def removeResume(request):
    if request.method == 'GET':
        nid = request.GET.get('id')

        resume = Resume.objects.get(id=nid)
        resume.delete()
        data = {
            'msg': 'success',
            'code': 200,
        }
        return JsonResponse(data=data, safe=False)
    else:
        data = {
            'msg': 'error',
            'code': 500,
        }
        return JsonResponse(data=data, safe=False)

def getBusinessInfo(request):
    if request.method == 'GET':
        id = request.GET.get('id')

        business = Business.objects.get(id=id)

        data = {
            'id': business.id,
            'businessName': business.businessName,
            'businessType': business.businessType,
            'businessPerson': business.businessPerson,
            'location': business.location,
        }
        return JsonResponse(data=data, safe=False)
    else:
        data = {
            'msg': 'error',
            'code': 500,
        }
        return JsonResponse(data=data, safe=False)

def editBusiness(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        businessName = request.GET.get('businessName')
        businessType = request.GET.get('businessType')
        businessPerson = request.GET.get('businessPerson')
        location = request.GET.get('location')

        business = Business.objects.get(id=id)
        business.businessName = businessName
        business.businessType = businessType
        business.businessPerson = businessPerson
        business.location = location
        business.save()
        data = {
            'msg': 'success',
            'code': 200,
        }
        return JsonResponse(data=data, safe=False)
    else:
        data = {
            'msg': 'error',
            'code': 500,
        }
        return JsonResponse(data=data, safe=False)

def sendStudentResume(request):
    if request.method == 'GET':
        bid = request.GET.get('bid')
        jid = request.GET.get('jid')
        sid = request.GET.get('sid')

        bus = BusinessAndStudent()
        bus.bid = bid
        bus.rid = sid
        bus.jid = jid
        bus.save()

        data = {
            'msg': 'success',
            'code': 200,
        }
        return JsonResponse(data=data, safe=False)
    else:
        data = {
            'msg': 'error',
            'code': 500,
        }
        return JsonResponse(data=data, safe=False)



def addCollege(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        collegeName= body['params']['collegeName']
        collegeAdmin= body['params']['collegeAdmin']
        college = College()
        college.collegeName = collegeName
        college.collegeAdmin = collegeAdmin
        college.save()
        data = {
            'msg': 'success',
            'code': 200,
        }
        return JsonResponse(data=data, safe=False)

    else:
        data = {
            'msg': 'error',
            'code': 500,
        }
        return JsonResponse(data=data, safe=False)

def allColleges(request):
    if request.method == 'GET':
        page = request.GET.get('page')
        pageSize = request.GET.get('pageSize')
        # id = request.GET.get('id')
        collegeName = request.GET.get('collegeName')
        collegeAdmin = request.GET.get('collegeAdmin')
        # print(collegeName)
        # print(name)
        colleges = College.objects.all()

        # print(collegeName)

        if len(collegeName) != 0:
            colleges = colleges.filter(collegeName__contains=collegeName)

        if len(collegeAdmin) != 0:
            colleges = colleges.filter(collegeAdmin__contains=collegeAdmin)

        count = len(colleges)
        # 将数据按照规定每页显示 10 条, 进行分割
        paginator = Paginator(colleges, pageSize)
        try:
            notices = paginator.page(page)
            # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            notices = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            notices = paginator.page(paginator.num_pages)

        collegeList = []
        print(colleges)

        for n in colleges:
            collegeList.append({
                'id': n.id,
                'collegeName': n.collegeName,
                'collegeAdmin': n.collegeAdmin
            })

        data = {
            'total': count,
            'colleges': collegeList
        }

        return JsonResponse(data=data, safe=False)
    else:
        data = {
            'msg': 'error',
            'code': 500,
        }
        return JsonResponse(data=data, safe=False)


def editCollege(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        collegeName = request.GET.get('collegeName')
        collegeAdmin = request.GET.get('collegeAdmin')

        college = College.objects.get(id=id)
        college.collegeName = collegeName
        college.collegeAdmin = collegeAdmin
        college.save()
        data = {
            'msg': 'success',
            'code': 200,
        }
        return JsonResponse(data=data, safe=False)
    else:
        data = {
            'msg': 'error',
            'code': 500,
        }
        return JsonResponse(data=data, safe=False)

def removeCollege(request):
    if request.method == 'GET':
        id = request.GET.get('id')

        college = College.objects.get(id=id)
        college.delete()
        data = {
            'msg': 'success',
            'code': 200,
        }
        return JsonResponse(data=data, safe=False)
    else:
        data = {
            'msg': 'error',
            'code': 500,
        }
        return JsonResponse(data=data, safe=False)

def addSubject(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        subjectName= body['params']['subjectName']
        subjectAdmin= body['params']['subjectAdmin']

        subject = Subject()
        subject.subjectName = subjectName
        subject.subjectAdmin = subjectAdmin
        subject.save()
        data = {
            'msg': 'success',
            'code': 200,
        }
        return JsonResponse(data=data, safe=False)

    else:
        data = {
            'msg': 'error',
            'code': 500,
        }
        return JsonResponse(data=data, safe=False)

def allSubjects(request):
    if request.method == 'GET':
        page = request.GET.get('page')
        pageSize = request.GET.get('pageSize')
        # id = request.GET.get('id')
        subjectName = request.GET.get('SubjectName')
        subjectAdmin = request.GET.get('SubjectAdmin')
        # print(SubjectName)
        # print(name)
        subjects = Subject.objects.all()


        if len(subjectName) != 0:
            subjects = subjects.filter(subjectName__contains=subjectName)

        if len(subjectAdmin) != 0:
            subjects = subjects.filter(subjectAdmin__contains=subjectAdmin)

        count = len(subjects)
        # 将数据按照规定每页显示 10 条, 进行分割
        paginator = Paginator(subjects, pageSize)
        try:
            notices = paginator.page(page)
            # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            notices = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            notices = paginator.page(paginator.num_pages)

        subjectList = []
        print(subjects)

        for n in subjects:
            subjectList.append({
                'id': n.id,
                'subjectName': n.subjectName,
                'subjectAdmin': n.subjectAdmin
            })

        data = {
            'total': count,
            'subjects': subjectList
        }

        return JsonResponse(data=data, safe=False)
    else:
        data = {
            'msg': 'error',
            'code': 500,
        }
        return JsonResponse(data=data, safe=False)


def editSubject(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        subjectName = request.GET.get('subjectName')
        subjectAdmin = request.GET.get('subjectAdmin')
        # print(subjectName)
        # print(id)
        subject = Subject.objects.get(id=id)
        subject.subjectName = subjectName
        subject.subjectAdmin = subjectAdmin
        subject.save()
        data = {
            'msg': 'success',
            'code': 200,
        }
        return JsonResponse(data=data, safe=False)
    else:
        data = {
            'msg': 'error',
            'code': 500,
        }
        return JsonResponse(data=data, safe=False)

def removeSubject(request):
    if request.method == 'GET':
        id = request.GET.get('id')

        subject = Subject.objects.get(id=id)
        subject.delete()
        data = {
            'msg': 'success',
            'code': 200,
        }
        return JsonResponse(data=data, safe=False)
    else:
        data = {
            'msg': 'error',
            'code': 500,
        }
        return JsonResponse(data=data, safe=False)

def addBusinessPerson(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        businessName= body['params']['businessName']
        location= body['params']['location']
        businessType = body['params']['businessType']
        uname = body['params']['uname']
        upasswd = body['params']['upasswd']
        name = body['params']['name']
        bno = body['params']['bno']
        phone = body['params']['phone']
        dept = body['params']['dept']
        businessPerson = body['params']['businessPerson']


        business = Business()
        business.businessPerson = businessPerson
        business.businessType = businessType
        business.businessName = businessName
        business.location = location
        business.save()

        bp = BusinessPerson()
        bp.bid = business.id
        bp.name = name
        bp.bno = bno
        bp.phone = phone
        bp.dept = dept
        bp.save()

        user = User()
        user.uname = uname
        user.upasswd = upasswd
        user.utype = '3'
        user.fkno = bp.id
        user.save()

        data = {
            'msg': 'success',
            'code': 200,
        }
        return JsonResponse(data=data, safe=False)

    else:
        data = {
            'msg': 'error',
            'code': 500,
        }
        return JsonResponse(data=data, safe=False)


def getCharts(request):
    if request.method == 'GET':
        id = request.GET.get('id')

        collage = Teacher.objects.get(tid=id).collage

        stus = Student.objects.filter(collage=collage)
        jobNum = 0
        eduNum = 0
        for s in stus:
            tmp = StudentJobEducation.objects.get(sid=s.sid)
            if tmp.jid != None:
                jobNum+=1
            else:
                eduNum+=1

        print(jobNum)
        print(eduNum)

        # 专业统计
        subjects = Subject.objects.filter(subjectAdmin=collage)
        jobMajor = {}
        eduMajor = {}
        subs = []

        for sub in subjects:
            subs.append(sub.subjectName)
            if not sub.subjectName in jobMajor:
                jobMajor[sub.subjectName] = 0
            if not sub.subjectName in eduMajor:
                eduMajor[sub.subjectName] = 0
        print(subjects)
        print(jobMajor)
        print(eduMajor)

        for s in stus:
            tmp = StudentJobEducation.objects.get(sid=s.sid)
            if tmp.jid != None:
                jobMajor[s.major] += 1
            else:
                eduMajor[s.major] += 1

        print(jobMajor)
        print(eduMajor)

        jobMajorList = []
        eduMajorList = []

        for i in jobMajor.values():
            jobMajorList.append(i)

        for i in eduMajor.values():
            eduMajorList.append(i)

        print(jobMajorList)

        print(jobNum)
        print(eduNum)
        data = {
            'jobNum': jobNum,
            'eduNum': eduNum,
            'subjects': subs,
            'jobMajor': jobMajorList,
            'eduMajor': eduMajorList,
            'code': 200,
        }
        return JsonResponse(data=data, safe=False)
    else:
        data = {
            'msg': 'error',
            'code': 500,
        }
        return JsonResponse(data=data, safe=False)

def getAllMajorAndCollege(request):
    if request.method == 'GET':

        subs = Subject.objects.all()
        colleges = College.objects.all()

        subsList = []
        collegesList = []

        for i in subs:
            subsList.append(i.subjectName)

        for i in colleges:
            collegesList.append(i.collegeName)


        data = {
            'subjects': subsList,
            'collegesList': collegesList,
            'msg': 'success',
            'code': 200,
        }
        return JsonResponse(data=data, safe=False)
    else:
        data = {
            'msg': 'error',
            'code': 500,
        }
        return JsonResponse(data=data, safe=False)

from django.db import models

# Create your models here.
class Job(models.Model):
    jid = models.AutoField(primary_key=True)
    businessName = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    jobName = models.CharField(max_length=255)
    businessYear = models.CharField(max_length=255)
    education = models.CharField(max_length=255)
    businessType = models.CharField(max_length=255)
    money = models.CharField(max_length=255)
    pubTime = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    bid = models.IntegerField(null=True)
    class Meta:
        db_table = 'Job'
        ordering = ['jid']

'''
id 学号 姓名 年龄 班级 性别 联系方式 院系
'''
class Student(models.Model):
    sid = models.AutoField(primary_key=True)
    sno = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    clazz = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    collage = models.CharField(max_length=255)
    university = models.CharField(max_length=255)
    major = models.CharField(max_length=255,null=True)
    email = models.CharField(max_length=255,null=True)
    class Meta:
        db_table = 'Student'
        ordering = ['sid']

"""
id 工号 姓名 年龄 班级 学科 院系
"""
class Teacher(models.Model):
    tid = models.AutoField(primary_key=True)
    tno = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    gender = models.CharField(max_length=255,null=True)
    phone = models.CharField(max_length=255,null=True)
    clazz = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    collage = models.CharField(max_length=255)
    university = models.CharField(max_length=255)
    class Meta:
        db_table = 'Teacher'
        ordering = ['tid']

class User(models.Model):
    uid = models.AutoField(primary_key=True)
    uname = models.CharField(max_length=255)
    upasswd = models.CharField(max_length=255)
    utype = models.CharField(max_length=255) # 0 管理员 1 学生 2 老师
    fkno = models.IntegerField()
    class Meta:
        db_table = 'User'
        ordering = ['uid']


class Admin(models.Model):
    aid = models.AutoField(primary_key=True)
    aname = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    collage = models.CharField(max_length=255)
    university = models.CharField(max_length=255)
    class Meta:
        db_table = 'Admin'
        ordering = ['aid']

class Education(models.Model):
    eid = models.AutoField(primary_key=True)
    education = models.CharField(max_length=255)
    major = models.CharField(max_length=255)
    university = models.CharField(max_length=255)
    class Meta:
        db_table = 'Education'
        ordering = ['eid']

class StudentJobEducation(models.Model):
    id = models.AutoField(primary_key=True)
    sid = models.IntegerField(null=True)
    jid = models.IntegerField(null=True)
    eid = models.IntegerField(null=True)
    class Meta:
        db_table = 'StudentJobEducation'
        ordering = ['id']

class JobInfo(models.Model):
    id = models.AutoField(primary_key=True)
    businessName=models.CharField(max_length=255)
    location=models.CharField(max_length=255)
    jobName=models.CharField(max_length=255)
    businessType=models.CharField(max_length=255)
    class Meta:
        db_table = 'JobInfo'
        ordering = ['id']

class Notice(models.Model):
    nid = models.AutoField(primary_key=True)
    pubTime = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    tid = models.IntegerField()

    class Meta:
        db_table = 'Notice'
        ordering = ['nid']

class ReadNotice(models.Model):
    rid = models.AutoField(primary_key=True)
    nid = models.IntegerField()
    sid = models.IntegerField()
    class Meta:
        db_table = 'ReadNotice'
        ordering = ['rid']

class Resume(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(null=True)
    reward = models.TextField()
    skill = models.TextField()
    evaluate = models.TextField()
    practice = models.TextField(null=True)
    sid = models.IntegerField()
    time = models.CharField(max_length=255,null=True)
    class Meta:
        db_table = 'Resume'
        ordering = ['id']

class Business(models.Model):
    id = models.AutoField(primary_key=True)
    businessName = models.CharField(max_length=255)
    businessPerson = models.CharField(max_length=255)
    businessType = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    class Meta:
        db_table = 'Business'
        ordering = ['id']

class BusinessAndStudent(models.Model):
    id = models.AutoField(primary_key=True)
    bid = models.IntegerField()
    rid = models.IntegerField()
    jid = models.IntegerField(null=True)
    class Meta:
        db_table = 'BusinessAndStudent'
        ordering = ['id']

class BusinessPerson(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    bno = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    dept = models.CharField(max_length=255)
    bid = models.IntegerField()

    class Meta:
        db_table = 'BusinessPerson'
        ordering = ['id']

class College(models.Model):
    id = models.AutoField(primary_key=True)
    collegeName = models.CharField(max_length=255)
    collegeAdmin = models.CharField(max_length=255)

    class Meta:
        db_table = 'College'
        ordering = ['id']


class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    subjectName = models.CharField(max_length=255)
    subjectAdmin = models.CharField(max_length=255)

    class Meta:
        db_table = 'Subject'
        ordering = ['id']
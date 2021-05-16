from django.contrib import admin
from django.urls import path,include
from . import views

# urlpatterns = [
#     path("register/",views.register,name = "register"),
#     path("login/",views.login,name = "login"),
#     path("main/",views.main,name = "main"),
#     path("list/",views.GoodsListView.as_view(),name = "list"),
#     path("detail/",views.show_goods_detail,name = "detail"),
#     path("add/",views.add_cart),
#     path("show_cart/",views.show_cart),
#     path("submit_orders/",views.submit_orders),
#     path("logout/",views.logout)
# ]

urlpatterns = [
    # path('hello/',  views.hello),
    path(r'login/',  views.login),
    path(r'allJobs/', views.allJob),
    path(r'getUser/', views.getUser),
    path(r'editUser/',views.editUser),
    path(r'addJob/', views.addJob),
    path(r'removeJob/', views.removeJob),
    path(r'editJob/', views.editJob),
    path(r'allUsers/', views.allUsers),
    path(r'editAuth/', views.editAuth),
    path(r'removeAuth/',views.removeAuth),
    path(r'addAuth/',views.addAuth),
    path(r'allStudents/',views.allStudents),
    path(r'addJobInfo/',views.addJobInfo),
    path(r'addEduInfo/',views.addEduInfo),
    path(r'getOnesJob/',views.getOnesJob),
    path(r'getOnesEdu/',views.getOnesEdu),
    path(r'editJobInfo/',views.editJobInfo),
    path(r'editEduInfo/',views.editEduInfo),
    path(r'editStudentInfo/',views.editStudentInfo),
    path(r'removeStu/',views.removeStu),
    path(r'removeJobInfo/',views.removeJobInfo),
    path(r'removeEduInfo/',views.removeEduInfo),
    path(r'addNotice/', views.addNotice),
    path(r'allNotices/', views.allNotices),
    path(r'editNotice/', views.editNotice),
    path(r'removeNotice/', views.removeNotice),
    path(r'getStuNoticeState/', views.getStuNoticeState),
    path(r'makeAllNoticeReaded/', views.makeAllNoticeReaded),
    path(r'getSutdentInfo/', views.getSutdentInfo),

    path(r'addResume/', views.addResume),
    path(r'allResumes/', views.allResumes),
    path(r'editResume/', views.editResume),
    path(r'removeResume/', views.removeResume),

    path(r'getBusinessInfo/', views.getBusinessInfo),
    path(r'editBusiness/', views.editBusiness),
    path(r'sendStudentResume/', views.sendStudentResume),

    path(r'addCollege/', views.addCollege),
    path(r'allColleges/', views.allColleges),
    path(r'editCollege/', views.editCollege),
    path(r'removeCollege/', views.removeCollege),

    path(r'addSubject/', views.addSubject),
    path(r'allSubjects/', views.allSubjects),
    path(r'editSubject/', views.editSubject),
    path(r'removeSubject/', views.removeSubject),

    path(r'addBusinessPerson/', views.addBusinessPerson),

    path(r'getCharts/', views.getCharts),

    path(r'getAllMajorAndCollege/', views.getAllMajorAndCollege),




]
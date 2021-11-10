import random
import urllib3
import time
import json
import requests
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
# from django.contrib.auth.hashers import make_password, check_password
from . import models
import datetime

# Create your views here.
import hashlib
import logging
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


logger = logging.getLogger('log')


def page_not_found(request, exception):  # 注意点 ①
    return render(request, '404.html')


def page_error(request):
    return render(request, '500.html')


def index(request):
    return render(request, 'index.html')


def home(request):
    """这个是首页文件"""
    return render(request, 'home.html')


def login(request):
    if request.method == 'GET':
        # 用户初次进入展示登录表单
        logger.info("请求登录页面")
        return render(request, 'login.html')
    elif request.method == 'POST':
        content = {
            'message': '123',
        }
        # 用户提交表单
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print(username, password)
        user = models.User.objects.filter(name=username).first()
        if user:
            if _hash_password(password) == user.hash_password:
                # if user.password == password:
                content['message'] = '登录成功'
                # 服务器设置sessionid和其他用户信息。sessionid(服务器给访问他的浏览器的身份证)自动生成的
                request.session['is_login'] = True
                request.session['username'] = username
                request.session['userid'] = user.id
                # 返回的响应中包含set-cookie（sessionid='asda'）
                return redirect('/index/')
            else:
                content['message'] = '密码错误'
                return render(request, 'login.html', context=content)
        else:
            content['message'] = '该用户未注册'
            return render(request, 'login.html', context=content)


def register(request):
    if request.method == 'GET':
        # 注册表表单
        return render(request, 'register.html')
    elif request.method == 'POST':
        # 后端表单验证
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        print(username, password, email)
        # if not (username.strip() and password.strip() and email.strip()):
        #     print("某个字段为空")
        #     return render(request, '/register', context={'message': '某个字段为空'})
        # if len(username)>20 or len(password) >20:
        #     print("用户名和密码过长")
        # redirect('/login/')

        # 写数据库
        user = models.User.objects.filter(email=email).first()
        if user:
            '用户已存在'
            return render(request, 'register.html', context={'message': '用户已注册'})
        hash_password = _hash_password(password)
        try:
            user1 = models.User(name=username, password=password,
                                email=email, hash_password=hash_password)
            user1.save()
            print('保存成功')
            return redirect('/login/')
        except Exception as e:
            print(f'保存失败{e}')
            return redirect('/register/')


def logout(request):
    """登出"""
    # 清除session登出
    request.session.flush()   # 清除此用户session对应的所有sessiondata
    return redirect('/index/')


def _hash_password(password):
    """哈希加密用户注册密码"""
    sha = hashlib.sha256()
    sha.update(password.encode(encoding='utf-8'))
    return sha.hexdigest()


"""
def _hash_password(password):
    哈希加密用户注册密码 加盐版
    salt = ''
    for i in range(4)
        salt +=str(random)
    sha = hashlib.sha256()
    sha.update(password.encode(encoding='utf-8'))
    return sha.hexdigest()
 """

# 查询数据库
# # 相当于 'select * from login_user where name=%s and password=%s' %s(username, password)
# result = models.User.objects.filter(name=username, password=password).first()


x = ''.join(str(random.choice(range(4)))for _ in range(4))
# 虽然课程名称采用4位数随机数，但是依然可能出现重复的课程名称导致建课失败，换个名字前缀即可，名字前缀是由前端穿过来的，当然你也可以把4改成8或者更多
"""必填参数"""

httphost = "http://lol-classes.aixuexi.com/"  # 这个可以决定是线上还是线下环境,当前测试环境
主讲ID = 330  # 主讲ID，自定义
辅导ID = 1028  # 基本用不上，辅导ID是植课植入的
classTypeIds = [127563]  # 150522 钟超有课件  fwr 宛荣的课 班型
diyLessonId = 1127450048
植课名单 = "https://h-ali-test.aixuexi.com/B:1030:K/1616169600/cd91ff4da36e4740bd3c160fdc015fc1.xlsx"  # 接口里面返回的可以自己抓 当前学员 13488883990-13488884008  密码qwer1234 或者123456 机构3202
模板名称 = "植课信息模版.xlsx"  # 名称应该是可以随便填吧
课程售价 = 0  # 单位：元 用于需要购课退费操作的，默认为 0


# courseName = "【测试】-单讲次排班建课" + x  # 课程名称，由前端传进来
liveRoomType = 3  # 直播间类型 1：三分屏，2半身直播，3小组课

课前辅导分钟 = 5  # 单位：分钟 辅导老师的时间，如果需要课前课后辅导，请不要设置为0
课后辅导分钟 = 5

辅导带班数量 = 30    #  决定一个辅导老师能带多少个班
班级人数 = 30       #  班级人数

"""初始化一些信息，如时间格式等，不需要修改，时间部分可以优化一下，懒~~~"""
#*********************************************************************************************************#
now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
s_now = int(time.strftime('%H', time.localtime(time.time())))
e_now = time.strftime('%Y-%m-%d ', time.localtime(time.time()))
当前时间 = e_now + str(s_now) + \
    time.strftime(':%M:%S', time.localtime(time.time()))

timeArray = time.strptime(now, "%Y-%m-%d %H:%M:%S")# 转为时间数组

# 转为时间戳
当前时间戳 = int(time.mktime(timeArray)) * 1000
beginDate = 当前时间戳
UTC时间戳 = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.localtime(time.time()))
年月日 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
print('当前时间:', 当前时间)

now_time = datetime.datetime.now()

# 这里是修复 没有课后辅导的bug
now = datetime.datetime.now()
改变的时间 = datetime.timedelta(seconds=0, minutes=5, hours=0)
当前时间戳加10分钟 = (改变的时间 + now).strftime("%Y-%m-%d %H:%M:%S")
timeArray = time.strptime(当前时间戳加10分钟, "%Y-%m-%d %H:%M:%S")
timeStamp = int(time.mktime(timeArray)) * 1000
print(timeStamp)
#******************************# 这里是修复 没有课后辅导的bug******************#

"""可配置项：# 1分钟 = 6W毫秒  5分钟 = 30W毫秒"""
#   注意时间不能跨天，接口会报错 例如 当前时间 23:59:00 则上课时长不能大于1分钟。
第一讲开课时间戳 = int(当前时间戳) + 120000        # 两分钟后开始上课
第一讲结课时间戳 = 第一讲开课时间戳 + 360000        # 第一节课持续时间 6分钟
第二讲开课时间戳 = 第一讲结课时间戳 + 120000
第二讲结课时间戳 = 第二讲开课时间戳 + 360000
第三讲开课时间戳 = 第二讲结课时间戳 + 120000
第三讲结课时间戳 = 第三讲开课时间戳 + 360000
第四讲开课时间戳 = 第三讲结课时间戳 + 120000
第四讲结课时间戳 = 第四讲开课时间戳 + 360000
第五讲开课时间戳 = 第四讲结课时间戳 + 120000
第五讲结课时间戳 = 第五讲开课时间戳 + 360000
第六讲开课时间戳 = 第五讲结课时间戳 + 120000
第六讲结课时间戳 = 第六讲开课时间戳 + 360000
开始售课时间戳 = 第一讲开课时间戳
结束售课时间戳 = 第五讲结课时间戳 + 900000


def getToken(request):
    """
    登录获取token,默认账号为[张佳]可自己更改\n
    return header\n
    """
    header = {'Content-Type': 'application/json', 'lol-code': 'LOL_CLASSES'}
    data = {"password": "xxxx", "rememberMe": "false",
            "type": "oa", 
            "username": "jNExVlKC1/mYQrg48PsXtS63Sb/BC5CDApySb3HoUkX7PpNeYsPSdLEZFFv+FeS/nHiUdSqKLgIhAOcT4RvvsN+ah9sPqgSw/xO2gtax0YCYt8hAVROCVIiVKuvMjzzcFybMSLAi526xTXKkxwFsmi2VMKEC1+9DDf9VLSf245s="}
    data = json.dumps(data)
    uurl = 'http://lol-user.aixuexi.com/user/auth/login'  # 测试环境
    # uurl = "https://adminzx.aixuexi.com/user/auth/login"  # 线上
    r = requests.post(uurl, data=data, headers=header, verify=False)
    # print(r.text)
    Authorization = r.json()['data']['token']
    sessionId = r.json()['data']['sessionId']
    header['Authorization'] = Authorization
    header['lol'] = sessionId
    print("调用header")
    # return HttpResponse(json.dumps(header,ensure_ascii=False))
    return header


def getCourseId(request, courseName):
    """
    获取 CourseId \n
    couroseName:课程名称\n
    方法:get\n
    return int(courseId)\n
    """
    header = getToken(request)
    # couroseName = "【测试】-单讲次课程无辅导3013"
    httphost = "http://lol-classes.aixuexi.com/"
    url = httphost + "lol/classes/course/list?requestType=1&name=" + courseName
    try:
        req = requests.get(url=url, headers=header)
        js = json.loads(req.text)
    except Exception as e:
        print(str(e))
    else:
        print(js)
        courseId = js['data']['courseList'][0]['id']
        # print("课程ID",courseId)
        # return HttpResponse(json.dumps(courseId,ensure_ascii=False))
        return courseId


def Cuo2Time(request, t):
    """
    时间戳转时间\n
    return Y-m-d H:i:s
    """
    timeStamp = t / 1000
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


def subSH(request, courseId):
    """
    提交审核\n
    方法:get\n
    courseID:课程ID

    """
    headers = getToken(request)
    url = httphost + \
        "lol/classes/course/submitAudit?courseIds=%2C" + str(courseId)
    try:
        req = requests.get(url=url, headers=headers, verify=False)
    except Exception as e:
        print(str(e))
    else:
        logger.info("提交审核完成")
        # print("提交审核完成:", json.loads(req.text)["msg"])
        return {"cood": 0, "msg:": "提交审核完成"}


def shCourse(request, courseId):
    """
    审核课程\n
    方法:get\n
    courseID:课程ID

    """
    headers = getToken(request)
    url = httphost + "lol/classes/course/audit?courseId=" + \
        str(courseId) + "&type=1"
    try:
        req = requests.get(url=url, headers=headers, verify=False)
    except Exception as e:
        print(str(e))
    else:
        logger.info("提交审核完成")
        print("审核完成:", json.loads(req.text)["msg"])
        return {"cood": 0, "msg:": "审核成功"}


def fenBan(request, courseId):
    """
    分班设置\n
    方法:post\n
    courseId:课程ID
    """
    url = httphost + "lol/classes/class/classificationRules/update"
    headers = getToken(request)
    data = {
        "classLimitNum": 班级人数,
        "splitClassNum": 辅导带班数量,
        "splitClassTime": 当前时间戳,
        "courseId": courseId
    }

    try:
        req = requests.post(url=url, headers=headers, json=data, verify=False)
        js = json.loads(req.text)

    except Exception as e:
        print(str(e))
        print("分班失败")
        # sys.exit()
    else:
        logger.info("分班完成")
        print("分班结果:", js["msg"])
        return {"cood": 0, "msg:": "分班成功"}


def addStuden(request, courseId):
    """
    植课\n
    方法:post\n
    courseId:课程ID
    """
    payload = {"requestType": 2, "targetCourseId": courseId,
               "excelUrl": 植课名单, "excelName": 模板名称}
    headers = getToken(request)
    url = httphost + "lol/classes/class/implantPlus"

    try:
        req = requests.post(
            url=url, headers=headers, json=payload, verify=False)
    except Exception as e:
        print(str(e))
        print("添加学员失败")
        logger.error("添加学员失败:", str(e))
    else:
        js = json.loads(req.text)
        logger.info("添加学员成功:", js)
        print("添加学员:", js['msg'])
        return {"cood": 0, "msg:": "植课成功"}


def buildCourse(request):
    """
    建课开始\n
    1、参数内置已经修改\n
    2、大部分可diy的参数已经修改了\n
    3、lessonQuery 中的长度为讲次，有几段就有几个讲次，注意num的value，应该对应上，当前默认为3个讲次\n

    """
    "需要先收集一波前端传过来的数据"
    courseName = request.POST.get('courseName')  # 1
    teacherId = request.POST.get('teacherId')  # 2
    _type = request.POST.get('_type')  # 3
    classTypeIds = request.POST.get('classTypeIds')  # 4
    diyLessonId = int(request.POST.get('diyLessonId'))  # 5
    liveRoomType = request.POST.get('liveRoomType')  # 6
    url = httphost + "lol/classes/course/add"

    headers = getToken(request)
    courseQuery = {
        "id": "",
        "name": courseName,
        "category": 1,  # 直播大班
        "type": _type,  # 1课程类型导流课，2学期同步课
        "liveRoomType": liveRoomType,  # 直播间类型 1：三分屏，2半身直播，3小组课
        "schoolYear": "20-21",  # 学年
        "subjectIds": [1],  # 学科，1数学
        "bookVersionIds": [1],  # 教材版本 1全国版
        "gradeIds": [1],  # 年级 1，一年级
        "teacherIds": [[主讲ID]],  # 教师ID
        "periods": [1],
        "teachingTime": 0,
        "systemId": 1,
        "periodMore": [],
        "periodSingle": [1],
        "teacherDtoList": [],
        "testStatus": 2,
        "classTypeIds": classTypeIds
    }
    courseSyncShowQuery = {
        "1": {
            "headImg": {},
            "detailsImage": {},
            "courseDetailImageList": [],
            "heights": []
        },
        "2": {
            "headImg": {},
            "detailsImage": {},
            "courseDetailImageList": [],
            "heights": []
        },
        "3": {
            "headImg": {},
            "detailsImage": {},
            "courseDetailImageList": [],
            "heights": []
        },
        "headImg": "http://storage.aixuexi.com/u/d2drMFKLf06",
        "detailsImage": "http://storage.aixuexi.com/u/1fDwUFd2836",
        "remind": "温馨提示：脚本创建"
    }
    第一讲次 = {
        "id": "null",
        "classTypeId": classTypeIds,
        "diyLessonId": diyLessonId,
        "name": "第一讲--" + str(x),
                "num": 1,
                "teacherId": teacherId,
                "replaceTeacherId": "",
                "liveRoomType": liveRoomType,
                "beginTime": 第一讲开课时间戳,
                "endTime": 第一讲结课时间戳,
                "startDate": UTC时间戳,
                "beginTimeVal": UTC时间戳,
                "endTimeVal": UTC时间戳,
                "beforeClassTimeVal": 课前辅导分钟,
                "afterClassTimeVal": 课后辅导分钟,
                "beforeClassEndTime": timeStamp,
                "beforeClassStatus": 1,
                "afterClassBeginTime": 第二讲开课时间戳 - 300000,
                "afterClassStatus": 1
    }
    第二讲次 = {
        "id": "null",
        "classTypeId": classTypeIds,
        "diyLessonId": diyLessonId + 1,
        "name": "第二讲--" + str(x),
                "num": 2,
                "teacherId": 主讲ID,
                "replaceTeacherId": "",
                "liveRoomType": liveRoomType,
                "beginTime": 第二讲开课时间戳,
                "endTime": 第二讲结课时间戳,
                "startDate": UTC时间戳,
                "beginTimeVal": UTC时间戳,
                "endTimeVal": UTC时间戳,
                "beforeClassTimeVal": 课前辅导分钟,
                "afterClassTimeVal": 课后辅导分钟,
                "beforeClassEndTime": 第二讲开课时间戳,
                "beforeClassStatus": 1,
                "afterClassBeginTime": 第二讲结课时间戳,
                "afterClassStatus": 1
    }
    第三讲次 = {
        "id": "null",
        "classTypeId": classTypeIds,
        "diyLessonId": diyLessonId + 2,
        "name": "第三讲--" + str(x),
                "num": 3,
                "teacherId": 主讲ID,  # 主讲ID,
                "replaceTeacherId": "",
                "liveRoomType": liveRoomType,
                "beginTime": 第三讲开课时间戳,
                "endTime": 第三讲结课时间戳,
                "startDate": UTC时间戳,
                "beginTimeVal": UTC时间戳,
                "endTimeVal": UTC时间戳,
                "beforeClassTimeVal": 课前辅导分钟,
                "afterClassTimeVal": 课后辅导分钟,
                "beforeClassEndTime": 第三讲开课时间戳,
                "beforeClassStatus": 1,
                "afterClassBeginTime": 第三讲结课时间戳,
                "afterClassStatus": 1
    }
    第四讲次 = {
        "id": "null",
        "classTypeId": classTypeIds,
        "diyLessonId": diyLessonId + 3,
        "name": "第四讲--" + str(x),
                "num": 4,
                "teacherId": 主讲ID,  # 主讲ID,
                "replaceTeacherId": "",
                "liveRoomType": liveRoomType,
                "beginTime": 第四讲开课时间戳,
                "endTime": 第四讲结课时间戳,
                "startDate": UTC时间戳,
                "beginTimeVal": UTC时间戳,
                "endTimeVal": UTC时间戳,
                "beforeClassTimeVal": 课前辅导分钟,
                "afterClassTimeVal": 课后辅导分钟,
                "beforeClassEndTime": 第四讲开课时间戳,
                "beforeClassStatus": 1,
                "afterClassBeginTime": 第四讲结课时间戳,
                "afterClassStatus": 1
    }
    第五讲次 = {
        "id": "null",
        "classTypeId": classTypeIds,
        "diyLessonId": diyLessonId + 4,
        "name": "第五讲--" + str(x),
                "num": 5,
                "teacherId": 主讲ID,  # 主讲ID,
                "replaceTeacherId": "",
                "liveRoomType": liveRoomType,
                "beginTime": 第五讲开课时间戳,
                "endTime": 第五讲结课时间戳,
                "startDate": UTC时间戳,
                "beginTimeVal": UTC时间戳,
                "endTimeVal": UTC时间戳,
                "beforeClassTimeVal": 课前辅导分钟,
                "afterClassTimeVal": 课后辅导分钟,
                "beforeClassEndTime": 第五讲开课时间戳,
                "beforeClassStatus": 1,
                "afterClassBeginTime": 第五讲结课时间戳,
                "afterClassStatus": 1
    }
    第六讲次 = {
        "id": "null",
        "classTypeId": classTypeIds,
        "diyLessonId": diyLessonId + 5,
        "name": "第六讲--" + str(x),
                "num": 6,
                "teacherId": 主讲ID,  # 主讲ID,
                "replaceTeacherId": "",
                "liveRoomType": liveRoomType,
                "beginTime": 第六讲开课时间戳,
                "endTime": 第六讲结课时间戳,
                "startDate": UTC时间戳,
                "beginTimeVal": UTC时间戳,
                "endTimeVal": UTC时间戳,
                "beforeClassTimeVal": 课前辅导分钟,
                "afterClassTimeVal": 课后辅导分钟,
                "beforeClassEndTime": 第六讲开课时间戳,
                "beforeClassStatus": 1,
                "afterClassBeginTime": 第六讲结课时间戳,
                "afterClassStatus": 1
    }
    课程定价 = {
        "saleLimitNum": 100,  # 招生人数
        "fixedPrice": 课程售价,
        "fixedPrice2": 课程售价,
        "fixedPrice3": 课程售价,
        "bsalePrice": 课程售价,
        "bsalePrice2": 课程售价,
        "bsalePrice3": 课程售价,
        "originalPrice": 课程售价,
        "originalPrice2": 课程售价,
        "originalPrice3": 课程售价,
        "saleBeginTime": 开始售课时间戳,
        "saleEndTime": 结束售课时间戳,
        "validBeginTime": "2021-04-15",
        "validEndTime": "2022-04-15",
        "splitClassTime": "",
        "hasBook": 0,
        "materialId": "",
        "rangeDate": [
            "2021-04-15T00:00:00.114Z",
            "2021-12-30T23:359:59.114Z"  # 课程有效期
        ]
    }

    data = {
        "courseQuery": courseQuery,
        "lessonQuery": [
            # 以下段落为讲次配置，例如只留下 第一讲次，注释其他，那么就只会有一个讲次。如果讲次大于1，第二到第六讲次可能出现无课后辅导
            第一讲次,
            # 第二讲次,
            # 第三讲次,
            # 第四讲次,
            # 第五讲次,
            # 第六讲次,
        ],
        "courseSyncShowQuery": courseSyncShowQuery,
        "courseSyncSellQuery": 课程定价,
        "courseDateTemplateQuery": {
            "beginDate": "null",  # 啥也不是，烦死了
            "courseSkipDateListQuery": [],
            "beginTime": "",
            "endTime": "",
            "courseWeekListQuery": [],
            "beforeClassTime": 课前辅导分钟,  # 课前辅导分钟,
            "afterClassTime": 课后辅导分钟,  # 课后辅导分钟
        }
    }

    req = requests.post(url=url, headers=headers, json=data)
    js = json.loads(req.text)

    print(js['msg'])
    print("课程名称:", courseName)
    courseId = getCourseId(request, courseName)
    print("课程ID:", courseId)
    print('主讲ID', str(主讲ID))

    print("课前辅导分钟:", 课前辅导分钟)
    print("课后辅导分钟:", 课后辅导分钟)

    print("第一节课：", Cuo2Time(request, 第一讲开课时间戳), Cuo2Time(request, 第一讲结课时间戳))
    print("第二节课：", Cuo2Time(request, 第二讲开课时间戳), Cuo2Time(request, 第二讲结课时间戳))
    print("第三节课：", Cuo2Time(request, 第三讲开课时间戳), Cuo2Time(request, 第三讲结课时间戳))
    print("第四节课：", Cuo2Time(request, 第四讲开课时间戳), Cuo2Time(request, 第四讲结课时间戳))
    print("第五节课：", Cuo2Time(request, 第五讲开课时间戳), Cuo2Time(request, 第五讲结课时间戳))
    print("第六节课：", Cuo2Time(request, 第六讲开课时间戳), Cuo2Time(request, 第六讲结课时间戳))

    subSH(request, courseId)    #提审
    shCourse(request, courseId) #审核
    fenBan(request, courseId)   #分班
    print(addStuden(request, courseId)) #添加学生
    # context = {}
    datas = {}  #自定义返回接口内容
    datas = {"msg": js['msg'], "courseName": courseName, "courseId": courseId, "主讲ID": 主讲ID, "辅导时间": 课前辅导分钟, "第一讲开课时间": Cuo2Time(
        request, 第一讲开课时间戳), "第一讲结课时间": Cuo2Time(request, 第一讲结课时间戳), "liveRoomType": liveRoomType, "classTypeIds": classTypeIds, "diyLessonId": diyLessonId, "code": 0}
    logger.info(datas)  # 日志
    return JsonResponse(datas)  #django 支持的返回json类型

    # return HttpResponse(json.dumps(datas,ensure_ascii=False))
    # return render(request,json.dumps(datas))


def test(request):
    """测试返回post响应数据"""
    courseName = request.POST.get('courseName')
    teacherId = request.POST.get('teacherId')
    startTime = request.POST.get('startTime')
    addStu = request.POST.get('addStu')
    data = {"code": 0, "msg": "sucess", "sucess": True, "data": {
        "courseName": courseName, "teacherId": teacherId, "startTime": startTime, "addStu": addStu}}
    # return render(request,"test.html",{"data":json.dumps(data)})
    return JsonResponse(data)
    # return HttpResponse(json.dumps(data,ensure_ascii=False))


def addCourse(request):
    """
    添加一个建课的页面
    课程名字，主讲ID，开课时间，等等
    """

    return render(request, "addCourse.html")

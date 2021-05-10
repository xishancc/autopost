# coding=utf-8
import time

import requests


def data(schoolcode, UA, cook):
    """获取处理后的数据
    :param schoolcode:学号编码
    :param UA:传入的UA
    :param cook:传入的cookie
    :return : 昨天/上一次的打卡数据
    """
    # 只需要得到cookie即可获取信息
    # 获取 昨天/最新 的打卡信息
    url1 = 'https://yq.weishao.com.cn/api/questionnaire/questionnaire/getQuestionNaireList?sch_code=' + schoolcode + '&stu_code=2020211760&authorityid=0&type=3&pagenum=1&pagesize=1000&stu_range=999&searchkey='
    head = {
        'Host': 'yq.weishao.com.cn',
        'User-Agent': UA,
        'Accept': '*/*',
        'Referer': 'https://yq.weishao.com.cn/questionnaire/my/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN, zh;q = 0.9',
        'Cookie': cook,
    }
    info = requests.get(url1, headers=head).json().get("data")[0]
    if info.get("createtime") == time.strftime("%Y-%m-%d"):
        return 0
    private = info['private_id']
    activityid = str(info["activityid"])
    url2 = 'https://yq.weishao.com.cn/api/questionnaire/questionnaire/getQuestionDetail?sch_code=chzu&stu_code=2020211760&activityid=' + activityid + '&can_repeat=1&page_from=my&private_id=' + private
    # data里面存放着最新的的打卡记录
    data = requests.get(url2, headers=head).json().get("data")
    true = data.get('already_answered')  # 存放true
    false = data.get("can_reanswer")  # 存放false
    data = data.get("question_list")
    # 但服务器返回的数据并不是真正提交的数据，需要处理
    # 下面开始处理昨天的记录
    # questions记录全部（包括未填写
    questions = []
    # questionsok记录昨天填写的题目
    questionsok = []
    type1 = []
    type2 = []
    type4 = []
    type10 = []
    type11 = []
    type12 = []
    type13 = []
    type14 = []
    type15 = []
    type16 = []
    type22 = []

    for i in range(len(data)):
        # 1：选择题    1:定位
        # 3：填空题。   2～14，16:选择
        # 7：定位。     15，22填空
        # 8：填空题（不在校，所在省市）
        # 9：滑动选择题（返回时间）
        num = data[i].get("question_type")
        if num == 1:
            type1.append(data[i])
        elif num == 2:
            type3.append(data[i])
        elif num == 4:
            type4.append(data[i])
        elif num == 10:
            type7.append(data[i])
        elif num == 11:
            type8.append(data[i])
        elif num == 12:
            type9.append(data[i])
        elif num == 13:
            type7.append(data[i])
        elif num == 14:
            type7.append(data[i])
        elif num == 15:
            type7.append(data[i])
        elif num == 16:
            type7.append(data[i])
        elif num == 22:
            type7.append(data[i])

    def ques():
        return {
            "questionid": '0',
            "optionid": 0,
            "optiontitle": 0,
            "question_sort": 0,
            "question_type": 1,
            "option_sort": 0,
            "range_value": "",
            "content": "",
            "isotheroption": 0,
            "otheroption_content": "",
            "isanswered": "",
            "answerid": 0,
            "hide": false,
            "answered": ''
        }

    for i in range(len(type1)):
        que = ques()
        opt = type1[i].get("option_list")

        if str(type1[i].get("user_answer_this_question")) == 'False':
            que['questionid'] = type1[i].get("questionid")
            que["question_type"] = type1[i].get("question_type")

        else:
            for ii in range(len(opt)):
                if str(opt[ii].get("optionid")) == type1[i].get("user_answer_optionid"):
                    que['questionid'] = opt[ii].get("questionid")
                    que["optionid"] = opt[ii].get("optionid")
                    que['optiontitle'] = opt[ii].get("title")
                    que["question_type"] = type1[i].get("question_type")
                    break
        que["answered"] = type1[i].get("user_answer_this_question")
        if que["answered"] == false:
            que["hide"] = true
        questions.append(que)

    for i in range(len(type2)):
        que = ques()
        que['questionid'] = type2[i].get("questionid")
        que['question_type'] = type2[i].get("question_type")
        que['content'] = type2[i].get("user_answer_content")
        que["answered"] = type2[i].get("user_answer_this_question")
        que["hide"] = true
        questions.append(que)

    for i in range(len(type4)):
        que = ques()
        que['questionid'] = type4[i].get("questionid")
        que['question_type'] = type4[i].get("question_type")
        que['content'] = type4[i].get("user_answer_content")
        que["answered"] = type4[i].get("user_answer_this_question")
        if que["answered"] == false:
            que["hide"] = true
        questions.append(que)

    for i in range(len(type10)):
        que = ques()
        que['questionid'] = type10[i].get("questionid")
        que['content'] = type10[i].get("user_answer_content")
        que['question_type'] = type10[i].get("question_type")
        que["answered"] = type10[i].get("user_answer_this_question")
        questions.append(que)

    for i in range(len(type11)):
        que = ques()
        que['questionid'] = type11[i].get("questionid")
        que['content'] = type11[i].get("user_answer_content")
        que['question_type'] = type11[i].get("question_type")
        que['answered'] = type11[i].get("user_answer_this_question")
        que["hide"] = true
        questions.append(que)

    for i in range(len(type12)):
        que = ques()
        que['questionid'] = type12[i].get("questionid")
        que['question_type'] = type12[i].get("question_type")
        que['content'] = type12[i].get("user_answer_content")
        que['answered'] = type12[i].get("user_answer_this_question")
        que["hide"] = true
        questions.append(que)

    for i in range(len(type13)):
        que = ques()
        que['questionid'] = type13[i].get("questionid")
        que['question_type'] = type13[i].get("question_type")
        que['content'] = type13[i].get("user_answer_content")
        que["answered"] = type13[i].get("user_answer_this_question")
        que["hide"] = true
        questions.append(que)
        
    for i in range(len(type14)):
        que = ques()
        que['questionid'] = type14[i].get("questionid")
        que['question_type'] = type14[i].get("question_type")
        que['content'] = type14[i].get("user_answer_content")
        que["answered"] = type14[i].get("user_answer_this_question")
        que["hide"] = true
        questions.append(que)
        
    for i in range(len(type15)):
        que = ques()
        que['questionid'] = type15[i].get("questionid")
        que['question_type'] = type15[i].get("question_type")
        que['content'] = type15[i].get("user_answer_content")
        que["answered"] = type15[i].get("user_answer_this_question")
        que["hide"] = true
        questions.append(que)
        
    for i in range(len(type16)):
        que = ques()
        que['questionid'] = type16[i].get("questionid")
        que['question_type'] = type16[i].get("question_type")
        que['content'] = type16[i].get("user_answer_content")
        que["answered"] = type16[i].get("user_answer_this_question")
        que["hide"] = true
        questions.append(que)
        
    for i in range(len(type22)):
        que = ques()
        que['questionid'] = type22[i].get("questionid")
        que['question_type'] = type22[i].get("question_type")
        que['content'] = type22[i].get("user_answer_content")
        que["answered"] = type22[i].get("user_answer_this_question")
        que["hide"] = true
        questions.append(que)
        
    # 选择排序法
    for i in range(len(questions) - 1):
        n = i
        for j in range(i + 1, len(questions)):
            if int(questions[n].get('questionid')) > int(questions[j].get("questionid")):
                n = j
        temp = questions[n]
        questions[n] = questions[i]
        questions[i] = temp

    for i in range(len(questions)):
        if questions[i].get("questionid") == 61838:
            del questions[i]["hide"]
        if str(questions[i].get('answered')) == "True":
            questions[i]["isanswered"] = true
            questionsok.append(questions[i])

    head4 = {
        'Host': 'yq.weishao.com.cn',
        'User-Agent': UA,
        'Accept': '*/*',
        'Referer': 'https://yq.weishao.com.cn/questionnaire',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN, zh;q = 0.9',
        'Cookie': cook,
    }
    userinfo = requests.get("https://yq.weishao.com.cn/userInfo", headers=head4).json().get("data")
    return {
        "sch_code": userinfo.get("schcode"),
        "stu_code": userinfo.get("stucode"),
        "stu_name": userinfo.get("username"),
        "identity": userinfo.get("identity"),
        "path": userinfo.get("path"),
        "organization": userinfo.get("organization"),
        "gender": userinfo.get("gender"),
        "activityid": activityid,
        "anonymous": 0,
        "canrepeat": 1,
        "repeat_range": 1,
        "question_data": questionsok,
        "totalArr": questions,
        "private_id": 0
    }

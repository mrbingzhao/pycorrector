#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   CorrectServer.py
@Describe :  
@Contact :   mrbingzhao@qq.com
@License :   (C)Copyright 2023/6/16, Liugroup-NLPR-CASIA

@Modify Time        @Author       @Version    @Desciption
----------------   -----------   ---------    -----------
2023/6/16 上午9:36   liubingzhao      1.0           ml
'''

from flask import Flask,request,jsonify
from flasgger import Swagger
import configparser

import logging,json

from pycorrector.macbert import macbert_corrector
from pycorrector import ConfusionCorrector, Corrector

app = Flask(__name__)
config = configparser.ConfigParser()
app.config.from_object(config)

swagger_config = Swagger.DEFAULT_CONFIG
swagger_config['title'] = "纠错API"
Swagger(app, config=swagger_config)

@app.route('/ml/correct/sentences', methods=['POST'])
def correctTxt():
    """
        句子纠错
        ---
        tags:
          - 句子纠错接口
        description:
            句子纠错接口，json格式
        consumes:
          - application/json
          - text/plain
        parameters:
          - name: body
            in: body
            required: true
            schema:
              id: 内容序号
              required:
                - data
              properties:
                data:
                    type: array
                    example: [
                            {
                              "content": "戴高乐注重经济发展，对制造业进行重点扶持，在高铁、核电、航人航空等高端制造业带动下，很快实现经济的腾飞。",
                              "id": "20323"
                            },{
                              "id": "20326",
                              "content":"机七学习是人工智能领遇最能体现智能的一个分知。中国人民都很支持国产心片的发展。"
                            },{
                              "id": "20327",
                              "content":"中国人民都很支持国产心片的发展。"
                            },{
                              "id": "20328",
                              "content":"美国专家劝中国不要执迷不否：若继续研发芯片，将直面经济伟机播报文章。"
                            }]
                    description: 待纠错文本内容
        responses:
            200:
                description: 成功
                example: {"status":1,"message":"请求成功","data":[{}]}
            406:
                description: 参数有误等
        """
    resData = []
    try:
        # reqData = json.loads(request.get_json())
        reqData = request.get_json()
        logging.info("RCV: ==>"+str(reqData))
        maxlen = 128
        for text in reqData['data']:
            content = {}
            if 'id' in text:
                content["id"] = text['id']
            # 单条待处理文本内容
            single_text = text['content']
            logging.info("confusion correct: ==>" + single_text)
            m = ConfusionCorrector(custom_confusion_path_or_dict='./my_custom_confusion.txt')
            single_text,single_text_err = m.confusion_correct(single_text)
            logging.info("confusion correct: ==>" + single_text + "; err:" +str(single_text_err))
            correctText, errText = bertCorrector.macbert_correct(single_text,maxlen=maxlen)
            errText.extend(single_text_err)
            content["content"] = correctText
            content['err'] = errText
            logging.info("Comput value: ==>" + str(errText))
            resData.append(content)
        response = {}
        response["status"] = Status.SUCCESS.value
        response["message"] = message=Status.SUCCESS_MSG.value
        response["data"] = resData
        resData = json.dumps(response,ensure_ascii=False)
        # return jsonify(status=Status.SUCCESS.value, message=Status.SUCCESS_MSG.value, data=resData)
        logging.info("SND value: ==>" + str(resData))
        return resData
    except Exception as e:
        logging.error(e)
        return jsonify(status=Status.FAILER.value, message=Status.FAILER_MSG.value)

@app.route('/ml/correct/text', methods=['POST'])
def correctTxts():
    """
        句子纠错
        ---
        tags:
          - 句子纠错接口
        description:
            句子纠错接口，json格式
        parameters:
          - name: body
            in: body
            required: true
            schema:
              id: 内容序号
              required:
                - data
              properties:
                data:
                    type: array
                    example: [{
                              "content": "机七学习是人工智能领遇最能体现智能的一个分知。我国的劳动任民非常的勤恳，愿意为了祖国的发展而付出努力。在日复一日的操劳之下，终于收获了最为美好的结果。现在比较可惜的是，人民币目前在国际化的发展道路之中遇到了瓶颈，所以我们目前还不能太早的庆祝。戴高乐注重经记发展，对制造业进行重点扶持，在高铁、核电、航人航空等高端制造业带动下，很快实现经济的腾飞。机七学习是人工智能领遇最能体现智能的一个分知。中国人民都很支持国产心片的发展。中国人民都很支持国产心片的发展。美国专家劝中国不要执迷不否：若继续研发芯片，将直面经济伟机播报文章.",
                              "id": "20323"
                            },{
                              "id": "20326",
                              "content":"机七学习是人工智能领遇最能体现智能的一个分知。中国人民都很支持国产心片的发展。"
                            }]
                    description: 待纠错文本内容
        responses:
            200:
                description: 成功
                example: {"status":1,"message":"请求成功","data":[{}]}
            406:
                description: 参数有误等
        """
    resData = []
    try:
        # reqData = json.loads(request.get_json())
        reqData = request.get_json()
        logging.info("RCV: ==>"+str(reqData))
        maxlen = 256
        for text in reqData['data']:
            content = {}
            if 'id' in text:
                content["id"] = text['id']
            #单条待处理文本内容
            single_text = text['content']
            m = ConfusionCorrector(custom_confusion_path_or_dict='./my_custom_confusion.txt')
            single_text, single_text_err = m.confusion_correct(single_text)
            logging.info("confusion correct: ==>" + single_text)
            #把长文本内容进行切分
            centences = centencesSplit(single_text,maxlen=maxlen)
            # 返回纠错后的全部文本内容
            correctTextAll = ""
            # 返回全部错误的文本位置
            errTextAll = []
            # 记录已处理的文本长度
            processed_length = 0
            for centence in centences:
                #单条切分后的文本纠错
                logging.info("centence value: ==>" + centence)
                correctText, errText = bertCorrector.macbert_correct(centence,maxlen=maxlen)
                errText.extend(single_text_err)
                logging.info("correctText value: ==>" + str(correctText))
                logging.info("errText value: ==>" + str(errText))
                correctTextAll += correctText
                # 更新错误位置信息的起始索引和结束索引
                updated_errText = []
                for err in errText:
                    updated_error = list(err)
                    updated_error[2] += processed_length
                    updated_error[3] += processed_length
                    updated_errText.append(tuple(updated_error))
                # 将错误位置信息添加到结果中
                errTextAll.extend(updated_errText)
                errTextAll.extend(single_text_err)
                processed_length += len(centence)
            content["content"] = correctTextAll
            content['err'] = errTextAll
            logging.info("Comput correctTextAll value: ==>" + str(correctTextAll))
            logging.info("Comput errTextAll value: ==>" + str(errTextAll))
            resData.append(content)
        response = {}
        response["status"] = Status.SUCCESS.value
        response["message"] = message=Status.SUCCESS_MSG.value
        response["data"] = resData
        resData = json.dumps(response,ensure_ascii=False)
        # return jsonify(status=Status.SUCCESS.value, message=Status.SUCCESS_MSG.value, data=resData)
        logging.info("SND value: ==>" + str(resData))
        return resData
    except Exception as e:
        logging.error(e)
        import traceback
        traceback.print_exc()
        return jsonify(status=Status.FAILER.value, message=Status.FAILER_MSG.value)

def centencesSplit(text,maxlen=128):
    import re
    # 待分割的文本
    # text = "机七学习是人工智能领遇最能体现智能的一个分知。我国的劳动任民非常的勤恳，愿意为了祖国的发展而付出努力。在日复一日的操劳之下，终于收获了最为美好的结果。现在比较可惜的是，人民币目前在国际化的发展道路之中遇到了瓶颈，所以我们目前还不能太早的庆祝。戴高乐注重经记发展，对制造业进行重点扶持，在高铁、核电、航人航空等高端制造业带动下，很快实现经济的腾飞。机七学习是人工智能领遇最能体现智能的一个分知。中国人民都很支持国产心片的发展。中国人民都很支持国产心片的发展。美国专家劝中国不要执迷不否：若继续研发芯片，将直面经济伟机播报文章."

    # 使用正则表达式按句号、问号、感叹号以及半角标点、省略号、4个及以上空格作为句子分隔符进行分割，保留标点符号
    sentences = re.split(r'(?<=[。？！.!])|\n+|\s{4,}', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    # 切分过长的句子
    new_sentences = []
    for s in sentences:
        if len(s) <= maxlen:
            new_sentences.append(s)
        else:
            # 处理特别长的句子
            if len(s) > maxlen:
                sub_sentences = re.findall(r'.{1,%d}' % maxlen, s)
                sub_sentences = [sub_s.strip() for sub_s in sub_sentences if sub_s.strip()]

            new_sentences.extend(sub_sentences)

    return new_sentences

from enum import Enum

class Status(Enum):
    SUCCESS = 1
    FAILER = 2
    SUCCESS_MSG = "请求成功"
    FAILER_MSG = "请求失败"


def logConfig():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='server.log',
                        filemode='w')

    # 定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

if __name__ == '__main__':
    logConfig()
    bertCorrector = macbert_corrector.MacBertCorrector()
    ## 默认访问apidocs地址可以查看数据接口说明
    app.run(host="0.0.0.0", port=9080, debug=True)

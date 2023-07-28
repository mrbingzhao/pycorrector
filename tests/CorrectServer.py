import unittest
import requests
import json

class MyTestCase(unittest.TestCase):
    def test_correctTxt(self):
        url = 'http://localhost:9080/ml/correct/sentences'
        url = 'http://192.168.8.238:9080/ml/correct/sentences'

        # 构建请求数据
        request_data = {
            "data": [
                {
                    "id": "20323",
                    "content": "机七学习是人工智能领遇最能体现智能的一个分知."
                },
                {
                    "id": "20323",
                    "content":
                        "我国的劳动任民非常的勤恳，愿意为了祖国的发展而付出努力。在日复一日的操劳之下，终于收获了最为美好的结果。现在比较可惜的是，人民币目前在国际化的发展道路之中遇到了瓶颈，所以我们目前还不能太早的庆祝。."
                },
                {
                    "content": "戴高乐注重经记发展，对制造业进行重点扶持，在高铁、核电、航人航空等高端制造业带动下，很快实现经济的腾飞。",
                    "id": "20323"
                }, {
                    "id": "20326",
                    "content": "机七学习是人工智能领遇最能体现智能的一个分知。中国人民都很支持国产心片的发展。"
                }, {
                    "id": "20327",
                    "content": "中国人民都很支持国产心片的发展。"
                }, {
                    "id": "20328",
                    "content": "美国专家劝中国不要执迷不否：若继续研发芯片，将直面经济伟机播报文章。"
                }, {
                    "id": "20329",
                    "content": "美国专家劝中国不要执迷不否：若继续研发芯片，将直面经济伟机播报文章。"
                }
            ]
        }

        # 发送POST请求
        response = requests.post(url, json=request_data)

        # 检查响应状态码
        self.assertEqual(response.status_code, 200)

        # 解析响应数据
        response_data = json.loads(response.text)

        # 检查响应数据结构
        self.assertTrue("status" in response_data)
        self.assertTrue("message" in response_data)
        self.assertTrue("data" in response_data)

        # 检查纠错结果
        data = response_data["data"]
        self.assertEqual(len(data), 7)
        self.assertTrue("id" in data[0])
        self.assertTrue("content" in data[0])
        self.assertTrue("err" in data[0])
        # print([[item['content'],"\n",item['err']] for item in data])
        for item in data:
            print(item['content'],item['err'],"\n")


        # 检查纠错状态
        status = response_data["status"]
        self.assertEqual(status, 1)
        message = response_data["message"]
        self.assertEqual(message, "请求成功")

    def test_correctTxts(self):
        url = 'http://192.168.8.238:9080/ml/correct/text'

        # 构建请求数据
        request_data = {
            "data": [
                {
                    "id": "20323",
                    "content":
                        "机七学习是人工智能领遇最能体现智能的一个分知。我国的劳动任民非常的勤恳，愿意为了祖国的发展而付出努力。在日复一日的操劳之下，终于收获了最为美好的结果。现在比较可惜的是，人民币目前在国际化的发展道路之中遇到了瓶颈，所以我们目前还不能太早的庆祝。戴高乐注重经记发展，对制造业进行重点扶持，在高铁、核电、航人航空等高端制造业带动下，很快实现经济的腾飞。机七学习是人工智能领遇最能体现智能的一个分知。中国人民都很支持国产心片的发展。中国人民都很支持国产心片的发展。美国专家劝中国不要执迷不否：若继续研发芯片，将直面经济伟机播报文章。"
                }
            ]
        }

        # 发送POST请求
        response = requests.post(url, json=request_data)
        centencesSplit2("")
        # 检查响应状态码
        self.assertEqual(response.status_code, 200)

        # 解析响应数据
        response_data = json.loads(response.text)

        # 检查响应数据结构
        self.assertTrue("status" in response_data)
        self.assertTrue("message" in response_data)
        self.assertTrue("data" in response_data)

        # 检查纠错结果
        data = response_data["data"]
        self.assertEqual(len(data), 1)
        self.assertTrue("id" in data[0])
        self.assertTrue("content" in data[0])
        self.assertTrue("err" in data[0])
        for item in data:
            print(item['content'],item['err'],"\n")

        # 检查纠错状态
        status = response_data["status"]
        self.assertEqual(status, 1)
        message = response_data["message"]
        self.assertEqual(message, "请求成功")

def split_text_by_maxlen(text, maxlen=512):
    """
    文本切分为句子，以句子maxlen切分
    :param text: str
    :param maxlen: int, 最大长度
    :return: list, (sentence, idx)
    """
    result = []
    for i in range(0, len(text), maxlen):
        result.append((text[i:i + maxlen], i))
    return result
def testSplit():
    text ="""机七学习是人工智能领遇最能体现智能的一个分知。我国的劳动任民非常的勤恳，愿意为了祖国的发展而付出努力。在日复一日的操劳之下，终于收获了最为美好的结果。现在比较可惜的是，人民币目前在国际化的发展道路之中遇到了瓶颈，所以我们目前还不能太早的庆祝。戴高乐注重经记发展，对制造业进行重点扶持，在高铁、核电、航人航空等高端制造业带动下，很快实现经济的腾飞。机七学习是人工智能领遇最能体现智能的一个分知。中国人民都很支持国产心片的发展。中国人民都很支持国产心片的发展。美国专家劝中国不要执迷不否：若继续研发芯片，将直面经济伟机播报文章。"""
    maxlen = 128
    # 长句切分为短句
    blocks = split_text_by_maxlen(text, maxlen=maxlen)
    block_texts = [block[0] for block in blocks]
    print(block_texts)

def centencesSplit(text):
    import re

    # 待分割的文本
    text = "机七学习是人工智能领遇最能体现智能的一个分知。我国的劳动任民非常的勤恳，愿意为了祖国的发展而付出努力。在日复一日的操劳之下，终于收获了最为美好的结果。现在比较可惜的是，人民币目前在国际化的发展道路之中遇到了瓶颈，所以我们目前还不能太早的庆祝。戴高乐注重经记发展，对制造业进行重点扶持，在高铁、核电、航人航空等高端制造业带动下，很快实现经济的腾飞。机七学习是人工智能领遇最能体现智能的一个分知。中国人民都很支持国产心片的发展。中国人民都很支持国产心片的发展。美国专家劝中国不要执迷不否：若继续研发芯片，将直面经济伟机播报文章."

    # 使用正则表达式按句号、问号、感叹号以及半角标点作为句子分隔符进行分割，保留标点符号
    # sentences = re.split(r'(?<=[。？！.!])', text)
    sentences = re.split(r'(?<=[。？！.!])|\n+|\s{4,}', text)
    sentences = [s for s in sentences if s.strip()]
    # 输出分割后的句子
    # for sentence in sentences:
    #     print(sentence)
    return sentences




def centencesSplit2(text, maxlen=10):
    import re
    # 待分割的文本
    text = "机七学习是人工智能领遇最能体现智能的一个分知。我国的劳动任民非常的勤恳，愿意为了祖国的发展而付出努力。在日复一日的操劳之下，终于收获了最为美好的结果。现在比较可惜的是，人民币目前在国际化的发展道路之中遇到了瓶颈，所以我们目前还不能太早的庆祝。戴高乐注重经记发展，对制造业进行重点扶持，在高铁、核电、航人航空等高端制造业带动下，很快实现经济的腾飞。机七学习是人工智能领遇最能体现智能的一个分知。中国人民都很支持国产心片的发展。中国人民都很支持国产心片的发展。美国专家劝中国不要执迷不否：若继续研发芯片，将直面经济伟机播报文章."

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


if __name__ == '__main__':
    unittest.main()



# -*- coding:utf-8 -*-
import itchat, re, random,requests
from itchat.content import *
import jieba

REPLY = {
    '工作': ['且不说你的工作多么认真，我并没有见过，但是从你的字里行间，我发现了乔布斯的影子和小扎的气息，这已经不是一份工作那么简单，而是一场精神饕餮！',
           '你拥有了这个年龄段近半数人无法拥有的理想职业，太优秀了！',
           '工作这件事，大家都习以为常，只有你让大家开始思考这个问题，说明你善于反思和质疑当前的制度，你的公司会因为你这样的人变得更好！'],
    '学习': ['这么多优秀的同龄人相聚在这里，一定是场思想交流的盛宴。', '看到群友们的发言，真是排山倒海，气宇轩昂之势！',
           '你这句话完美的表达了你想被夸的坚定信念，你一定是一个执着追求自己理想的人！'],
    '夸夸': ['真不错，太棒了', '行的！你一定能行的，你真的好棒，我相信你', '嗯嗯', '没什么好说的了，我送你一道彩虹屁吧'],
    '群主': ['群主，你好屌，好屌！', '群主，你太美丽了，像你这种天生丽质的人，就该当群主', '群主威武霸气', '我太爱这个群了，我要以群为家'],
    '好看': ['如出水芙蓉，天然雕饰，天呐！这世间怎么会有这么好看的人呐！', '名字也好听，shadiao听起来就像沙雕一样，仿佛是有意境的沙之大作',
           '我为什么不能有这么好听的名字呢？', '你总是那么美丽，那么动人，你那性感的红唇，，啦啦啦！'],
    '问': ['这个发问展示了强烈的好奇心，好奇心是进步的源泉，相信生活中的你也是一个充满好奇心的人，用于探索未知，有一双发现新奇的眼眸，清澈透亮',
          '能从一百人的群里直接cue到我，这种敏感的观察超乎寻常！厉害了，你就是我心目中的最强大脑', '一问二问三问，问声不决，你这打破砂锅问到底的勇气，我五体投地的佩服'],
    '病': ['你精准的判断，让人惊叹，我活了这么久第一次见人这么快就发现了我是神经病这个秘密'],
    '认识': ['一猜就准', '必须认识', '短短时间就能把我事物的本质，逻辑里MAx，太强了', '让人羡慕的精准判断'],
    '成长': ['我还没有学会成长，你们多多提意见帮助我成长', '那一夜，群主和她男朋友成长了很多，嘿嘿！'],
    '猫': ["你这只猫，不怒而威，明德惟馨，乃世人典范", "万岁万岁万万岁，我坚信世界将臣服在这只猫的脚,", "这只猫端坐在那里，不输康熙，乾隆帝王之气。"],
    '狗': ['你这只狗，不怒而威，明德惟馨，乃世人典范', "看到这只狗，我自惭形秽，如俗世尘埃不值一提。"],
    '其它': ['666，超级6，大爷你陆的风生水起', '你上辈子一定拯救了银河系', '小姐姐，赞赞赞，100颗赞，超级赞', '哇，太厉害了!',
           '这波操作真是让我大开眼界，太厉害了', '你渊博的学识，深邃的眼神，彻底征服了我'],
    '图': ['这张图惟妙惟肖,纤毫毕现,欣赏过后仍然回味无穷,让人感觉韵味十足，实在是太好了！', '图片赏心悦目，栩栩如生，虽然只是小小的一幅图，但是丝毫不简单，图中藏有大乾坤，实在是太棒了！'],
    '新人进群': ['你这么优秀的人加盟我们群，实在是本群的广大群友之福，热烈欢迎你的到来','你的到来真是让本群大大长脸，蓬荜生辉，实在是太荣幸了，太赞了', '千万次等待，终于等到这一天，谢天谢地你来了，太棒了'],

}

KEY = '4a9d31d3cc2b4ad7a0a68e26fb19cd85'
def get_response(msg):
    # 使用图灵聊天机器人
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key': KEY,
        'info': msg,
        'userid': 'wechat-robot',
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        return r.get('text')
    except:
        return  # 将会返回一个None


def generate_msg():
    # 生成随机消息
    amazing1 = ['哦,我的天呐', '简直不可思议了', '不敢相信我的眼睛啊', '太让人惊叹了']
    source2 = ['，这个问题表现出你是个', '，你的言语说明你是个', "，从这个问题可以看得出你是个", "，这句话完美的体现了你是个"]
    succeed3 = ["的人，你日后的道路一定会", "的人，你将来百分之一百的能"]

    character = ['平易近人', '宽宏大度', '冰清玉洁', '持之以恒', '锲而不舍', '废寝忘食', '大义凛然', '临危不俱', '光明磊落', '不屈不挠', '鞠躬尽瘁']
    intelligence = ['料事如神', '足智多谋', '融会贯通', '学贯中西', '博古通今', '才华横溢', '出类拔萃', '博大精深', '集思广益', '举一反三']
    eloquence = ['能说会道', '巧舌如簧', '能言善辩', '滔滔不绝', '伶牙俐齿', '出口成章', '语惊四座', '娓娓而谈', '妙语连珠', '口若悬河']
    deportment = ['憨态可掬', '文质彬彬', '风度翩翩', '相貌堂堂', '落落大方', '斗志昂扬', '意气风发', '威风凛凛', '容光焕发', '神采奕奕']
    career = ['节节高攀', '顺风顺水', '大展宏图', '财源亨通', '生意兴隆', '财源广进', '日进斗金', '前程似锦', '飞黄腾达', '官运亨通', '步步高升', '万事胜意', '青云直上',
              '高登显位']
    choice_one = random.choice([character, intelligence, eloquence, deportment])
    text = random.choice(amazing1) + random.choice(source2) + ",".join(random.sample(choice_one, 3)) + random.choice(
        succeed3) + ",".join(random.sample(career, 3)) + '...'
    return text
    # 哦，我的天呐，"+"从这个问题可以看得出你是个"+知识渊博，出口成章，落落大方+"的人，日后的道路一定会" + 生意兴隆
    # text = "惊叹词" + ",从这个问题可以看得出你是个" + "特定赞美词3个不重复" + "的人，日后的道路一定会" + "事业祝福词"
    # print(random.sample(choice_one, 3)) #随机三个不重复
    # print(random.choices(choice_one, k=3)) #随机三个可能出现重复

def split_msg(doc):
    # 对收到的信息进行分词处理，判断有词库中是否出现过
    pattern = re.compile(u'[\\s\\d,.<>/?:;\'\"[\\]{}()\\|~!@#$%^&*\\-_=+a-zA-Z，。《》、？：；“”‘’｛｝【】（）…￥！—┄－]+')
    doc = pattern.sub(r'', doc)  # 将无意义的符号给替换为空字符串
    word_list = ' '.join(jieba.cut(doc)).split(' ')
    replay = ['工作', '学习', '夸夸', '群主', '好看', '病', '认识', '问', '成长', '狗', '猫', '图']
    match = [l for l in word_list if l in replay]  # 取两个列表中的相同元素：也可以使用set(word_list)&set(replay)
    match = match[0] if match else ''
    return match

"""
body = {"scene":"talk","text": "本来今天高高兴兴"}
text	string	是	待识别情感文本，输入限制512字节
scene	string	否	default（默认项-不区分场景），talk（闲聊对话-如度秘聊天等），task（任务型对话-如导航对话等），customer_service（客服对话-如电信/银行客服等）
"""
def get_emotion(text):
    "百度对话情绪识别接口"
    url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/emotion?access_token=24.7f133bd89413775142d9b215ac69e510.2592000.1555819994.282335-15822276'
    body = {"scene":"","text":text}
    res = requests.post(url,headers={'Content-Type': 'application/json',},json=body)
    if res.json().get('error_code'): #如果有错误码，直接返回空
        return
    bb = res.json().get('items')[0] # 取第一条
    label = bb.get('label')
    if label != "neutral": #如果判断有情绪倾向，进行回复
        reply = "".join(bb.get('replies'))
        return reply

def send_msg(msg):
    # 生成消息并发送
    if msg['isAt']:  # 如果@发文的微信名
        randomIdx = random.randint(0, len(REPLY['其它']) - 1)
        itchat.send('%s：%s' % (msg['ActualNickName'], REPLY['其它'][randomIdx]), msg['FromUserName'])
        return
    
    doc = msg['Text']  # 接收到的消息
    reply = get_emotion(doc)
    if reply: #如果百度情感分析有内容返回
        itchat.send('%s：%s' % (msg['ActualNickName'],reply), msg['FromUserName'])
    else:
        match = split_msg(doc) #分词，比照固有词库
        if match:
            randomIdx = random.randint(0, len(REPLY[match]) - 1)  # 发送者的昵称username = msg['ActualNickName']
            itchat.send('%s：%s' % (msg['ActualNickName'], REPLY[match][randomIdx]), msg['FromUserName'])
        else: #图灵机器人与固定句式随机出发
            random.choice([itchat.send('%s：%s' % (msg['ActualNickName'], get_response(msg['Text'])), msg['FromUserName']),itchat.send('%s：%s' % (msg['ActualNickName'], generate_msg()), msg['FromUserName'])])

@itchat.msg_register([TEXT], isGroupChat=True)
def text_reply(msg):  # 监控文本
    if msg['User']['NickName'] == '测试群':
        send_msg(msg)


@itchat.msg_register([PICTURE], isGroupChat=True)
def pic_reply(msg):  # 监控图片
    msg.download(msg.fileName)
    # os.remove(msg.fileName)
    if msg.fileName:
        randomIdx = random.randint(0, len(REPLY['图']) - 1)
        itchat.send('%s' % (REPLY['图'][randomIdx]), msg['FromUserName'])


@itchat.msg_register([NOTE], isGroupChat=True)
def search_add_friend(msg):  # 监控拉人进群
    print(msg['FromUserName'], msg['ActualNickName'])
    randomIdx = random.randint(0, len(REPLY['新人进群']) - 1)
    itchat.send('%s' % (REPLY['新人进群'][randomIdx]), msg['FromUserName'])


itchat.auto_login(enableCmdQR=False, hotReload=True, picDir=r'/root/qrcode.jpeg')
# itchat.auto_login(enableCmdQR=False, hotReload=True,picDir=r'C:\Users\yy\Desktop\kuakua\qrcode.jpeg')
itchat.run()

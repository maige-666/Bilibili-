import os
import requests
import re
import json
import time



class Bili_vadio():
    def __init__(self):
        self.url = input("请输入你要下载的视频的URL: ")
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
                        'referer':'https://www.bilibili.com/','cookie': "buvid3=01B2A898-0FAC-6607-AD32-80A4DC4115FA46259infoc; _uuid=31F18FD0-C5EB-5F80-5333-5FDE7D2F997A48252infoc; b_ut=1; i-wanna-go-back=-1; buvid_fp=01B2A898-0FAC-6607-AD32-80A4DC4115FA46259infoc; buvid_fp_plain=01B2A898-0FAC-6607-AD32-80A4DC4115FA46259infoc; fingerprint=1292ae6a494ff44601529d98f02669d2; rpdid=|(m)mk~uYJR0J'uYJR||lJ)l; blackside_state=1; bp_t_offset_443878656=581465110764587783; LIVE_BUVID=AUTO5916342239542784; CURRENT_QUALITY=0; bp_video_offset_400518824=582172191233084166; SESSDATA=1d8b18d5%2C1649941174%2C264e5%2Aa1; bili_jct=a05541b30d61172da5a51dbd586f3bed; DedeUserID=443878656; DedeUserID__ckMd5=7dcf40c9d443499b; sid=kp4loujk; bp_video_offset_443878656=582182464793930555; PVID=8; CURRENT_BLACKGAP=0; CURRENT_FNVAL=976; innersign=0"}



    def get_data(self):##得到资源的名称，视频和音频的下载地址

        res = requests.get(self.url,headers=self.headers)

        data1 = re.findall('<script>window.__playinfo__=(.+?)</script>',res.text)[0]
         #data1：在text中得到对应的数据
        data2 = json.loads(data1)
         #data2：json解析之后的数据（py字典）

        title= re.findall('<title data-vue-meta="true">(.+?)\d*_哔哩哔哩_bilibili',res.text)[0]
        title = title.replace(' ','')
         #得到视频的题目

        res_audio=data2['data']['dash']['audio'][0]['baseUrl']
        res_video=data2['data']['dash']['video'][0]['baseUrl']
        data_list = [title,res_audio,res_video]

        return data_list


    def save(self,title,audio,video):##视频，音频保存

        audio_content = requests.get(audio,headers=self.headers).content
        video_content = requests.get(video,headers=self.headers).content

        with open(title+'.mp3','wb') as f:
            f.write(audio_content)
        with open(title+'.mp4','wb') as f:
            f.write(video_content)

    def merge_date(self,title):##视频音频合并

        COMMAND = f"ffmpeg -i {title}.mp3 -i {title}.mp4 -c:a copy -c:v copy E:\\bilibili视频\\{title}_.mp4 "
        os.system(COMMAND)


    def dele(self,title):##删除原来的视频和音频
        os.remove(title+'.mp3')
        os.remove(title+'.mp4')



    def run(self):
        self.save(self.get_data()[0],self.get_data()[1],self.get_data()[2])
        self.merge_date(self.get_data()[0])
        time.sleep(2)
        self.dele(self.get_data()[0])




bi = Bili_vadio()
bi.run()
print("下载完成")
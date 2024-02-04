# 获取视频(音频)的双语字幕文件 get video(audio) srt file

开发环境：  
Pyhton 3.12  
Pytorch 2.2  
[requirement.txt](https://github.com/machenme/video2srt/blob/main/requirement.txt)

## 输出结果 srt文件 output srt file
```bash
1
00:00:02,540 --> 00:00:07,560
Defining functions, one of the most important things you will do in this class.
定义函数，这是您在这个类中要做的最重要的事情之一。

2
00:00:09,000 --> 00:00:16,020
Before I talk about the details of defining functions, let's just take a moment to appreciate this moment.
在我讨论定义函数的细节之前，让我们花点时间来欣赏一下这一时刻。

3
00:00:16,760 --> 00:00:24,180
So, I told you on the first day that this course is all about abstraction, and today we're learning tools for abstraction.
所以，我在第一天告诉你，这门课程都是关于抽象的，今天我们正在学习抽象工具。

```

## 使用方法 usage

使用mp3文件会跳过ffmpeg转换阶段  
use mp3 file will ignore ffmpeg trnaform part  


`python getVideoSrt.py xxx.mp4` 默认生成en-zh双语字幕  
`python getVideoSrt.py xxx.mp4 en zh zh` 生成单中文字幕   
`python getVideoSrt.py xxx.mp4 medium fra en fra-en`

```bash
usage: 1.py [-h] filename [model_name] [from_lang] [to_lang] [srt_type]

获取视频字幕.

positional arguments:
  filename    文件路径
  model_name  whisper模型选择 (default: base.en), whisper model select 参考信息 https://github.com/openai/whisper
  from_lang   视频原始语言 (default: en)
  to_lang     双语字幕第二语言 (default: zh)
  srt_type    字幕类型，单中？单英？中英？英中？ (default: en-zh) Subtitle type, single Chinese? single English? zh-en? en-zh?

options:
  -h, --help  show this help message and exit
```
你可以 更改下面两个python变量 控制每一句字幕的提前出现时间和延后消失时间，默认延迟消失0.2秒  
You can change the following two python variables to control the early appearance time and delayed disappearance time of each subtitle. The default delay is 0.2 seconds.  
```bash
    start_early_time = 0
    end_late_time = 0.2
```

## 百度翻译支持的语言 Baidu translate support language
<table class="inner-html-table"><thead><tr style="background-color: #f0f0f0;"><th>名称</th><th>代码</th><th>名称</th><th>代码</th><th>名称</th><th>代码</th></tr></thead><tbody><tr><td>自动检测</td><td>auto</td><td>中文</td><td>zh</td><td>英语</td><td>en</td></tr><tr><td>粤语</td><td>yue</td><td>文言文</td><td>wyw</td><td>日语</td><td>jp</td></tr><tr><td>韩语</td><td>kor</td><td>法语</td><td>fra</td><td>西班牙语</td><td>spa</td></tr><tr><td>泰语</td><td>th</td><td>阿拉伯语</td><td>ara</td><td>俄语</td><td>ru</td></tr><tr><td>葡萄牙语</td><td>pt</td><td>德语</td><td>de</td><td>意大利语</td><td>it</td></tr><tr><td>希腊语</td><td>el</td><td>荷兰语</td><td>nl</td><td>波兰语</td><td>pl</td></tr><tr><td>保加利亚语</td><td>bul</td><td>爱沙尼亚语</td><td>est</td><td>丹麦语</td><td>dan</td></tr><tr><td>芬兰语</td><td>fin</td><td>捷克语</td><td>cs</td><td>罗马尼亚语</td><td>rom</td></tr><tr><td>斯洛文尼亚语</td><td>slo</td><td>瑞典语</td><td>swe</td><td>匈牙利语</td><td>hu</td></tr><tr><td>繁体中文</td><td>cht</td><td>越南语</td><td>vie</td><td>&nbsp;</td><td>&nbsp;</td></tr></tbody></table>

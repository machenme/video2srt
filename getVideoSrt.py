import argparse
import whisper
import requests
import random
import time
import tqdm
from hashlib import md5
from ffmpeg import input, output


def make_md5(s, encoding="utf-8"):
    return md5(s.encode(encoding)).hexdigest()


def baidu_translate(ori_text):

    endpoint = "http://api.fanyi.baidu.com"
    path = "/api/trans/vip/translate"
    url = endpoint + path
    salt = random.randint(1, 65536)
    sign = make_md5(appid + ori_text + str(salt) + appkey)

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    payload = {
        "appid": appid,
        "q": ori_text,
        "from": args.from_lang,
        "to": args.to_lang,
        "salt": salt,
        "sign": sign,
    }

    # Send request
    r = requests.post(url, params=payload, headers=headers)
    result = r.json()

    # Show response
    # result = json.dumps(result, indent=4, ensure_ascii=False)
    return result


def get_need(segment):
    start = change_time(float(segment["start"] + start_early_time))
    end = change_time(float(segment["end"]) + end_late_time)
    time_line = f"{start} --> {end}"
    ori_text = str(segment["text"]).strip()

    # 单语字幕
    if args.srt_type == args.from_lang:
        return f"{time_line}\n{ori_text}\n"
    else:
        trans_text = baidu_translate(ori_text)["trans_result"][0]["dst"]
        if args.srt_type == args.to_lang:
            return f"{time_line}\n{trans_text}\n"
        elif args.srt_type == f"{args.from_lang}-{args.to_lang}":
            return f"{time_line}\n{ori_text}\n{trans_text}\n"
        else:
            return f"{time_line}\n{trans_text}\n{ori_text}\n"


def change_time(time):
    time = float(time)

    # 将秒转换为毫秒
    time_in_ms = int(time * 1000)

    # 使用 divmod 计算小时、分钟和秒
    hours, remaining_ms = divmod(time_in_ms, 3600000)
    mins, secs_in_ms = divmod(remaining_ms, 60000)
    secs, min_sec = divmod(secs_in_ms, 1000)

    # 使用0填充不够的部分
    return f"{hours:0>2}:{mins:0>2}:{secs:0>2},{min_sec:0>3}"


def video2audio(video_file_name: str):
    # 输出的MP3文件路径
    audio_name = video_file_name.split(".")[0] + ".mp3"

    # 使用ffmpeg-python提取音频
    input_audio = input(video_file_name)
    output_audio = output(input_audio, audio_name, codec="mp3").run()
    return audio_name


def save2file(srts, filename):
    filename = str(filename).split(".")[0]
    try:
        with open(f"{filename}.srt", "w", encoding="utf-8") as f:
            for line in srts:
                # 在每个条目之后添加一个空行
                f.write(line + "\n")
    except:
        print("faild to write to txt")


def main():

    model = whisper.load_model(args.model_name)
    if args.filename:
        if str(args.filename).endswith("mp3"):
            audio_name = args.filename
        else:
            audio_name = video2audio(args.filename)
        results = model.transcribe(audio_name, word_timestamps=True)
    else:

        print("请提供文件名。使用 -n 或 --filename 参数。")

    srts = []
    progress_bar_width = 80
    for idx, i in tqdm.tqdm(
        enumerate(results["segments"]),
        total=len(results["segments"]),
        ncols=progress_bar_width,
    ):
        ele = str(f"{idx+1}\n{get_need(i)}")
        srts.append(ele)
        time.sleep(0.1)

    save2file(srts, args.filename)


if __name__ == "__main__":
    
    # from_lang = "en"
    # to_lang = "zh"
    # model_name = "base.en"

    parser = argparse.ArgumentParser(description="获取视频字幕.")

    parser.add_argument("filename", type=str, help="文件路径")

    parser.add_argument(
        "model_name",
        type=str,
        default="base.en",
        nargs="?",
        help="whisper模型选择 (default: base.en), whisper model select 参考信息 https://github.com/openai/whisper ",
    )
    parser.add_argument(
        dest="from_lang",
        type=str,
        default="en",
        nargs="?",
        help="视频原始语言 (default: en)",
    )
    parser.add_argument(
        dest="to_lang",
        type=str,
        default="zh",
        nargs="?",
        help="双语字幕第二语言 (default: zh)",
    )

    parser.add_argument(
        dest="srt_type",
        type=str,
        default="en-zh",
        nargs="?",
        help="字幕类型，单中？单英？中英？英中？(default: en-zh)Subtitle type, single Chinese? single English? zh-en? en-zh?",
    )

    args = parser.parse_args()

    # GET baidu API from https://api.fanyi.baidu.com/manage/developer
    appid = "XXXXXXXXXXXXXXXXX"
    appkey = "**************"
    start_early_time = 0
    end_late_time = 0.2
    
    main()

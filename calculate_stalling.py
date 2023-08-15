######## DEPRECATED ########


from moviepy.editor import VideoFileClip
import json
from haralyzer import HarPage
import re
from datetime import datetime, timedelta
def get_video_duration(file_path):
    try:
        video = VideoFileClip(file_path)
        duration = video.duration
        video.close()
        return duration
    except Exception as e:
        print(f"Error: {e}")
        return None


def calculate_stalling(mp4_files):
    """
    res n = startedDateTime(initial time of request) + wait[n]
    sum_of_durations = duration 1 + duration 2 + ... + duration n
    if res n > sum_of_durations 0...n-1: stalling detected
    stalling = res n - sum_of_durations
    after stalling duration is same as res n because when res arrived video played and
    duration is time of point that video played
    video['time'] is wait time
    """
    stalling = []
    threshold = 1
    segments = []
    for mp4 in mp4_files:
        segments.append({'path': f'./libs/mp4_files/{mp4}.mp4', 'duration': get_video_duration(f'./libs/mp4_files/{mp4}.mp4')})
    # print(segments)
    f = open("network_log1.har")
    har_json = f.read()
    har_dict = json.loads(har_json)
    page = HarPage(har_data=har_dict, page_id="aparat.ir/")
    video_requests = page.filter_entries(content_type='video', status_code="2.*")
    # print(dict(video_requests[0]))
    real_video_requests = []
    list(map(lambda x: real_video_requests.append(x) if re.search(r".*aparat\.com.*/aparat-video/.*",
                                                                  dict(x)['request']['url']) else None, video_requests))

    first_wait_time = real_video_requests[0]['time']
    # print("firstwait",first_wait_time)
    # first_res_date_time is video playing starting point
    first_res_date_time = datetime.fromisoformat(real_video_requests[0]['startedDateTime'].replace("Z", "+00:00")) + timedelta(milliseconds=first_wait_time)
    # print("firstres",first_res_date_time)
    sum_of_durations = first_res_date_time
    first = True
    counter = -1
    index  = 0
    files = []
    while counter < len(real_video_requests) - 1:
        counter += 1
        video = real_video_requests[counter]
        # quality = video['request']['url'].split(".apt")[0].split("/")[4].split("-")[1]
        file_name = f"{video['request']['url'].split('.ts')[0].split('/')[-1]}"
        if file_name in files:
            continue
        # print(file_name, index, counter)
        files.append(file_name)
        # Sum of durations to previous segments
        if index != 0:
            # print("duration",index,segments[index - 1]['duration'])
            sum_of_durations +=  timedelta(seconds=segments[index - 1]['duration'])

        # print("sum_of_d",index,sum_of_durations)
        wait_time = video['time']
        # print("wait_time",index,wait_time)
        start_date_time = datetime.fromisoformat(video['startedDateTime'].replace("Z", "+00:00"))
        # print("start_date_time",index,start_date_time)
        res_date_time = start_date_time + timedelta(milliseconds=wait_time)
        # print("res_date_time",index,res_date_time)
        if res_date_time > sum_of_durations:
            stalling_time = res_date_time - sum_of_durations
            if stalling_time > timedelta(seconds=threshold):
                print("Stalling Detected")
                start = sum_of_durations - first_res_date_time
                duration = stalling_time
                print(start.total_seconds(), duration.total_seconds())
                # First element of stalling array can not be anything other than [0,duration] then when we dont want this we must add [0,0] to the first element
                if first:
                    stalling.append([0,0])
                    first = False
                stalling.append([start.total_seconds(), duration.total_seconds()])
                # After stalling duration is same as res_date_time becuase when res arrived video played and duration is time of point that video played
                sum_of_durations = res_date_time
        index  += 1
    return stalling

# calculate_stalling(["s-1-v1-a1-1690267137.973778","s-1-v1-a1-1690267140.072595","s-2-v1-a1-1690267142.595068","s-3-v1-a1-1690267144.946665","s-4-v1-a1-1690267147.385547", "s-5-v1-a1-1690267149.55657","s-6-v1-a1-1690267151.94897","s-7-v1-a1-1690267154.394765","s-8-v1-a1-1690267156.483345","s-9-v1-a1-1690267158.602453","s-10-v1-a1-1690267160.75423","s-11-v1-a1-1690267163.349664","s-12-v1-a1-1690267165.477136","s-13-v1-a1-1690267168.03126","s-14-v1-a1-1690267170.581914","s-15-v1-a1-1690267173.131788","s-16-v1-a1-1690267175.3422","s-17-v1-a1-1690267178.119569","s-18-v1-a1-1690267180.269125","s-19-v1-a1-1690267182.934324","s-20-v1-a1-1690267185.629064","s-21-v1-a1-1690267188.339831","s-22-v1-a1-1690267190.568714","s-23-v1-a1-1690267193.133739","s-24-v1-a1-1690267195.463462","s-25-v1-a1-1690267198.202104","s-26-v1-a1-1690267200.812938","s-27-v1-a1-1690267203.148984","s-28-v1-a1-1690267205.4574","s-29-v1-a1-1690267208.06207","s-30-v1-a1-1690267210.64317"])
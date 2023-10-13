import datetime
import json
import socket
from haralyzer import HarPage
import re
import statistics
import subprocess


def get_ip_address(domain):
    try:
        domain_encoded = domain.encode('idna').decode()
        server_ip = socket.gethostbyname(domain_encoded)
        return server_ip
    except socket.gaierror:
        return None


def get_main_parameters(host, count=5):
    print("Pinging host: " + host)
    try:
        ping_output = subprocess.check_output(['ping', '-c', str(count), host], stderr=subprocess.STDOUT,
                                              timeout=5)
        ping_output = ping_output.decode('utf-8')
        delay_values = re.findall(r'time=(\d+\.\d+) ms', ping_output)

        packet_loss_match = re.search(r'(\d+)% packet loss', ping_output)
        if packet_loss_match:
            packet_loss = int(packet_loss_match.group(1))
        else:
            packet_loss = count  # Assume all packets are lost in case of a timeout

        if delay_values:
            delay = float(delay_values[0]) / 1000  # Convert to seconds
            jitter = statistics.pstdev(map(float, delay_values)) / 1000  # Convert to seconds
            return delay, jitter, packet_loss
        else:
            return None, None, packet_loss
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        print("exception", e)
        return None, None, count  # Assume all packets are lost in case of an error or timeout


def calculate_qos():
    f = open("network_log1.har")
    har_json = f.read()
    har_dict = json.loads(har_json)
    page = HarPage(har_data=har_dict, page_id="aparat.ir/")
    video_requests = page.filter_entries(content_type='video', status_code="2.*")
    # print(dict(video_requests[0]))
    real_video_requests = []
    list(map(lambda x: real_video_requests.append(x) if re.search(r".*aparat\.com.*/aparat-video/.*",
                                                                  dict(x)['request']['url']) else None, video_requests))
    startup_time = real_video_requests[0][
                       'time'] / 1000  # https://www.mux.com/blog/the-video-startup-time-metric-explained
    # Calculate buffering ratio
    start_time = datetime.datetime.fromisoformat(real_video_requests[0]['startedDateTime'].replace('Z', ''))
    end_time = datetime.datetime.fromisoformat(
        real_video_requests[-1]['startedDateTime'].replace('Z', '')) + datetime.timedelta(
        milliseconds=real_video_requests[-1]['time'])
    total_duration = (end_time - start_time).total_seconds()
    buffering_time = sum([entry["timings"]["wait"] for entry in real_video_requests]) / 1000  # In Seconds
    buffering_ratio = buffering_time / total_duration
    # Calculate rebuffering time
    rebuffering_times = []
    for i in range(1, len(real_video_requests)):
        if real_video_requests[i]["timings"]["wait"] > real_video_requests[i - 1]["timings"]["receive"]:
            rebuffering_times.append(real_video_requests[i]["timings"]["wait"])
    avg_rebuffering_time = sum(rebuffering_times) / len(rebuffering_times) / 1000 if len(
        rebuffering_times) != 0 else 0  # In Seconds
    # Calculate avg bitrate
    total_size = sum(entry['response']['bodySize'] + entry['response']['headersSize'] for entry in real_video_requests)
    avg_bitrate = float(total_size) * 8 / float(total_duration) / 10 ** 6  # IN Mbps
    domain = dict(real_video_requests[0])['request']['url'].split("/")[1].split("aparat.com")[0] + "aparat.com"
    server_ip = get_ip_address(domain)
    delay, jitter, packet_loss = get_main_parameters(host=server_ip, count=3)
    print(
        f" startup_time:{round(startup_time, 2)} secs,\n"
        f" bufferring_time:{round(buffering_time, 2)} secs,\n"
        f" total_duration:{round(total_duration, 2)} secs,\n"
        f" buffering_ratio:{round(buffering_ratio, 2)},\n"
        f" avg_rebuffering_time:{round(avg_rebuffering_time, 2)} secs,\n"
        f" total_size:{round(total_size / 10 ** 6, 2)} Mbits,\n"
        f" avg_bitrate:{round(avg_bitrate, 2)} Mbps,\n"
        f" delay:{round(delay, 4) if delay else -1} seconds,\n"
        f" jitter:{round(jitter, 4) if jitter else -1} seconds,\n"
        f" packet_loss:{round(packet_loss, 2)}%"
    )
    return {
        "startup_time": round(startup_time, 2),
        "buffering_time": round(buffering_time, 2),
        "total_duration": round(total_duration, 2),
        "buffering_ratio": round(buffering_ratio, 2),
        "avg_rebuffering_time": round(avg_rebuffering_time, 2),
        "total_size": round(total_size, 2),
        "avg_bitrate": round(avg_bitrate, 2),
        "delay": round(delay, 2) if delay else -1,
        "jitter": round(jitter, 2) if jitter else -1,
        "packet_loss": round(packet_loss, 2),
    }

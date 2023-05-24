import datetime
import json
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from db import DB_OBJECT
from process_har import process_har

duration = 10


def hover(driver):
    action = ActionChains(driver)
    player = driver.find_element(By.CLASS_NAME, 'player-wrapper')
    action.move_to_element(player).perform()
    time.sleep(1)


def crawl(url, driver, server, proxy):
    stopped = False
    print('===============QoE Assessment in Multimedia===============')
    print(f"Request to {url}")
    driver.get(url)
    # Measure page load time and throughput
    start_time = time.time()
    driver.find_element(By.TAG_NAME, 'html')
    end_time = time.time()
    page_load_time = end_time - start_time
    throughput = len(driver.page_source) / page_load_time
    test_model = DB_OBJECT()
    test_model.initial_parameters_calculation(url, throughput, page_load_time)
    timing_script = """
    return performance.timing;
    """
    timing_data = driver.execute_script(timing_script)
    test_model.extract_browser_parameters(timing_data)

    driver.implicitly_wait(20)
    driver.find_element(By.CLASS_NAME, "romeo-player-tooltip")
    WebDriverWait(driver, 10)
    try:
        start = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'romeo-play-toggle'))
        )
        start.click()
    except:
        print("Not found start button")

    # Wait until the element is clickable with the specified timeout
    try:
        hover(driver)
        advertise = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'vast-skip-button'))
        )
    except:
        advertise = False
        pass

    # advertise= driver.find_element(By.CLASS_NAME, "vast-skip-button")
    if advertise:
        advertise.click()
    else:
        try:
            play_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'romeo-play-toggle'))
            )
            play_button.click()
        except:
            return False

    print('video started')
    start_time = datetime.datetime.now()
    time.sleep(duration)
    hover(driver)

    try:
        driver.find_element(By.CLASS_NAME, "romeo-button").click()
    except:
        server.stop()
        driver.quit()
        stopped = True
    video = driver.find_element(By.TAG_NAME, "video")
    resolution = (video.get_attribute('videoWidth'), video.get_attribute('videoHeight'))
    test_model.resolution = resolution
    print(f'after {duration} seconds video stopped')
    quality = driver.execute_script("return arguments[0].getVideoPlaybackQuality()", video)
    total_frames = quality['totalVideoFrames']
    # driver.close()
    print("process ended.")
    if not stopped:
        server.stop()
        driver.quit()
    end_time = datetime.datetime.now()
    main_video_duration = (end_time - start_time).total_seconds()
    test_model.main_video_duration = main_video_duration
    avg_frame_rate = quality['totalVideoFrames'] / main_video_duration
    test_model.avg_frame_rate = avg_frame_rate


    print('===============QoE Assessment in Multimedia===============')

    with open("network_log1.har", "w", encoding="utf-8") as f:
        f.write(json.dumps(proxy.har))

    try:
        process_har(json.dumps(proxy.har), test_model)
        return True
    except Exception as e:
        print(e)
        return False

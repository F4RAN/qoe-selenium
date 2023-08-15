import datetime
import json
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from db import DB_OBJECT
from process_har import process_har

timeout = 120
duration = 40
check_advertise_time = 2
while_sleep = 0.5

def hover(driver):
    action = ActionChains(driver)
    player = driver.find_element(By.CLASS_NAME, 'player-wrapper')
    action.move_to_element(player).perform()
    time.sleep(1)


def crawl(url, driver, server, proxy):
    advertise = True
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
    # romeo-controls romeo-controls-pause desktop romeo-controls-hide ad-mode

    # try:
    #     WebDriverWait(driver, timeout).until(
    #         EC.presence_of_element_located((By.CLASS_NAME, "romeo-player-tooltip"))
    #     )
    # except:
    #     return False
    advertise_mode = True
    while True:
        try:
            controls = driver.find_element(By.CLASS_NAME, "romeo-controls")
            classess = controls.get_attribute("class").split()
            if controls and ("ad-mode" not in classess):
                break
            elif controls and ("ad-mode" in classess):
                print("Finding skip button, Please wait...")
                try:
                    skip = driver.find_element(By.CLASS_NAME, 'vast-skip-button')
                    skip.click()
                except:
                    play = driver.find_element(By.CLASS_NAME, 'romeo-play-toggle')
                    label = play.get_attribute("aria-label")
                    # $('.romeo-play-toggle').getAttribute('aria-label') == "پخش K"
                    if play and label == "پخش K":
                        play.click()
                    pass
        except:
            pass
        time.sleep(0.5)





    # try:
    #     hover(driver)
    #     driver.find_element(By.CLASS_NAME, 'vast-skip-counter')
    #     skip = True
    # except:
    #     advertise = False
    #     skip = False


    # Wait until the element is clickable with the specified timeout
    # if skip:
    #     try:
    #         hover(driver)
    #         advertise = WebDriverWait(driver, check_advertise_time).until(
    #             EC.element_to_be_clickable((By.CLASS_NAME, 'vast-skip-button'))
    #         )
    #     except:
    #         advertise = False
    #         pass

    # advertise= driver.find_element(By.CLASS_NAME, "vast-skip-button")
    # if advertise and skip:
    #     advertise.click()

    print('video started')
    start_time = datetime.datetime.now()
    counter = 0
    stalling_time = 0
    stall = False
    current = False
    is_start_time = True
    last_current = 0
    stalling = [[0,0]]
    last_time = datetime.timedelta(0)
    additional_timer = datetime.timedelta(0)
    # Try to pause
    while True:
        if counter > timeout - duration:
            break
        hover(driver)
        try:
            # element = WebDriverWait(driver, check_advertise_time).until(
            #     EC.presence_of_element_located((By.CLASS_NAME, 'romeo-current'))
            # )
            element = driver.find_element(By.CLASS_NAME, "romeo-current")
            current = int(element.get_attribute("innerText").split(":")[1])
            print(current)


            try:
                spinner = driver.find_element(By.CLASS_NAME, 'romeo-loading-spinner')
                if spinner:
                    stall = True
            except:
                if stalling_time > 0:
                    stalling.append([start_time, stalling_time])
                stall = False
                is_start_time = True
                stalling_time = 0
                additional_timer = 0
            if int(current) == int(last_current):
                print("Timer stucks")
                now = datetime.datetime.now()
                time_delt = now - last_time
                additional_timer += time_delt.total_seconds()
            last_time = datetime.datetime.now()

            # Stalling check
            if stall and current:
                if is_start_time:
                    start_time = current
                    is_start_time = False

                stalling_time = int(additional_timer)
                print(f"Stall detected in {start_time} for {stalling_time} secs ")


            last_current = current
            if int(current) >= duration:
                hover(driver)
                player = driver.find_element(By.CLASS_NAME, 'player-wrapper')
                player.click()
                print(
                    f'after {duration + counter if advertise == False else duration + counter} seconds video stopped')
                break
        except Exception as e:
            try:
                start = driver.find_element(By.CLASS_NAME, 'romeo-play-toggle')
                label = start.get_attribute("aria-label")
                # $('.romeo-play-toggle').getAttribute('aria-label') == "پخش K"
                if start and label == "پخش K":
                    start.click()
            except:
                print("Can not find start button, Please wait...")
                pass
            # print(e)
            print("Can not get video Timer, Please wait...")
            pass

        time.sleep(while_sleep)
        counter += 1


    print("Stalling: ", stalling)
    video = driver.find_element(By.TAG_NAME, "video")
    resolution = (video.get_attribute('videoWidth'), video.get_attribute('videoHeight'))
    test_model.resolution = resolution

    quality = driver.execute_script("return arguments[0].getVideoPlaybackQuality()", video)
    total_frames = quality['totalVideoFrames']
    # driver.close()
    print("process ended.")

    # Timed out or pass duration
    server.stop()
    driver.quit()

    end_time = datetime.datetime.now()
    # main_video_duration = (duration + counter) if counter <= timeout - duration else timeout
    # Seen by client
    main_video_duration = current
    test_model.main_video_duration = main_video_duration
    avg_frame_rate = quality['totalVideoFrames'] / main_video_duration
    test_model.avg_frame_rate = avg_frame_rate

    print('===============QoE Assessment in Multimedia===============')

    with open("network_log1.har", "w", encoding="utf-8") as f:
        f.write(json.dumps(proxy.har))

    try:
        process_har(json.dumps(proxy.har), test_model, stalling)
        return True
    except Exception as e:
        print(e)
        return False

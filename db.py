import datetime
import json
import sqlite3
from haralyzer import HarParser, HarPage


class DB_OBJECT:
    def __init__(self):
        self.conn = ""
        self.c = ""
        self.url = ""
        # From Selenium (Browser)
        self.throughput = 0
        self.page_load_time = 0
        self.dns_resolution_time = 0
        self.connection_time = 0
        self.ttfb = 0
        self.content_load_time = 0
        self.delay = 0
        self.total_load_time = 0
        self.total_size = 0
        self.total_size_trans = 0
        self.page_size = 0
        self.image_size = 0
        self.css_size = 0
        self.text_size = 0
        self.js_size = 0
        self.audio_size = 0
        self.video_size = 0
        self.initial_load_time = 0
        self.page_load_time = 0
        self.image_load_time = 0
        self.css_load_time = 0
        self.js_load_time = 0
        self.audio_load_time = 0
        self.video_load_time = 0
        self.html_load_time = 0
        self.resolution = (0, 0)
        self.main_video_duration = 0
        self.avg_frame_rate = 0
        # From QoS Calculation
        self.startup_time = 0
        self.buffering_time = 0
        self.buffering_ratio = -1
        self.avg_rebuffering_time = -1
        self.total_size_with_buffer = -1
        self.avg_bitrate = -1
        self.delay_qos = -1
        self.jitter = -1
        self.packet_loss = -1
        # From QoE Calculation
        self.mos = 0
        self.stalling = []

    def create_db_record(self):
        self.conn = sqlite3.connect('network_performance.db')
        self.c = self.conn.cursor()
        # Check if the network_data table exists
        self.c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='network_data'")
        table_exists = self.c.fetchone() is not None
        if not table_exists:
            self.c.execute('''CREATE TABLE network_data
                             (test_no INTEGER PRIMARY KEY AUTOINCREMENT,
                              url TEXT,
                              timestamp DATETIME,
                              delay FLOAT,
                              throughput FLOAT,
                              dns_resolution_time FLOAT,
                              connection_time FLOAT,
                              ttfb FLOAT,
                              content_load_time FLOAT,
                              stalling TEXT,
                              mos FLOAT,
                              initial_load_time FLOAT,
                              page_load_time FLOAT,
                              css_load_time FLOAT,
                              js_load_time FLOAT,
                              audio_load_time FLOAT,
                              video_load_time FLOAT,
                              html_load_time FLOAT,
                              video_width INTEGER,
                              video_height INTEGER,
                              main_video_duration FLOAT,
                              avg_frame_rate FLOAT,
                              startup_time FLOAT,
                              buffering_time FLOAT,
                              buffering_ratio FLOAT,
                              avg_rebuffering_time FLOAT,
                              total_size_with_buffer FLOAT,
                              avg_bitrate FLOAT,
                              delay_qos FLOAT,
                              jitter FLOAT,
                              packet_loss FLOAT        
                          )''')

    def insert_db_record(self):
        insert_data = (
            self.url,
            datetime.datetime.now(),
            self.delay,
            self.throughput,
            self.dns_resolution_time,
            self.connection_time,
            self.ttfb,
            float(self.content_load_time),
            round(float(self.mos), 2),
            self.stalling,
            self.initial_load_time,
            self.page_load_time,
            self.css_load_time,
            self.js_load_time,
            self.audio_load_time,
            self.video_load_time,
            self.html_load_time,
            self.resolution[0],
            self.resolution[1],
            self.main_video_duration,
            self.avg_frame_rate,
            self.startup_time,
            self.buffering_time,
            self.buffering_ratio,
            self.avg_rebuffering_time,
            self.total_size_with_buffer,
            self.avg_bitrate,
            self.delay_qos,
            self.jitter,
            self.packet_loss
        )

        self.c.execute(
            '''INSERT INTO network_data (
                url, 
                timestamp, 
                delay, 
                throughput, 
                dns_resolution_time, 
                connection_time, 
                ttfb, 
                content_load_time, 
                mos,
                stalling,
                initial_load_time, 
                page_load_time, 
                css_load_time, 
                js_load_time, 
                audio_load_time, 
                video_load_time, 
                html_load_time,
                video_width,
                video_height,
                main_video_duration,
                avg_frame_rate,
                startup_time,
                buffering_time,
                buffering_ratio,
                avg_rebuffering_time,
                total_size_with_buffer,
                avg_bitrate,
                delay_qos,
                jitter,
                packet_loss             
            ) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            insert_data
        )

    def drop_db_connection(self):
        # Commit the changes and close the database connection
        self.conn.commit()
        self.conn.close()

    def initial_parameters_calculation(self, url, throughput, page_load_time):
        self.url = url
        self.throughput = throughput
        self.page_load_time = page_load_time

        
    def extract_browser_parameters(self, timing_data):
        self.dns_resolution_time = timing_data['domainLookupEnd'] - timing_data['domainLookupStart']
        self.connection_time = timing_data['connectEnd'] - timing_data['connectStart']
        self.ttfb = timing_data['responseStart'] - timing_data['requestStart']
        self.content_load_time = timing_data['responseEnd'] - timing_data['navigationStart']
        self.delay = self.page_load_time - self.content_load_time

    def set_mos(self, mos):
        self.mos = mos

    def set_stalling(self, stalling):
        if len(stalling) > 0:
            self.stalling = " | ".join(str(stall[0]) + " - " + str(stall[1]) for stall in stalling)
        else:
            self.stalling = "NULL"

    def set_qos(self, qos):

        self.startup_time = qos['startup_time']
        self.buffering_time = qos['buffering_time']
        self.buffering_ratio = qos['buffering_ratio']
        self.avg_rebuffering_time = qos['avg_rebuffering_time']
        self.total_size_with_buffer = qos['total_size']
        self.avg_bitrate = qos['avg_bitrate']
        self.delay_qos = qos['delay']
        self.jitter = qos['jitter']
        self.packet_loss = qos['packet_loss']

    def extract_har_parameters(self, har):
        # Parse the HAR file data
        har_data = json.loads(har)
        har_parser = HarParser.from_string(har)
        har_page = HarPage('aparat.ir/', har_data=har_data)
        self.total_size = har_page.get_total_size
        self.total_size_trans = har_page.get_total_size_trans
        self.page_size = har_page.page_size
        self.image_size = har_page.image_size
        self.css_size = har_page.css_size
        self.text_size = har_page.text_size
        self.js_size = har_page.js_size
        self.audio_size = har_page.audio_size
        self.video_size = har_page.video_size
        self.initial_load_time = har_page.initial_load_time
        self.css_load_time = har_page.css_load_time
        self.js_load_time = har_page.js_load_time
        self.audio_load_time = har_page.audio_load_time
        self.video_load_time = har_page.video_load_time
        self.html_load_time = har_page.html_load_time
    
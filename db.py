import datetime
import json
import sqlite3
from haralyzer import HarParser, HarPage


class DB_OBJECT:
    def __init__(self):
        self.conn = ""
        self.c = ""
        self.url = ""
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
        self.mos = 0

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
                              mos FLOAT,
                              total_load_time FLOAT,
                              total_size FLOAT,
                              total_size_trans FLOAT,
                              page_size FLOAT,
                              image_size FLOAT,
                              css_size FLOAT,
                              text_size FLOAT,
                              js_size FLOAT,
                              audio_size FLOAT,
                              video_size FLOAT,
                              initial_load_time FLOAT,
                              page_load_time FLOAT,
                              css_load_time FLOAT,
                              js_load_time FLOAT,
                              audio_load_time FLOAT,
                              video_load_time FLOAT,
                          html_load_time FLOAT)''')

    def insert_db_record(self):
        # PING JITTER THROUGHPUT PACKET_LOSS
        print(float(self.mos))
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
            self.total_load_time,
            self.total_size,
            self.total_size_trans,
            self.page_size,
            self.image_size,
            self.css_size,
            self.text_size,
            self.js_size,
            self.audio_size,
            self.video_size,
            self.initial_load_time,
            self.page_load_time,
            self.css_load_time,
            self.js_load_time,
            self.audio_load_time,
            self.video_load_time,
            self.html_load_time
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
                total_load_time, 
                total_size, 
                total_size_trans, 
                page_size, 
                image_size, 
                css_size, 
                text_size, 
                js_size, 
                audio_size, 
                video_size, 
                initial_load_time, 
                page_load_time, 
                css_load_time, 
                js_load_time, 
                audio_load_time, 
                video_load_time, 
                html_load_time
            ) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            insert_data
        )

    def drop_db_connection(self):
        # Commit the changes and close the database connection
        self.conn.commit()
        self.conn.close()

    def initial_parameters_calculation(self,url, throughput, page_load_time):
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

    def extract_har_parameters(self, har):
        # Parse the HAR file data
        har_data = json.loads(har)
        har_parser = HarParser.from_string(har)
        har_page = HarPage('aparat.ir/',har_data=har_data)

        self.total_load_time = har_page.get_load_time
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

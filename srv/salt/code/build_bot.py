import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

Keys = webdriver.common.keys.Keys
user_name = "xxxxxxxx"
password = "xxxxxxxx"

class NRbot(object):
    driver = webdriver.Firefox(firefox_profile=None, firefox_binary=None, timeout=30, capabilities=None, proxy=None, executable_path='wires')
    driver.implicitly_wait(4)

    def login(self):
        self.driver.get('https://login.newrelic.com/login?return_to=%2Foauth_provider%2Fauthorize%3Fresponse_type%3Dcode%26client_id%3D%252BvB2dkv4yOb37C00ACk%252B6A%253D%253D%26redirect_uri%3Dhttps%253A%252F%252Frpm.newrelic.com%252Fauth%252Fnewrelic%252Fcallback%26state%3Dfce2d40ee0eb96ac4ac0c7857218eb15d57c6346a17da671')
        self.driver.find_element_by_id("login_email").send_keys(user_name)
        self.driver.find_element_by_id("login_password").send_keys(password)
        self.driver.find_element_by_id("login_submit").click()
        return True

    def new_dash(self,dash_name):
        self.driver.get("https://insights.newrelic.com/accounts/49454/dashboards")
        self.driver.find_element_by_css_selector('.btn-success').click()

        ## Remove initial strong from query box.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
        time.sleep(1)
        self.driver.find_element_by_css_selector("input.form-control:nth-child(2)").send_keys(Keys.BACKSPACE,Keys.BACKSPACE,Keys.BACKSPACE,Keys.BACKSPACE,Keys.BACKSPACE,Keys.BACKSPACE,Keys.BACKSPACE,Keys.BACKSPACE)

        ## Insert Dashboard name                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
        time.sleep(1)
        self.driver.find_element_by_css_selector("input.form-control:nth-child(2)").send_keys(dash_name)
        self.driver.find_element_by_css_selector("a.btn-success").click()
        time.sleep(2)
        return self.driver.current_url

    def add_item_to_dash(self,dash_url,command,title):
        self.driver.get(dash_url)

        ## Remove initial strong from query box.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
        self.driver.find_element_by_css_selector("textarea.ace_text-input").send_keys(Keys.BACKSPACE,Keys.BACKSPACE,Keys.BACKSPACE,Keys.BACKSPACE,Keys.BACKSPACE,Keys.BACKSPACE)

        ## Insert your command.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
        self.driver.find_element_by_css_selector("textarea.ace_text-input").send_keys(command)

        ## Execute your command.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
        self.driver.find_element_by_css_selector("button.btn-primary").click()

        ## Wait for item dropdown.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
        WebDriverWait(self.driver, 4).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.form-group")))
        time.sleep(2)

        ## Insert title.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
        self.driver.find_element_by_css_selector("input.form-control:nth-child(1)").send_keys(title)

        ## Add to item to dash.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
        self.driver.find_element_by_css_selector("button.btn.btn-success.btn-block").click()

def gen_new_dash(bot,site,dash_template):
    name = dash_template['name'].format(site)
    dash_url = bot.new_dash(name)
    for item in dash_template['items']:
        nrql = item['nrql'].format(site)
        title = item['title'].format(site)
        bot.add_item_to_dash(dash_url,nrql,title)

current_dashboards = [
    {
        'name':"{0} performance",
        'items':[
            {'title':'{0}.com avg page load','nrql':"SELECT average(duration) FROM PageView WHERE pageUrl LIKE '%www.{0}.com%' SINCE 1 day ago COMPARE WITH 1 day ago"},
            {'title':'m.{0}.com avg page load','nrql':"SELECT average(duration) FROM PageView WHERE pageUrl LIKE '%m.{0}.com%' SINCE 1 day ago COMPARE WITH 1 day ago"},
            {'title':'{0}.com HP01 and RP01 load time','nrql':"SELECT percentile(duration, 95)/1000 FROM SyntheticCheck WHERE monitorName = '{0} homepage HP01 and RP01 load time'"},
            {'title':'{0}.com avg page load time','nrql':"SELECT average(duration) FROM PageView WHERE pageUrl LIKE '%www.{0}.com%' SINCE 1 day ago COMPARE WITH 1 day ago TIMESERIES AUTO"},
            {'title':'m.{0}.com avg page load time','nrql':"SELECT average(duration) FROM PageView WHERE pageUrl LIKE '%m.{0}.com%' SINCE 1 day ago COMPARE WITH 1 day ago TIMESERIES AUTO"},
            {'title':'Sites document complete','nrql':"SELECT filter(percentile(page_load_time, 95) / 1000, WHERE pageUrl LIKE '%www.{0}.com%') as '{0}', filter(percentile(page_load_time, 95) / 1000, WHERE pageUrl LIKE '%m.{0}.com%') as '{0} mobile' FROM PageAction WHERE actionName = 'nr_footer_stats' SINCE 15 days ago TIMESERIES AUTO"},
            ]
    },
    {
        'name':"{0} Performance KPIs",
        'items':[
            {'title':'{0}.com avg page load time','nrql':"SELECT average(duration) as 'Avg Duration (sec)' FROM PageView WHERE pageUrl LIKE '%www.{0}.com%' SINCE 1 day ago"},
            {'title':'m.{0}.com avg page load time','nrql':"SELECT average(duration) as 'Avg Duration (sec)' FROM PageView WHERE pageUrl LIKE '%m.{0}.com%' SINCE 1 day ago"},
            {'title':'{0}.com page views','nrql':"SELECT count(*) FROM PageView WHERE pageUrl LIKE '%www.{0}.com%' SINCE 1 day ago COMPARE WITH 1 day ago"},
            {'title':'m.{0}.com page views','nrql':"SELECT count(*) FROM PageView WHERE pageUrl LIKE '%m.{0}.com%' SINCE 1 day ago COMPARE WITH 1 day ago"},
            {'title':'{0}.com visitors','nrql':"SELECT uniquecount(session) as 'Visitors' FROM PageView WHERE pageUrl LIKE '%www.{0}.com%' SINCE 1 day ago COMPARE WITH 1 day ago"},
            {'title':'m.{0}.com avg page views per visitor','nrql':"SELECT uniquecount(session) as 'Visitors' FROM PageView WHERE pageUrl LIKE '%m.{0}.com%' SINCE 1 day ago COMPARE WITH 1 day ago"},
            {'title':'{0}.com avg page views per visitor','nrql':"SELECT count(*)/uniqueCount(session) as 'Page Views' FROM PageView SINCE 1 day ago WHERE pageUrl LIKE '%www.{0}.com%'"},
            {'title':'m.{0}.com avg page views per visitor','nrql':"SELECT count(*)/uniqueCount(session) as 'Page Views' FROM PageView SINCE 1 day ago WHERE pageUrl LIKE '%m.{0}.com%'"},
            {'title':'Page Views','nrql':"SELECT filter(count(*),WHERE pageUrl LIKE '%www.{0}.com%' as '{0}.com'), filter(count(*), WHERE pageUrl LIKE '%m.{0}.com%' as 'm.{0}.com') FROM PageView  SINCE 1 day ago"},
            {'title':'Page Views Over Time','nrql':"SELECT filter(count(*),WHERE pageUrl LIKE '%www.{0}.com%' as '{0}.com'), filter(count(*), WHERE pageUrl LIKE '%m.{0}.com%' as 'm.{0}.com') FROM PageView  SINCE 1 day ago TIMESERIES AUTO"},
            {'title':'Avg Page Load Time (sec)','nrql':"SELECT filter(average(duration),WHERE pageUrl LIKE '%www.{0}.com%' as '{0}.com'), filter(average(duration), WHERE pageUrl LIKE '%m.{0}.com%' as 'm.{0}.com') FROM PageView  SINCE 1 day ago"},
            {'title':'Avg Page Load Time Over Time (sec)','nrql':"SELECT filter(average(duration),WHERE pageUrl LIKE '%www.{0}.com%' as '{0}.com'), filter(average(duration), WHERE pageUrl LIKE '%m.{0}.com%' as 'm.{0}.com') FROM PageView  SINCE 1 day ago TIMESERIES AUTO"},
            {'title':'Visitors Over Time','nrql':"SELECT filter(uniquecount(session),WHERE pageUrl LIKE '%www.{0}.com%' as '{0}.com'), filter(uniquecount(session), WHERE pageUrl LIKE '%m.{0}.com%' as 'm.{0}.com') FROM PageView  SINCE 1 day ago TIMESERIES AUTO"},
            {'title':'Visitors','nrql':"SELECT filter(uniquecount(session),WHERE pageUrl LIKE '%www.{0}.com%' as '{0}.com'), filter(uniquecount(session), WHERE pageUrl LIKE '%m.{0}.com%' as 'm.{0}.com') FROM PageView  SINCE 1 day ago"},
            ]
    },
    {
        'name':"{0} Performance Trends",
        'items':[
            {'title':'{0}.com avg page load time','nrql':"SELECT average(duration) as 'Avg Duration (sec)' FROM PageView WHERE pageUrl LIKE '%www.{0}.com%' SINCE 1 day ago COMPARE WITH 1 day ago TIMESERIES AUTO"},
            {'title':'m.{0}.com avg page load time','nrql':"SELECT average(duration) as 'Avg Duration (sec)' FROM PageView WHERE pageUrl LIKE '%m.{0}.com%' SINCE 1 day ago  COMPARE WITH 1 day ago TIMESERIES AUTO"},
            {'title':'{0}.com page views','nrql':"SELECT count(*) FROM PageView WHERE pageUrl LIKE '%www.{0}.com%' SINCE 1 day ago COMPARE WITH 1 day ago  TIMESERIES AUTO"},
            {'title':'m.{0}.com page views','nrql':"SELECT count(*) FROM PageView WHERE pageUrl LIKE '%m.{0}.com%' SINCE 1 day ago COMPARE WITH 1 day ago TIMESERIES AUTO"},
            {'title':'{0}.com visitors','nrql':"SELECT uniquecount(session) as 'Visitors' FROM PageView WHERE pageUrl LIKE '%www.{0}.com%' SINCE 1 day ago COMPARE WITH 1 day ago TIMESERIES AUTO"},
            {'title':'m.{0}.com visitors','nrql':"SELECT uniquecount(session) as 'Visitors' FROM PageView WHERE pageUrl LIKE '%m.{0}.com%' SINCE 1 day ago COMPARE WITH 1 day ago TIMESERIES AUTO"},
            {'title':'{0}.com avg page views per visitor','nrql':"SELECT count(*)/uniqueCount(session) as 'Page Views' FROM PageView SINCE 1 day ago WHERE pageUrl LIKE '%www.{0}.com%'  COMPARE WITH 1 day ago TIMESERIES AUTO"},
            {'title':'m.{0}.com avg page views per visitor','nrql':"SELECT count(*)/uniqueCount(session) as 'Page Views' FROM PageView SINCE 1 day ago WHERE pageUrl LIKE '%m.{0}.com%'  COMPARE WITH 1 day ago TIMESERIES AUTO"},
            {'title':'{0}.com avg page load time','nrql':"SELECT average(duration) FROM PageView WHERE pageUrl LIKE '%www.{0}.com%' SINCE 1 day ago COMPARE WITH 1 day ago TIMESERIES AUTO"},
            {'title':'m.{0}.com avg page load time','nrql':"SELECT average(duration) FROM PageView WHERE pageUrl LIKE '%m.{0}.com%' SINCE 1 day ago COMPARE WITH 1 day ago TIMESERIES AUTO"},
            ]
    },
    {
        'name':"{0} Performance & Interaction",
        'items':[
            {'title':'Avg Page Load Time (sec)','nrql':"SELECT filter(average(duration),WHERE pageUrl LIKE '%www.{0}.com%' as '{0}.com'), filter(average(duration), WHERE pageUrl LIKE '%m.{0}.com%' as 'm.{0}.com') FROM PageView  SINCE 1 day ago"},
            {'title':'Page Views','nrql':"SELECT filter(count(*),WHERE pageUrl LIKE '%www.{0}.com%' as '{0}.com'), filter(count(*), WHERE pageUrl LIKE '%m.{0}.com%' as 'm.{0}.com') FROM PageView  SINCE 1 day ago"},
            {'title':'Visitors','nrql':"SELECT filter(uniquecount(session),WHERE pageUrl LIKE '%www.{0}.com%' as '{0}.com'), filter(uniquecount(session), WHERE pageUrl LIKE '%m.{0}.com%' as 'm.{0}.com') FROM PageView  SINCE 1 day ago"},
            {'title':'Avg Page Load Time Over Time (sec)','nrql':"SELECT filter(average(duration),WHERE pageUrl LIKE '%www.{0}.com%' as '{0}.com'), filter(average(duration), WHERE pageUrl LIKE '%m.{0}.com%' as 'm.{0}.com') FROM PageView  SINCE 1 day ago TIMESERIES AUTO"},
            {'title':'Page Views Over Time','nrql':"SELECT filter(count(*),WHERE pageUrl LIKE '%www.{0}.com%' as '{0}.com'), filter(count(*), WHERE pageUrl LIKE '%m.{0}.com%' as 'm.{0}.com') FROM PageView  SINCE 1 day ago TIMESERIES AUTO"},
            {'title':'Visitors Over Time','nrql':"SELECT filter(uniquecount(session),WHERE pageUrl LIKE '%www.{0}.com%' as '{0}.com'), filter(uniquecount(session), WHERE pageUrl LIKE '%m.{0}.com%' as 'm.{0}.com') FROM PageView  SINCE 1 day ago TIMESERIES AUTO"},
            {'title':'{0}.com','nrql':"SELECT count(*), average(duration) as 'Avg Page Load Time (sec)' FROM PageView WHERE pageUrl LIKE '%www.{0}.com%' SINCE 1 day ago"},
            {'title':'m.{0}.com','nrql':"SELECT count(*), average(duration) as 'Avg Page Load Time (sec)' FROM PageView WHERE pageUrl LIKE '%m.{0}.com%' SINCE 1 day ago"},
            {'title':'Top 5 Stories - {0}.com','nrql':"SELECT count(*) as 'Page Views' FROM PageView WHERE pageUrl LIKE '%www.{0}.com/%/%-%-%' SINCE 1 day ago facet pageUrl limit 5"},
            {'title':'Top 5 Stories - m.{0}.com','nrql':"SELECT count(*) as 'Page Views' FROM PageView WHERE pageUrl LIKE '%m.{0}.com/%/%-%-%' SINCE 1 day ago facet pageUrl limit 5"},
            {'title':'Top 5 Slowest Pages - {0}.com','nrql':"SELECT average(duration) as 'Avg Page Laod Time (sec)' FROM PageView WHERE pageUrl LIKE '%www.{0}.com/%/%-%-%' SINCE 1 day ago facet pageUrl limit 5"},
            {'title':'Top 5 Slowest Pages - m.{0}.com','nrql':"SELECT average(duration) as 'Avg Page Laod Time (sec)' FROM PageView WHERE pageUrl LIKE '%m.{0}.com/%/%-%-%' SINCE 1 day ago facet pageUrl limit 5"},
            ]
    },
]

sites = [
    "wsbradio",
    "whio",
    "wokv",
    "news965",
    "krmg",
    "1073theeagle",
    "wbli",
    "wedr",
    "yourgeorgiacountry",
    "kiss104fm",
    ]

if __name__ == '__main__':
    bot = NRbot()
    bot.login()
    for site in sites:
        for dashboard in current_dashboards:
            time.sleep(1)
            gen_new_dash(bot,site,dashboard)

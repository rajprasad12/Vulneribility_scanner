import requests
import re
from bs4 import BeautifulSoup

class Scanner:
    def __init__(self,url):
        self.session= requests.Session()
        self.target_url= url
        self.target_link= []
    
    def extract_links(self,url=None):# extract all links from a site

        try:
            if url==None:
                url= self.target_url
            response=self.session.get('http://' + url)
            href_links= re.findall('(?:href=")(.*?)"', response.content.decode('utf-8'))
            for link in href_links:
                if self.target_url in link and link not in self.target_link:
                    self.target_link.append(url)
                    print(link)
                    self.extract_links(link)
    
        except requests.exceptions.ConnectionError:
            pass

    def extract_forms(self,url):
        response= self.session.get(url).content
        parse_html= BeautifulSoup(response, 'html.parser')
        return parse_html.findAll('form')
    
    def submit_form(self, form, value, url ):
        action= form.get('action')
        post_url= urljoin(url, action)
        print(post_url)
        method= form.get('method') 
        print(action)
        print(method)
        
        input_list= form.findAll('input')
        post_data={}
        for input in input_list:
            input_name= input.get('name')
            input_type= input.get('text')
            #input_type2= input.get('password')
            input_value= input.get('value')
            if input_type=='text' and input_type=='password':
                input_value=value
            post_data[input_name]= input_value
            if method=='post':
                return self.session.post(post_url, data=post_data)
            return self.session.get(post_url, params=post_data)

    def run_scanner(self):
        for link in self.target_link:
            forms= self.extract_forms(link)
            for form in forms:
                print('[+] Testing form in '+ link)
                found_xss= self.xss_form(form, link)
                if found_xss:
                    print('\n\n[+] Discovered XSS' + link + 'in the following form')
                    print(form) 


            if '=' in link:
                print('\n\n[+] Testing ' + link)
                found_xss= slef.xss_link(link)
                if found_xss:
                    print('[+] Discovered XSS' + link)
                    
    
    def xss_link(self, url):
        xss_test= "<script>alert('hacked')</script>"
        url= url.replace('=', '=' + xss_test)
        response= self.session.get(url)
        if xss_test in response.content:
            return True


    def xss_form(self, form, url):
        xss_test= "<script>alert('hacked')</script>"
        response= self.submit_form(form, xss_test, url)
        if xss_test in response.content:
            return True

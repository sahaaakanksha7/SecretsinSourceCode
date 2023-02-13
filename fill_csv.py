#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 06:43:33 2019

@author: aakanksha
Script to get features from the identified secrets and store it in csv file
"""

import os
import json
from pprint import pprint
import csv
from bs4 import BeautifulSoup

path = '/directory/toread/JSONResults'
secret = []
file = []
repo = [] 
line = []
entropy = []
have_brackets = []
have_arrow = []
have_dot = []
count_dot = []
comment_list = []
start_dollar = []
space = []
words = []
number = []
have_parantheses = []
is_html = []
test = []
readme_list = []
conf = []
p_list = []
s_list = []
lang = []
ent01 = []
ent12 = []
ent23 = []
ent34 = []
ent4 = []

def matched(str):
    count1 = 0
    count2 = 0
    for i in str:
        if i == "(":
            count1 += 1
        elif i == ")":
            count2 += 1
    if count1 != 0 and count2 != 0 and count1 == count2:
            have_parantheses.append("Yes")
    else:
        have_parantheses.append("No")

#print(matched('bytes(buffer(password))'))
#print(matched('password + b'' * blocksize - len(password)'))


def matched_1(str):
    count1 = 0
    count2 = 0
    for i in str:
        if i == "[":
            count1 += 1
        elif i == "]":
            count2 += 1
    if count1 != 0 and count2 !=0 and count1 == count2:
            have_brackets.append("Yes")
    else:
        have_brackets.append("No")
             
def arrow(str):
    c = "->"
    if c in str:
        return "Yes"
    return "No"

def dot(str):
    count = 0
    for i in str:
        if i == ".":
            count += 1
        
    #if count != 0:
        #count_dot.append(count)
        #have_dot.append("Yes")
    return count    
    

def comment(str):
    if str.startswith("#") or str.startswith("*") or str.startswith("/*") or str.startswith("//"):
                      comment_list.append("Yes")
    else:
        comment_list.append("No")
#print(dot(' $_COOKIE [password]'))  

def startsymbol(str):
    if str.startswith("$"):
        start_dollar.append("Yes")
    else:
        start_dollar.append("No")
    
    
#print(startsymbol("{var.$pingdom_password}"))   
    
def havespace(str):
    for c in str:
        if c.isspace():
            return "Yes"
    return "No"

#print(havespace("wKH-qr-Grg; */"))
#html = """<input id=\"password\" type=\"text\" name=\"password\" required><br><br>"""
#print(bool(BeautifulSoup(html, "html.parser").find()))
    

def check_null_None(str):
    str = str.lower()
    if (str.find("none") == -1 and str.find("nil") == -1 and str.find("null") == -1 and str.find("true") == -1 and str.find("false") == -1 and str.find("undefined") == -1):        
        words.append("No")
    else:
        words.append("Yes")


def is_number(s):
    try:
        if float(s):
            return "Yes"
        if int(s):
            return "Yes"
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return "Yes"
    except (TypeError, ValueError):
        pass
    return "No"

#print(is_number("0000"))
#print(is_number(0xCE4B)) #but "0xCE4B" doesn't work
#print(is_number("90867b984d2a5038ee21a190996b900b"))
#print(int(0x0000))
    

    
def check(string): 
    string = string.lower()
    if (string.find("test") == -1) and (string.find("example") == -1) : 
        test.append("No")
    else: 
        test.append("Yes")
        
def readme(string):
    string = string.lower()
    file_name = string.split('/')[-1]
    if(file_name.endswith('.md') or file_name.find("readme") != -1 or file_name.endswith('.rst')):
        readme_list.append("Yes")
    else:
        readme_list.append("No")
        
def configure(string):
    string = string.lower()
    if (string.find("yml") == -1 and string.find("yaml") == -1 and string.find("conf") == -1 and string.find("config") == -1 and string.find("cfg") == -1 and string.find("cnf") == -1 and string.find("configure") == -1):
        conf.append("No")
    else:
        conf.append("Yes")
        
        
def properties(string):
    string= string.lower()
    file_name = string.split('/')[-1]
    if(file_name.endswith('.properties')):
        p_list.append("Yes")
    else:
        p_list.append("No")
        
def settings(string):
    string= string.lower()
    file_name = string.split('/')[-1]
    if file_name.find("settings") == -1:
        s_list.append("No")
    else:
        s_list.append("Yes")
    
def language(string):
    string= string.lower()
    if string.find("lang") == -1 and string.find("language") == -1 and string.find("locale") == -1:
        lang.append("No")
    else:
        lang.append("Yes")
    
    
def entropycheck(ent):
    if ent >= 0 and ent < 1:
            ent01.append("Yes")
    else:
        ent01.append("No")
            
    if ent >= 1 and ent < 2:
            ent12.append("Yes")
    else:
        ent12.append("No")
            
    if ent >= 2 and ent < 3:
        ent23.append("Yes")
    else:
        ent23.append("No")
        
    if ent >= 3 and ent < 4:
        ent34.append("Yes")
    else:
        ent34.append("No")
        
    if ent >=4:
        ent4.append("Yes")
    else:
        ent4.append("No")
        
            
        
    
    

#check(string.lower(), sub_str1.lower(), sub_str2.lower()) 



files = os.listdir(path)
for name in files:
    print(name)
    filePath = os.path.join(path, name)
    File = open(filePath, mode = "r")
    data = json.load(File)
    length = len(data['password extracted'])
    for i in range(length):
        #pprint(data['password extracted'][i]['Password Value'])
        if len(data['password extracted'][i]['Line']) > 200:
            continue
        secret.append(data['password extracted'][i]['Password Value'])
        pwd = data['password extracted'][i]['Password Value']
        check_null_None(pwd)
        value = is_number(pwd)
        number.append(value)
        matched(pwd)
        matched_1(pwd)
        value1 = havespace(pwd)
        space.append(value1)
        startsymbol(pwd)
   
        value3 = dot(pwd)
        count_dot.append(value3)
        value2 = arrow(pwd)
        have_arrow.append(value2)
        #pprint(data['password extracted'][i]['File'])
        file.append(data['password extracted'][i]['File'])
        fd = data['password extracted'][i]['File']
        check(fd)
        readme(fd)
        configure(fd)
        settings(fd)
        properties(fd)
        language(fd)
        #pprint(data['password extracted'][i]['Repo Name'])
        repo.append(data['password extracted'][i]['Repo Name'])
        line.append(data['password extracted'][i]['Line'])
        html = data['password extracted'][i]['Line']
        is_html.append(bool(BeautifulSoup(html, "html.parser").find()))
        comment(html)
        #entropy.append(data['password extracted'][i]['Entropy'])
        #ent = data['password extracted'][i]['Entropy']
        #entropycheck(ent)

        

with open('feature_file.csv', 'a') as csvfile:
     
     fieldnames = ['Label','Secret','File', 'Repo Name', 'Line','Does this have()',	'Have [] in value.',	'Does this have .?',	'.Count',	'Have $ in start?', 'Has space?',	'Line Has html tags?',	'Line starts with #,*, /*, //',	'Has -> in password value.','Entropy', 'Entropy[0,1)',	'Entropy[1,2)',	'Entropy[2,3)',	'Entropy[3,4)',	'Entropy 4 above','Type of File	Language File?',	'Readme File?',	'Configuration File/ .YAML/.yml?',	'Properties file?',	'Settings file?',	'File or directory has test?' , 'Is null/nil/undefined/None/true/false',	'Is numeric?(Without quotes)',	'Does username exists in 5 lines up pr down?']
     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
       
     writer.writeheader()

     for count in range(len(secret)):
        writer.writerow({'Label':'N', 'Secret': secret[count],'File':file[count], 'Repo Name': repo[count],'Line':line[count], 'Does this have()':have_parantheses[count],	'Have [] in value.':have_brackets[count],	'Does this have .?':'No',	'.Count':count_dot[count],	'Have $ in start?':start_dollar[count], 'Has space?':space[count],	'Line Has html tags?':is_html[count],	'Line starts with #,*, /*, //':comment_list[count],	'Has -> in password value.':have_arrow[count],'Entropy': '0', 'Entropy[0,1)':'No',	'Entropy[1,2)': 'No',	'Entropy[2,3)':'No',	'Entropy[3,4)': 'No',	'Entropy 4 above':'No','Type of File	Language File?':lang[count],	'Readme File?':readme_list[count],	'Configuration File/ .YAML/.yml?':conf[count],	'Properties file?':p_list[count],	'Settings file?':s_list[count],	'File or directory has test?':test[count],'Is null/nil/undefined/None/true/false':words[count],	'Is numeric?(Without quotes)':number[count],	'Does username exists in 5 lines up pr down?':'No'})
                         
        #writer.writerow({'Label':'N', 'Secret': secret[count],'File':file[count], 'Repo Name': repo[count],'Line':line[count], 'Does this have()':have_parantheses[count],	'Have [] in value.':have_brackets[count],	'Does this have .?':'No',	'.Count':count_dot[count],	'Have $ in start?':start_dollar[count], 'Has space?':space[count],	'Line Has html tags?':is_html[count],	'Line starts with #,*, /*, //':comment_list[count],	'Has -> in password value.':have_arrow[count],'Entropy':entropy[count], 'Entropy[0,1)':ent01[count],	'Entropy[1,2)':ent12[count],	'Entropy[2,3)':ent23[count],	'Entropy[3,4)':ent34[count],	'Entropy 4 above':ent4[count],'Type of File	Language File?':lang[count],	'Readme File?':readme_list[count],	'Configuration File/ .YAML/.yml?':conf[count],	'Properties file?':p_list[count],	'Settings file?':s_list[count],	'File or directory has test?':test[count],'Is null/nil/undefined/None/true/false':words[count],	'Is numeric?(Without quotes)':number[count],	'Does username exists in 5 lines up pr down?':'No'})
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
                        
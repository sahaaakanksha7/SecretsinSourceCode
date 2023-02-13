# -*- coding: utf-8 -*-
"""

@author: aakanksha
Script to enlist Github repositories with specific keywords
https://developer.github.com/v3/search/#text-match-metadata


"""

import requests
import csv

#url = 'https://api.github.com/search/repositories?q=stars:%3E=1000+&sort=stars&order=desc'

def rsa():
    url = 'https://api.github.com/search/code?q="BEGIN+RSA+PRIVATE"&page=20'
    
    resp = requests.get(url=url, auth = ('', ''))
    data = resp.json()
    repoCount = data["total_count"]
    print("Total_Count" + str(repoCount))
    try:
        file = open("gitrepolist_rsa.txt","a")
    except:
        print("Error occured while opening the file")
        
    
    for i in range(30):
        file.write(data["items"][i]["repository"]["html_url"])
        file.write('\r\n')
    

##main()
#uniqlines = []
#uniqlines = list(set(open('gitrepolist.txt').readlines()))
#print(len(uniqlines))
def readtext():
    file = open('pwd_list.txt', 'r')
    lines=file.readlines()
    result=[]
    for x in lines:
     result.append(x.split(' ')[0])
     file.close()
    
    file = open('pwd_list_out.txt', 'w')
    for count in range(len(result)):
        file.write(result[count])
        file.write('\r\n')

def apikey():
    url = 'https://api.github.com/search/code?q=apikey&page=16'
    
    resp = requests.get(url=url, auth = ('', ''))
    data = resp.json()
    repoCount = data["total_count"]
    print("Total_Count" + str(repoCount))
    try:
        file = open("gitrepolist_api.txt","a")
    except:
        print("Error occured while opening the file")
        
    #print(data["items"][29]["clone_url"])
    
    for i in range(30):
        file.write(data["items"][i]["repository"]["html_url"])
        file.write('\r\n')
        
        
def secretkey():
    url = 'https://api.github.com/search/code?q=secret&page=3'
    resp = requests.get(url=url, auth = ('', ''))
    data = resp.json()
    repoCount = data["total_count"]
    print("Total_Count" + str(repoCount))
    try:
        file = open("gitrepolist_secret.txt","a")
    except:
        print("Error occured while opening the file")
        

    
    for i in range(30):
        file.write(data["items"][i]["repository"]["html_url"])
        file.write('\r\n')
        
def passwordkey():
    url = 'https://api.github.com/search/code?q=password&page=3'
    resp = requests.get(url=url, auth = ('', ''))
    data = resp.json()
    repoCount = data["total_count"]
    print("Total_Count" + str(repoCount))
    try:
        file = open("gitrepolist_passw.txt","a")
    except:
        print("Error occured while opening the file")
    
    for i in range(30):
        file.write(data["items"][i]["repository"]["html_url"])
        file.write('\r\n')
 

#rsa()
#apikey()
#secretkey()
#passwordkey()









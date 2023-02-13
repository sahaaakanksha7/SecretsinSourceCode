# -*- coding: utf-8 -*-
"""

@author: aakanksha
Multithreaded code to scan the files in a cloned repository.

"""
import os
import logging
import threading
import re
try:
    from pip import main as pipmain
except:
    from pip._internal import main as pipmain
#try:
    #import Levenshtein
#except ImportError:       
    #subprocess.call(['pip', 'install', 'python-levenshtein'])
    #pipmain(['install', 'python-levenshtein'])##Requires Levenshtein wheel to be installed.
    #import Levenshtein 
try:
    import queue
except ImportError:
    import Queue as queue
import time
from time import gmtime, strftime
import json
import math
from collections import Counter


logging.basicConfig(filename="sample.log", filemode="w", level=logging.INFO)


BASE64_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="


key_strings_found = []
scanned_paths = []
scanned_files = []
lines = []
mydata = threading.local()
data = {}
entropyValue = []
commonPassword = []
distance = []


ignored_extensions = (
                     ".css", ".woff", ".woff2", ".jpg", ".jpeg", ".png", ".gif", ".ico", ".sln", ".svg", ".tiff",
                     ".ttf", ".eot", ".pyc", ".exe", ".jar", ".apk", ".gz", ".zip", "csproj", "sqlproj", ".md", 
                     ".cna", ".gitignore", ".gitattributes"
                     )
ignored_files = (
                "composer.lock",
                "vendor/composer/installed.json",
                "gemfile.lock",
                "yarn.lock",
                "package-lock.json"

                ) 
'''passfields = ['add_password', 'pass', 'password', '_password', 'passwd', 'session_password', 'sessionpassword', 
                  'login_password', 'loginpassword', 'form_pw', 'pw', 'userpassword', 'pwd', 'upassword', 'login_password'
                  'passwort', 'passwrd', 'wppassword', 'upasswd', 'pin']'''

regex_dict = {                
        'Twitter Oauth 2': '[t|T][w|W][i|I][t|T][t|T][e|E][r|R].*.([0-9a-zA-Z]{35,44})',
        "Facebook Oauth 2": "[f|F][a|A][c|C][e|E][b|B][o|O][o|O][k|K].*.([0-9a-f]{32})",
        "Twitter Oauth": "[t|T][w|W][i|I][t|T][t|T][e|E][r|R].*['|\"]([0-9a-zA-Z]{35,44})['|\"]",
        "Generic AppSecret": "[a|A][p|P][p|P][s|S][e|E][c|C][r|R][e|E][t|T].*.([0-9a-zA-Z]{32,45})",
        "Google Oauth 2": "[c|C][l|L][i|I][e|E][n|N][T|T][_][s|S][e|E][c|C][r|R][e|E][t|T].*[:].*([a-zA-Z0-9-_]{24})",
        "Slack Token1": "xox[p|b|o|a].*",
        "ContentSearchPatterns_azure_secret_1":'(?:>|\'|=|")([a-zA-Z0-9/+]{43}=)[^{@]',
        "ContentSearchPatterns_azure_secret_2":'(?:>|\'|=|"|#)([a-zA-Z0-9/+]{86}==)',
        "Generic AppSecret 2": "[a|A][p|P][p|P][s|S][e|E][c|C][r|R][e|E][t|T].*['|\"]([0-9a-zA-Z]{32,45})['|\"]",
        "Generic Secret": "[s|S][e|E][c|C][r|R][e|E][t|T].*['|\"]([0-9a-zA-Z]{32,45})['|\"]",
        "GitHub": "[g|G][i|I][t|T][h|H][u|U][b|B].*[['|\"]0-9a-zA-Z]{35,40}['|\"]",
        "RSA private key": "-----BEGIN RSA PRIVATE KEY-----.*",
        "RSA public key":"-----BEGIN RSA PUBLIC KEY-----.*",
        "Private key": "-----BEGIN PRIVATE KEY-----.*",
        "GitHub 2": "[g|G][i|I][t|T][h|H][u|U][b|B].*[c|C][l|L][i|I][e|E][n|N][T|T][s|S][e|E][c|C][r|R][e|E][t|T].*([0-9a-zA-Z]{35,40})",
        "Facebook Oauth": "[f|F][a|A][c|C][e|E][b|B][o|O][o|O][k|K].*['|\"]([0-9a-f]{32})['|\"]",
        "Generic Password": ".*[p|P][a|A][s|S][s|S][w|W][o|O][r|R][d|D].*[:=](.*)",       
        "Slack Token": "(xox[p|b|o|a]-[0-9]{12}-[0-9]{12}-[0-9]{12}-[a-z0-9]{32})",
        "SSH (OPENSSH) private key": "-----BEGIN OPENSSH PRIVATE KEY-----",
        "SSH (DSA) private key": "-----BEGIN DSA PRIVATE KEY-----",
        "SSH (EC) private key": "-----BEGIN EC PRIVATE KEY-----",
        "PGP private key block": "-----BEGIN PGP PRIVATE KEY BLOCK-----",
        "Google Oauth": "(\"client_secret\":\"[a-zA-Z0-9-_]{24}\")",
        "AWS API Key": "AKIA[0-9A-Z]{16}",
        "Heroku API Key": "[h|H][e|E][r|R][o|O][k|K][u|U].*[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}",
        "Generic Secret": "[s|S][e|E][c|C][r|R][e|E][t|T].*['|\"]([0-9a-zA-Z]{32,45})['|\"]",
        "Generic API Key": "[a|A][p|P][i|I][_]?[k|K][e|E][y|Y].*['|\"]([0-9a-zA-Z]{32,45})['|\"]",
        "Slack Webhook": "https://hooks.slack.com/services/T[a-zA-Z0-9_]{8}/B[a-zA-Z0-9_]{8}/[a-zA-Z0-9_]{24}",
        "Google (GCP) Service-account": "\"type\": \"service_account\"",
        "Twilio API Key": "SK[a-z0-9]{32}",
        "Password in URL": "//[^/\\s:]+:[^/\\s:]+@",
        'Secrets1':'(Password|pass|passwd|session_password|login_password|login_password|_password)\s*[:=](\s*"[^"\r\n]+")',
        'Tokens':'(API_tokens|api_tokens|tokens|Tokens)\s*[:=](\s*"[^"\r\n][a-f0-9]{16}")'
        }


def scanDir(path):

    P = queue.Queue()
    for root, dirs, files in os.walk(path):
        for file_ in files:
            filePath = os.path.join(root, file_)
            P.put(filePath)
   
    while P.empty() is False:
          scanFile(P.get())
    
    try:              
            data['password extracted'] = []
            #print(key_strings_found)
            for x in range(len(key_strings_found)):
                   #print (key_strings_found[x])
                   if str(path) not in str(scanned_files[x]):
                      pass
                   else:
                      data['password extracted'].append({'Repo Name': os.path.basename(path).replace('_git_',''),'File': os.path.relpath(scanned_files[x]).strip(), 'Line': lines[x].strip(), 'Password Value': key_strings_found[x][-1].strip().replace('"', '') if type(key_strings_found[x]) == tuple else key_strings_found[x].strip().replace('"', ''), 'Entropy' : entropyValue[x]})
                      #data['password extracted'].append({'Repo Name': os.path.basename(path).replace('_git_',''),'File': os.path.relpath(scanned_files[x]).strip(), 'Password Value': key_strings_found[x][-1].strip().replace('"', '') if type(key_strings_found[x]) == tuple else key_strings_found[x].strip().replace('"', ''),'Entropy' : entropyValue[x], 'Common Password' : commonPassword[x] , 'Levenshtein Distance': distance[x]})
    
            with open('JSONResults_JanRepo/%s.json' %os.path.basename(path), 'w+') as outfile:
                       json.dump(data, outfile, indent=2)
                       outfile.write('\n')
    except Exception as e:
        print("Json error")
        logging.error("Error occured while writing to JSON")
                           

def LD(match):
    if type(match) == tuple:
        word = match[-1]
    else:
        word = match
    commonPassword.append("No")
    distance.append("0.0")
    with open('common_password.txt', 'r') as f:
        for line in f:
            if Levenshtein.ratio(word, line) > 0.5:
                commonPassword.pop()
                commonPassword.append("Yes")
                distance.pop()
                distance.append(Levenshtein.ratio(word, line))
                return
 



def shannon_entropy(data, iterator):
    """
    Borrowed from http://blog.dkbza.org/2007/05/scanning-data-for-entropy-anomalies.html
    """
    if not data:
        return 0
    entropy = 0
    for x in iterator:
        p_x = float(data.count(x))/len(data)
        if p_x > 0:
            entropy += - p_x*math.log(p_x, 2)
    return entropy

##Not required
def get_strings_of_set(word, char_set, threshold=20):
    count = 0
    letters = ""
    strings = []
    for char in word:
        if char in char_set:
            letters += char
            count += 1
        else:
            if count > threshold:
                strings.append(letters)
            letters = ""
            count = 0
    if count > threshold:
        strings.append(letters)
    return strings




def find_entropy(match):
        #stringsFound = []
        if type(match) == tuple:
            word = match[-1]
        else:
            word = match
            
        wordEntropy = shannon_entropy(word, BASE64_CHARS)
        entropyValue.append(wordEntropy)
        return
            
def scanFile(file):
    #print(file)
    
    if file.endswith(ignored_extensions) or file.endswith(ignored_files):
        pass
    try:
            File = open(file, mode = "r")
            
            for line in File:
                for k, v in regex_dict.items():                          
                    match_obj = re.findall(v, line)
                    if match_obj:
                        for match in match_obj: # Put condition for null matches
                            if file in scanned_files and match in key_strings_found: ## To remove duplicates
                                continue
#                            if line.count('=') == 1 or line.count(':') == 1:
#                                print(line)
#                                key_strings_found.append(re.split(':|=', line)[1])
#                            else:
#                            i = 0
#                            match_edit = match
#                            while i < len(match_edit)/2:
#                                match_edit = match_edit.replace(match_edit[i], '*')
#                                i=i+1    
                            key_strings_found.append(match)
                            scanned_files.append(file)
                            lines.append(line)
                            find_entropy(match)
                            #LD(match)
       
    except IOError as e:
             logging.error(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " " + "I/O error({0}): {1}".format(e.errno, e.strerror))
    except Exception as e:
             logging.error("Unexpected Error Occured\n")
             logging.error(e)
    #finally:
             #File.close()
    

def pywalker(path):
    Q = queue.Queue()
    threads_limit = 50
    threads_state = []
    
    if not os.path.exists('JSONResults'): ##Directory to save the JSON files with identified secrets.
       print("Does not Exist!")
       os.mkdir('JSONResults') 
    
    dir_list = next(os.walk(path))[1]
    for dir_ in dir_list:
                dirPath = os.path.join(path, dir_)
                print(dirPath)
                Q.put(dirPath)

    
    while Q.empty() is False:
        if (threading.active_count() < (threads_limit + 1)):
                    t = threading.Thread(target=scanDir, args=(Q.get(),))
                    t.daemon = True
                    t.start()
                    threads_state.append(t)

        else:
                    time.sleep(0.5)
        


    for _ in threads_state:
        _.join()
    
        
if __name__ == '__main__':
    output_path =  '/path/to/directory/with/cloned/repositories'
    pywalker(output_path)

# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 10:06:01 2018

@author: aakanksha

python clone_thread.py --filepath  /pathto/file --outputpath /pathto/storeresults

"""

import argparse
try:
    from pip import main as pipmain
except:
    from pip._internal import main as pipmain
try:
    import git
except ImportError:
    pipmain(['install', 'gitpython']) ##Needs GitSCM for windows and add git to your path
    import git


from git import Repo
import threading
#import del_func
import glob
import logging
from time import gmtime, strftime
from multiprocessing import Process
from git import (
    Reference,
    Head,
    TagReference,
    RemoteReference,
    Commit,
    SymbolicReference,
    GitCommandError,
    RefLog
)
#import repo_scan
#import git_history
import os
try:
    import queue
except ImportError:
    import Queue as queue
import time


logging.basicConfig(filename="sample.log", filemode="w", level=logging.INFO)

    
def cloneRepo(URL, cloningpath, username=None, token=None):
    """
    Clones a single GIT repository.
    Input:-
    URL: GIT repository URL.
    cloningPath: the directory that the repository will be cloned at.
    Optional Input:-
    username: Github username.
    token: Github token or password.
    """
    try:
        try:
            if not os.path.exists(cloningpath):
                os.mkdir(cloningpath)
        except Exception:
            pass
        URL = URL.replace("git://", "https://")
        if (username or token) is not None:
            URL = URL.replace("https://", "https://{}:{}@".format(username, token))
        repopath = URL.split("/")[-2] + "_" + URL.split("/")[-1]
        #print(repopath)
        if repopath.endswith(".git"):
            repopath = "_git_" + repopath[:-4]
            print(repopath)
        if '@' in repopath:
            repopath = repopath.replace(repopath[:repopath.index("@") + 1], "")
        fullpath = cloningpath + "/" + repopath
        with threading.Lock():
            logging.info(fullpath)

        if os.path.exists(fullpath):
            git.Repo(fullpath).remote().pull()

            
        else:
            repo = git.Repo.clone_from(URL, fullpath)
            for branch in repo.refs:
                #print (branch)
                if (
                        isinstance(branch, TagReference)
                        or str(branch) == "origin/HEAD"
                        or str(branch) == "origin/master"
                        or not str(branch).startswith("origin")
                   ):
                    continue
                branch = str(branch).replace('origin/', '')
                git.Repo.clone_from(URL, fullpath + "/" + branch, branch = branch) ##Cloning all the branches of the Repository
            

    except Exception as e:
        logging.error("Error: There was an error in cloning [{}]".format(URL))
        logging.error(e)
        
        
    
def cloneBulkRepos(URLs, cloningPath, threads_limit=20, username=None, token=None):
    """
    Clones a bulk of GIT repositories.
    Input:-
    URLs: A list of GIT repository URLs.
    cloningPath: the directory that the repository will be cloned at.
    Optional Input:-
    threads_limit: The limit of working threads.
    username: Github username.
    token: Github token or password.
    """

    Q = queue.Queue()
    threads_state = []
    for URL in URLs:
        Q.put(URL)

    while Q.empty() is False:
        if (threading.active_count() < (threads_limit + 1)):
            t = threading.Thread(target=cloneRepo, args=(Q.get(), cloningPath,), kwargs={"username": username, "token": token})
            t.daemon = True
            t.start()
            threads_state.append(t)
        else:
            time.sleep(0.5)


    for _ in threads_state:
        _.join()

    
def main(filepath):
    """
    The main function.
    """    
    username=None
    token=None
    threads_limit = 20
    URLs = []


    try:
        with open(filepath) as fp:
            for cnt, line in enumerate(fp):
                if line == '\n':
                    continue
                repo_name = line.split("/")[-1]
                URLs.extend(line.split())
                logging.info("repo_name:  " + repo_name)
    except Exception as e:
        logging.error(e)
        
    
    URLs = list(set(URLs))    
    logging.info(URLs)
    cloneBulkRepos(URLs, output_path, threads_limit=threads_limit,  username=username, token=token)


if (__name__ == "__main__"):
    
    parser = argparse.ArgumentParser(description='Find secrets hidden in the depths of git.')
    parser.add_argument('-f','--filepath', dest="filepath", help="File containing list of repositories to scan.")
    parser.add_argument('-o','--outputpath', dest="outputpath", help="The path where repositories will be cloned.")
    parser.add_argument('-y', '--history', help='Scan History of a Repo.Note: This would increase the space and time required for the scan.', dest="history", default=False)
    
    args = parser.parse_args()
    
    output_path = args.outputpath
    filepath = args.filepath
    
    try:
        main(filepath)
        print(output_path)
        #git_scan.pywalker(output_path)
        for file in glob.glob("JSONResults/*.json"):
            if os.stat(file).st_size == 34:
                os.remove(file)
        
        if args.history:
            git_history.pywalker(output_path)
            for file in glob.glob("JSONHistory/*.json"):
                if os.stat(file).st_size == 34:
                    os.remove(file)   
            
        final_path = output_path.replace('/', "\\")
        #del_func.deleteDir(final_path)
        
    except KeyboardInterrupt:
            print('\nKeyboardInterrupt Detected.')
            print('\nExiting...')
            exit(0)


import os
import sys
import time
import glob
import datetime
import sqlite3
import numpy as np

def setup_path():
    # path to the Million Song Dataset code
    # CHANGE IT TO YOUR LOCAL CONFIGURATION
    msd_code_path='/home/ubuntu/project/helper_functions/MSongsDB'
    assert os.path.isdir(msd_code_path),'wrong path' # sanity check
    # we add some paths to python so we can import MSD code
    # Ubuntu: you can change the environment variable PYTHONPATH
    # in your .bashrc file so you do not have to type these lines
    sys.path.append( os.path.join(msd_code_path,'PythonSrc') )

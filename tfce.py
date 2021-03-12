import numpy as np
from array import array
import subprocess
import os

from config import *

def tfce(conf, df1,df2, title): #модифицированный пример из гитхаба Платона
    path_home = conf.path_home
    verbose = conf.verbose

    # create random data arrays
    A = df1
    A = A.transpose()
    B = df2
    B = B.transpose()
    subject_count = A.shape[0]
    data_length = A.shape[1]
    # check that python outputs data to binary files with expected byte count
    assert array("B", [0]).itemsize == 1
    assert array("I", [0]).itemsize == 4
    assert array("d", [0]).itemsize == 8

# write input data to file
    data_file = open("data.bin", "wb")
    array("I", [subject_count]).tofile(data_file)
    for s in range(subject_count):
        array("I", [data_length]).tofile(data_file)
        array("d", A[s]).tofile(data_file)
        array("I", [data_length]).tofile(data_file)
        array("d", B[s]).tofile(data_file)
    data_file.close()
    if verbose:
        print(f'Channel {title} is being processed')
        print(f'df1 shape is {df1.shape}')
    # call libtfce binary
    subprocess.call([
        path_home + 'libtfce',
    #    "--explore",
        "-e", "1",
        "-h", "2",
        "--input-file", "data.bin",
        "--output-file", f"{title}.bin",
        "--permutation-count", "1000",
        "--type", "1d"],
        stderr=subprocess.DEVNULL)

    # read result back

    result_file = open(f"{title}.bin", "rb")
    result_size = array("I", [])
    result_size.fromfile(result_file, 1)
    result = array("B", [])
    result.fromfile(result_file, result_size[0])
    result = result.tolist()
    result_file.close()
#    print(result)
    return (result)

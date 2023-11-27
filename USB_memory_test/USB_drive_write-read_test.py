"""
USB flash drive speed and reliability test
Write one file of random integers
Copy it enough times to fill the drive
Compare all the files to the first one to verify drive integrity.
Erase all files, repeat.

17 November 2023
"""

import time
import os
import filecmp
import random
import pickle
import shutil



def main():
    
    iterations=300
    path='d:\\'
    file='testfile'
    
    comparison_errors=0
    
    for i in range (0,iterations):
        print('Cycle ', i+1, ' of ', iterations)
        # write a random file and fill drive with duplicates of it
        write_random_files(path)
        # compare all files with the zeroth one
        print ('verifying files.')
        # verify all the files
        good_compare=compare_files_with_zeroth(path,file)
        if not good_compare:
            comparison_errors += 1
        # delete all the files and start over
        remove_files_in_directory(path)
    print ('Total errors during ',iterations,' iterations: ', comparison_errors)
   
def write_random_files(path): # write random files in specified numbers to path
    file='testfile'
    tick=time.time()  # set a timer
    filenumber=0
    # Compute one file of random numbers and write it
    file_zero=path+file+'_'+str(filenumber)
    with open(file_zero, 'ab') as f:
        for _ in range(1,1000000):
            pickle.dump(random.getrandbits(32), f) # https://docs.python.org/3/library/pickle.html#
    # compute how many duplicates of that file to write
    filestats=os.stat(file_zero) # gives a list of several statistics.
    filesize=filestats.st_size
    disc_cap=shutil.disk_usage('d:')[0] # bytes
    number_of_files=int(disc_cap/filesize)
    print('writing ', number_of_files, ' files of size ',filesize)
    # make copies of that random file
    for filenumber in range(1,number_of_files):
        shutil.copyfile(file_zero, path+file+'_'+str(filenumber))
    tock=time.time()  # reset clock for process timing
    print('execution time: ', tock-tick, ' seconds')
    return number_of_files


def compare_files_with_zeroth(path, file):
    print('comparing files')
        # Get a list of all files in the directory
    files = os.listdir(path)
    files.remove('System Volume Information') # hidden in each directory
    # file to test other against
    file_number_0=path+file+'_'+str(0)
    # Iterate through the files and compare each with file 0
    compares=True # need to declare this outside the for loop
    for file_name in files:
        file_number_n = os.path.join(path, file_name)
        compares=filecmp.cmp(file_number_0, file_number_n, shallow=False)
        if compares:
            pass # print ('Files compare properly')
        else:
            print('Comparison error: ', file_name)
    return compares # returns only one flag per whole-directory iteration


def remove_files_in_directory(directory_path):
    print('removing files')
    # Get a list of all files in the directory
    files = os.listdir(directory_path)
    # Iterate through the files and remove them
    for file_name in files:
        file_path = os.path.join(directory_path, file_name)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                #print(f"Removed: {file_path}")
        except Exception as e:
            print(f"Error removing {file_path}: {e}")


if __name__ == '__main__':
    print('starting main()')
    main()

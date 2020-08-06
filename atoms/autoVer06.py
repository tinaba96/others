import glob
import sys
import os
import copy
import subprocess as sp


def cp(center_name, shake_int, dir_init_word, cent):
    target_dir_list = glob.glob(dir_init_word+'*.dat')  #list of datfile
    target_dir_list.sort()
    center_n = -1

    for tdi in range(len(target_dir_list)):
        if center_name in target_dir_list[tdi]:
            center_n = tdi

    if center_n==-1:
        return(-1)

    ret = []

    shell_cmd1 = 'qsub -v param='
    shell_cmd2 = ' go2.sh'

    for i in shake_int:
        ret.append(target_dir_list[center_n+i])
        shell_cmd = shell_cmd1+str(cent+i)+shell_cmd2
        cp_sub(target_dir_list[center_n], target_dir_list[center_n+i], shell_cmd, center_n)

    return(ret)


def cp_sub(center_dir_name, target_dir_name, shell_cmd=None, num=None):
    center_dat_name = glob.glob(center_dir_name) #current file
    target_dat_name = glob.glob(target_dir_name) #next file

    if done_check([target_dir_name], num):
        print 'The job has already done in "' + target_dir_name + '"'
        return
    
    key_words_1 = '<Atoms.SpeciesAndCoordinates'
    key_words_2 = 'Atoms.SpeciesAndCoordinates>'
    data = []
    flag = 0

    while not os.path.exists(center_dat_name[0]+'#'):
        continue
        
    print 'reading dat# starting :',  center_dat_name[0] + '#'

    while True:
	    if open(center_dat_name[0]+'#', 'r'):
		    for line in open(center_dat_name[0]+'#', 'r'):
			if key_words_1 in line:
			    flag = 1
			    continue
			if key_words_2 in line:
			    flag = 0
			    break
			if flag==1:
			    data.append(line)
		    if len(data) != 8: #not enough data
			continue
		    else: #enough data -> finish
    			print 'reading dat# finished : ', center_dat_name[0] + '#'
			break
	    else:
		continue
	
    
    f = open(target_dat_name[0]+'.backup', 'w')
    for line in open(target_dat_name[0], 'r'):
        f.write(line)
    f.close()
    
    flag = 0
    count = 0
    f = open(target_dat_name[0], 'w')
    for line in open(target_dat_name[0]+'.backup', 'r'):
        if key_words_2 in line:
            flag = 0
        if flag==1:
            if count < 8:
                f.write(data[count])
                count += 1
            else:
                flag = 0
        else:
            f.write(line)
    
        if key_words_1 in line:
            flag = 1
    f.close()

    if shell_cmd is not None:
        res = sp.check_call(shell_cmd, shell=True)  #throw the command
        print' ==> running command : ', shell_cmd

def done_check(ret, num):
    count = 0
    for d in ret:
        l = glob.glob(str(num)+'.out')
        if len(l)!=0:
            count += 1

    if len(ret)==count:
        return(True)
    else:
        return(False)
            
if __name__=='__main__':
    dir_ini_word = 'p-p1' #this is not an important variable
    shell_cmd1 = 'qsub -v param='
    shell_cmd2 = ' go2.sh'

    center_n = 392  #center
    n_min = 370  #target
    n_max = 400  #target
    
    lc = center_n - 1
    rc = center_n + 1
    ret = cp(str(center_n), [-1, 1], dir_ini_word, center_n)

    if ret==-1:
        print('There is no that center in this directory')
        sys.exit()

    lflag = True
    rflag = True
    lret = copy.deepcopy(ret)
    rret = copy.deepcopy(ret)
    while lflag or rflag:
        if lflag: # going down
            lret = cp(str(lc), [-1], dir_ini_word, lc)
            lc -= 1
            while lret==-1:
                if lc < (n_min+1):
                    lflag = False
                    lret = []
                    break
                lret = cp(str(lc), [-1], dir_ini_word, lc)
                lc -= 1

            if lc < (n_min+1):
                lflag = False

        if rflag: # going up 
            rret = cp(str(rc), [1], dir_ini_word, rc)
            rc += 1
            while rret==-1:
                if (n_max-1) < rc:
                    rflag = False
                    rret = []
                    break
                rret = cp(str(rc), [1], dir_ini_word, rc)
                rc += 1
            if (n_max-1) < rc:
                rflag = False

    print 'all done'

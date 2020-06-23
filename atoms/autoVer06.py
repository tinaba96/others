import glob
import sys
import os
import copy
import subprocess as sp

def cp(center_name, shake_int, dir_init_word, shell_cmd=None):
    target_dir_list = glob.glob(dir_init_word+'*')
    target_dir_list.sort()
    center_n = -1
    for tdi in range(len(target_dir_list)):
        if center_name in target_dir_list[tdi]:
            center_n = tdi

    if center_n==-1:
        return(-1)

    ret = []
    #print target_dir_list[center_n]+':'
    for i in shake_int:
        #print target_dir_list[center_n+i]
        if i < 0:
            print 'cp :', target_dir_list[center_n+i], '<--', target_dir_list[center_n]
        else:
            print 'cp :', target_dir_list[center_n], '-->', target_dir_list[center_n+i]
        ret.append(target_dir_list[center_n+i])
        cp_sub(target_dir_list[center_n], target_dir_list[center_n+i], shell_cmd)
        print

    return(ret)
        
def cp_sub(center_dir_name, target_dir_name, shell_cmd=None):
    #center_dat_name = glob.glob(center_dir_name+'/*.dat')[0]
    #target_dat_name = glob.glob(target_dir_name+'/*.dat')[0]
    center_dat_name = glob.glob('/*.dat')[0]
    target_dat_name = glob.glob(target_dir_name+'/*.dat')[0]

    #print 'center_dat_name = ' + center_dat_name
    #print 'target_dat_name = ' + target_dat_name

    if done_check([target_dir_name]):
        print 'The job has already done in "' + target_dir_name + '"'
        return
    
    key_words_1 = '<Atoms.SpeciesAndCoordinates'
    key_words_2 = 'Atoms.SpeciesAndCoordinates>'
    data = []
    flag = 0
    for line in open(center_dir_name+'/'+center_dat_name+'#', 'r'):
        if key_words_1 in line:
            flag = 1
            continue
        if key_words_2 in line:
            flag = 0
            break
        if flag==1:
            data.append(line)
    
    f = open(target_dir_name+'/'+target_dat_name+'.backup', 'w')
    for line in open(target_dir_name+'/'+target_dat_name, 'r'):
        f.write(line)
    f.close()
    
    flag = 0
    count = 0
    f = open(target_dir_name+'/'+target_dat_name, 'w')
    for line in open(target_dir_name+'/'+target_dat_name+'.backup', 'r'):
        if key_words_2 in line:
            flag = 0
    
        if flag==1:
            #print line.strip(), '-->', data[count].strip()
            f.write(data[count])
            count += 1
        else:
            f.write(line)
    
        if key_words_1 in line:
            flag = 1
    f.close()

    if shell_cmd is not None:
        #os.system('cd '+target_dir_name+'; '+shell_cmd)
        #print 'cd '+target_dir_name+'; '+shell_cmd
        res = sp.check_call('cd '+target_dir_name+'; '+shell_cmd, shell=True)
        #print res

def done_check(ret):
    count = 0
    for d in ret:
        l = glob.glob(d+'/*.out')
        if len(l)!=0:
            count += 1

    if len(ret)==count:
        return(True)
    else:
        return(False)
            
if __name__=='__main__':
    dir_ini_word = 'p-ap2'
    shell_cmd = 'qsub go2.sh'

    center_n = 392
    n_min = 370
    n_max = 400
    
    lc = center_n - 1
    rc = center_n + 1

    ret = cp(str(center_n), [-1, 1], dir_ini_word, shell_cmd)

    if ret==-1:
        print 'There is no that center in this directory'
        sys.exit()

    while not done_check(ret):
        pass

    lflag = True
    rflag = True
    lret = copy.deepcopy(ret)
    rret = copy.deepcopy(ret)
    while lflag or rflag:
        if done_check(lret) and lflag:
            lret = cp(str(lc), [-1], dir_ini_word, shell_cmd)
            lc -= 1
            while lret==-1:
                if lc < (n_min+1):
                    lflag = False
                    lret = []
                    break
                lret = cp(str(lc), [-1], dir_ini_word, shell_cmd)
                lc -= 1

            if lc < (n_min+1):
                lflag = False


                
        if done_check(rret) and rflag:
            rret = cp(str(rc), [1], dir_ini_word, shell_cmd)
            rc += 1
            while rret==-1:
                if (n_max-1) < rc:
                    rflag = False
                    rret = []
                    break
                rret = cp(str(rc), [1], dir_ini_word, shell_cmd)
                rc += 1

            if (n_max-1) < rc:
                rflag = False

        #print 'lc, lf =', lc, lflag, ': rc, rf  =', rc, rflag
                
    print 'done'

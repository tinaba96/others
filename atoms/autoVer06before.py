import glob
import sys
import os
import copy
import subprocess as sp

def cp(center_name, shake_int, dir_init_word, cent):
#def cp(center_name, shake_int, dir_init_word, shell_cmd=None):
    #target_dir_list = glob.glob(dir_init_word+'*')  #list of datfile
    target_dir_list = glob.glob(dir_init_word+'*.dat')  #list of datfile
    target_dir_list.sort()
    #print(target_dir_list)
    center_n = -1

    for tdi in range(len(target_dir_list)):
        if center_name in target_dir_list[tdi]:
            center_n = tdi

    if center_n==-1:
        return(-1)

    ret = []

    shell_cmd1 = 'qsub -v param='
    shell_cmd2 = ' go2.sh'

    #print target_dir_list[center_n]+':'
    for i in shake_int:
	'''
        #print target_dir_list[center_n+i]
        if i < 0:
            #print 'cp :', target_dir_list[center_n+i], '<--', target_dir_list[center_n]
            #print('lcreal :', lc, ' : ', shell_cmd1+str(lc+i)+shell_cmd2)
            #shell_cmd = shell_cmd1+str(lc+i)+shell_cmd2
        else:
            #print 'cp :', target_dir_list[center_n], '-->', target_dir_list[center_n+i]
            #print('rcreal :', rc, ' : ', shell_cmd1+str(rc+i)+shell_cmd2)
            #shell_cmd = shell_cmd1+str(rc+i)+shell_cmd2
	'''
        ret.append(target_dir_list[center_n+i])
        shell_cmd = shell_cmd1+str(cent+i)+shell_cmd2
        cp_sub(target_dir_list[center_n], target_dir_list[center_n+i], shell_cmd, center_n)
        #cp_sub(target_dir_list[center_n], target_dir_list[center_n+i], shell_cmd)
        #print('check')

    return(ret)


def cp_sub(center_dir_name, target_dir_name, shell_cmd=None, num=None):
    #center_dat_name = glob.glob(center_dir_name+'/*.dat')[0]
    #target_dat_name = glob.glob(target_dir_name+'/*.dat')[0]
    #center_dat_name = glob.glob(center_dir_name+'/*.dat')
    #target_dat_name = glob.glob(target_dir_name+'/*.dat')
    center_dat_name = glob.glob(center_dir_name)
    target_dat_name = glob.glob(target_dir_name)

    #print 'center_dat_name = ' + center_dat_name
    #print 'target_dat_name = ' + target_dat_name

    if done_check([target_dir_name], num):
        print 'The job has already done in "' + target_dir_name + '"'
        return
    
    key_words_1 = '<Atoms.SpeciesAndCoordinates'
    key_words_2 = 'Atoms.SpeciesAndCoordinates>'
    data = []
    flag = 0

    while not os.path.exists(center_dat_name[0]+'#'):
        continue
        
    #for line in open(center_dir_name+'/'+center_dat_name+'#', 'r'):
    print('reading dat# starting : ', center_dat_name[0] + '#')

    while True:
	    if open(center_dat_name[0]+'#', 'r'):
		    for line in open(center_dat_name[0]+'#', 'r'):
			#print('line', line)
			if key_words_1 in line:
			    #print('check flag')
			    flag = 1
			    continue
			if key_words_2 in line:
			    flag = 0
			    break
			if flag==1:
			    #print('check append')
			    data.append(line)
		    if len(data) != 8:
			#print 'waiting'
			continue
		    else:
    			print('reading dat# finished : ', center_dat_name[0] + '#')
			break
	    else:
		#print 'continue'
		continue
	
    
    #f = open(target_dir_name+'/'+target_dat_name+'.backup', 'w')
    f = open(target_dat_name[0]+'.backup', 'w')
    for line in open(target_dat_name[0], 'r'):
    #for line in open(target_dir_name+'/'+target_dat_name, 'r'):
        f.write(line)
    f.close()
    
    flag = 0
    count = 0
    #f = open(target_dir_name+'/'+target_dat_name, 'w')
    f = open(target_dat_name[0], 'w')
    #for line in open(target_dir_name+'/'+target_dat_name+'.backup', 'r'):
    for line in open(target_dat_name[0]+'.backup', 'r'):
        if key_words_2 in line:
            flag = 0
        if flag==1:
            #print('len(data)',  len(data))
            #print line.strip(), '-->', data[count].strip()
            #if count < len(data)-1:
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
        #os.system('cd '+target_dir_name+'; '+shell_cmd)
        #print 'cd '+target_dir_name+'; '+shell_cmd
        #res = sp.check_call('cd '+target_dir_name+'; '+shell_cmd, shell=True)
    	#print('count:', shell_cmd)
        res = sp.check_call(shell_cmd, shell=True)
        print' ==> running command : ', shell_cmd

def done_check(ret, num):
    count = 0
    for d in ret:
        #l = glob.glob(d+'/*.out')
        l = glob.glob(str(num)+'.out')
        if len(l)!=0:
            count += 1

    if len(ret)==count:
        return(True)
    else:
        return(False)
            
if __name__=='__main__':
    dir_ini_word = 'p-p1'
    shell_cmd1 = 'qsub -v param='
    shell_cmd2 = ' go2.sh'

    center_n = 392
    n_min = 370
    n_max = 400
    
    lc = center_n - 1
    rc = center_n + 1
    #print('check1')
    #ret = cp(str(center_n), [-1, 1], dir_ini_word, shell_cmd1+str(center_n)+shell_cmd2)
    ret = cp(str(center_n), [-1, 1], dir_ini_word, center_n)

    if ret==-1:
        print('There is no that center in this directory')
        sys.exit()

    #print('check2')
    #while not done_check(ret, center_n):
    #    pass

    #print('check3')
    lflag = True
    rflag = True
    lret = copy.deepcopy(ret)
    rret = copy.deepcopy(ret)
    while lflag or rflag:
        #print('1che')
        #if done_check(lret) and lflag:
        #if done_check(lret, lc+1) and lflag:
        if lflag:
            #print('lcshell :', shell_cmd1+str(lc)+shell_cmd2)
            #print('lcbefore :', lc)
            #lret = cp(str(lc), [-1], dir_ini_word, shell_cmd1+str(lc)+shell_cmd2)
            lret = cp(str(lc), [-1], dir_ini_word, lc)
            lc -= 1
            #print('lcafter :', lc)
            while lret==-1:
                if lc < (n_min+1):
                    lflag = False
                    lret = []
                    break
                lret = cp(str(lc), [-1], dir_ini_word, lc)
                #lret = cp(str(lc), [-1], dir_ini_word, shell_cmd1+str(lc)+shell_cmd2)
                #print('2ch')
                lc -= 1

            if lc < (n_min+1):
                lflag = False

        #if done_check(rret) and rflag:
        #if done_check(rret, rc-1) and rflag:
        if rflag:
            #print('rcshell :', shell_cmd1+str(rc)+shell_cmd2)
            #print('rcbefore:', rc)
            rret = cp(str(rc), [1], dir_ini_word, rc)
            #rret = cp(str(rc), [1], dir_ini_word, shell_cmd1+str(rc)+shell_cmd2)
            rc += 1
            #print('rcafter:', rc)
            while rret==-1:
                #print('4ch')
                if (n_max-1) < rc:
                    rflag = False
                    rret = []
                    break
                rret = cp(str(rc), [1], dir_ini_word, rc)
                #rret = cp(str(rc), [1], dir_ini_word, shell_cmd1+str(rc)+shell_cmd2)
                rc += 1

            if (n_max-1) < rc:
                rflag = False

        #print 'lc, lf =', lc, lflag, ': rc, rf  =', rc, rflag
                
    print 'done'

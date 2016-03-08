#coding=utf-8  
#-*- coding: utf-8 -*-
#!/usr/bin/python
      
import ftplib 
import os  
import socket 
import zipfile 
import time
import shutil

ftphost = '18.8.5.99'
ftpusrname = 'IUNI-release'
ftppwd = 'IUNI-release'
remote_file = '/U5-AlphaOS2.0_no_signd/'
#/N1-AlphaOS2.0/
unzip_file ='BBL7505A'
#U0001A02


def CHECKENV():
    if os.path.isdir(os.getcwd()+'/release'):
        shutil.rmtree(os.getcwd()+'/release')
    else:
        pass
    
    if os.path.isfile(os.getcwd()+'/Performance.html'):
        os.remove(os.getcwd()+'/Performance.html')
    else:
        pass
 
def DownloadROM():    
    print '****************START connecting FTP*************************'
    try:
        f=ftplib.FTP(ftphost)
        print '***Connected to ftphost "%s"' % ftphost       
    except:        
        for T in range(1,6):
            print 'NO'+T
            try:
                f=ftplib.FTP(ftphost)
                print '***Connected to ftphost "%s"' % ftphost
                break
            except:
                print 'ERROR:cannot reach " %s"' % ftphost
                f.quit()
 
    print '****************START login FTP*************************'
    try:
        f.login(ftpusrname,ftppwd)
        print '*** Logged in as "ftp-aurora"'
    except:        
        for Q in range(1,6):
            print 'NO' % Q
            try:
                f.login(ftpusrname,ftppwd)
                print '*** Logged in as "ftp-aurora"'
                break
            except:
                print ' login fAIL' 
           
#    print '****************START Download LK.BIN*************************'
#    try:
#        f.cwd(remote_fastboot)
#        fastboot_file = f.nlst()
#        for bat_file in fastboot_file:
#            f.retrbinary('RETR %s' %bat_file,open(bat_file,'wb').write)
#            print "*** Downloaded %s success" %bat_file    
#            
#    except:
#        print 'ERROR: cannot downloaded file "%s"' % bat_file
     
    print '****************START Search ROMFILE*************************'
    try:
        nowfile =f.nlst(remote_file)[-19]
        f.cwd(nowfile)
        ROMFILE =f.nlst(nowfile)[0].split('/')[-1]
    except :
        print '***cannot found ROMFILE'
        return
 
    print '*** Found "%s" ROMFILE success' % ROMFILE 
    #����Զ���ļ�
    print '****************START Download ROMFILE*************************'
    try:
        f.retrbinary('RETR %s' %ROMFILE,open(ROMFILE,'wb').write)
        print "*** Downloaded %s success" %ROMFILE
        f.close()
    except:
        print 'ERROR: cannot downloaded file "%s"' % ROMFILE
 
def unzip():
    for filename in os.listdir(os.getcwd()):
        if os.path.isfile(filename) and unzip_file in filename:
            try:
                file_zip =zipfile.ZipFile(filename,'r')    
                for newfile in file_zip.namelist():
                    file_zip.extract(newfile,os.getcwd())          
                print '*** zip success' 
            except:
                print"*** zip failed"
            file_zip.close()  
            os.remove(filename)
 
def Fastbootlk():
    print '****************START Fastboot LK.BIN*************************'
    try:
        print "*** rebooting into fastboot"
        os.system('adb reboot bootloader')
        print "*** fastboot lk.bin"
        os.system('fastboot flash lk lk.bin')
        print "*** rebooting......"
        os.system('fastboot reboot')
    except:
        print '***  Cannot fastboot lk.bin'
         
def FoundDevice():
    print '**************rebooting ,checkDevice....******************'
    a = True
    runtime = 0
    while a == True:
        time.sleep(180)
        deviceText = os.popen('adb get-state').readline()
        if 'device' in deviceText:
            print 'Find devices success.'
            time.sleep(30)
            a = False
        else:
            print 'Find device fial.'
            runtime += 1
            if runtime <= 5:
                print 'NO' + str(runtime) 
                continue
            else:
                print 'time out,stop running '
                exit()
 
def FastbootRom():    
    #fastboot ROM
    #os.system('sleep 120')
    print '****************START fastboot ROM*************************'
    try:
        for item in os.listdir(os.getcwd()):
            curfile = os.getcwd()+'//'+item
            if os.path.isdir(curfile):    
                for ROM in os.listdir(curfile):
                    os.chdir( curfile+'//'+ROM)
                    print ROM
        os.system('adb reboot bootloader')
        os.system('fastboot flash boot boot.img')
        os.system('fastboot flash system system.img')
#        os.system('fastboot flash userdata userdata.img')
#        os.system('fastboot flash persist persist.img')
        os.system('fastboot flash recovery recovery.img')
        os.system('fastboot reboot')
    except:
        print "*** cannot found ROMFILE"



def main():
    CHECKENV()  
    DownloadROM()
    unzip()
    Fastbootlk()
    FoundDevice()
    FastbootRom()     
    
if __name__ == '__main__':  
    main()

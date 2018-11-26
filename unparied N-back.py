#!/user/bin/python
#created by M Zhang on 02MAR2016

from psychopy import visual, sound, core, event,logging
from random import randint

#an example window to draw stimuli in
win=visual.Window([1024,768],fullscr=False,allowGUI=False,color=(-1.0,-1.0,-1.0))
# an example sequence for testing purpose
vsequence=[0,1,2,0,3,2,1,2,1,1]
asequence=[0,2,1,2,2,3,1,3,0,3]
#an example file
filename='unpaired.csv'

#unpaired nback task
#takes two sequences in argument
def unpaired (file, nback_no, window, vseq, aseq, trial_no=None, adaptive=False, duration=1.0):
    f=open(file,'w')
    audicode=['C','D','E','F']
    colorcode=['red','blue','green','yellow']
    trial_no=len(vseq)
    ready=visual.TextStim(window,'ready?', color=(1.0,1.0,1.0))
    vstimlist=[];astimlist=[]
    vtarget=[0,0];atarget=[0,0]
    n=0
    #create two stimuli lists and mark down target trials
    for i in vseq:
        vstimlist.append(visual.Rect(window,width=0.5,height=0.5,lineColor=colorcode[i],fillColor=colorcode[i], pos=(0,0)))
        astimlist.append(sound.Sound(audicode[aseq[n]],octave=4, sampleRate=44100, secs=duration,bits=8))
        if n > nback_no-1:
            #if the event match with n events ago (n specified by 'nback_no')
            #mark it as a target trial
            if i==vseq[n-nback_no]:
                vtarget.append(1)
            else:
                vtarget.append(0)
            if aseq[n]==aseq[n-nback_no]:
                atarget.append(1)
            else:
                atarget.append(0)
        n = n+1

    ready.draw()
    window.flip()
    event.waitKeys(keyList=['return'])
    n=0
    #play/draw stimuli and record response time
    for vtrial in vstimlist:
        response=None; hit=None; time=None;mod=None;target=False
        vtrial.draw()
        astimlist[n].play()
        starttime=window.flip()
        #each stimulus is displayed for the duration specified
        response=event.waitKeys(maxWait=duration-(1/120.0),keyList=['l'],timeStamped=True)
        while(logging.defaultClock.getTime() - starttime) <= duration:
            pass
        #Currently only RT for catch trials will be recorded
        if vtarget[n]==1 or atarget[n]==1:
            hit=False;target=True
            if vtarget[n]==1:
                mod='visual'
            else:
                mod='auditory'
            if response!=None:
                time=response[0][1]-starttime
                hit=True
        win.flip()
#output includes: condition, trial number, whether it's target, modality of target, whether a hit, RT
        f.write('%s, %d, %s, %s, %s, %s\n'%('unpaired', n+1, target, str(mod), str(hit), str(time)))
        n = n+1
        core.wait(0.5)
    f.close()

unpaired(filename, 2,win,vsequence,asequence)
win.close()
core.quit()
     
     
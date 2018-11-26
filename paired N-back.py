#!/user/bin/python
#created by M Zhang on 02MAR2016

from psychopy import visual, sound, core, event,logging
from random import randint

#an example window to draw stimuli in
win=visual.Window([1024,768],fullscr=False,allowGUI=False,color=(-1.0,-1.0,-1.0))
# an example sequence for testing purpose
sequence=[0,1,2,0,3,2,1,2,1,1]
#an example file
filename='paired.csv'

#paired nback task
#Currently auditory sequence and visual sequence are exactly the same, though it may not be the best way
#think about this later
def paired (file, nback_no, window, seq, trial_no=None, adaptive=False, duration=1.0):
    f=open(file,'w')
    #pairing rule is [C-red,D-blue,E-green,F-yellow]
    audicode=['C','D','E','F']
    colorcode=['red','blue','green','yellow']
    trial_no=len(seq)
    ready=visual.TextStim(window,'ready?', color=(1.0,1.0,1.0))
    vstimlist=[];astimlist=[]
    target=[0,0]
    n=0
    #create two stimuli lists and mark down target trials
    for i in seq:
        vstimlist.append(visual.Rect(window,width=0.5,height=0.5,lineColor=colorcode[i],fillColor=colorcode[i], pos=(0,0)))
        astimlist.append(sound.Sound(audicode[i],octave=4, sampleRate=44100, secs=duration,bits=8))
        if n > nback_no-1:
            #if the event match with n events ago (n specified by 'nback_no')
            #mark it as a target trial
            if i==seq[n-nback_no]:
                target.append(1)
            else:
                target.append(0)
        n = n+1

    ready.draw()
    window.flip()
    event.waitKeys(keyList=['return'])
    n=0
    #play/draw stimuli and record response time
    for vtrial in vstimlist:
        response=None; hit=None; time=None
        vtrial.draw()
        astimlist[n].play()
        starttime=window.flip()
        #each stimulus is displayed for the duration specified
        response=event.waitKeys(maxWait=duration-(1/120.0),keyList=['l'],timeStamped=True)
        while(logging.defaultClock.getTime() - starttime) <= duration:
            pass
        #Currently only RT for catch trials will be recorded
        if target[n]==1:
            hit=False
            if response!=None:
                time=response[0][1]-starttime
                hit=True
        win.flip()
#output includes: condition, trial number, whether it's target, whether a hit, RT
        f.write('%s, %d, %s, %s, %s\n'%('paired', n+1, str(target[n]==1), str(hit), str(time)))
        n = n+1
        core.wait(0.5)
    f.close()

paired(filename, 2,win,sequence)
win.close()
core.quit()
     
     
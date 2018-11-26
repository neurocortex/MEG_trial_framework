#!/user/bin/python
#created by M Zhang on 13FEB2016

from psychopy import visual, sound, core, event,logging

#an example window to draw stimuli in
win=visual.Window([1024,768],fullscr=False,allowGUI=False,color=(-1.0,-1.0,-1.0))
# an example sequence for testing purpose
sequence=[0,1,2,0,3,2,1,2,1,1]
#an example file
filename='anback.csv'

#auditory nback task
def anback (file, nback_no, window, seq, trial_no=None, adaptive=False, duration=1.0):
    f=open(file,'w')
    audicode=['C','D','E','F']
    trial_no=len(seq)
    ready=visual.TextStim(window,'ready?', color=(1.0,1.0,1.0))
    cross=visual.TextStim(window,'+',color='white')
    stimlist=[]
    target=[0,0]
    n=0
    #create stimuli list and mark down target trials
    for i in seq:
        stimlist.append(sound.Sound(audicode[i],octave=4, sampleRate=44100, secs=duration,bits=8))
        if n > nback_no-1:
            #if the event match with the one n events ago (n specified by argument 'nback_no')
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
    #play stimuli and record response time
    for trial in stimlist:
        response=None; hit=None; time=None
        cross.draw()
        trial.play()
        starttime=window.flip()
        #each stimulus is played for the duration specified
        response=event.waitKeys(maxWait=duration-(1/120.0),keyList=['l'],timeStamped=True)
        while(logging.defaultClock.getTime() - starttime) <= duration:
            pass
        #Currently only RT for catch trials will be recorded
        if target[n]==1:
            hit=False
            if response!=None:
                time=response[0][1]-starttime
                hit=True
        #output includes: condition, trial number, whether it's target, whether a hit, RT
        f.write('%s, %d, %s, %s, %s\n'%('auditory', n+1, str(target[n]==1), str(hit), str(time)))
        n = n+1
        win.flip()
        core.wait(0.5)
    f.close()

anback(filename, 2,win,sequence)
win.close()
core.quit()
     
     
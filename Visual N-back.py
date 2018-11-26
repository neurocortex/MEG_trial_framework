#!/user/bin/python
#created by M Zhang on 13FEB2016

from psychopy import visual, core, event,logging

#an example window to draw stimuli in
win=visual.Window([1024,768],fullscr=False,allowGUI=False,color=(-1.0,-1.0,-1.0))
# an example sequence for testing purpose
sequence=[0,1,2,0,3,2,1,2,1,1]
#an example file
filename='vnback.csv'

#visual nback task
def vnback (file, nback_no, window, seq, trial_no=None, adaptive=False, duration=1.0):
    f=open(file,'w')
    colorcode=['red','blue','green','yellow']
    trial_no=len(seq)
    ready=visual.TextStim(window,'ready?', color=(1.0,1.0,1.0))
    stimlist=[]
    target=[0,0]
    n=0
    #create stimuli list and mark down target trials
    for i in seq:
        stimlist.append(visual.Rect(window,width=0.5,height=0.5,lineColor=colorcode[i],fillColor=colorcode[i], pos=(0,0)))
        if n > nback_no-1:
            #if the event match with the one n events ago (n specified by 'nback_no')
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
    #draw stimuli and record response time
    for trial in stimlist:
        response=None; hit=None; time=None
        trial.draw()
        starttime=window.flip()
        #each stimulus is presented for the duration specified
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
        f.write('%s, %d, %s, %s, %s\n'%('visual', n+1, str(target[n]==1), str(hit), str(time)))
        n = n+1
        win.flip()
        core.wait(0.3)
    f.close()

vnback(filename, 2,win,sequence)
win.close()
core.quit()
     
     
'''
    framework for running behavioral N-back tests  
    
    TODO:
    -fix auditiory stimuli list creation bug (nback_tests.py, line:243)
'''
        
#imports
from psychopy import visual,core
from random import randint, shuffle
import csv
from nback_tests import vNback, aNback, nInterleaved, nPaired, nUnpaired

     
#structures
wnd = visual.Window([1024,768],fullscr=False,allowGUI=True,units='pix',color=(-1,-1,-1)) #psychopy window
funcLis = [] #list to hold all testing functions
'''
output file writer, takes command line input (from experimenter)and creates
a .csv file with that name. Could be improved, but gives us some control
'''
outName = raw_input('output file name/subject identifier: ') + '.csv'
#outName = '.csv' #use this line if you need to manually set output file for debugging or whatever
outFile = open(outName, 'wb')
outWr = csv.writer(outFile)


#functions
def seqGen(length): #this is for generating test sequences, returns a list of desired length
    seq = []    
    for i in range(length):
        seq.append(randint(0,3))
    return seq        

    
def popFuncLis(lis):
    '''
    within here all the test functions should be appeneded to the funcLis list, ie. all the tests we will run
    a few more conditions need to be created (I think?) and one needs fixing- but the rest work! pretty good going
    thus far
    '''
    funcLis.append(vNback)
    funcLis.append(aNback)
    funcLis.append(nInterleaved)
    funcLis.append(nPaired)
    funcLis.append(nUnpaired) #this function is broken, specifically building the note list
    
    return 0


#main
if __name__ == '__main__':
    popFuncLis(funcLis) #populate list of test functions
    shuffle(funcLis) #randomize order of tests performed
    
    wnd.flip() #initialize window    
    
    #loop that executes test functions
    for test in funcLis:
        print str(test)+": test started" #for debugging
        test(outWr, 2, wnd, seqGen(5))#filled with the generic arguments for all our test functions
        print str(test)+": test ended"        
        #outFile.close()
    outFile.close()
    wnd.close()
    print "tetst concluded"    
    

    
    
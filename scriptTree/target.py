#!/usr/bin/env python

#Copyright (C) 2011 by Benedict Paten (benedictpaten@gmail.com)
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

import sys
from sonLib.bioio import system

class Target(object):
    """Each job wrapper extends this class.
    """
    
    def __init__(self, time=sys.maxint, memory=sys.maxint, cpu=sys.maxint):
        """This method must be called by any overiding constructor.
        """
        self.__followOn = None
        self.__children = []
        self.__childCommands = []
        self.__memory = memory
        self.__time = time #This parameter is no longer used.
        self.__cpu = cpu
        self.globalTempDir = None
        if self.__module__ == "__main__":
            raise RuntimeError("The module name of class %s is __main__, which prevents us from serialising it properly, \
please ensure you re-import targets defined in main" % self.__class__.__name__)
        self.importStrings = set((".".join((self.__module__, self.__class__.__name__)),))
        self.loggingMessages = []

    def run(self):
        """Do user stuff here, including creating any follow on jobs.
        This function must not re-pickle the pickle file, which is an input file.
        """
        pass
    
    def setFollowOnTarget(self, followOn):
        """Set the follow on target.
        Will complain if follow on already set.
        """
        assert self.__followOn == None
        self.__followOn = followOn
        
    def addChildTarget(self, childTarget):
        """Adds the child target to be run as child of this target.
        """
        self.__children.append(childTarget)
    
    def addChildCommand(self, childCommand, runTime=sys.maxint):
        """A command to be run as child of the job tree.
        """
        self.__childCommands.append((str(childCommand), float(runTime)))
    
    def getRunTime(self):
        """Get the time the target is anticipated to run.
        """
        return self.__time
    
    def getGlobalTempDir(self):
        """Get the global temporary directory.
        """
        #Check if we have initialised the global temp dir - doing this
        #just in time prevents us from creating temp directories unless we have to.
        if self.globalTempDir == None:
            self.globalTempDir = self.stack.getGlobalTempDir()
        return self.globalTempDir
    
    def getLocalTempDir(self):
        """Get the local temporary directory.
        """
        return self.stack.getLocalTempDir()
        
    def getMemory(self):
        """Returns the number of bytes of memory that were requested by the job.
        """
        return self.__memory
    
    def getCpu(self):
        """Returns the number of cpus requested by the job.
        """
        return self.__cpu
    
    def getFollowOn(self):
        """Get the follow on target.
        """
        return self.__followOn
     
    def getChildren(self):
        """Get the child targets.
        """
        return self.__children[:]
    
    def getChildCommands(self):
        """Gets the child commands, as a list of tuples of strings and floats, representing the run times.
        """
        return self.__childCommands[:]
    
    def logToMaster(self, string):
        """Send a logging message to the master. Will only reported if logging is set to INFO level in the master.
        """
        self.loggingMessages.append(str(string))
    
####
#Private functions
#### 
    
    def setGlobalTempDir(self, globalTempDir):
        """Sets the global temp dir.
        """
        self.globalTempDir = globalTempDir
        
    def isGlobalTempDirSet(self):
        return self.globalTempDir != None
    
    def setStack(self, stack):
        """Sets the stack object that is calling the target.
        """
        self.stack = stack
        
    def getMasterLoggingMessages(self):
        return self.loggingMessages[:]

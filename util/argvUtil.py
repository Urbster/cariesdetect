"""
    Utility to deal with command line arguments.

    In particular if idle is used, dealing with command line arguments
    and default values can be tedious.
"""

__License = \
"""
Copyright (c) 2010, Peter Roesch <Peter.Roesch@hs-augsburg.de>
All rights reserved.

This software is distributed WITHOUT ANY WARRANTY; without even
the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
PURPOSE. See LICENSE.TXT in a parent directory for more information.
"""

from sys import argv


def setArguments(descriptionsAndDefaults, useDefaultsUnconditionally = False):
    """
        Set argv list according to user input or to default values.

        @param descriptionsAndDefaults tuple of tuples containing descriptions
            and default values of command line parameters. Example:
            ( ('description1', 'default1'), ('description2', 'default2'))
        @param useDefaultsUnconditionally Flag indicating whether the user 
            should be asked for argv values (default) or whether the default 
            values should be applied without user input.
    """
    if len(argv) != 1 + len(descriptionsAndDefaults):
        arguments = []
        if (useDefaultsUnconditionally):
            for a in descriptionsAndDefaults:
                arguments.append(a[1])
        else:
            print "Enter arguments for '%s': " % (argv[0])
            print "    (Empty input accepts default values)"
            for a in descriptionsAndDefaults:
                tmpString = a[0] + "\n [%s]:" % (a[1])
                reply = raw_input(tmpString)
                if len(reply) > 0:
                    arguments.append(reply)
                else:
                    arguments.append(a[1])
        #
        # don't touch argv[0] which contains the name of the script
        argv[1:] = arguments

if __name__ == '__main__':
    import os
    #
    # check if running in idle (tested on debian and winXP)
    runningInIdle = False
    try:
        runningInIdle = 'idle-python' in __file__
    except:
        runningInIdle = True
    #
    # description of arguments
    descriptionsAndDefaults = (
        ('Name of input file:', 'myInFile'),
        ('Name of output file:', 'myOutFile',),
        ('Variance (mm)', '3')
    )
    #
    # use defaults if running in idle
    setArguments(descriptionsAndDefaults,
        useDefaultsUnconditionally = runningInIdle)
    #
    # print arguments
    print 'command line arguments:\n', argv


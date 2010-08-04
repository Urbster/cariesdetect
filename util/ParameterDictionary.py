from __future__ import with_statement
"""
    Utility to deal with parameter files.

    A parameter file is read and represented as a class.
"""

__License = \
"""
Copyright (c) 2010, Peter Roesch <Peter.Roesch@hs-augsburg.de>
All rights reserved.

This software is distributed WITHOUT ANY WARRANTY; without even
the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
PURPOSE. See LICENSE.TXT in a parent directory for more information.
"""

import os

class ParameterDictionary(object):
    """
    Create and manage dictionary from paramter file.

    # create dictionary from file \n
    parDict = ParameterDictionary('myTestFile') \n
    # Access to second component of parameter 'testPar': \n
    parDict.get('testPar')[1] \n
    # \n
    # File Format: \n
    # \n
    # comment 1 \n
    par1_Name par1_Val1 par1_Val2 ... \n
    # \n
    par2_Name par2_Val1 par2_Val2 \n

    """
    #
    # constructor
    #
    def __init__(self, parameterFileName, commentChar = '#'):
        """
        @param parameterFileName Name of parameter file
        @param commentChar Lines starting with this character are ignored.
            Default: '#'
        """
        self.__dictionary = {}
        self.__parameterFileName = parameterFileName
        with open(self.__parameterFileName) as inFile:
            for line in inFile:
                line = line.strip()
                if len(line) > 0 and line[0] != commentChar:
                    words = line.split()
                    self.__dictionary[words[0]] = words[1:]
    #
    # conversion to string
    #
    def __str__(self):
        return 'ParameterDictionary from file "' + \
            self.__parameterFileName + '":\n' + \
            str(self.__dictionary)
    #
    # access individual parameters
    #
    def get(self, paramName):
        """
        Find parameter, return None if parameter is not present.

        @param paramName Name of parameter to look for.
        @return parameter Value(s)
        """
        try:
            param = self.__dictionary[paramName]
        except:
            param = None
        return param
#
# minimal test / demo program
#
if __name__ == '__main__':
    #
    # create simple parameter file
    import tempfile
    tmpFile = tempfile.mkstemp(suffix = '.par')
    testFileName = tmpFile[1]
    os.write(tmpFile[0], '# comment 1\n\n  n1 pn1 pn2 pn3\n n2\n  ' + 
        'name3   bla         bli        blu\n')
    os.close(tmpFile[0])
    #
    # read file into dictionary
    parameterDict = ParameterDictionary(testFileName)
    os.remove(testFileName)
    print 'dictionary:\n', parameterDict
    print 'name3[2]:', parameterDict.get('name3')[2]


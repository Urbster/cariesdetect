"""
Helper functions to load and store 3D images
"""

__License = \
"""
Copyright (c) 2010, Peter Roesch <Peter.Roesch@hs-augsburg.de>
All rights reserved.

This software is distributed WITHOUT ANY WARRANTY; without even
the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
PURPOSE. See LICENSE.TXT in a parent directory for more information.
"""

import itk
import os

def createImageFileName(inImName):
    """
    Create the absolute path to an image file from the input string.

    If the parameter inImName does not correspond to an existing 
    file, the environment variable MED_BV_DATA_ROOT is read and inImName
    is regarded as a file name relative to the path specifide by
    MED_BV_DATA_ROOT.

    @param inImName Input image name.
    @return Absolute path to corresponding image file.
    """
    defaultDirName = os.path.join(os.sep, 'GB', 'images3D')
    if not os.path.isfile(inImName):
        baseDirName = os.getenv('MED_BV_DATA_ROOT', defaultDirName)
        finalName = os.path.join(baseDirName, inImName)
    else:
        finalName = inImName
    if not os.path.isfile(finalName):
        print 'Error: image "%s" not found' % (inImName)
        return None
    else:
        return finalName


def readImage(imName, pixelType = itk.F, dim = 3, beVerbose = True):
    """
    read an image and return an itk reference.

    If the parameter inImName does not correspond to an existing image
    file, the environment variable MED_BV_DATA_ROOT is read and inImName
    is regarded as a file name relative to the path specifide by
    MED_BV_DATA_ROOT.
    
    @param imName Name of the image file (passed to createImageFileName)
    @param pixelType Type of pixels/voxels, default: itk.F
    @param dim Image dimension, default: 3
    @param beVerbose Flag determining wheterh a message is printed
        after the image has been loaded (default: True)
    @return Reference to the image
    @see createImageFileName
    """
    #
    # use absolute path or search in directory given in MED_BV_DATA_ROOT 
    imageFileName = createImageFileName(imName)
    if imageFileName:
        # 
        # set up and execute reader
        imageType = itk.Image[pixelType, dim]
        reader = itk.ImageFileReader[imageType].New(FileName = imageFileName)
        reader.Update()
        if beVerbose:
            print 'image "%s" read' % (imageFileName)
        return reader.GetOutput()

def writeImage(outFileName, input, beVerbose = True):
    """
    Write input to disk.
    
    @param outFileName Name of the output file
    @param input Reference to the object providing the input to store
    @param beVerbose Flag determining wheterh a message is printed
        after the input has been written (default: True)
    """
    #
    # set up and execute writer
    writer = itk.ImageFileWriter[input].New(Input = input,
                                            FileName = outFileName)
    writer.Update()
    if beVerbose:
        print 'file "%s" written' % (outFileName)

if __name__ == '__main__':
    # 
    # test / demo
    img = readImage(os.path.join('CThead', 'CThead_l3.mhd'))
    itk.echo(img)
    writeImage('/tmp/out.mhd', img)

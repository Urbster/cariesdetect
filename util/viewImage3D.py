"""
    Display 3D images and segmentations using external viewers.
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
import subprocess
import os
import tempfile
import imageIO
import threading


def __tmpFileFromImage(theImage, comment=''):
    """
        @param theImage Any possible input to an itk.ImageFileWriter,
            e.g. a reference to an itk.Image object.
        @param comment Comment to be included in the image file name.
        @return Name of the image file created.
    """

    if theImage == None:
        return None
    if len(comment) > 0:
        myPrefix = comment + '___'
    else:
        myPrefix = ''
    #
    # create temporary file, use the file name and discard the actual file
    outFile = tempfile.mkstemp(suffix = '.mhd', prefix = myPrefix)
    imName = outFile[1]
    os.close(outFile[0])
    #
    # store the image and return file name
    imageIO.writeImage(imName, theImage, beVerbose=False)
    return imName

def __viewImage(greyImage, segmentationImage=None, comment='',
        viewerCommand=''):
    """
        Display an image using an image viewer.

        The environment variable MED_BV_VIEWER_COMMAND specifies the
        location of the itksnap command used for image display.
        
        @param greyImage Either an image file name or an itk image instance.
        @param segmentationImage Either an image file name or an itk image 
            instance corresponding to the segmentation result. Default: None.
        @param comment Comment to be incorporated in temporary file name.
        @param viewerCommand Full path to image viewer command.
    """
    #
    # names of temporary files to be removed after the viewer is closed
    tmpFileNameList = []
    #
    # get name of grey value image
    if type(greyImage) == type('str'):
        greyImageName = imageIO.createImageFileName(greyImage)
    else:
        greyImageName = __tmpFileFromImage(greyImage, comment)
        if greyImageName != None:
            tmpFileNameList.append(greyImageName)
        else:
            return
    #
    # get name of image containing segmentation results
    if type(segmentationImage) == type('str'):
        segmentationImageName = imageIO.createImageFileName(segmentationImage)
    else:
        segmentationImageName = __tmpFileFromImage(segmentationImage)
        if segmentationImageName != None:
            tmpFileNameList.append(segmentationImageName)
    #
    # path to the image viewer executable, use environment variable if present
    if viewerCommand == '':
        viewerCommand = os.getenv('MED_BV_VIEWER_COMMAND', 
            os.path.join(os.path.sep, 'GB', 'itksnap', 'bin', 'itksnap'))
    if segmentationImageName != None:
        command = [viewerCommand, '-g', greyImageName, 
            '-s', segmentationImageName]
    else:
        command = [viewerCommand, greyImageName]
    # 
    # execute viewer 
    viewProcess = subprocess.Popen(command)
    viewProcess.wait()
    # 
    # remove temporary files after viewer has been closed
    for fileName in tmpFileNameList:
        os.remove(fileName)
        os.remove(fileName[:-3] + 'raw')

def viewImage(greyImage, segmentationImage=None, comment='', viewerCommand=''):
    """
        Display an image using an image viewer run in a separate thread.

        The environment variable MED_BV_VIEWER_COMMAND specifies the
        location of the itksnap command used for image display.
        
        @param greyImage Either an image file name or an itk image instance.
        @param segmentationImage Either an image file name or an itk image 
            instance corresponding to the segmentation result. Default: None.
        @param comment Comment to be incorporated in temporary file name.
        @param viewerCommand Full path to image viewer command.
            Default: '/GB/itksnap/bin/itksnap'
    """
    #
    # create and start thread executing the __viewImage function
    myThread = threading.Thread(target=__viewImage,
        args= (greyImage, segmentationImage, comment, viewerCommand))
    myThread.start()

if __name__ == '__main__':
    greyImName = os.path.join('MRI_crop', 'MRIcrop-grey_orig.mhd')
    segmentationImName = os.path.join('MRI_crop', 'MRIcrop-seg_orig.mhd')
    viewImage(greyImName, segmentationImage=segmentationImName, 
        comment='ReadFromFile')
    greyIm = imageIO.readImage(greyImName)
    segmentationIm = imageIO.readImage(segmentationImName)
    viewImage(greyIm, segmentationImage=segmentationIm, 
        comment='ConvertedFromImageReferences')
    metaViewer = os.path.join(os.path.sep, 'GB', 'itk', 'bin', 'ImageViewer')
    if os.path.isfile(metaViewer):
        viewImage(greyIm, comment='AlternativeViewer', viewerCommand=metaViewer)

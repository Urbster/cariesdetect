import itk
import sys
import os

sys.path.append('util')
from imageIO import readImage
from viewImage3D import viewImage

def smooth(inImg):
    aniso = itk.GradientAnisotropicDiffusionImageFilter[inImg,inImg].New(
            Input = inImg)
    aniso.SetTimeStep(0.025)
    aniso.SetConductanceParameter(1.0)
    aniso.SetNumberOfIterations(5)
    outImg = aniso.GetOutput()
    aniso.Update()
    return outImg


def segmentImage(inImg):

    outImg = smooth(inImg)
    #doSegment
    return outImg


def findCaries(imgNameInput):
    print imgNameInput
    
    if os.path.exists(imgNameInput):
    
        inImg = readImage(imgNameInput)
        outImg = segmentImage(inImg)
        viewImage(outImg)
        #raw_input('Press <Return> to continue')
        #writeImage(imgNameOutput,binaryThrFiltered.GetOutput())
        
    else:
        print "Eingabedatei existiert nicht"
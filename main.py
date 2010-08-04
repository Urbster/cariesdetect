from findCaries import findCaries

#imgNameInput = sys.argv[1]
#inImg = readImage(imgNameInput)
#gaus1 = itk.DiscreteGaussianImageFilter[inImg,inImg].New(Input = inImg)


        
if __name__ == '__main__':

    imgNameInput = "../images/128365.jpg"#argv[0]#
    findCaries(imgNameInput)

#!/usr/bin/env python
# coding: utf-8


import olefile
import sys


###########################################################################
# Print a progressbar that could be overriden at next call
# Add an endline char when the entire progression is done
def print_progressbar(step, maxi):

    done = int(step/maxi*31) * "#"
    rest = (30-int(step/maxi*31)) * " "
    percent = int(step/maxi*100)
    bar = f"[{done}{rest}]{percent}%"

    # display
    sys.stdout.write('\r')
    sys.stdout.write(bar)
    sys.stdout.flush()

    # add endline if finished
    if step == maxi:
        sys.stdout.write("\n")


###########################################################################
# Zvi reader class
# Extract contents binary file of images from .zvi
class ZviReader(olefile.OleFileIO):


    #######################################################################
    # Return the number of detected images
    # value = -1 if there is no image found
    def getNumberOfImages(self):

        # check if the directory where image are expectedly saved exist
        if self.exists("Image"):

            # loop for counting
            n = 0
            while self.exists(f"Image/Item({n})"): n += 1
            return n

        else:
            return -1


    #######################################################################
    # Extract images as array of byte squences
    # Return it and the number of extracted images as tuple ([number, array of sequences]).
    # The number is -1 if images are not found
    def getImages(self):

        # check if images are found
        frameNumber = self.getNumberOfImages()
        if frameNumber == -1: return -1, []

        else:
            frames = [] # array for byte sequences
            
            for n in range(frameNumber):

                streamFilename = f"Image/Item({n})/Contents"

                # read sequence in file if file image is found
                if self.exists(streamFilename):
                    stream = self.openstream(streamFilename)
                    f = stream.read()
                    stream.close()
                else:
                    f = False

                frames.append(f)
                print_progressbar(n, frameNumber-1)

            return frameNumber, frames


    #######################################################################
    # Launch the extraction of images byte sequences in zvi file
    @staticmethod
    def load(filename):

        if olefile.isOleFile(filename):
            reader = ZviReader(filename)
            n, f = reader.getImages()
            reader.close()

            return n, f

        else:
            return -1, []

# USAGE

# ontario-lake python search2.py --index index2.csv --query queries2/20131009_174225659_ios.jpg --result-path dataset2
# california python search2.py --index index2.csv --query queries2/dsc_0029.jpg --result-path dataset2
# graduation python search2.py --index index2.csv --query queries2/img_0118.jpg --result-path dataset2


# import the necessary packages
from pyimagesearch.colordescriptor import ColorDescriptor
from pyimagesearch.searcher import Searcher
import argparse
import cv2

def fitToScreen(image):
    height, width, channels = image.shape
    aspect_ratio = float(width)/height
    if(height>width):

        if(height>1000):
            scale = height/1000
            #the line below is redundant but makes code more intuitive
            height = height/scale
            print height, width, aspect_ratio
            #aspect_ratio = width/height #this WAS giving x/0 error because it was truncating it as an int
            width = height*aspect_ratio 
        return (int(width),int(height))

    if(width>1000):
        scale = width/1000
        #the line below is redundant but makes code more intuitive
        width = width/scale
        height = width/aspect_ratio 
    return (int(width),int(height))

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--index", required = True,
    help = "Path to where the computed index will be stored")
ap.add_argument("-q", "--query", required = True,
    help = "Path to the query image")
ap.add_argument("-r", "--result-path", required = True,
    help = "Path to the result path")
args = vars(ap.parse_args())


# initialize the image descriptor
cd = ColorDescriptor((8, 12, 3))

# load the query image and describe it
query = cv2.imread(args["query"])
height, width, channels = query.shape
print height, width, channels
features = cd.describe(query)

# perform the search
searcher = Searcher(args["index"])
results = searcher.search(features)

# display the query

cv2.namedWindow("Query", cv2.WINDOW_NORMAL)        # Create window with freedom of dimensions
scale_width,scale_height = fitToScreen(query)
query2 = cv2.resize(query,(scale_width,scale_height) )
cv2.imshow("Query", query2)
cv2.resizeWindow("Query", scale_width, scale_height)
#cv2.waitKey(0) #show the window indefinitely until a key is pressed

# loop over the results
for (score, resultID) in results:
    # load the result image and display it
    result = cv2.imread(args["result_path"] + "/" + resultID)
    cv2.namedWindow("Result: %s" % resultID, cv2.WINDOW_NORMAL)
    scale_width, scale_height = fitToScreen(result)
    result2 = cv2.resize(result,(scale_width,scale_height))
    cv2.imshow("Result: %s" % resultID, result2)
    cv2.resizeWindow("Result: %s" % resultID, scale_width, scale_height)
    cv2.waitKey(0)
    


#-----Statement of Authorship----------------------------------------#
#
#  By submitting this task the signatories below agree that it
#  represents our own work and that we both contributed equally to
#  it.  We are aware of the University rule that a student must not
#  act in a manner which constitutes academic dishonesty as stated
#  and explained in QUT's Manual of Policies and Procedures,
#  Section C/5.3 "Academic Integrity" and Section E/2.1 "Student
#  Code of Conduct".
#
#  Driver's student no: N9516778
#  Driver's name: LAM KWOK SHING, TONI
#
#  Navigator's student no: N9550151
#  Navigator's name: Li Jia Jie, Jacky
#--------------------------------------------------------------------#


#-----Task Description-----------------------------------------------#
#
#  IMAGE WATERMARKING
#
#  In this task you develop two functions for hiding and revealing
#  secret images as invisible watermarks within other images.  You
#  need to develop two functions:
#
#  1. add_watermark - Take an image and a black-and-white "watermark"
#     and embed the watermark invisibly in the image.
#
#  2. reveal_watermark - Given an image file with a secret watermark,
#     process the file so that the watermark is revealed.
#
#  To do this you will need to make use of the functions provided
#  by the Python Imaging Library (PIL).  See the task's instructions
#  for further detail.
#--------------------------------------------------------------------#


#-----Automatic Tests------------------------------------------------#
#
#  This section contains unit tests that are used to run your
#  program.  Note that "passing" these tests does NOT mean that you
#  have satisfied the requirements for the task, because these tests
#  merely call the functions, but do not check that the image files
#  produced are correct.

"""
The first group of tests are for your "reveal_watermark" function.
They aim to retrieve the watermarks that have already been added to
two separate images.  Note that Tests 2 and 3 remove old copies of
the target files, if they exist.


Test 1.  Special case - Watermarked file does not exist, so
         your function should just return False and not change
         any files.
>>> reveal_watermark('Mystery_X.bmp')
False


Test 2.  Normal case - Watermarked file contains a secret image.
         Your code should produce the watermark in new file
         "BryceCanyon_X_O.bmp".  Hint: US pioneer Ebenezer Bryce
         famously described the canyon that now bears his name as
         "a hell of a place to lose a cow"!
>>> try:
...     remove('BryceCanyon_X_O.bmp')
... except:
...     pass
>>> reveal_watermark('BryceCanyon_X.bmp')
True


Test 3.  Normal case - Watermarked file contains a secret image.
         Your code should produce the watermark in new file
         "Beach_X_O.bmp".  Hint: Cluck, cluck, cluck!
>>> try:
...     remove('Beach_X_O.bmp')
... except:
...     pass
>>> reveal_watermark('Beach_X.bmp')
True


The next group of tests are for your "add_watermark" function.
They require that your "reveal_watermark" function works correctly,
because they will use it to check that the watermark has indeed been
added to the target file.  Therefore, you must have a working
"reveal_watermark" function before you can attempt to pass these
tests.  Apart from the first two, each test (1) removes old files, if
any, (2) calls the "add_watermark" function to add a watermark, and
(3) calls the "reveal_watermark" function to retrieve the watermark.


Test 4.  Special case - Image file does not exist, so
         your function should just return False and not change
         any files.
>>> add_watermark('Mystery_X.bmp', 'dog_watermark.bmp')
False


Test 5.  Special case - Watermark file does not exist, so
         your function should just return False and not change
         any files.
>>> add_watermark("StoryBridge_X.bmp", "elephant_watermark.bmp")
False


Test 6.  Normal case - Image can be watermarked successfully.
         In this test you add the dog watermark to the image of
         Brisbane's Story Bridge, creating file "StoryBridge_X.bmp".
         Then this file is processed to reveal the watermark,
         creating file "StoryBridge_X_O.bmp".
>>> try:
...     remove('StoryBridge_X.bmp')
... except:
...     pass
>>> try:
...     remove('StoryBridge_X_O.bmp')
... except:
...     pass
>>> add_watermark('StoryBridge.bmp', 'dog_watermark.bmp')
True
>>> reveal_watermark('StoryBridge_X.bmp')
True


Test 7.  Normal case - Image can be watermarked successfully.
         In this test you add the sheep watermark to the image of
         a field of flowers, creating file "Flowers_X.bmp".
         Then this file is processed to reveal the watermark,
         creating file "Flowers_X_O.bmp".
>>> try:
...     remove('Flowers_X.bmp')
... except:
...     pass
>>> try:
...     remove('Flowers_X_O.bmp')
... except:
...     pass
>>> add_watermark('Flowers.bmp', 'sheep_watermark.bmp')
True
>>> reveal_watermark('Flowers_X.bmp')
True

"""
# 
#--------------------------------------------------------------------#



#-----Students' Solution---------------------------------------------#
#
#  Complete the task by filling in the template below.

from PIL import Image
from random import randint
from re import sub

##### PUT YOUR SOLUTION HERE

# Change the value of DEBUG_MODE to 'True' if you want to check status
# of each process, but it may results in failure in testmode
DEBUG_MODE = False

# A function to print the debug message in IDLE if debug mode is turned on
def debugMsg(message):
    if DEBUG_MODE:
        print "DEBUG:", message


# A function to open specific image file and return it as image object
def openImageFile(filename):
    debugMsg("Opening image:"+filename)
    try:
        inputImage = Image.open(filename)
        debugMsg("...[OK]")
        return inputImage
    except IOError as errorMsg:
        debugMsg("I/O error #%s: %s" %(errorMsg.errno, errorMsg.strerror))

        
# A function to encode a single pixel by adding either one of RGB value
# with certain amount. In this program, we will use the blue value.
def encodePixel(original_pixel_RGB, encode_condition):
    MAX_RGB_VALUE = 255
    ENCODE_INCREMENT_BUFFER = 2
    ENCODE_INCREMENT = 1

    # Check whether the encode condition is passed, then proces encoding;
    # otherwise, return the original color
    if encode_condition == True:
        (color_red, color_green, color_blue) = original_pixel_RGB

        # Check if the color is at the maximun allowed value
        # to prevent the value from out of range
        if color_blue >= MAX_RGB_VALUE:
            color_blue -= ENCODE_INCREMENT_BUFFER

        color_blue += ENCODE_INCREMENT
        return (color_red, color_green, color_blue)
    else:
        return original_pixel_RGB


# A function to decode a single pixel by checking whether the sum of the RGB
# value is even or not
def decodePixel(pixel_RGB):
    WATERMARK_RGB = (0,0,0)   # RGB value of black color
    NON_WATERMARK_RGB = (255,255,255)   # RGB value of white color

    is_sum_of_RGB_even = sum(pixel_RGB)%2 == 0
    return WATERMARK_RGB if is_sum_of_RGB_even else NON_WATERMARK_RGB


# A function to convert the given image object to a list of pixel
def imageToPixels(image_obj):
    try:
        if image_obj == None:
            raise ValueError("Image is empty.")
        return list(image_obj.getdata())
    except ValueError as errorMsg:
        debugMsg("ERROR: %s" %(errorMsg))


# A function to save the image file with the given name and image ceontent
def saveImage(filename, image_content, image_dimension):
    NEW_IMAGE_COLOR_MODE = 'RGB'
    
    image_width = image_dimension[0]
    image_height = image_dimension[1]

    debugMsg("Saving image file")
    try:
        new_image = Image.new(NEW_IMAGE_COLOR_MODE,
                     (image_width,image_height))
        new_image.putdata(image_content)
        new_image.save(filename)
        debugMsg("...[OK]")
        debugMsg("Saved image successfully, filename:"+filename)
        return True
    except IOError as errorMsg:
        debugMsg("Image file:"+filename+" not save due to error:")
        debugMsg(str(errorMsg))
        return False


# A function to make each sum of RGB value of the pixels in the image
# to be odd
def refineImage(pixels_list):
    debugMsg("Rendering image (step 1 - refining)")
    refined_pixel_list = []
    for pixel in pixels_list:
        # if the sum of this pixel is even,
        # then the encode condition is true, and vice versa
        encode_condition = sum(pixel)%2==0
        
        refined_pixel = encodePixel(pixel, encode_condition)
        refined_pixel_list.append(refined_pixel)
    debugMsg("...[OK]")
    return refined_pixel_list


# A function to combine a single pixel
def combinePixel(working_pixel, warermark_pixel):
    # if the sum of this watermark pixel is zero,
    # then the encode condition is true, and vice versa.
    # Then the working pixel is encoded based on the encode condition
    encode_condition = sum(warermark_pixel) == 0
    return encodePixel(working_pixel, encode_condition)


# A function to randomly generate interference pixel
def interferencePixel(working_pixel):
    # if the random integer number is 1,
    # then the encode condition is true, and vice versa.
    # Then the working pixel is encoded based on the encode condition
    encode_condition = randint(0,1)==1
    return encodePixel(working_pixel, encode_condition)


# A function to combine the working image and the watermark image
def combineImage(working_pixels, working_image_size,
                 watermark_pixels, watermark_image_size):
    
    debugMsg("Rendering image (step 2 - combining)")
    combined_pixels = []
    combined_image_width = working_image_size[0]
    combined_image_height = working_image_size[1]

    # calculate the margin of the watermark image
    horizontal_left_margin = (combined_image_width - watermark_image_size[0])/2
    horizontal_right_margin = combined_image_width - watermark_image_size[0]\
                            - horizontal_left_margin
    vertical_top_margin = (combined_image_height - watermark_image_size[1])/2
    vertical_bottom_margin = combined_image_height - watermark_image_size[1]\
                            - vertical_top_margin
                        
    working_pointer = 0
    watermark_pointer = 0
    # Go through the image row by row
    for current_pos_Y in range(combined_image_height):
        # Go through the image column by column
        for current_pos_X in range(combined_image_width):
            # Check if the current pixel is overlapped with the watermark image
            # i.e. inside the margin
            if (horizontal_left_margin < current_pos_X <= \
                combined_image_width-horizontal_right_margin)\
                and (vertical_top_margin < current_pos_Y <= \
                     combined_image_height-vertical_bottom_margin):
                new_pixel = combinePixel(working_pixels[working_pointer],
                                         watermark_pixels[watermark_pointer])
                watermark_pointer += 1
            else:
                # watermark out of range, generate interference pixel
                new_pixel = interferencePixel(working_pixels[working_pointer])
            combined_pixels.append(new_pixel)
            working_pointer += 1
    debugMsg("...[OK]")
    return combined_pixels


# A function to retrive the watermark image from the watermarked image
def refineWatermark(watermarked_pixels):
    debugMsg("Rendering image")
    refined_pixel_list = []
    for pixel in watermarked_pixels:
        refined_pixel = decodePixel(pixel)
        refined_pixel_list.append(refined_pixel)
    debugMsg("...[OK]")
    return refined_pixel_list


# A function the add the watermark image into the given working image
# so that the watermark image is hidden in the working image that
# is not visible by human eyes.
def add_watermark(working_file,watermark_file):
    try:
        # Open image files
        working_image = openImageFile(working_file)
        if working_image == None:
            raise ValueError("Working image is empty")
        watermark_image = openImageFile(watermark_file)
        if watermark_image == None:
            raise ValueError("Watermark image is empty")

        # Get the dimension of the images
        working_image_size = working_image.size
        watermark_image_size = watermark_image.size

        # Get the pixel list of the image
        working_image_pixels = imageToPixels(working_image)
        watermark_image_pixels = imageToPixels(watermark_image)

        # Refine the working image
        # to make the sum of each pixel to be an even number
        refined_image_pixels = refineImage(working_image_pixels)
        
        watermarked_image_pixels = combineImage(
                                       refined_image_pixels,
                                       working_image_size,
                                       watermark_image_pixels,
                                       watermark_image_size
                                    )
        watermarked_image_file = sub('\.','_X.',working_file)
        save_result = saveImage(watermarked_image_file,
                                watermarked_image_pixels,
                                working_image_size)
        return save_result
    except ValueError as errorMsg:
        debugMsg(errorMsg)
    return False


# A function to retrive the watermark image from a given watermarked image.
def reveal_watermark(working_file):
    try:
        # open the working image file
        working_Image = openImageFile(working_file)
        if working_Image == None:
            raise ValueError("Working image is empty")

        # Get attributess of the working image and convert it to pixel list
        working_image_size = working_Image.size
        working_image_pixels = imageToPixels(working_Image)
        
        refined_watermark_pixels = refineWatermark(working_image_pixels)

        # Save the refined image
        watermark_image_file = sub('\.','_O.',working_file)
        save_result = saveImage(watermark_image_file, refined_watermark_pixels,
                                working_image_size)
        return save_result
    except ValueError as errorMsg:
        debugMsg(errorMsg)
    return False

#
#--------------------------------------------------------------------#



#-----Testing--------------------------------------------------------#
#
# The following code (when uncommented) will run your functions on
# the supplied images.  You should comment it out while developing
# your functions, but leave it uncommented when you submit your
# solution for marking.
#
if __name__ == '__main__':
    from os import remove
    from doctest import testmod
    testmod(verbose=True)
#
#--------------------------------------------------------------------#

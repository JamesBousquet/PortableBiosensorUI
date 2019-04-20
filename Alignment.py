import os
import PySpin

NUM_IMAGES = 1
def configure_custom_image_settings(nodemap):
    try:
        result = True
        node_pixel_format = PySpin.CEnumerationPtr(nodemap.GetNode('PixelFormat'))
        if PySpin.IsAvailable(node_pixel_format) and PySpin.IsWritable(node_pixel_format):
            # Retrieve the desired entry node from the enumeration node
            node_pixel_format_mono16 = PySpin.CEnumEntryPtr(node_pixel_format.GetEntryByName('Mono16'))
            if PySpin.IsAvailable(node_pixel_format_mono16) and PySpin.IsReadable(node_pixel_format_mono16):
                # Retrieve the integer value from the entry node
                pixel_format_mono16 = node_pixel_format_mono16.GetValue()
                # Set integer as new value for enumeration node
                node_pixel_format.SetIntValue(pixel_format_mono16)
            else:
                print 'Pixel format mono 16 not available...'
        else:
            print 'Pixel format not available...'
    except PySpin.SpinnakerException as ex:
        print 'Error: %s' % ex
        return False
    return result


def acquire_images(cam, nodemap, nodemap_tldevice):
    """
    :param cam: Camera to acquire images from.
    :param nodemap: Device nodemap.
    :param nodemap_tldevice: Transport layer device nodemap.
    :type cam: CameraPtr
    :type nodemap: INodeMap
    :type nodemap_tldevice: INodeMap
    :return: True if successful, False otherwise.
    :rtype: bool
    """
    try:
        result = True
        node_acquisition_mode = PySpin.CEnumerationPtr(nodemap.GetNode('AcquisitionMode'))
        if not PySpin.IsAvailable(node_acquisition_mode) or not PySpin.IsWritable(node_acquisition_mode):
            print 'Unable to set acquisition mode to continuous (enum retrieval). Aborting...'
            return False
        node_acquisition_mode_continuous = node_acquisition_mode.GetEntryByName('Continuous')
        if not PySpin.IsAvailable(node_acquisition_mode_continuous) or not PySpin.IsReadable(node_acquisition_mode_continuous):
            print 'Unable to set acquisition mode to continuous (entry retrieval). Aborting...'
            return False
        acquisition_mode_continuous = node_acquisition_mode_continuous.GetValue()
        node_acquisition_mode.SetIntValue(acquisition_mode_continuous)
        cam.BeginAcquisition()
        for i in range(NUM_IMAGES):
            try:
                image_result = cam.GetNextImage()
                if image_result.IsIncomplete():
                    print 'Image incomplete with image status %d ...' % image_result.GetImageStatus()
                else:
                    image_converted = image_result.Convert(PySpin.PixelFormat_Mono16)
                    # Create a unique filename
                    filename = 'PreparationUtils/View.tiff'
                    image_converted.Save(filename)
                    #print 'Image saved at %s' % filename
                    image_result.Release()
            except PySpin.SpinnakerException as ex:
                print 'Error: %s' % ex
                return False
        cam.EndAcquisition()
    except PySpin.SpinnakerException as ex:
        print("HEREHEREHER EEEEE")
        print 'Error: %s' % ex
        return False
    return result
    
def run_single_camera(cam):
    global nodemap
    global nodemap_tldevice
    try:
        result = True
        # Retrieve TL device nodemap and print device information
        nodemap_tldevice = cam.GetTLDeviceNodeMap()
        # Initialize camera
        cam.Init()
        # Retrieve GenICam nodemap
        nodemap = cam.GetNodeMap()
        # Configure custom image settings
        if not configure_custom_image_settings(nodemap):
            return False
        # Acquire images
        result &= acquire_images(cam, nodemap, nodemap_tldevice)
        # Deinitialize camera
        cam.DeInit()
    except PySpin.SpinnakerException as ex:
        print 'Error: %s' % ex
        result = False
    return result

result = 1
cam_system = PySpin.System.GetInstance()
# Retrieve list of cameras from the system
cam_list = cam_system.GetCameras()
for i, CAM in enumerate(cam_list):
    cam = CAM
result &= run_single_camera(cam)
del cam
cam_list.Clear()









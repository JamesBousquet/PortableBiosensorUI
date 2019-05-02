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
        print 'HERE4.1'
        for i in range(NUM_IMAGES):
            try:
                image_result = cam.GetNextImage()
                print 'HERE4.11'
                if image_result.IsIncomplete():
                    print 'Image incomplete with image status %d ...' % image_result.GetImageStatus()
                else:
                    image_converted = image_result.Convert(PySpin.PixelFormat_Mono16)
                    print 'HERE4.12'
                    # Create a unique filename
                    filename = 'PreparationUtils/View.tiff'
                    image_converted.Save(filename)
                    print 'HERE4.13'
                    #print 'Image saved at %s' % filename
                    image_result.Release()
                    print 'HERE4.2'
            except PySpin.SpinnakerException as ex:
                print 'Error: %s' % ex
                return False
        cam.EndAcquisition()
        print 'HERE4.3'
    except PySpin.SpinnakerException as ex:
        print 'Error: %s' % ex
        return False
    return result
    
def run_single_camera(cam):
    global nodemap
    global nodemap_tldevice
    try:
        result = True
        print 'here4.1'
        # Retrieve TL device nodemap and print device information
        nodemap_tldevice = cam.GetTLDeviceNodeMap()
        print 'here4.2'
        # Initialize camera
        cam.Init()
        print 'here4.3'
        # Retrieve GenICam nodemap
        nodemap = cam.GetNodeMap()
        print 'here4.4'
        # Configure custom image settings
        if not configure_custom_image_settings(nodemap):
            return False
        # Acquire images
        result &= acquire_images(cam, nodemap, nodemap_tldevice)
        print 'here4.5'
        # Deinitialize camera
        cam.DeInit()
        print 'here4.6'
    except PySpin.SpinnakerException as ex:
        print 'Error: %s' % ex
        result = False
    return result


result = 1
print 'here1'
cam_system = PySpin.System.GetInstance()
print 'here2'
# Retrieve list of cameras from the system
cam_list = cam_system.GetCameras()
print 'here3'
for i, CAM in enumerate(cam_list):
    cam = CAM
    print 'here4'
result &= run_single_camera(cam)
print 'here5'
del cam
cam_list.Clear()









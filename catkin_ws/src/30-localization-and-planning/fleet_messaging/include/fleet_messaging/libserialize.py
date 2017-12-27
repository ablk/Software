"""
This file contains the serializer library for the fleet communication project.
"""


# Import modules
from proto.ByteMultiArray_pb2 import ByteMultiArray


class TempStruct:
    """
    Temporary class needed for C-like structs.
    """
    pass


def serialize(ros_msg):
    """
    This function is used to serialize the ByteMultiArray data.
    Inputs:
    - ros_msg: ROS message to be serialized
    Outputs:
    - bma_data: serialized data (see ByteMultiArray.proto)
    """
    # Create the Serialization objects
    bma = ByteMultiArray()

    # Loop through the dimensions in the layout
    for dim in ros_msg.layout.dim:
        ma_dim = bma.layout.dim.add()
        ma_dim.label = dim.label
        ma_dim.size = dim.size
        ma_dim.stride = dim.stride

    # Set the data offset
    bma.layout.data_offset = ros_msg.layout.data_offset

    # Set the data
    print "ros_msg.data out: {}".format(ros_msg.data)
    # bma.data = str(ros_msg.data)
    bma.data = bytes(ros_msg.data)
    print "bma.data out: {}".format(bma.data)
    bma_data = bma.SerializeToString()

    return bma_data

def parse(bma_data):
    """
    This function is used to parse the ByteMultiArray data.
    Inputs:
    - bma_data: ByteMultiArray data (see ByteMultiArray.proto)
    - ros_msg:  Empty ROS message
    Outputs:
    - ros_msg: ROS message ByteMultiArray
    """
    # Instantiate the proto object
    bma = ByteMultiArray()

    # Parse the data
    bma_data_joined = "".join(bma_data)
    bma.ParseFromString(bma_data_joined)

    # Populate the ROS message
    dim = []
    for dim_tmp in bma.layout.dim:
        mad = TempStruct()
        mad.label = dim_tmp.label
        mad.size = dim_tmp.size
        mad.stride = dim_tmp.stride
        dim.append(mad)
    layout = TempStruct()
    layout.dim = dim
    layout.data_offset = bma.layout.data_offset
    ros_msg = TempStruct()
    ros_msg.layout = layout
    print "bma.data in: {}".format(bma.data)
    ros_msg.data = tuple(map(bytes, bma_data))
    print "ros_msg.data in: {}".format(ros_msg.data)

    return ros_msg

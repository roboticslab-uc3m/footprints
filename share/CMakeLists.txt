# Copyright: UC3M 2017
# Author: Aitor Gonzalez
# CopyPolicy: Released under the terms of the GNU GPL v2.0.
# 

find_package(YARP REQUIRED)
list(APPEND CMAKE_MODULE_PATH ${YARP_MODULE_PATH})
include(YarpInstallationHelpers)
yarp_configure_external_installation(footprints)

### Go through single applications

#add_subdirectory(prog)


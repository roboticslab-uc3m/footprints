// -*- mode:C++; tab-width:4; c-basic-offset:4; indent-tabs-mode:nil -*-

/**
 *
 * @ingroup RightFootprint_programs
 * \defgroup RightFootprint RightFootprint
 *
 * @brief Creates an instance of teo::RightFootprint.
 *
 * @section RightFootprint_legal Legal
 *
 * Copyright: 2017 (C) Universidad Carlos III de Madrid
 *
 * Author:Juan Miguel Garcia y Aitor Gonzalez 2017
 *
 * CopyPolicy: This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License 3.0 or later
 *
 * <hr>
 *
 * This file can be edited at LeftLeg
 *
 */

#include <yarp/os/all.h>

#include "RightFootprint.hpp"


using namespace yarp::os;

int main(int argc, char **argv) {

    ResourceFinder rf;
    rf.setVerbose(true);
    rf.setDefaultContext("RightFootprint");
    //rf.setDefaultConfigFile("manipWaiterExecManip.ini");
    rf.setDefaultConfigFile("/usr/local/share/teo/contexts/kinematics/leftLegKinematics.ini");
    rf.configure(argc, argv);

    teo::RightFootprint mod;
    if(rf.check("help")) {
        return mod.runModule(rf);
    }

    printf("Run \"%s --help\" for options.\n",argv[0]);
    printf("%s checking for yarp network... ",argv[0]);
    fflush(stdout);
    Network yarp;
    if (!yarp.checkNetwork()) {
        fprintf(stderr,"[fail]\n%s found no yarp network (try running \"yarpserver &\"), bye!\n",argv[0]);
        return 1;
    } else printf("[ok]\n");

    return mod.runModule(rf);
}


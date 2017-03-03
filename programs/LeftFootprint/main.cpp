// -*- mode:C++; tab-width:4; c-basic-offset:4; indent-tabs-mode:nil -*-

/**
 *
 * @ingroup LeftFootprint_programs
 * \defgroup LeftFootprint LeftFootprint
 *
 * @brief Creates an instance of teo::LeftFootprint.
 *
 * @section LeftFootprint_legal Legal
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

#include "LeftFootprint.hpp"

using namespace std;
using namespace yarp::os;

int main(int argc, char **argv) {

    double ang_0, ang_1, ang_2, ang_3;

    ResourceFinder rf;
    rf.setVerbose(true);
    rf.setDefaultContext("LeftFootprint");
    rf.setDefaultConfigFile("/usr/local/share/teo/contexts/kinematics/leftLegKinematics.ini");
    rf.configure(argc, argv);

    teo::LeftFootprint mod;
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


// -*- mode:C++; tab-width:4; c-basic-offset:4; indent-tabs-mode:nil -*-

#include "RightFootprint.hpp"

namespace teo
{

/************************************************************************/

bool RightFootprint::configure(ResourceFinder &rf) {

    std::string remote = rf.check("remote",yarp::os::Value(DEFAULT_REMOTE),"remote robot to be used").asString();

    printf("--------------------------------------------------------------\n");
    if (rf.check("help")) {
        printf("RightFootprint options:\n");
        printf("\t--help (this help)\t--from [file.ini]\t--context [path]\n");
        printf("\t--remote ('teo' or 'teoSim')\n");
    }
    printf("RightFootprint using remote: %s [%s]\n",remote.c_str(),DEFAULT_REMOTE);

    printf("--------------------------------------------------------------\n");
    if(rf.check("help")) {
        ::exit(1);
    }

    //-- Robot device
    Property rightLegOptions;
    rightLegOptions.put("device","remote_controlboard");
    std::string localStr("/RightFootprint/");
    localStr += remote;
    localStr += "/rightLeg";
    rightLegOptions.put("local",localStr);
    std::string remoteStr("/");
    remoteStr += remote;
    remoteStr += "/rightLeg";
    rightLegOptions.put("remote",remoteStr);
    rightLegDevice.open(rightLegOptions);

    if( ! rightLegDevice.isValid() )    {
        printf("leftArm remote_controlboard instantiation not worked.\n");
        return false;
    }
    if( ! rightLegDevice.view(iEncoders) )    {
        printf("view(iEncoders) not worked.\n");
        return false;
    }
    if( ! rightLegDevice.view(iPositionControl) )    {
        printf("view(iPositionControl) not worked.\n");
        return false;
    }
    if( ! rightLegDevice.view(iPositionDirect) )    {
        printf("view(iPositionDirect) not worked.\n");
        return false;
    }
    if( ! rightLegDevice.view(iVelocityControl) )    {
        printf("view(iVelocityControl) not worked.\n");
        return false;
    }

    inCvPort.setIEncodersControl(iEncoders);
    inCvPort.setIPositionControl(iPositionControl);
    inCvPort.setIPositionDirect(iPositionDirect);
    inCvPort.setIVelocityControl(iVelocityControl);

    //-- Solver device
    yarp::os::Property solverOptions;
    solverOptions.fromString( rf.toString() );
    std::string solverStr = "KdlSolver";
    solverOptions.put("device",solverStr);

    solverDevice.open(solverOptions);
    if( ! solverDevice.isValid() )    {
        CD_ERROR("solver device not valid: %s.\n",solverStr.c_str());
        return false;
    }
    if( ! solverDevice.view(iCartesianSolver) )    {
        CD_ERROR("Could not view iCartesianSolver in: %s.\n",solverStr.c_str());
        return false;
    }
    inCvPort.setICartesianSolver(iCartesianSolver);

    //-----------------OPEN LOCAL PORTS------------//
    inSrPort.setInCvPortPtr(&inCvPort);
    inCvPort.useCallback();
    inSrPort.useCallback();
    inSrPort.open("/rightFootprint/DialogueManager/command:i");
    inCvPort.open("/rightFootprint/cvBottle/state:i");

    return true;
}

/************************************************************************/
double RightFootprint::getPeriod() {
    return 2.0;  // Fixed, in seconds, the slow thread that calls updateModule below
}

/************************************************************************/
bool RightFootprint::updateModule() {
    //printf("StateMachine in state [%d]. RightFootprint alive...\n", stateMachine.getMachineState());
    return true;
}

/************************************************************************/

bool RightFootprint::interruptModule() {
    printf("RightFootprint closing...\n");
    inCvPort.disableCallback();
    inSrPort.disableCallback();
    inCvPort.interrupt();
    inSrPort.interrupt();
    inCvPort.close();
    inSrPort.close();

    solverDevice.close();
    leftArmDevice.close();
    return true;
}

/************************************************************************/

}  // namespace teo

// -*- mode:C++; tab-width:4; c-basic-offset:4; indent-tabs-mode:nil -*-

#include "InCvPort.hpp"

namespace teo
{

/************************************************************************/
void InCvPort::setFollow(int value)
{
    follow = value;
}

/************************************************************************/

void InCvPort::onRead(Bottle& b) {
    calculatePosition();

}

/************************************************************************/

void InCvPort::ReadFTSensorRight(Bottle& FTSensor){
    //Funcion para leer los datos del sensor del pie derecho

    _sensor_right.fx = FTSensor.get(0).asDouble();
    _sensor_right.fy = FTSensor.get(1).asDouble();
    _sensor_right.fz = FTSensor.get(2).asDouble();
    _sensor_right.mx = FTSensor.get(3).asDouble();
    _sensor_right.my = FTSensor.get(4).asDouble();
    _sensor_right.mz = FTSensor.get(5).asDouble();
}

/************************************************************************/

void InCvPort::calculatePosition(){
    /** ----- Obtain current joint position --------------- **/
        std::vector<double> currentQ(6);

        if ( ! iEncoders->getEncoders( currentQ.data() ) )    { //obtencion de los valores articulares (encoders absolutos)
            CD_WARNING("getEncoders failed, not updating control this iteration.\n");
            return;
        }
        /** --------------------------------------------------- **/


    /** ----- Obtain current cartesian position ---------- **/
        std::vector<double> currentX, desireX;
        if ( ! iCartesianSolver->fwdKin(currentQ,currentX) )    {
            CD_ERROR("fwdKin failed.\n");
        }

        yarp::os::Bottle state;
        state.addDouble(currentX[0]);
        state.addDouble(currentX[1]);
        printf("La coordenada x del pie derecho es: %f\n", -currentX[1]);
        printf("La coordenada y del pie derecho es: %f\n", currentX[0]);
        outPort->write(state);

}

/************************************************************************/

void InCvPort::setOutFootPrintPort(yarp::os::Port* outFootPrintPort) {
    this->outPort = outFootPrintPort;
}

/************************************************************************/

}  // namespace teo


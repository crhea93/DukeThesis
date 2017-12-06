#include "readinicCoupled.h"

template<>
InputParameters validParams<readinicCoupled>()
{
    InputParameters params = validParams<InitialCondition>();
    params.addParam<std::vector<double>>("init_val","Initial Pore Pressure Value");
    params.addRequiredCoupledVar("sat_inv","Saturation of Invading Fluid");
    return params;
}

readinicCoupled::readinicCoupled(const InputParameters & parameters) :
InitialCondition(parameters),
_init_val(getParam<std::vector<double>>("init_val")),
_sat_val(coupledValue("sat_inv"))
{}

void
readinicCoupled::initialSetup(){

}
Real
readinicCoupled::value(const Point & p)
{
  return _init_val[0]*(1-_sat_val[_qp])+1e-2;
}

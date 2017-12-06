/****************************************************************/
/*               DO NOT MODIFY THIS HEADER                      */
/* MOOSE - Multiphysics Object Oriented Simulation Environment  */
/*                                                              */
/*           (c) 2010 Battelle Energy Alliance, LLC             */
/*                   ALL RIGHTS RESERVED                        */
/*                                                              */
/*          Prepared by Battelle Energy Alliance, LLC           */
/*            Under Contract No. DE-AC07-05ID14517              */
/*            With the U. S. Department of Energy               */
/*                                                              */
/*            See COPYRIGHT for full restrictions               */
/****************************************************************/

#include "ConstantSource.h"

template <>
InputParameters
validParams<ConstantSource>()
{
  InputParameters params = validParams<DiracKernel>();
  params.addRequiredParam<Real>("value", "The value of the point source");
  params.addParam<std::vector<std::string> >("shapes", "array of shape types: crack, circle");
  params.addParam<std::vector<Real> >("centers_tips", "coordinates");
  params.declareControllable("value");
  return params;
}

ConstantSource::ConstantSource(const InputParameters & parameters)
  : DiracKernel(parameters),
    _value(getParam<Real>("value")),
    _centers_tips(getParam<std::vector<Real> >("centers_tips")),
    _shapes(getParam<std::vector<std::string> >("shapes"))
{

}

void
ConstantSource::addPoints()
{
  double p0,p1;
  double aux_distance = 0.0;
  double current_value = 0.0;
  double _center_x, _center_y, _radius_a;
      _center_x = _centers_tips[0];
      _center_y = _centers_tips[1];
      _radius_a = _centers_tips[2];

      p0 = _q_point[_qp](0);
      p1 = _q_point[_qp](1);
        aux_distance=sqrt((p0-(_center_x))*(p0-(_center_x))+(p1-(_center_y))*(p1-(_center_y)));//distance to center
        if (aux_distance<_radius_a){
          _p(0) = p0;
          _p(1) = p1;
          addPoint(_p);
        }
}

Real
ConstantSource::computeQpResidual()
{
  //  This is negative because it's a forcing function that has been brought over to the left side
  return -_test[_i][_qp] * _value;
}

/****************************************************************/
/* MOOSE - Multiphysics Object Oriented Simulation Environment  */
/*                                                              */
/*          All contents are licensed under LGPL V2.1           */
/*             See LICENSE for full restrictions                */
/****************************************************************/

#include "NodalMassS.h"

// MOOSE includes
#include "MooseVariable.h"

// C++ includes
#include <iostream>

template <>
InputParameters
validParams<NodalMassS>()
{
  InputParameters params = validParams<TimeKernel>();
  params.addRequiredParam<UserObjectName>(
      "fluid_density",
      "A RichardsDensity UserObject that defines the fluid density as a function of pressure.");
  params.addClassDescription("Fluid mass lumped to the nodes divided by dt");
  return params;
}

NodalMassS::NodalMassS(const InputParameters & parameters)
  : TimeKernel(parameters),
    _density(getUserObject<RichardsDensity>("fluid_density")),
    _porosity(getMaterialProperty<Real>("porosity"))
{
}

Real
NodalMassS::computeQpResidual()
{
  Real density;
  Real mass;
    density = _density.density(_u[_qp]);
    mass = _porosity[_qp] * density * (_u[_qp]);
  return _test[_i][_qp] * mass / _dt;
}

Real
NodalMassS::computeQpJacobian()
{

  Real mass_prime;

    Real density = _density.density(_u[_qp]);
    mass_prime = _porosity[_qp] * density;

  return _test[_i][_qp] * mass_prime / _dt;
}

Real
NodalMassS::computeQpOffDiagJacobian(unsigned int jvar)
{

  Real mass_prime;


  // we're calculating the deriv wrt porepressure
  mass_prime = 0.0;


  return _test[_i][_qp] * mass_prime / _dt;
}

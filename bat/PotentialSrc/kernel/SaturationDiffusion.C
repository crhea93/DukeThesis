/****************************************************************/
/* MOOSE - Multiphysics Object Oriented Simulation Environment  */
/*                                                              */
/*          All contents are licensed under LGPL V2.1           */
/*             See LICENSE for full restrictions                */
/****************************************************************/

#include "SaturationDiffusion.h"

template <>
InputParameters
validParams<SaturationDiffusion>()
{
  InputParameters params = validParams<Kernel>();
  params.addRequiredParam<UserObjectName>(
      "fluid_density",
      "A RichardsDensity UserObject that defines the fluid density as a function of pressure.");
  params.addRequiredParam<UserObjectName>(
      "fluid_relperm",
      "A RichardsRelPerm UserObject that defines the fluid relative permeability "
      "as a function of water saturation (eg RichardsRelPermPower)");
  params.addRequiredParam<Real>("fluid_viscosity", "The fluid dynamic viscosity");
  params.addRequiredParam<Real>("diffusivity", "Diffusivity as a function of S");
  params.addClassDescription("Diffusion part of the Flux according to Darcy-Richards flow.  The "
                             "Variable of this Kernel must be the saturation.");
  return params;
}

SaturationDiffusion::SaturationDiffusion(const InputParameters & parameters)
  : Kernel(parameters),
    _density(getUserObject<RichardsDensity>("fluid_density")),
    _relperm(getUserObject<RichardsRelPerm>("fluid_relperm")),
    _viscosity(getParam<Real>("fluid_viscosity")),
    _permeability(getMaterialProperty<RealTensorValue>("permeability")),
    _diffusivity(getParam<Real>("diffusivity"))
{
}

Real
SaturationDiffusion::computeQpResidual()
{
  Real coef = _diffusivity * _relperm.relperm(_u[_qp]) * _density.density(_u[_qp]) / _viscosity;
  return -coef * _grad_test[_i][_qp] * (_permeability[_qp] * _grad_u[_qp]);
}

Real
SaturationDiffusion::computeQpJacobian()
{
   return 0.0;
}

Real
SaturationDiffusion::computeQpOffDiagJacobian()
{
  return 0.0;

}

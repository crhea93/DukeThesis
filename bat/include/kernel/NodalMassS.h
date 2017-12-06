/****************************************************************/
/* MOOSE - Multiphysics Object Oriented Simulation Environment  */
/*                                                              */
/*          All contents are licensed under LGPL V2.1           */
/*             See LICENSE for full restrictions                */
/****************************************************************/

#ifndef NODALMASSP
#define NODALMASSS

#include "TimeKernel.h"
#include "Material.h"
#include "RichardsDensity.h"

// Forward Declarations
class NodalMassS;

template <>
InputParameters validParams<NodalMassS>();

/**
 * fluid_mass/dt lumped to the nodes
 */
class NodalMassS : public TimeKernel
{
public:
  NodalMassS(const InputParameters & parameters);

protected:
  virtual Real computeQpResidual();

  virtual Real computeQpJacobian();

  virtual Real computeQpOffDiagJacobian(unsigned int jvar);

  const RichardsDensity & _density;

  /// current value of the porosity
  const MaterialProperty<Real> & _porosity;
};

#endif // Q2PNODALMASS

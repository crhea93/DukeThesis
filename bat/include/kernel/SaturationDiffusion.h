/****************************************************************/
/* MOOSE - Multiphysics Object Oriented Simulation Environment  */
/*                                                              */
/*          All contents are licensed under LGPL V2.1           */
/*             See LICENSE for full restrictions                */
/****************************************************************/

#ifndef SATURATIONDIFFUSION
#define SATURATIONDIFFUSION

#include "Kernel.h"
#include "RichardsDensity.h"
#include "RichardsRelPerm.h"
#include "Material.h"
#include "Function.h"

// Forward Declarations
class SaturationDiffusion;

template <>
InputParameters validParams<SaturationDiffusion>();

/**
 * Diffusive Kernel that models nonzero capillary pressure in Q2P models
 * The Variable of this Kernel should be the saturation
 */
class SaturationDiffusion : public Kernel
{
public:
  SaturationDiffusion(const InputParameters & parameters);

protected:
  virtual Real computeQpResidual();

  virtual Real computeQpJacobian();

  virtual Real computeQpOffDiagJacobian();

  /// water density
  const RichardsDensity & _density;

  /// water relative permeability
  const RichardsRelPerm & _relperm;


  /// fluid viscosity
  Real _viscosity;

  /// permeability
  const MaterialProperty<RealTensorValue> & _permeability;

  Real _diffusivity;
};

#endif // Q2PSATURATIONDIFFUSION

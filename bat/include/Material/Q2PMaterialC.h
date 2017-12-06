/****************************************************************/
/* MOOSE - Multiphysics Object Oriented Simulation Environment  */
/*                                                              */
/*          All contents are licensed under LGPL V2.1           */
/*             See LICENSE for full restrictions                */
/****************************************************************/

#ifndef Q2PMATERIALC_H
#define Q2PMATERIALC_H

#include "Material.h"

// Forward Declarations
class Q2PMaterialC;

template <>
InputParameters validParams<Q2PMaterialC>();

/**
 * Q2P Material.  Defines permeability, porosity and gravity
 */
class Q2PMaterialC : public Material
{
public:
  Q2PMaterialC(const InputParameters & parameters);

protected:
  /// porosity as entered by the user
  //Real _material_por;
  const VariableValue & _porosity_var;
  const VariableValue & _porosity_var_old;
  /// porosity changes.  if not entered they default to zero
  const VariableValue & _por_change;
  const VariableValue & _por_change_old;

  /// permeability as entered by the user
  RealTensorValue _material_perm;

  /// gravity as entered by user
  RealVectorValue _material_gravity;

  /// material properties
  MaterialProperty<Real> & _porosity_old;
  MaterialProperty<Real> & _porosity;
  MaterialProperty<RealTensorValue> & _permeability;
  MaterialProperty<RealVectorValue> & _gravity;

  std::vector<const VariableValue *> _perm_change;

  virtual void computeQpProperties();
};

#endif // Q2PMATERIALC_H

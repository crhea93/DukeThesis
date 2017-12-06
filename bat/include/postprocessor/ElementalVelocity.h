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

#ifndef ELEMENTALVELOCITY_H
#define ELEMENTALVELOCITY_H

// MOOSE includes
#include "GeneralPostprocessor.h"

// Forward Declarations
class ElementalVelocity;
class MooseMesh;

namespace libMesh
{
class Elem;
}

template <>
InputParameters validParams<ElementalVelocity>();

class ElementalVelocity : public GeneralPostprocessor
{
public:
  ElementalVelocity(const InputParameters & parameters);

  virtual void initialize() override {}
  virtual void execute() override {}
  virtual Real getValue() override;

protected:
  MooseMesh & _mesh;
  std::string _var_name;
  Elem * _element;
  //std::vector<Elem> * _elements;
  std::string _outputname;
};

#endif // ELEMENTALVELOCITY_H

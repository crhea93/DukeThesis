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

#ifndef NODALPRINTOUT_H
#define NODALPRINTOUT_H

#include "GeneralPostprocessor.h"

// Forward Declarations
class NodalPrintOut;
class MooseMesh;

namespace libMesh
{
class Node;
}

template <>
InputParameters validParams<NodalPrintOut>();

/**
 * Sums a nodal value across all processors and multiplies the result
 * by a scale factor.
 */
class NodalPrintOut : public GeneralPostprocessor
{
public:
  NodalPrintOut(const InputParameters & parameters);

  virtual void initialize() override {}
  virtual void execute() override {}
  virtual Real getValue() override;

protected:
  MooseMesh & _mesh;
  std::string _var_name;
  Node * _node_ptr;
  //const Real _scale_factor;
  std::string _outputname;
};

#endif // NODALPRINTOUT_H

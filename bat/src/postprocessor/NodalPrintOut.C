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

#include "NodalPrintOut.h"

// MOOSE includes
#include "MooseMesh.h"
#include "MooseVariable.h"
#include "SubProblem.h"

#include "libmesh/node.h"

template <>
InputParameters
validParams<NodalPrintOut>()
{
  InputParameters params = validParams<GeneralPostprocessor>();
  params.addRequiredParam<VariableName>("variable", "The variable to be monitored");
  //params.addRequiredParam<unsigned int>("nodeid", "The ID of the node where we monitor");
  //params.addParam<Real>("scale_factor", 1, "A scale factor to be applied to the variable");
  params.addClassDescription("Outputs values of a nodal variable at a particular location");
  params.addRequiredParam<std::string>("output","Name to output csv file");
  return params;
}

NodalPrintOut::NodalPrintOut(const InputParameters & parameters)
  : GeneralPostprocessor(parameters),
    _mesh(_subproblem.mesh()),
    _var_name(parameters.get<VariableName>("variable")),
      _outputname(getParam<std::string>("output"))
    //_node_ptr(_mesh.getMesh().query_node_ptr(getParam<unsigned int>("nodeid"))),
    //_scale_factor(getParam<Real>("scale_factor"))
{
  // This class may be too dangerous to use if renumbering is enabled,
  // as the nodeid parameter obviously depends on a particular
  // numbering.
  /*if (_mesh.getMesh().allow_renumbering())
    mooseError("NodalVariableValue should only be used when node renumbering is disabled.");

  bool found_node_ptr = _node_ptr;
  _communicator.max(found_node_ptr);

  if (!found_node_ptr)
    mooseError("Node #",
               getParam<unsigned int>("nodeid"),
               " specified in '",
               name(),
               "' not found in the mesh!");*/
}

Real
NodalPrintOut::getValue()
{
  double value = 0.0;
  std::ofstream file;
  file.open(_outputname+".txt");
  //if (_node_ptr && _node_ptr->processor_id() == processor_id())
  //  value = _subproblem.getVariable(_tid, _var_name).getNodalValue(*_node_ptr);

  for (int i=0;i<_mesh.getMesh().n_nodes();i++){
    _node_ptr = _mesh.getMesh().query_node_ptr(i);
    //MooseVariable & var = _subproblem.getVariable(_tid, _var_name);
    //const VariableValue & u = var.sln();
    //value = u[i];

    value = _subproblem.getVariable(_tid, _var_name).getNodalValue(*_node_ptr);

    //std::cout<<value<<std::endl;
    file<<_mesh.getMesh().node(i)(0)<<" "<<_mesh.getMesh().node(i)(1)<<" "<<std::to_string(value)<<std::endl;
  }
  file.close();
  //gatherSum(value);

  return value;
}

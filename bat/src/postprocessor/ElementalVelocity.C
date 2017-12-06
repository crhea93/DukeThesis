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

#include "ElementalVelocity.h"

// MOOSE includes
#include "MooseMesh.h"
#include "MooseVariable.h"
#include "SubProblem.h"
#include <fstream>
template <>
InputParameters
validParams<ElementalVelocity>()
{
  InputParameters params = validParams<GeneralPostprocessor>();
  params.addRequiredParam<VariableName>("variable", "The variable to be monitored");
  //params.addRequiredParam<unsigned int>("elementid", "The ID of the element where we monitor");
  params.addClassDescription("Outputs an elemental variable value at a particular location");
  params.addRequiredParam<std::string>("output","Name to output csv file");
  return params;
}

ElementalVelocity::ElementalVelocity(const InputParameters & parameters)
  : GeneralPostprocessor(parameters),
    _mesh(_subproblem.mesh()),
    _var_name(parameters.get<VariableName>("variable")),
    _outputname(getParam<std::string>("output"))
    //_element(_mesh.getMesh().query_elem_ptr(parameters.get<unsigned int>("elementid")))
{
  // This class may be too dangerous to use if renumbering is enabled,
  // as the nodeid parameter obviously depends on a particular
  // numbering.
  if (_mesh.getMesh().allow_renumbering())
    mooseError("ElementalVariableValue should only be used when node renumbering is disabled.");
}

Real
ElementalVelocity::getValue()
{
  Real value = 0;
  std::ofstream file;
  file.open(_outputname+".csv");
  file<<"X1"<<","<<"Y1"<<","<<"X2"<<","<<"Y2"<<","<<"X3"<<","<<"Y3"<<","<<"Vel"<<std::endl;
  for (int i=0;i<_mesh.getMesh().n_elem();i++){
    //if (_element && (_element->processor_id() == processor_id()))
    //{
      _element = _mesh.getMesh().query_elem_ptr(i);

      _subproblem.prepare(_element, _tid);
      _subproblem.reinitElem(_element, _tid);
      //std::cout<<_mesh.getMesh().n_elem();
      //std::cout<<_element->point(0)(0)<<std::endl;
      //std::cout<<i<<std::endl;
      MooseVariable & var = _subproblem.getVariable(_tid, _var_name);
      const VariableValue & u = var.sln();
      unsigned int n = u.size();
      for (unsigned int i = 0; i < n; i++)
        value += u[i];
      //std::cout<<value<<std::endl;
      value /= n;
      for (int j=0;j<3;j++){
        for (int k=0;k<2;k++){
          file<<std::to_string(_element->point(j)(k))<<",";
        }
      }
      //value = u[i];
      gatherSum(value);
      file<<std::to_string(value)<<std::endl;
      value = 0.0;
    //}

  //  gatherSum(value);
  }
 file.close();
  return value;
}

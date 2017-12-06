#include "BatApp.h"
#include "Moose.h"
#include "AppFactory.h"
#include "ModulesApp.h"
#include "MooseSyntax.h"
//------------ CARTER CREATED MODULES -----------//
#include "readinic.h"
#include "readinicCoupled.h"
#include "PPInit.h"
#include "PhasefieldShapes.h"
#include "ConstantCoupled.h"
#include "PorosityRand.h"
#include "ConstantSource.h"
#include "NodalPrintOut.h"
//----------- AUGMENTED RICHARDSON MODULES ------//
//#include "NodalMassS.h"
//#include "NodalMassP.h"
//#include "NodalMassOldS.h"
//#include "NodalMassOldP.h"
//#include "SaturationFlux.h"
//#include "SaturationDiffusion.h"
//#include "PorepressureFlux.h"
#include "Q2PMaterialC.h"
//#include "TimeDerivativeS.h"
//#include "TimeDerivativeP.h"
//----------- AUGMENTED MOOSE MODULES ---------------------//
#include "DarcyVelocity.h"
#include "ElementalVelocity.h"

template<>
InputParameters validParams<BatApp>()
{
  InputParameters params = validParams<MooseApp>();
  return params;
}

BatApp::BatApp(InputParameters parameters) :
    MooseApp(parameters)
{
  Moose::registerObjects(_factory);
  ModulesApp::registerObjects(_factory);
  BatApp::registerObjects(_factory);

  Moose::associateSyntax(_syntax, _action_factory);
  ModulesApp::associateSyntax(_syntax, _action_factory);
  BatApp::associateSyntax(_syntax, _action_factory);
}

BatApp::~BatApp()
{
}

// External entry point for dynamic application loading
extern "C" void BatApp__registerApps() { BatApp::registerApps(); }
void
BatApp::registerApps()
{
  registerApp(BatApp);
}

// External entry point for dynamic object registration
extern "C" void BatApp__registerObjects(Factory & factory) { BatApp::registerObjects(factory); }
void
BatApp::registerObjects(Factory & factory)
{
//----------Carter Made----------------//
  //ICS
  registerInitialCondition(readinic);
  registerInitialCondition(readinicCoupled);
  registerInitialCondition(PPInit);
  registerInitialCondition(PhasefieldShapes);
  registerInitialCondition(PorosityRand);
  //KERNELS
  registerKernel(ConstantCoupled);
  //registerKernel(ConstantSource);
  //registerKernel(NodalMassS);
  //registerKernel(NodalMassP);
  //registerKernel(NodalMassOldS);
  //registerKernel(NodalMassOldP);
  //registerKernel(SaturationFlux);
  //registerKernel(PorepressureFlux);
  //registerKernel(SaturationDiffusion);
  //registerKernel(TimeDerivativeS);
  //registerKernel(TimeDerivativeP);
  //MATERIALS
  registerMaterial(Q2PMaterialC);
  //AUXKERNELS
  registerAuxKernel(DarcyVelocity);
  //POSTPROCESSORS
  registerPostprocessor(NodalPrintOut);
  registerPostprocessor(ElementalVelocity);
  //OUTPUTS
  //registerOutput(ExodusExt);
}

// External entry point for dynamic syntax association
extern "C" void BatApp__associateSyntax(Syntax & syntax, ActionFactory & action_factory) { BatApp::associateSyntax(syntax, action_factory); }
void
BatApp::associateSyntax(Syntax & /*syntax*/, ActionFactory & /*action_factory*/)
{


}

#ifndef BATAPP_H
#define BATAPP_H

#include "MooseApp.h"

class BatApp;

template<>
InputParameters validParams<BatApp>();

class BatApp : public MooseApp
{
public:
  BatApp(InputParameters parameters);
  virtual ~BatApp();

  static void registerApps();
  static void registerObjects(Factory & factory);
  static void associateSyntax(Syntax & syntax, ActionFactory & action_factory);
};

#endif /* BATAPP_H */

#ifndef READINIC_H
#define READINIC_H

// MOOSE Includes
#include "InitialCondition.h"
#include <vector>

// Forward Declarations
class readinic;
template<>
InputParameters validParams<readinic>();


class readinic : public InitialCondition
{
public:
    readinic(const InputParameters & parameters);
    
    virtual Real value(const Point & p) override;
    virtual void initialSetup() override;
private:
    std::string _dataFile;
    std::vector<double> _vals;
    
};

#endif //READINIC_H

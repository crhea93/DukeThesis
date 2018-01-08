[Mesh]
  type = FileMesh
file = /home/crhea/Documents/DukeThesis/Mesh/Disk_ref.e
[]



[UserObjects]
  [./DensityWater]
    type = RichardsDensityConstBulk
    dens0 = 1
    bulk_mod = 1
  [../]
  [./DensityGas]
    type = RichardsDensityConstBulk
    dens0 = 0.5
    bulk_mod = 0.5
  [../]
  [./RelPermWater]
    type = RichardsRelPermPower
    simm = 0.0
    n = 2
  [../]
  [./RelPermGas]
    type = Q2PRelPermPowerGas
    simm = 0.0
    n = 3
  [../]
[]

[Variables]
  [./pp]
     #scaling = 1e-8
  [../]
  [./sat]
  [../]
[]

[AuxVariables]
[./porosity]
[../]
[./porosity_old]
[../]
  [./velocity_x]
    order = CONSTANT
    family = MONOMIAL
  [../]
  [./velocity_y]
    order = CONSTANT
    family = MONOMIAL
  [../]
[]
#[BCs]
#  [./central_constant]
#   type = DirichletBC
#   boundary = 5
#   variable = sat
#   value = 0.99
#   [../]
#[]
[Q2P]
  porepressure = pp
  saturation = sat
  water_density = DensityWater
  water_relperm = RelPermWater
water_viscosity = 1000.0
  gas_density = DensityGas
  gas_relperm = RelPermGas
  gas_viscosity = 0.5
  diffusivity = 10.0
  output_total_masses_to = 'CSV'
  save_gas_flux_in_Q2PGasFluxResidual = true
  save_water_flux_in_Q2PWaterFluxResidual = true
  save_gas_Jacobian_in_Q2PGasJacobian = true
  save_water_Jacobian_in_Q2PWaterJacobian = true
[]
[AuxKernels]
  [./velocity_x]
    type = DarcyVelocity
    variable = velocity_x
    component = x
    execute_on = timestep_end
    darcy_pressure = pp
  [../]
  [./velocity_y]
    type = DarcyVelocity
    variable = velocity_y
    component = y
    execute_on = timestep_end
    darcy_pressure = pp
  [../]
[]
[Kernels]
#Keep pressure in central region constant
[./central_drop]
  type = ConstantCoupled
  variable = sat
  epsilon = 0.01
  shapes = 'circle'
  centers_tips = '0.0 0.0 0.01'
  press_init_val = 0.99
[../]
[]


[ICs]
[./sat_init]
  type = readinic
  variable = sat
dataFile = /media/crhea/Data/Results/Thesis/SweepSimulations/Viscosity_1000.0/MOOSEValues_sat_updated.txt
[../]
[./pp_init]
  type = readinic
  variable = pp
dataFile = /media/crhea/Data/Results/Thesis/SweepSimulations/Viscosity_1000.0/MOOSEValues_press_updated.txt
[../]
[./porosity_init]
  type = readinic
  variable = porosity
dataFile = /media/crhea/Data/Results/Thesis/SweepSimulations/Viscosity_1000.0/Porosity.txt
[../]
[./porosity_init_old]
  type = readinic
  variable = porosity_old
dataFile = /media/crhea/Data/Results/Thesis/SweepSimulations/Viscosity_1000.0/Porosity_old.txt
[../]
[]

[Materials]
  [./rock]
    type = Q2PMaterialC
    block = 1
    por_var = porosity
    por_var_old = porosity_old
    mat_permeability = '1E-2 0 0  0 1E-2 0  0 0 1E-2'
    gravity = '0 0 0'
  [../]
[]
[Postprocessors]
  [./dofs]
    type = NumDOFs
  [../]
  [./veltyx]
    type = ElementalVelocity
    variable = velocity_x
    output =/media/crhea/Data/Results/Thesis/SweepSimulations/Viscosity_1000.0/velocitiesX
  [../]
  [./veltyy]
    type = ElementalVelocity
    variable = velocity_y
    output = /media/crhea/Data/Results/Thesis/SweepSimulations/Viscosity_1000.0/velocitiesY
  [../]
  [./sat_updated_out]
    type = NodalPrintOut
    variable = sat
     output = /media/crhea/Data/Results/Thesis/SweepSimulations/Viscosity_1000.0/MOOSEValues_sat_updated
  [../]
  [./press_updated_out]
    type = NodalPrintOut
    variable = pp
     output = /media/crhea/Data/Results/Thesis/SweepSimulations/Viscosity_1000.0/MOOSEValues_press_updated
  [../]
[]


[Preconditioning]
  active = 'andy'
  [./andy]
    type = SMP
    full = true
    petsc_options_iname = '-ksp_type -pc_type -snes_atol -snes_rtol -snes_max_it'
    petsc_options_value = 'bcgs bjacobi 1E-12 1E-10 10000'
  [../]
[]

[Executioner]
  type = Transient
  solve_type = Newton
  dt = 0.001
  end_time = 0.001
[]

[Outputs]
file_base = /media/crhea/Data/Results/Thesis/SweepSimulations/Viscosity_1000.0/MOOSEFILES/MOOSEOutput
exodus = true
  [./CSV]
    type = CSV
  [../]
[]

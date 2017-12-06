[Mesh]
  type = FileMesh
file = /home/crhea/Dropbox/Thesis/Mesh/square_Ref1.e
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
  [../]
  [./sat]
  [../]
[]

[AuxVariables]
[./porosity]
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
[./NodalMassSat]
  type = NodalMassS
  variable = sat
  fluid_density = DensityWater
[../]
[./NodalMassPress]
  type = NodalMassP
  variable = sat
  saturation_variable = sat
  fluid_density = DensityGas
[../]
[./NodalMassOldSat]
  type = NodalMassOldS
  variable = sat
  fluid_density = DensityWater
[../]
[./NodalMassOldPress]
  type = NodalMassOldP
  variable = sat
  saturation_variable = sat
  fluid_density = DensityGas
[../]
[./PPFlux]
  type = PorepressureFlux
  variable = pp
  fluid_density = DensityGas
  fluid_relperm = RelPermGas
  fluid_viscosity = 0.5 #Viscosity of Gas
  saturation_variable = sat
[../]
[./SatFlux]
  type = SaturationFlux
  variable = sat
  fluid_density = DensityWater
  fluid_relperm = RelPermWater
  fluid_viscosity = 0.8 #Viscosity of Water
  porepressure_variable = pp
[../]
[./SatDiff]
  type = SaturationDiffusion
  variable = sat
  fluid_density = DensityWater
  fluid_relperm = RelPermWater
  fluid_viscosity = 0.8 #Viscosity of Water
  diffusivity = 0.0 #Diffusivity Constant
  porepressure_variable = pp
[../]



[]




[ICs]
[./sat_init]
  type = PhasefieldShapes
  variable = sat
  shapes = 'circle'
  epsilon = 0.1
  centers_tips = '0.0 0.0 0.1'
[../]
[./pp_init]
  type = PPInit
  variable = pp
  press_init_val = 1.5
  shapes = 'circle'
  epsilon = 0.1
  centers_tips = '0.0 0.0 0.1'

[../]
[./porosity_init]
  type = readinic
  variable = porosity
dataFile = Porosity.txt
[../]
[]

[Materials]
  [./rock]
    type = Q2PMaterialC
    block = 1
    por_var = porosity
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
    output = velocitiesX
  [../]
  [./veltyy]
    type = ElementalVelocity
    variable = velocity_y
    output = velocitiesY
  [../]
  [./sat_updated_out]
    type = NodalPrintOut
    variable = sat
     output = MOOSEValues_sat_updated
  [../]
  [./press_updated_out]
    type = NodalPrintOut
    variable = pp
     output = MOOSEValues_press_updated
  [../]
[]



[Executioner]
  type = Transient
  solve_type = 'JFNK'

  l_tol = 1.0e-4
  nl_rel_tol = 1.0e-4
  nl_abs_tol = 1.0e-4

  dt = 0.01
  end_time = 10.0
[]

[Outputs]
file_base = Mode1/MOOSEOutput
  exodus = true
  [./CSV]
    type = CSV
  [../]
[]

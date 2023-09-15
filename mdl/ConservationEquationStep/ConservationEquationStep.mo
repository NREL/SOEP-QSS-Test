within ;
model ConservationEquationStep
  "Model that tests the conservation equation"
extends Modelica.Icons.Example;
 package Medium = Buildings.Media.Air "Medium model";

  constant Modelica.Units.SI.SpecificEnergy h_fg=
      Buildings.Media.Air.enthalpyOfCondensingGas(273.15 + 37)
    "Latent heat of water vapor";

  Buildings.Fluid.Interfaces.ConservationEquation dynBal(
    redeclare package Medium = Medium,
    energyDynamics=Modelica.Fluid.Types.Dynamics.FixedInitial,
    fluidVolume=1,
    use_mWat_flow=true,
//  simplify_mWat_flow=false,
    nPorts=2)           "Dynamic conservation equation"
    annotation (Placement(transformation(extent={{-10,30},{10,50}})));

  Buildings.Fluid.Sources.Boundary_pT sin(
    use_p_in=false,
    redeclare package Medium = Medium,
    p=101325,
    T=283.15,
    nPorts=1)
      annotation (Placement(
        transformation(extent={{80,-10},{60,10}})));
  Buildings.Fluid.Sources.MassFlowSource_T bou(
    redeclare package Medium = Medium,
    m_flow=0.1,
    nPorts=1)    "Boundary condition for mass flow rate"
    annotation (Placement(transformation(extent={{-80,-10},{-60,10}})));

  Modelica.Blocks.Sources.Step QSen_flow(height=1000,startTime=900)
    "Sensible heat flow rate"
    annotation (Placement(transformation(extent={{-80,60},{-60,80}})));
  Modelica.Blocks.Sources.Step QLat_flow(height=1000, startTime=1800)
    "Latent heat flow rate"
    annotation (Placement(transformation(extent={{-80,20},{-60,40}})));
protected
  Modelica.Blocks.Math.Gain mWat_flow(
    final k(unit="kg/J") = 1/h_fg,
    u(final unit="W"),
    y(final unit="kg/s")) "Water flow rate due to latent heat gain"
    annotation (Placement(transformation(extent={{-48,20},{-28,40}})));
equation

  connect(dynBal.Q_flow, QSen_flow.y) annotation (Line(points={{-12,46},{-36,46},
          {-36,70},{-59,70}}, color={0,0,127}));
  connect(dynBal.ports[1], sin.ports[1])
    annotation (Line(points={{-1,30},{2,30},{2,0},{60,0}}, color={0,127,255}));
  connect(bou.ports[1], dynBal.ports[2])
    annotation (Line(points={{-60,0},{1,0},{1,30}}, color={0,127,255}));
  connect(QLat_flow.y, mWat_flow.u)
    annotation (Line(points={{-59,30},{-50,30}}, color={0,0,127}));
  connect(mWat_flow.y, dynBal.mWat_flow) annotation (Line(points={{-27,30},{-20,
          30},{-20,42},{-12,42}}, color={0,0,127}));
  annotation (
  experiment(
      StopTime=2700,
      Tolerance=1e-06,
      __Dymola_Algorithm="Cvode"),
    uses(Modelica(version="4.0.0"), Buildings(version="10.0.0")));
end ConservationEquationStep;

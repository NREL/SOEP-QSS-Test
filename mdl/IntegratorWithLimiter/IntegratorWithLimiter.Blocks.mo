within ;
model IntegratorWithLimiter
  Modelica.Blocks.Sources.Constant const(k=1)
    annotation (Placement(transformation(extent={{-60,-10},{-40,10}})));
  Modelica.Blocks.Continuous.Integrator int(initType=Modelica.Blocks.Types.Init.InitialState)
    annotation (Placement(transformation(extent={{-20,-10},{0,10}})));
  Modelica.Blocks.Nonlinear.Limiter limiter(uMax=1, homotopyType=Modelica.Blocks.Types.LimiterHomotopy.NoHomotopy)
    annotation (Placement(transformation(extent={{20,-10},{40,10}})));
equation
  connect(const.y, int.u)
    annotation (Line(points={{-39,0},{-22,0}}, color={0,0,127}));
  connect(int.y, limiter.u)
    annotation (Line(points={{1,0},{18,0}}, color={0,0,127}));
  annotation (uses(Modelica(version="3.2.3")));
end IntegratorWithLimiter;

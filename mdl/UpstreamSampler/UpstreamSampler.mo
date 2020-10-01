within ;
model UpstreamSampler
  "Model with a time sampler and when constructs downstream"
  Buildings.Controls.OBC.CDL.Discrete.Sampler sam1(final samplePeriod=0.1)
    annotation (Placement(transformation(extent={{-60,-10},{-40,10}})));
  Buildings.Controls.OBC.CDL.Continuous.Gain gai(final k=0.5)
    annotation (Placement(transformation(extent={{-30,-10},{-10,10}})));
  Buildings.Controls.OBC.CDL.Continuous.Greater gre
    annotation (Placement(transformation(extent={{0,-10},{20,10}})));
  Buildings.Controls.OBC.CDL.Discrete.Sampler sam2(final samplePeriod=0.1)
    annotation (Placement(transformation(extent={{-60,-40},{-40,-20}})));
  Buildings.Controls.OBC.CDL.Logical.Switch swi
    annotation (Placement(transformation(extent={{40,-10},{60,10}})));
  Buildings.Controls.OBC.CDL.Conversions.RealToInteger reaToInt
    annotation (Placement(transformation(extent={{72,-10},{92,10}})));
  Buildings.Controls.OBC.CDL.Continuous.Greater greHys(h=1)
    annotation (Placement(transformation(extent={{0,-80},{20,-60}})));
  Buildings.Controls.OBC.CDL.Continuous.Sources.Constant con(k=0)
    annotation (Placement(transformation(extent={{0,20},{20,40}})));
  Buildings.Controls.OBC.CDL.Continuous.Sources.Constant con1(k=1)
    annotation (Placement(transformation(extent={{0,-40},{20,-20}})));
  Buildings.Controls.OBC.CDL.Continuous.Sources.Sine sin1(freqHz=0.5)
    annotation (Placement(transformation(extent={{-92,-10},{-72,10}})));
  Buildings.Controls.OBC.CDL.Continuous.Sources.Constant con2(k=0.1)
    annotation (Placement(transformation(extent={{-92,-40},{-72,-20}})));
equation
  connect(sam2.y, gre.u2) annotation (Line(points={{-38,-30},{-8,-30},{-8,-8},{
          -2,-8}}, color={0,0,127}));
  connect(sam1.y, gai.u)
    annotation (Line(points={{-38,0},{-32,0}}, color={0,0,127}));
  connect(gai.y, gre.u1)
    annotation (Line(points={{-8,0},{-2,0}}, color={0,0,127}));
  connect(gre.y, swi.u2)
    annotation (Line(points={{22,0},{38,0}}, color={255,0,255}));
  connect(swi.y, reaToInt.u)
    annotation (Line(points={{62,0},{70,0}}, color={0,0,127}));
  connect(con.y, swi.u1)
    annotation (Line(points={{22,30},{30,30},{30,8},{38,8}}, color={0,0,127}));
  connect(con1.y, swi.u3) annotation (Line(points={{22,-30},{30,-30},{30,-8},{38,
          -8}}, color={0,0,127}));
  connect(greHys.u1, gai.y) annotation (Line(points={{-2,-70},{-4,-70},{-4,0},{-8,
          0}}, color={0,0,127}));
  connect(greHys.u2, sam2.y) annotation (Line(points={{-2,-78},{-20,-78},{-20,-30},
          {-38,-30}}, color={0,0,127}));
  connect(sin1.y, sam1.u)
    annotation (Line(points={{-70,0},{-62,0}}, color={0,0,127}));
  connect(sam2.u, con2.y)
    annotation (Line(points={{-62,-30},{-70,-30}}, color={0,0,127}));
  annotation (
    Icon(coordinateSystem(preserveAspectRatio=false)),
    Diagram(coordinateSystem(preserveAspectRatio=false)),
    uses(Buildings(version="8.0.0")));
end UpstreamSampler;

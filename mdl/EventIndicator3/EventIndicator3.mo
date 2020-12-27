model EventIndicator3
  // Event indicator test model
  // Zero-crossing events change the state derivative via a discrete variable updated with the pre() operator
  Real x(start=1, fixed=true);
  discrete Real y(start=1, fixed=true);
equation
  der(x) = y;
  when (x >= 2) then
    y = pre(y)-2;
  elsewhen (x <= 1) then
    y = pre(y)+2;
  end when;
  annotation(experiment(StartTime=0, StopTime=5, Tolerance=1e-4));
end EventIndicator3;

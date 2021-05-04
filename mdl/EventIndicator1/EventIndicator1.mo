model EventIndicator1
  // Event indicator test model
  // Zero-crossing events change the state derivative via a discrete variable
  Real x(start=1, fixed=true);
  discrete Real y(start=1, fixed=true);
//  discrete output Real y(start=1, fixed=true); // As an output y is not short-circuited in dependencies
equation
  der(x) = y;
  when (x >= 2) then
    y = -1;
  elsewhen (x <= 1) then
    y = +1;
  end when;
  annotation(experiment(StartTime=0, StopTime=5, Tolerance=1e-4));
end EventIndicator1;

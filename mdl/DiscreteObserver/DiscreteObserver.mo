model DiscreteObserver
  // Discrete variable observer test model
  Real x(start=1, fixed=true);
  discrete output Real y(start=1, fixed=true); // y is an output so it is not short-circuited in dependencies
equation
  der(x) = y;
  when (x >= 2) then
    y = -x;
  elsewhen (x <= 1) then
    y = +x;
  end when;
  annotation(experiment(StartTime=0, StopTime=5, Tolerance=1e-4));
end DiscreteObserver;

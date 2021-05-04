model EventIndicator2
  // Event indicator test model
  // Zero-crossing events change the state value via reinit
  Real x(start=1, fixed=true);
equation
  der(x) = x;
  when (x >= 2) then
    reinit(x, 1);
  end when;
  annotation(experiment(StartTime=0, StopTime=5, Tolerance=1e-4));
end EventIndicator2;

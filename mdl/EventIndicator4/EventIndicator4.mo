model EventIndicator4
  // Event indicator test model
  // Zero-crossing events change the state derivative via a discrete variable
  // The zero-crossing functions cross zero rather than bouncing off it to show that the QSS-FMU zero-crossing protocol works well in this case
  // The discrete variable is an output so we can get its correct output even if tracked by QSS
  Real x(start=0, fixed=true);
  discrete output Real y(start=1, fixed=true);
equation
  der(x) = y;
  when (sin(time) >= 0.5) then
    y = -1;
  elsewhen (sin(time) <= -0.5) then
    y = +1;
  end when;
  annotation(experiment(StartTime=0, StopTime=25, Tolerance=1e-4));
end EventIndicator4;

model Achilles
  Real x1(start=0.0, fixed=true);
  Real x2(start=2.0, fixed=true);
equation
  der(x2) = -x1;
  der(x1) = 1.5 * x2 - 0.5 * x1;
annotation( experiment(StartTime=0, StopTime=10, Tolerance=1e-4) );
end Achilles;

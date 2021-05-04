model Achilles1
  output Real x1( start=0.0, fixed=true );
  input Real x2;
equation
  der(x1) = 1.5 * x2 - 0.5 * x1;
annotation( experiment( StartTime=0, StopTime=10, Tolerance=1e-4 ) );
end Achilles1;

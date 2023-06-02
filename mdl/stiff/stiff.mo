model stiff
  Real x1( start=0.0, fixed=true );
  Real x2( start=20.0, fixed=true );
equation
  der(x1) = 0.01 * x2;
  der(x2) = 2020.0 - 100.0 * x1 - 100.0 * x2;
annotation( experiment( StartTime=0, StopTime=600, Tolerance=1e-4 ) );
end stiff;

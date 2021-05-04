model sinusoid "This model simulates slow and fast dynamics via sinusoids"
  Real x1(start=0.01, fixed=true) "State variable";
  Real x2(start=0, fixed=true) "State variable";
equation
  der(x1) = 0.01 * cos( time );
  der(x2) = cos( time * 100 );
annotation ( experiment( StartTime=0, StopTime=1, Tolerance=1e-4 ) );
end sinusoid;

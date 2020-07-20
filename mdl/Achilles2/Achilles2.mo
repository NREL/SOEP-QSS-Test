model Achilles2
  input Real x1;
  output Real x2( start=2.0, fixed=true );
equation
  der(x2) = -x1;
annotation( experiment( StartTime=0, StopTime=10, Tolerance=1e-4 ) );
end Achilles2;

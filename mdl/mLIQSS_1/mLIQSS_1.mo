model mLIQSS_1 "Simple system demonstrating limitations of LIQSS solvers from Improving Linearly Implicit Quantized State System Methods paper"
  Real x1(start=-4, fixed=true);
  Real x2(start=+4, fixed=true);
equation
  der(x1) = -x1 - x2 + 0.2;
  der(x2) = +x1 - x2 + 1.2;
annotation( experiment( StartTime=0, StopTime=10, Tolerance=1e-12 ) );
end mLIQSS_1;

model DepTest4
  discrete output Real d(start = 0, fixed = true);
equation
  d = integer(time);
annotation( experiment(StartTime=0, StopTime=2.5, Tolerance=1e-4) );
end DepTest4;

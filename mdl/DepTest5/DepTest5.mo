model DepTest5
  Real s(start=0.0, fixed=true);
  Real r(start=1.0, fixed=true);
equation
  der(s) = 0.1;
  if time > r then
    r = s;
  else
    r = 1.0;
  end if;
annotation( experiment(StartTime=0, StopTime=5, Tolerance=1e-4) );
end DepTest5;

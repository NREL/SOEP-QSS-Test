model DepTest
  discrete Real l(start = 1.0, fixed = true);
equation
  when time > pre(l) then
    l = pre(l) + 1.0;
  end when;
annotation( experiment(StartTime=0, StopTime=5, Tolerance=1e-4) );
end DepTest;

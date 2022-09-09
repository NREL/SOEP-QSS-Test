model TimeTest
  discrete output Real x( start=0.0, fixed=true );
  discrete output Real nextSample( start = 1, fixed = true );
algorithm
  when time > pre(nextSample) then
    x := x + 1;
    nextSample := pre(nextSample) + 1;
  end when;
annotation( experiment( StartTime=0, StopTime=2, Tolerance=1e-4 ) );
end TimeTest;

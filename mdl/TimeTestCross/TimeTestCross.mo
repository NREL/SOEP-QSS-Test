model TimeTestCross
  discrete output Real x1( start=0.0, fixed=true);
  discrete output Real x2( start=0.0, fixed=true);
  discrete output Real nextSample1(start = 1, fixed = true);
  discrete output Real nextSample2(start = 1, fixed = true);
equation
  when time >= pre(nextSample1) then
    x1 = pre(x1) + 2;
    nextSample2 = pre(nextSample2) + 1;
  end when;
  when time >= pre(nextSample2) then
    x2 = pre(x2) + 1;
    nextSample1 = pre(nextSample1) + 1;
  end when;
annotation (experiment(StartTime = 0, StopTime = 2, Tolerance = 1e-4),
    Documentation(info = "<p>
This is a variant of the model TimeTest.
In this model, the first when block changes the
zero crossing function of the second when block
and vice versa.
</p>"));
end TimeTestCross;

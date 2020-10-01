within ;
model StateEvent6
  // This model has 8 state events at t=1.35s,
  // t = 2.39s, t = 3.85s, t = 4.9s, t = 6.35s,
  // t = 7.4s, t = 8.85s, t = 9.9s
  // when simulated from 0 to 10s.
  Real x1(start=1.1, fixed=true);
  Real x2(start=-2.5, fixed=true);
  Real x3(start=4, fixed=true);
  discrete output Real y;
equation
  der(x1) = cos(2*3.14*time/2.5);
  der(x2) = 1;
  der(x3) = -2;
  when (x1 > 1) then
    y = 1;
  elsewhen (x1 <= 1) then
    y = 0;
  end when
annotation (Documentation(info="<html>
<p>
This model has 8 state event at 1.35, 2.39,
3.85, 4.9, 6.35, 7.4, 8.85, 9.9s when simulated from 0 to 10s.
</p>
</html>"));
annotation( experiment( StartTime=0, StopTime=10, Tolerance=1e-4 ) );
end StateEvent6;

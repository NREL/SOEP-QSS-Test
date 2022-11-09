model DepTest6
  discrete output Real d;
  Real s1(start=0.0, fixed=true);
  Real s2(start=0.0, fixed=true);
  Real s3(start=0.0, fixed=true);
equation

  if time <= 5 then
    d = integer(0.5 + 0.75*sin(time)); // d changes
  else
    d = integer(0.5 + 0.45*sin(time)); // d fixed
  end if;

  der(s1) = 1 * ( 1.0 + d );
  der(s2) = 2 * ( 2.0 + d );
  der(s3) = 3 * ( 3.0 + d );

annotation( experiment(StartTime=0, StopTime=10, Tolerance=1e-4) );
end DepTest6;

// Demos purpose of discrete variables as update propagation firewalls
// Bypassing d in the QSS dependencies causes unnecessary state updates for t>5

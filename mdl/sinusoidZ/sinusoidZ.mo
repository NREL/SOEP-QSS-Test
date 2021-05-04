model sinusoidZ "This model is a simple torture test for zero crossings"
  Real x(start=1, fixed=true) "State variable";
  discrete output Real y(start=1, fixed=true) "Control variable";
equation
  der(x) = 50*y;
//when (sin(time*1000)+1 <= 0) then // FMU doesn't detect these "touch" crossings
  when (sin(time*1000)+0.9999 <= 0) then // FMU misses some of these "near-touch" crossings
//when (sin(time*1000)+0.999 <= 0) then
    y = -pre(y);
  end when;
annotation ( experiment( StartTime=0, StopTime=1, Tolerance=1e-6 ) );
end sinusoidZ;

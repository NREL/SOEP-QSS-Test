model IntegratorWithLimiter
  extends Modelica.Icons.Example;
  Real x( start=0.0, fixed=true );
  discrete Real y( start=0.0, fixed=true );
equation
  der(x) = 1;
  if ( x < 1 ) then
    y = 0;
  else
    y = 1;
  end if;
annotation ( experiment( StopTime=2, Tolerance=1e-6 ) );
end IntegratorWithLimiter;

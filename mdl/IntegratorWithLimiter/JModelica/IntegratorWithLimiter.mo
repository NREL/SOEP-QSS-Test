model IntegratorWithLimiter
  extends Modelica.Icons.Example;
  Real x( start=0.0, fixed=true );
  discrete Real y( start=0.0, fixed=true );
  Modelica.Blocks.Interfaces.RealOutput __zc_z "Zero crossing function";
  Modelica.Blocks.Interfaces.RealOutput __zc_der_z "Derivative of zero crossing function";
equation
  der(x) = 1;
  if ( x < 1 ) then
    y = 0;
  else
    y = 1;
  end if;
  __zc_z = x - 1;
  __zc_der_z = 1;
annotation ( experiment( StopTime=2, Tolerance=1e-6 ) );
end IntegratorWithLimiter;

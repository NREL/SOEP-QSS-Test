model EventIndicator5
  // Event indicator test model
  // Zero-crossing events change the state derivative via a discrete variable
  // A discrete sampler is used in the zero-crossing functions
  Real T(start=1, fixed=true);
  discrete output Real y(start=1, fixed=true);
equation
  der(T) = y;
  when sample(0,0.1) and (T > 2.99) then
    y = -1;
  elsewhen sample(0,0.1) and (T < 1.01) then
    y = +1;
  end when;
  annotation(experiment(StartTime=0, StopTime=10, Tolerance=1e-4));
end EventIndicator5;

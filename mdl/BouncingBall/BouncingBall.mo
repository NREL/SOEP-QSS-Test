model BouncingBall "This model simulates the bouncing ball"
  extends Modelica.Icons.Example;
  type Height = Real (quantity="Height", unit="m");
  type Velocity = Real (quantity="Velocity", unit="m/s");
  parameter Real e=0.8 "Coefficient of restitution";
  parameter Height h0=1.0 "Initial height";
  Height h;
  Velocity v(start=0.0, fixed=true);
initial equation
  h = h0;
equation
  v = der(h);
  der(v) = -9.80665;
  when h < 0 then
    reinit(v, -e*pre(v));
  end when;
annotation (
  experiment( StartTime=0, StopTime=3, Tolerance=1e-4 ),
  Icon(coordinateSystem(preserveAspectRatio=false)),
  Diagram(coordinateSystem(preserveAspectRatio=false)),
  Documentation(revisions="<html>
<ul>
<li>
June 20, 2017, by Thierry S. Nouidui:<br/>
Implemented first version.
</li>
</ul>
</html>", info="<html>
<p>
This model simulates the bouncing ball.
</p>
<p>
This model has 12 state events when simulated from 0 to 3s.
</p>
</html>"));
end BouncingBall;

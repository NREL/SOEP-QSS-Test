model ZCBoolean2
  "This model tests state event detection with boolean zero crossing"
  extends Modelica.Icons.Example;
  function booToRea "This function converts a Boolean to a Real"
    input Boolean u "Boolean input";
    output Real y "Real output";
  algorithm
    y := if u then 1.0 else 0.0;
  end booToRea;
  Real x(start=1, fixed=true);
  Real u "Internal input signal";
  Boolean yBoo "Boolean variable";
  Boolean yBooPre "Boolean variable for pre(yBoo)";
  discrete Modelica.Blocks.Interfaces.RealOutput y(start=1.0, fixed=true);
initial equation
  pre(yBoo) = true;
equation
  u = Modelica.Math.sin(time);
  der(x) = y;
  when (pre(yBoo) and u >= 0.5) then
    y = 1.0;
    yBoo = false;
  elsewhen (not pre(yBoo) and u <= -0.5) then
    y = -1.0;
    yBoo = true;
  end when;
  // Defining the boolean conditional
  // variable for the zero crossing variables
  yBooPre = pre(yBoo);
  annotation (
    experiment( StartTime=0, StopTime=10, Tolerance=1e-4 ),
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
This model has 4 state events at
t=0.5235s, 3.66519s, 6.80678s,
9.94838s when simulated from 0 to 10s.
This model has a variable <pre>yBooPre</pre>
which is used to multiply the zero crossing
variables so they can be updated when the correct
conditions are met.
</p>
</html>"));
end ZCBoolean2;

model Quadratic "This model simulates a quadratic"
  extends Modelica.Icons.Example;
  Real x(start=0, fixed=true) "State variable";
equation
  der(x) = time;
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
This model simulates a quadratic.
</p>
</html>"));
end Quadratic;

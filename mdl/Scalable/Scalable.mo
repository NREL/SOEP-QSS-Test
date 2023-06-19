within Buildings.Examples.ScalableBenchmarks.BuildingVAV.Examples;
model Scalable "Closed-loop model with Z zones in F floors"
  extends Buildings.Examples.ScalableBenchmarks.BuildingVAV.Examples.OneFloor_OneZone(
    nFlo=1,
    nZon=1);

annotation (
  experiment(StopTime=604800, Tolerance=1e-06),
  Diagram(coordinateSystem(preserveAspectRatio=false, extent={{-360,-120},{140,200}})),
  Documentation(info="<html>
<p>
The model demonstrates the scalability of model
<a href=\"modelica://Buildings.Examples.ScalableBenchmarks.BuildingVAV.Examples.OneFloor_OneZone\">
Buildings.Examples.ScalableBenchmarks.BuildingVAV.Examples.OneFloor_OneZone</a>
by setting it to be a multizone model with Z zones in F floors, i.e.
<code>nFlo=F, nZon=Z</code>.
</p></html>", revisions="<html>
<ul>
<li>
June 16, 2017, by Jianjun Hu:<br/>
First implementation.
</li>
</ul>
</html>"));
end Scalable;

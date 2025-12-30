# Interactive Fibre Angle Calculator

A Dash app for exploring fibre angles on a braiding machine with 192 horn gears. Adjust mandrel diameter, horn gear speed (HGS), and a target fibre angle to see the required mandrel velocity and visualize the relationship.

## Quick start

1. Install dependencies (use a virtual environment if you prefer):

```
pip install dash dash-bootstrap-components plotly numpy
```

2. Run the app:

```
python radiiBraid_interactive.py
```

3. Open the browser at http://127.0.0.1:8050/ (shown in the terminal) to use the UI.

## How it works

The fibre angle $\alpha$ in degrees is computed from:

$$
\alpha = \tan^{-1}\left(\frac{\pi \cdot d_m \cdot \text{HGS}}{(n/4) \cdot v \cdot 60}\right)
$$

- $d_m$: mandrel diameter (mm)
- HGS: horn gear speed (RPM)
- $n$: number of horn gears (fixed at 192)
- $v$: mandrel surface velocity (mm/s)

For a chosen target angle, the app finds the velocity $v$ where the computed $\alpha$ is closest to the target and highlights that intersection.

## UI controls

- Mandrel diameter: slider and numeric input, 1 to 1000 mm.
- Horn gear speed: slider and numeric input, 25 to 150 RPM.
- Target fibre angle: slider and numeric input, 10 to 80 degrees.

## Outputs

- Plot of fibre angle versus mandrel velocity with the current HGS and mandrel diameter.
- Dashed target-angle line.
- Red marker at the velocity where the computed angle meets the target.
- Text panel summarizing the inputs and the velocity needed to achieve the target angle.

## Notes

- The velocity search range is 0 to 100 mm/s. Adjust this in radiiBraid_interactive.py if you need to explore higher speeds.
- All angles are shown in degrees; velocities are in mm/s.

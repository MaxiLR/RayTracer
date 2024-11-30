#include "colors.inc"

light_source {
  <30, 50, -30>, 
  color rgb <1, 1, 1>
}

light_source {
  <-30, 20, -10>,
  color rgb <0.8, 0.8, 1>
}

light_source {
  <0, 10, 30>,
  color rgb <1, 0.6, 0.6>
}

camera {
  location <5, 5, -10>
  look_at <-0.5, -0.75, -0.5>
  angle 40
}


box { <-4.2, -4.2, -4.2>, <-2.2, -2.2, -2.2> pigment { color rgb <1, 0, 0> } scale <0.4,0.4,0.4>}
box { <-2, -4.2, -4.2>, <0.001, -2.2, -2.2> pigment { color rgb <0, 1, 0> } scale <0.4,0.4,0.4>}
box { <0.2, -4.2, -4.2>, <2.2, -2.2, -2.2> pigment { color rgb <0, 0, 1> } scale <0.4,0.4,0.4>}
box { <-4.2, -4.2, -2>, <-2.2, -2.2, 0> pigment { color rgb <1, 1, 0> } scale <0.4,0.4,0.4>}
box { <-2, -4.2, -2>, <0.001, -2.2, 0> pigment { color rgb <1, 0.5, 0> } scale <0.4,0.4,0.4>}
box { <0.2, -4.2, -2>, <2.2, -2.2, 0> pigment { color rgb <1, 1, 1> } scale <0.4,0.4,0.4>}
box { <-4.2, -4.2, 0.2>, <-2.2, -2.2, 2.2> pigment { color rgb <0, 1, 1> } scale <0.4,0.4,0.4>}
box { <-2, -4.2, 0.2>, <0.001, -2.2, 2.2> pigment { color rgb <1, 0, 1> } scale <0.4,0.4,0.4>}
box { <0.2, -4.2, 0.2>, <2.2, -2.2, 2.2> pigment { color rgb <0.5, 0.5, 0.5> } scale <0.4,0.4,0.4>}

box { <-4.2, -2, -4.2>, <-2.2, 0, -2.2> pigment { color rgb <1, 0, 0> } scale <0.4,0.4,0.4>}
box { <-2, -2, -4.2>, <0.001, 0, -2.2> pigment { color rgb <0, 1, 0> } scale <0.4,0.4,0.4>}
box { <0.2, -2, -4.2>, <2.2, 0, -2.2> pigment { color rgb <0, 0, 1> } scale <0.4,0.4,0.4>}
box { <-4.2, -2, -2>, <-2.2, 0, 0> pigment { color rgb <1, 1, 0> } scale <0.4,0.4,0.4>}
box { <-2, -2, -2>, <0.001, 0, 0> pigment { color rgb <1, 0.5, 0> } scale <0.4,0.4,0.4>}
box { <0.2, -2, -2>, <2.2, 0, 0> pigment { color rgb <1, 1, 1> } scale <0.4,0.4,0.4>}
box { <-4.2, -2, 0.2>, <-2.2, 0, 2.2> pigment { color rgb <0, 1, 1> } scale <0.4,0.4,0.4>}
box { <-2, -2, 0.2>, <0.001, 0, 2.2> pigment { color rgb <1, 0, 1> } scale <0.4,0.4,0.4>}
box { <0.2, -2, 0.2>, <2.2, 0, 2.2> pigment { color rgb <0.5, 0.5, 0.5> } scale <0.4,0.4,0.4>}

box { <-4.2, 0.2, -4.2>, <-2.2, 2.2, -2.2> pigment { color rgb <1, 0, 0> } scale <0.4,0.4,0.4>}
box { <-2, 0.2, -4.2>, <0.001, 2.2, -2.2> pigment { color rgb <0, 1, 0> } scale <0.4,0.4,0.4>}
box { <0.2, 0.2, -4.2>, <2.2, 2.2, -2.2> pigment { color rgb <0, 0, 1> } scale <0.4,0.4,0.4>}
box { <-4.2, 0.2, -2>, <-2.2, 2.2, 0> pigment { color rgb <1, 1, 0> } scale <0.4,0.4,0.4>}
box { <-2, 0.2, -2>, <0.001, 2.2, 0> pigment { color rgb <1, 0.5, 0> } scale <0.4,0.4,0.4>}
box { <0.2, 0.2, -2>, <2.2, 2.2, 0> pigment { color rgb <1, 1, 1> } scale <0.4,0.4,0.4>}
box { <-4.2, 0.2, 0.2>, <-2.2, 2.2, 2.2> pigment { color rgb <0, 1, 1> } scale <0.4,0.4,0.4>}
box { <-2, 0.2, 0.2>, <0.001, 2.2, 2.2> pigment { color rgb <1, 0, 1> } scale <0.4,0.4,0.4>}
box { <0.2, 0.2, 0.2>, <2.2, 2.2, 2.2> pigment { color rgb <0.5, 0.5, 0.5> } scale <0.4,0.4,0.4>}

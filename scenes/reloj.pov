#include "colors.inc"

camera {
  location <30, -10, 50>
  look_at <0, 0, 0>
  angle 35
}

light_source {
  <0,0,20>,
  color rgb <1, 1, 1>
}

box { <-10, -10, -1>, <10, 10, -0.5> pigment { color rgb <1, 0, 0> } }
box { <-9, -9, -0.8>, <9, 9, -0.1> pigment { color rgb <1, 1, 1> } }

sphere { <7, 0, 0>, 0.5 pigment { color rgb <1, 0, 0> } }
sphere { <5.5, 5.5, 0>, 0.5 pigment { color rgb <1, 0, 0> } }
sphere { <0, 7, 0>, 0.5 pigment { color rgb <1, 0, 0> } }
sphere { <-5.5, 5.5, 0>, 0.5 pigment { color rgb <1, 0, 0> } }
sphere { <-7, 0, 0>, 0.5 pigment { color rgb <1, 0, 0> } }
sphere { <-5.5, -5.5, 0>, 0.5 pigment { color rgb <1, 0, 0> } }
sphere { <0, -7, 0>, 0.5 pigment { color rgb <1, 0, 0> } }
sphere { <5.5, -5.5, 0>, 0.5 pigment { color rgb <1, 0, 0> } }
sphere { <7, 0, 0>, 0.5 pigment { color rgb <1, 0, 0> } }
sphere { <5.5, 5.5, 0>, 0.5 pigment { color rgb <1, 0, 0> } }
sphere { <0, 7, 0>, 0.5 pigment { color rgb <1, 0, 0> } }
sphere { <-5.5, 5.5, 0>, 0.5 pigment { color rgb <1, 0, 0> } }


box { <0.1, 0, -0.05>, <0.3, 4, 0.05> pigment { color rgb <1, 0, 0> } }

box { <0, 0.05, -0.05>, <5, 0.15, 0.05> pigment { color rgb <1, 0, 0> } }

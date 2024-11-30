#include "colors.inc"

light_source {
    <0, 70, -100>, color rgb <1, 1, 1>
}

light_source {
    <100, 70, 100>, color rgb <0.5, 0.5, 0.5>
}

camera {
    location <-5, 7, -14>
    look_at <0, 0, 0>
    angle 45
}

box {
    <-50, -22, -50>, <50, -21, 50>
    pigment { color rgb <0.5, 0.8, 1> }
    scale 0.3
    translate <0, 2.5, 0>
}

sphere {
    <0, 0, 0>, 0.75
    pigment { color rgb <0, 0, 1> }
    translate <0, 2.5, 0>
}
sphere {
    <-0.21, 0.15, -0.6>, 0.12
    pigment { color rgb <1, 1, 1> }
    translate <0, 2.5, 0>
}
sphere {
    <0.21, 0.15, -0.6>, 0.12
    pigment { color rgb <1, 1, 1> }
    translate <0, 2.5, 0>
}
box {
    <-2, 0, -0.3>, <-2.5, 3, 0.3>
    pigment { color rgb <1, 0.8, 0> }
    scale 0.3
    translate <0, 2.5, 0>
}
box {
    <2, 0, -0.3>, <2.5, 3, 0.3>
    pigment { color rgb <1, 0.8, 0>  }
    scale 0.3
    translate <0, 2.5, 0>
}

box {
    <-3, -6.5, -2>, <3, -2, 2>
    pigment { color rgb <1, 0, 0> }
    scale 0.3
    translate <0, 2.5, 0>
}
box {
    <-2.2, -12, -1.8>, <2.2, -6.5, 1.8>
    pigment { color rgb <0, 0, 1> }
    scale 0.3
    translate <0, 2.5, 0>
}

ovus {
    1, 0.7
    translate <-3.5, -4, 0>
    pigment { color rgb <1, 0.8, 0> }
    scale 0.3
    translate <0, 2.5, 0>
}
box {
    <-3.2, -4, -0.3>, <-4.2, -9, 0.3>
    pigment { color rgb <1, 0, 0>  }
    rotate <45, 0, 0>
    scale 0.3
    translate <0, 2.3, 0.8>
}
sphere {
    <-1.11, -2.4, 0>, 0.24
    pigment { color rgb <0, 0, 1>  }
    translate <0, 2.8, -1.1>
}

ovus {
    1, 0.7
    translate <3.5, -4, 0>
    pigment { color rgb <1, 0.8, 0> }
    scale 0.3
    translate <0, 2.5, 0>
}
box {
    <3.2, -4, -0.3>, <4.2, -9, 0.3>
    pigment { color rgb <1, 0, 0>  }
    scale 0.3
    translate <0, 2.5, 0>
}
sphere {
    <1.11, -2.8, 0>, 0.24
    pigment { color rgb <0, 0, 1>  }
    translate <0, 2.5, 0>
}

box {
    <-1.6, -12, -0.35>, <-0.6, -20, 0.35>
    pigment { color rgb <1, 0, 0>  }
    scale 0.3
    translate <0, 2.5, 0>
}
ovus {
    1, 0.7
    translate <-1.2, -20, 0>
    pigment { color rgb <0, 0, 1>  }
    scale 0.3
    translate <0, 2.5, 0>
}

box {
    <0.6, -12, -0.35>, <1.6, -20, 0.35>
    pigment { color rgb <1, 0, 0>  }
    scale 0.3
    translate <0, 2.5, 0>
}
ovus {
    1, 0.7
    translate <1.2, -20, 0>
    pigment { color rgb <0, 0, 1>  }
    scale 0.3
    translate <0, 2.5, 0>
}

box {
    <-2.1, -20, -1.5>, <-0.4, -21, 1.5>
    pigment { color rgb <0, 0, 1>  }
    scale 0.3
    translate <0, 2.5, 0>
}
box {
    <0.4, -21, -1.5>, <2.1, -20, 1.5>
    pigment { color rgb <0, 0, 1>  }
    scale 0.3
    translate <0, 2.5, 0>
}

cone {
    <0, 0, 0>, 0.3,
    <0, 7, 0>, 0
    pigment { color rgb <1, 0.8, 0> }
    scale 0.3
    translate <0, 2.5, 0>
}
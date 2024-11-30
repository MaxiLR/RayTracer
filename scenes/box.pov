#include "colors.inc"

light_source {
    <15, 30, 0>, color rgb <1, 1, 1>
}

camera {
    location <0, 10, -10>
    look_at <0, 0, 0>
    angle 45
}

box {
    <-1.5,0,-1.5>,<1.5,3,1.5> 
    pigment{
        color rgb <1,0,0>
    }
}

box {
    <-100,-100,-100>,<100,0,100> 
    pigment{
        color rgb <1,1,0>
    }
}
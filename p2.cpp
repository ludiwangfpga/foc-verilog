#include <stdint.h>
#include "park_inverse.h"
#include "sin_cos_table.h"

void park_inverse(int64_t& s_axis, int64_t& m_axis){
#pragma HLS interface axis port=m_axis
#pragma HLS interface ap_ctrl_none port=return
#pragma HLS interface axis port=s_axis
    int64_t in_data, res;
    int32_t Vd, Vq, Theta;
    int32_t Vd_cos, Vq_sin, Vq_cos, Vd_sin;
    int32_t Valpha, Vbeta;
    int32_t cos_theta, sin_theta;

    // Process data
    in_data = s_axis;                           // Assign input value
    Vd = int16_t(in_data & 0xFFFF);              // Extract Vd - bits[15..0] from input value
    Vq = int16_t((in_data >> 16) & 0xFFFF);      // Extract Vq - bits[32..16] from input value
    Theta = int16_t((in_data >> 32) & 0xFFFF);   // Extract Theta - bits[47..32] from input value

    // Rest of the code remains the same
    cos_theta = (int32_t)cos_table[Theta];
    sin_theta = (int32_t)sin_table[Theta];
    Vd_cos = Vd * cos_theta;
    Vq_sin = Vq * sin_theta;
    Vq_cos = Vq * cos_theta;
    Vd_sin = Vd * sin_theta;
    Valpha = (Vd_cos - Vq_sin) >> 15;
    Vbeta  = (Vq_cos + Vd_sin) >> 15;
    Valpha = (Valpha > MAX_LIM) ? MAX_LIM : Valpha;    // Clip max
    Valpha = (Valpha < MIN_LIM) ? MIN_LIM : Valpha;    // Clip min
    Vbeta  = (Vbeta  > MAX_LIM) ? MAX_LIM : Vbeta;    // Clip max
    Vbeta  = (Vbeta  < MIN_LIM) ? MIN_LIM : Vbeta;    // Clip min

    // Write output stream
    res =    (((int64_t)Theta << 32)    & 0x0000FFFF00000000) | // Put Theta bits[47:32]
            (((int64_t)Vbeta << 16)    & 0x00000000FFFF0000) | // Put Vbeta bits[31:16]
            ( (int64_t)Valpha            & 0x000000000000FFFF);    // Put Valpha bits[15:0]
    m_axis = res;                                // Assign result to the output value
}

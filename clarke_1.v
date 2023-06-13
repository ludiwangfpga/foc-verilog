`timescale 1ns / 1ps
module clarke_inverse (
    input  wire               clk,
    input  wire               rst,
    input  wire               enable,
    input  wire       [63:0]  s_axis,
    output reg        [63:0]  m_axis
);

    // Constants
    parameter MAX_LIM = 16'h7FFF;
    parameter MIN_LIM = 16'h8001;
    parameter SQRT3C = 32'h0000DDB4;

    // Variables
    reg  [15:0] Valpha, Vbeta, Theta;
    reg  [31:0] s3vb;
    reg  [15:0] Va, Vb, Vc;
    // Clock process
    always @(posedge clk) begin
        if (rst) begin
            // Reset logic here
        end else if (enable) begin
            // Decode input stream
            Valpha <= s_axis[15:0];
            Vbeta <= s_axis[31:16];
            Theta <= s_axis[47:32];

            // Process data
            Va <= Valpha;
            s3vb <= Vbeta * SQRT3C;
          
            Vb <= ((s3vb >> 15) - Valpha)>> 1 ;
            
            Vc <= (0 - Valpha - (s3vb >> 15)) >> 1;

            
            // Write output stream
            m_axis <= {Theta, Vc, Vb, Va};
        end
    end

endmodule


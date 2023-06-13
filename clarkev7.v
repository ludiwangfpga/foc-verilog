`timescale 1ns / 1ps
module clarke_inverse (
   input  wire                clk,
    input  wire               rst,
    input  wire       [63:0]  s_axis,
    input  wire               s_axis_tvalid,
    input  wire               m_axis_tready,
    output wire               s_axis_tready,
    output reg        [63:0]  m_axis,
    output reg                m_axis_tvalid
    
    //input  wire               enable,

);

    // Constants

    parameter SQRT3C = 32'h0000DDB4;
    assign m_axis_tready = 1'b1;
    // Variables
    reg  [15:0] Valpha, Vbeta, Theta;
    reg  [31:0] s3vb;
    reg  [15:0] Va, Vb, Vc;
    // Clock process
    always @(posedge clk) begin
        if (rst) begin
            // Reset logic here
      Valpha <= 16'd0;
      Vbeta <= 16'd0;
      Theta <= 16'd0;
      s3vb <= 0;
      Va <= 32'd0;
      Vb <= 32'd0;
      Vc <= 32'd0;
        end else if (s_axis_tvalid) begin
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
            m_axis_tvalid <= 1'b1;
           
        end
    end
assign s_axis_tready = 1'b1;
endmodule

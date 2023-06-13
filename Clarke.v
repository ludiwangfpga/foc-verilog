`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/05/09 12:57:23
// Design Name: 
// Module Name: Clarke_Inverse
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////

`timescale 1ns / 1ps

module Clarke_Inverse (
  input wire clk,
  input wire reset,
  input wire [63:0] s_axis_tdata,
  input wire s_axis_tvalid,
  output wire s_axis_tready,
  output reg [63:0] m_axis_tdata,
  output reg m_axis_tvalid,
  input wire m_axis_tready
);

  reg [15:0] Valpha, Vbeta, Theta;
  reg signed [31:0] s3vb; // Clarke Inverse
  reg signed [31:0] Va, Vb, Vc; // Clarke Inverse -> SVPWM
  reg [1:0] state = 0;
  parameter signed [31:0] MAX_LIM = 32767; // 
  parameter signed [31:0] MIN_LIM = -32767; // 
  parameter signed [31:0] SQRT3C = 28377; // sqrt(3)*(2^15)


  assign m_axis_tready = 1'b1;

  always @(posedge clk) begin
    if (reset) begin
      Valpha <= 16'd0;
      Vbeta <= 16'd0;
      Theta <= 16'd0;
      s3vb <= 0;
      Va <= 32'd0;
      Vb <= 32'd0;
      Vc <= 32'd0;
      state <= 2'b00;
    end else begin
      case (state)
        2'b00: begin // Wait for valid input data
          if (s_axis_tvalid) begin
            Valpha <= s_axis_tdata[15:0];
            Vbeta <= s_axis_tdata[31:16];
            Theta <= s_axis_tdata[47:32];
            s3vb <= Vbeta * SQRT3C;
            state <= 2'b01;
          end
        end
        2'b01: begin // Process data
          
          Va <= Valpha;
          Vb <= ((s3vb >> 15) - Valpha) >> 1;
          Vc <= (0 - Valpha - (s3vb >> 15)) >> 1;
          Vb <= (Vb > MAX_LIM) ? MAX_LIM : Vb;
          Vb <= (Vb < MIN_LIM) ? MIN_LIM : Vb;
          Vc <= (Vc > MAX_LIM) ? MAX_LIM : Vc;
          Vc <= (Vc < MIN_LIM) ? MIN_LIM : Vc;
          state <= 2'b10;
        end
        2'b10: begin // Output result
          m_axis_tdata <= {Theta, Vc, Vb, Va};
          m_axis_tvalid <= 1'b1;
          state <= 2'b00;
        end
      endcase
    end
  end

  assign s_axis_tready = (state == 2'b00);

endmodule




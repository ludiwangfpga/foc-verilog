`timescale 1ns / 1ps

module tb_park_inverse;

    // Parameters
    reg clk;
    reg rst;
    reg enable;
    reg [31:0] s_axis1;
    reg [31:0] s_axis2;
    wire [63:0] m_axis;

    // Instantiate the park_inverse module
    park_inverse u1 (
        .clk(clk),
        .rst(rst),
        .enable(enable),
        .s_axis1(s_axis1),
        .s_axis2(s_axis2),
        .m_axis(m_axis)
    );

    // Clock process
    initial begin
        clk = 0;
        forever #10 clk = ~clk;
    end

    // Stimulus process
    initial begin
        // Reset
        rst = 1;
        enable = 0;
        s_axis1 = 0;
        s_axis2 = 0;
        #20 rst = 0;

        // Apply some input data
        #20 enable = 1;
        // s_axis is formed by {Theta, Vq, Vd}
        #20 s_axis1 = { 16'hFC28, 16'hFDA8};
            s_axis2 = { 16'h0064}; // Theta is 888 (16'h0064), Vq is 16'h1111, Vd is 16'h2222
       // #20 s_axis = {16'h0064, 16'hFC28, 16'hFDA8}; // Theta is 888 (16'h0064), Vq is 16'h3333, Vd is 16'h4444
        
        // Finish the simulation
        #200 $finish;
    end

endmodule


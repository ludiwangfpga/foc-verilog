module parkclark_tb;

  // Parameters
  parameter CLK_PERIOD = 10; // 10 ns

  // Inputs
  reg clk;
  reg reset;
  reg [63:0] s_axis_tdata;
  reg s_axis_tvalid;
  reg m_axis_tready;

  // Outputs
  wire s_axis_tready;
  wire [63:0] m_axis_tdata;
  wire m_axis_tvalid;

  // Instantiate the clarke_inverse module
  parkclarke dut (
    .clk(clk),
    .reset(reset),
    .tlast(tlast),
    .s_axis_tdata(s_axis_tdata),
    .s_axis_tvalid(s_axis_tvalid),
    .m_axis_tdata(m_axis_tdata),
    .m_axis_tvalid(m_axis_tvalid),
    .m_axis_tready(m_axis_tready),
    .s_axis_tready(s_axis_tready)
  );

  // Clock generation
  always #((CLK_PERIOD / 2)) clk = ~clk;

  // Initial block
  initial begin
    $dumpfile("parkclark_tb.vcd");
    $dumpvars(0, parkclark_tb);

    clk = 0;
    reset = 1;
    s_axis_tdata = 64'h0000_FC28_FDA8_0064;
    s_axis_tvalid = 0;
    m_axis_tready = 1;

    // Wait for some time
    #100;

    // Deassert reset
    reset = 0;

    // Start providing input values
    s_axis_tvalid = 1;

    // Wait for simulation to finish
    #500;

    $finish;
  end

  // Monitor the output m_axis
  always @(posedge clk) begin
    if (m_axis_tvalid) begin
      $display("m_axis = %h", m_axis_tdata);
    end
  end

endmodule

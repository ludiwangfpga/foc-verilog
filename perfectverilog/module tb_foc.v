`timescale 1ns/1ps

module tb_foc();

    reg [15:0] angle; // 电角度, 现在明确指定为16位
    reg S_AXI_ACLK;    
    reg [15:0] ud; // 16-bit fixed point number
    reg [15:0] uq;  // 时钟信号
    wire signed [31:0] ia, ib, ic; // 输出电流值

    // 实例化待测模块
    foc uut (
        .angle(angle),
        .S_AXI_ACLK(S_AXI_ACLK),
        .ud(ud),
        .uq(uq),
        .ia(ia),
        .ib(ib),
        .ic(ic)
    );

    initial begin
        // 初始化信号
        S_AXI_ACLK = 0;
        ud = 16'd0001; // 示例值
        uq = 16'd0000; // 示例值

        // 创建时钟信号，假设时钟周期为10 ns（100 MHz）
        forever #5 S_AXI_ACLK = ~S_AXI_ACLK;
    end

    initial begin
        // 模拟一个周期的输入
        for (angle = 0; angle < 502; angle = angle + 1) begin
            #1; // 假设每个度对应10 ns
        end
        
        // 结束模拟
        $stop;
    end

    initial begin
        // 每个时钟周期输出信号的值
        while (1) begin
            @(posedge S_AXI_ACLK);
            $display($time, " ia=%d ib=%d ic=%d", ia, ib, ic);
        end
    end

endmodule

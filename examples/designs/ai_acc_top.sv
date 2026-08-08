module ai_acc_top(input logic clk, input logic rst_n, input logic [7:0] a, b, output logic [15:0] y);
  logic [3:0] count;
  counter u_counter(.clk(clk), .rst_n(rst_n), .count(count));
  mac_unit u_mac(.clk(clk), .a(a), .b(b), .y(y));
endmodule

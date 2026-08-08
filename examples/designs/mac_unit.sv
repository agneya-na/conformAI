module mac_unit(input logic clk, input logic [7:0] a, b, output logic [15:0] y);
  always_ff @(posedge clk) begin
    y <= a * b;
  end
endmodule

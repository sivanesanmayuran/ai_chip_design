// Simple APB3 GPIO. Regs: 0x0 DATA_OUT, 0x4 DIR (1=out), 0x8 DATA_IN (ro)
module apb_gpio #(
  parameter int WIDTH = 8
) (
  input  logic             pclk,
  input  logic             presetn,
  input  logic             psel,
  input  logic             penable,
  input  logic             pwrite,
  input  logic [3:0]       paddr,
  input  logic [31:0]      pwdata,
  output logic [31:0]      prdata,
  output logic             pready,
  input  logic [WIDTH-1:0] gpio_in,
  output logic [WIDTH-1:0] gpio_out,
  output logic [WIDTH-1:0] gpio_dir
);
  assign pready = 1'b1;

  wire wr = psel & penable & pwrite;

  always_ff @(posedge pclk or negedge presetn) begin
    if (!presetn) begin
      gpio_out <= '0;
      gpio_dir <= '0;
    end else if (wr) begin
      case (paddr[3:2])
        2'd0: gpio_out <= pwdata[WIDTH-1:0];
        2'd1: gpio_dir <= pwdata[WIDTH-1:0];
        default: ;
      endcase
    end
  end

  always_comb begin
    prdata = '0;
    case (paddr[3:2])
      2'd0: prdata[WIDTH-1:0] = gpio_out;
      2'd1: prdata[WIDTH-1:0] = gpio_dir;
      2'd2: prdata[WIDTH-1:0] = gpio_in;
      default: ;
    endcase
  end
endmodule

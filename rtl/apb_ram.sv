`timescale 1ns / 1ps

module apb_ram (
    input  logic        pclk,
    input  logic        presetn,   // active-low reset
    input  logic        psel,
    input  logic        penable,
    input  logic        pwrite,
    input  logic [31:0] paddr,
    input  logic [31:0] pwdata,
    output logic [31:0] prdata,
    output logic        pready,
    output logic        pslverr
);

    // 32 x 32-bit memory
    logic [31:0] mem [0:31];

    typedef enum logic [1:0] {
        IDLE     = 2'b00,
        SETUP    = 2'b01,
        ACCESS   = 2'b10,
        TRANSFER = 2'b11
    } state_t;

    state_t state;

    integer i;

    always_ff @(posedge pclk) begin
        if (!presetn) begin
            state   <= IDLE;
            prdata  <= 32'h0;
            pready  <= 1'b0;
            pslverr <= 1'b0;

            for (i = 0; i < 32; i++) begin
                mem[i] <= 32'h0;
            end
        end
        else begin
            case (state)

                IDLE: begin
                    pready  <= 1'b0;
                    pslverr <= 1'b0;
                    state   <= SETUP;
                end

                SETUP: begin
                    if (psel)
                        state <= ACCESS;
                end

                ACCESS: begin
                    if (penable) begin
                        pready <= 1'b1;

                        // WRITE
                        if (pwrite) begin
                            if (paddr < 32) begin
                                mem[paddr] <= pwdata;
                                pslverr    <= 1'b0;
                            end
                            else begin
                                pslverr <= 1'b1;
                            end
                        end
                        // READ
                        else begin
                            if (paddr < 32) begin
                                prdata  <= mem[paddr];
                                pslverr <= 1'b0;
                            end
                            else begin
                                prdata  <= 32'hXXXXXXXX;
                                pslverr <= 1'b1;
                            end
                        end

                        state <= TRANSFER;
                    end
                end

                TRANSFER: begin
                    pready  <= 1'b0;
                    pslverr <= 1'b0;
                    state   <= SETUP;
                end

                default: state <= IDLE;

            endcase
        end
    end

endmodule


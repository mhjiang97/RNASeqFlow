library(hexSticker)
library(showtext)
font_add_google("Gochi Hand", "gochi")
showtext_auto()
img <- "./VCG41165645202.jpg"
sticker(
  img, package = "RSWP", p_size = 10, s_x = 1, s_y = .75, s_width = .6, s_height = .5,
  h_size = .7, h_fill = "white", p_color = "#228B22", h_color = "#006400", p_family = "gochi",
  filename = "~/Downloads/test.png"
)

from PIL import Image
import numpy as np

def get_palette (data):
	unique, counts = np.unique(data.reshape(-1, data.shape[2]), axis = 0, return_counts = True)
	mask = (unique[:, 3] != 0)
	return sorted(zip(unique[mask], counts[mask]), key = lambda x: x[1], reverse = True)

def replace_color (data, src, dst):
	red, green, blue, alpha = data.T
	src_mask = (red == src[0]) & (green == src[1]) & (blue == src[2])
	data[..., :-1][src_mask.T] = dst
	return

def swap_palettes (path1, path2):
	image1 = Image.open(path1).convert('RGBA')
	image2 = Image.open(path2).convert('RGBA')
	data1 = np.array(image1)
	data2 = np.array(image2)
	palette1 = get_palette(data1)
	palette2 = get_palette(data2)
	for color1, color2 in zip(palette1, palette2):
		replace_color(data1, color1[0][:3], color2[0][:3])
		replace_color(data2, color2[0][:3], color1[0][:3])
	image1 = Image.fromarray(data1)
	image2 = Image.fromarray(data2)
	return image1, image2

if __name__ == '__main__':
	image1, image2 = swap_palettes('sprites/6.png', 'sprites/151.png')
	image1.show()
	image2.show()

# todo:
# - smarter recoloring than just sorted by frequency? maybe group colors into sub-palettes?
# - input via either args or prompt
# - quickplay (users enter two pokemon to see their swap)
# - advanced (users pick any number of palettes and any number of pokemon to see all the combinations)
# - output sprites in sheet; each row is a new sprite, columns are 1x, 2x, 4x
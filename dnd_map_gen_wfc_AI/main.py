import logging
from Logic.test import test
from Logic.difficulty import difficultyPixels
from Logic.PatternLogic import PatternLogic
from Logic.Pattern import Pattern
from Logic.directions import Directions

import matplotlib.pyplot as plt
import warnings
import matplotlib
import numpy as np
import random
import math
from Logic.Index import Index

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


map = test()
diff = difficultyPixels()
patternLogic = PatternLogic()
show_old_map = True
show_steps = False
default_color ='Spectral'
#base (4,4)
input_size = (8, 8 )
output_size = (25, 25) #base = 25
difficulty = 9
#only 9 = (8,8)

N_size = 2
warnings.filterwarnings("ignore", category=matplotlib.cbook.mplDeprecation)
directions = Directions(output_size)
 
def get_pixels_based_on_difficulty(dif):
    pixels = diff.get_pixels_based_on_dif(dif)
    logging.info(f'getting pixels based on difficulty: {dif}')  
    logging.info(f'pixels: {pixels}')
    return pixels

def get_all_valid_options_for_tiles(dif):
    pixels = get_pixels_based_on_difficulty(dif)
    logging.info(f'getting paterns based on pixels')  

    patterns, weights, probability = patternLogic.calculate_patterns_weights_propability(N_size,input_size,pixels)
    logging.info(f'patterns: {len(patterns)}')
    return patterns, weights, probability


def show_plots(dif):
    pixels = get_pixels_based_on_difficulty(dif)
    patterns, weights, probability = get_all_valid_options_for_tiles(difficulty)
    plt.imshow(pixels, cmap= default_color, vmin=0, vmax=255) 
    # valid colors 'Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'hot', 'hot_r', 'hsv', 'hsv_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma', 'magma_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'turbo', 'turbo_r', 'twilight', 'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r', 'winter', 'winter_r'
    plt.show()
    plt.figure(figsize=(25,25))
    for m in range(len(patterns)):
        axs = plt.subplot(4, math.ceil(len(patterns)/4), m+1)
        axs.imshow(patterns[m].pixels, cmap= default_color, vmin=0, vmax=255)
        axs.set_xticks([])
        axs.set_yticks([])
        plt.title("weight: %.0f prob: %.2f"%(weights[patterns[m]], probability[patterns[m]]))
    plt.show()



def main():

    logging.info("start get_all_valid_options_for_tiles")
    patterns, weights, probability = get_all_valid_options_for_tiles(difficulty)
    logging.info("creating index")
    index = Index(patterns, output_size)

    
    def get_offset_tiles(pattern: Pattern, offset: tuple):


        if offset == (0, 0):
            return pattern.pixels
        if offset == (-1, -1):
            return tuple([pattern.pixels[1][1]])
        if offset == (0, -1):
            return tuple(pattern.pixels[1][:])
        if offset == (1, -1):
            return tuple([pattern.pixels[1][0]])
        if offset == (-1, 0):
            return tuple([pattern.pixels[0][1], pattern.pixels[1][1]])
        if offset == (1, 0):
            return tuple([pattern.pixels[0][0], pattern.pixels[1][0]])
        if offset == (-1, 1):
            return tuple([pattern.pixels[0][1]])
        if offset == (0, 1):
            return tuple(pattern.pixels[0][:])
        if offset == (1, 1):
            return tuple([pattern.pixels[0][0]])
    dirs = directions.give_dirs()
    rules_num = 0
    for pattern in patterns:
        for d in dirs:
            for pattern_next in patterns:
                overlap = get_offset_tiles(pattern_next, d)
                og_dir = tuple([d[0]*-1, d[1]*-1])
                part_of_og_pattern = get_offset_tiles(pattern, og_dir)
                if (overlap) == (part_of_og_pattern):
                    index.add_rule(pattern, d, pattern_next)
                    rules_num+=1
    logging.info(f'rules: {rules_num}')

    def initialize_wave_function(size):    
        coefficients = []
        
        for col in range(size[0]):
            row = []
            for r in range(size[1]):
                row.append(patterns)
            coefficients.append(row)
        return coefficients

    coefficients = initialize_wave_function(output_size)

    def is_fully_collapsed():
        for col in coefficients:
            for entry in col:
                if(len(entry)>1):
                    return False
        return True

    def get_possible_patterns_at_position(position):
        x, y = position
        possible_patterns = coefficients[x][y]
        return possible_patterns

    def get_shannon_entropy(position):

        x, y = position
        entropy = 0
        
        # A cell with one valid pattern has 0 entropy
        if len(coefficients[x][y]) == 1:
            return 0
        
        for pattern in coefficients[x][y]:
            entropy += probability[pattern] * math.log(probability[pattern], 2)
        entropy *= -1
        
        entropy -= random.uniform(0, 0.1)
        return entropy

    def get_min_entropy_pos():
        minEntropy = None
        minEntropyPos = None
        
        for x, col in enumerate(coefficients):
            for y, row in enumerate(col):
                entropy = get_shannon_entropy((x, y))
                
                if entropy == 0:
                    continue
                
                if minEntropy is None or entropy < minEntropy:
                    minEntropy = entropy
                    minEntropyPos = (x, y)
        return minEntropyPos


    def observe():
        min_entropy_pos = get_min_entropy_pos()
        
        if min_entropy_pos == None:
            print("All tiles have 0 entropy")
            return
        
        possible_patterns = get_possible_patterns_at_position(min_entropy_pos)
        
        max_p = 0
        for pattern in possible_patterns:
            if max_p < probability[pattern]:
                max_p == probability[pattern]
        
        
        semi_random_pattern = random.choice([pat for pat in possible_patterns 
                                            if probability[pat]
                                            >=max_p])
        # TODO dont forget to check the probability of the pattern
        coefficients[min_entropy_pos[0]][min_entropy_pos[1]] = semi_random_pattern
        
        return min_entropy_pos


    def propagate(min_entropy_pos):
        stack = [min_entropy_pos]
        
        while len(stack) > 0:
            pos = stack.pop()
            
            possible_patterns = get_possible_patterns_at_position(pos)
            for d in directions.valid_dirs(pos):
                adjacent_pos = (pos[0] + d[0], pos[1] + d[1])
                possible_patterns_at_adjacent = get_possible_patterns_at_position(adjacent_pos)
                
                if not isinstance(possible_patterns_at_adjacent, list):
                    possible_patterns_at_adjacent = [possible_patterns_at_adjacent]
                for possible_pattern_at_adjacent in possible_patterns_at_adjacent:
                    if len(possible_patterns) > 1:
                        is_possible = any([index.check_possibility(pattern, possible_pattern_at_adjacent, d) for pattern in possible_patterns])
                    else:
                        is_possible = index.check_possibility(possible_patterns, possible_pattern_at_adjacent, d)                    

                    if not is_possible:
                        x, y = adjacent_pos
                        coefficients[x][y] = [patt for patt in coefficients[x][y] if patt.pixels != possible_pattern_at_adjacent.pixels]
                            
                        if adjacent_pos not in stack:
                            stack.append(adjacent_pos)

    logging.info("start main loop")


    import matplotlib.animation as animation

    


    count = 0

    # Create a placeholder image
    im = plt.imshow([[0]*len(coefficients[0])]*len(coefficients), cmap=default_color, vmin=0, vmax=255)
    plt.show(block=False)

    while not is_fully_collapsed():
        count += 1
        min_entropy_pos = observe()
        propagate(min_entropy_pos)                    

        final_pixels = []
        for coefficient in coefficients:
            row = []
            for item in coefficient:
                first_pixel = item.pixels[0][0] if not isinstance(item, list) else item[0].pixels[0][0]
                row.append(first_pixel)
            final_pixels.append(row)

        # Update the image data and redraw
        im.set_data(final_pixels)
        plt.draw()
        plt.pause(0.001)  # pause a bit so that the plot gets updated
        
    plt.imshow(final_pixels, cmap=default_color, vmin=0, vmax=255)
    plt.show()
    pixel_1 = [[216, 216, 216, 216, 216, 216, 216, 216, 216, 216, 216, 228, 216, 228, 216, 216, 216, 228, 216, 216, 216, 216, 216, 228, 216], [228, 228, 216, 228, 228, 216, 228, 228, 216, 228, 216, 228, 216, 228, 216, 228, 216, 228, 216, 228, 228, 228, 216, 228, 216], [216, 216, 216, 216, 216, 216, 216, 216, 216, 216, 216, 216, 216, 216, 216, 228, 216, 216, 216, 228, 252, 228, 216, 216, 216], [228, 228, 216, 228, 216, 228, 228, 216, 228, 216, 228, 216, 228, 228, 216, 228, 216, 228, 216, 228, 228, 228, 216, 228, 216], [216, 216, 216, 216, 216, 216, 216, 216, 216, 216, 228, 216, 216, 216, 216, 216, 216, 216, 216, 216, 216, 216, 216, 216, 216], [228, 228, 216, 228, 216, 228, 228, 216, 228, 216, 216, 216, 228, 216, 228, 216, 228, 228, 216, 228, 228, 216, 228, 228, 216], [216, 216, 216, 216, 216, 216, 216, 216, 216, 216, 228, 216, 216, 216, 216, 216, 216, 216, 216, 216, 216, 216, 216, 216, 216], [228, 228, 228, 216, 228, 216, 228, 216, 228, 216, 216, 216, 228, 216, 228, 216, 228, 228, 228, 216, 228, 228, 228, 216, 228], [216, 216, 216, 216, 228, 216, 216, 216, 228, 216, 228, 216, 228, 216, 216, 216, 228, 252, 228, 216, 228, 252, 228, 216, 228], [228, 228, 228, 216, 216, 216, 228, 216, 216, 216, 216, 216, 216, 216, 228, 216, 228, 228, 228, 216, 228, 228, 228, 216, 228], [216, 216, 216, 216, 228, 216, 228, 216, 228, 216, 228, 216, 228, 216, 216, 216, 216, 216, 216, 216, 216, 216, 216, 216, 228], [228, 228, 228, 216, 216, 216, 216, 216, 216, 216, 228, 216, 216, 216, 228, 228, 216, 228, 216, 228, 228, 228, 228, 216, 228], [216, 216, 216, 216, 228, 228, 228, 228, 228, 216, 216, 216, 228, 216, 216, 216, 216, 216, 216, 216, 216, 216, 216, 216, 216], [228, 228, 228, 216, 216, 216, 216, 216, 216, 216, 228, 216, 228, 216, 228, 216, 228, 216, 228, 216, 228, 228, 228, 216, 228], [216, 216, 216, 216, 228, 228, 228, 216, 228, 216, 216, 216, 216, 216, 228, 216, 216, 216, 228, 216, 228, 252, 228, 216, 228], [228, 216, 228, 216, 216, 216, 216, 216, 216, 216, 228, 228, 228, 216, 228, 216, 228, 216, 216, 216, 228, 228, 228, 216, 216], [228, 216, 228, 216, 228, 216, 228, 228, 228, 216, 228, 252, 228, 216, 216, 216, 216, 216, 228, 216, 228, 252, 228, 216, 228], [228, 216, 216, 216, 216, 216, 216, 216, 216, 216, 228, 228, 228, 216, 228, 216, 228, 216, 228, 216, 228, 228, 228, 216, 216], [216, 216, 228, 216, 228, 216, 228, 216, 228, 216, 228, 252, 228, 216, 216, 216, 228, 216, 228, 216, 216, 216, 216, 216, 228], [228, 216, 216, 216, 228, 216, 216, 216, 228, 216, 228, 228, 228, 216, 228, 216, 216, 216, 216, 216, 228, 228, 228, 216, 216], [228, 216, 228, 216, 228, 216, 228, 216, 228, 216, 216, 216, 216, 216, 228, 216, 228, 216, 228, 216, 216, 216, 216, 216, 228], [228, 216, 228, 216, 216, 216, 216, 216, 216, 216, 228, 228, 228, 216, 228, 216, 228, 216, 216, 216, 228, 216, 228, 216, 228], [228, 216, 216, 216, 228, 216, 228, 228, 228, 216, 228, 252, 228, 216, 216, 216, 216, 216, 228, 216, 228, 216, 228, 216, 216], [216, 216, 228, 216, 216, 216, 216, 216, 216, 216, 228, 228, 228, 216, 228, 228, 228, 216, 228, 216, 216, 216, 216, 216, 228], [228, 216, 216, 216, 228, 216, 228, 228, 228, 216, 228, 252, 228, 216, 228, 252, 228, 216, 228, 216, 228, 228, 228, 216, 228]]
    pixel_2 = [[180, 192, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 192, 180, 192, 192, 180, 192, 180, 192, 192, 180], [180, 192, 180, 192, 192, 192, 192, 192, 192, 192, 180, 192, 192, 192, 180, 192, 180, 180, 180, 180, 180, 180, 180, 180, 180], [180, 192, 180, 192, 204, 192, 204, 192, 204, 192, 180, 192, 204, 192, 180, 180, 180, 192, 192, 192, 180, 192, 192, 192, 180], [180, 192, 180, 192, 192, 192, 192, 192, 192, 192, 180, 192, 192, 192, 180, 192, 180, 192, 204, 192, 180, 180, 180, 180, 180], [180, 192, 180, 192, 204, 192, 204, 192, 204, 192, 180, 192, 204, 192, 180, 192, 180, 192, 192, 192, 180, 192, 192, 180, 192], [180, 192, 180, 192, 192, 192, 192, 192, 192, 192, 180, 192, 192, 192, 180, 192, 180, 192, 204, 192, 180, 180, 180, 180, 180], [180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 192, 192, 192, 180, 192, 192, 192, 180], [180, 192, 180, 192, 180, 192, 180, 192, 180, 192, 192, 192, 180, 192, 180, 192, 180, 192, 204, 192, 180, 180, 180, 180, 180], [180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 192, 180, 180, 180, 192, 192, 192, 180, 192, 180, 192, 180], [192, 192, 192, 192, 180, 192, 180, 192, 180, 192, 180, 192, 180, 180, 180, 192, 180, 180, 180, 180, 180, 192, 180, 192, 180], [180, 180, 180, 180, 180, 180, 180, 192, 180, 180, 180, 180, 180, 192, 180, 192, 180, 192, 180, 192, 180, 180, 180, 180, 180], [180, 192, 180, 192, 180, 192, 180, 180, 180, 192, 180, 192, 180, 180, 180, 192, 180, 192, 180, 180, 180, 192, 192, 192, 180], [180, 192, 180, 180, 180, 180, 180, 192, 180, 192, 180, 180, 180, 192, 180, 192, 180, 180, 180, 192, 180, 192, 204, 192, 180], [180, 192, 180, 192, 192, 192, 180, 180, 180, 180, 180, 192, 180, 180, 180, 192, 180, 192, 180, 192, 180, 192, 192, 192, 180], [180, 180, 180, 180, 180, 180, 180, 192, 192, 192, 180, 192, 180, 192, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180], [180, 192, 192, 192, 180, 192, 180, 180, 180, 180, 180, 180, 180, 192, 180, 192, 192, 192, 192, 192, 192, 180, 192, 192, 180], [180, 192, 204, 192, 180, 180, 180, 192, 180, 192, 180, 192, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180], [180, 192, 192, 192, 180, 192, 180, 192, 180, 192, 180, 192, 180, 192, 180, 192, 192, 180, 192, 180, 192, 192, 192, 192, 192], [180, 192, 204, 192, 180, 192, 180, 180, 180, 180, 180, 192, 180, 180, 180, 180, 180, 180, 180, 180, 192, 204, 192, 204, 192], [180, 192, 192, 192, 180, 192, 180, 192, 192, 192, 180, 192, 180, 192, 192, 180, 192, 192, 192, 180, 192, 192, 192, 192, 192], [180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 192, 180, 180, 180, 180, 192, 204, 192, 180, 180, 180, 180, 180, 180], [180, 192, 192, 192, 180, 192, 192, 180, 192, 192, 180, 192, 180, 192, 192, 180, 192, 192, 192, 180, 192, 180, 192, 180, 192], [180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 192, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 192, 180, 180], [192, 192, 180, 192, 192, 192, 180, 192, 180, 192, 180, 180, 180, 192, 180, 192, 192, 192, 180, 192, 192, 180, 192, 180, 192], [180, 180, 180, 180, 180, 180, 180, 192, 180, 180, 180, 192, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 192, 180, 192]]
    pixel_3 = [[108, 120, 120, 132, 120, 120, 120, 132, 132, 132, 132, 132, 120, 108, 108, 108, 132, 120, 108, 108, 108, 108, 108, 120, 132], [132, 132, 120, 132, 120, 132, 120, 120, 108, 120, 108, 120, 120, 108, 120, 120, 132, 108, 108, 120, 120, 120, 108, 120, 120], [108, 120, 120, 132, 120, 132, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 132, 120, 108, 120, 132, 132, 132, 132, 120], [108, 108, 108, 132, 108, 132, 120, 120, 120, 108, 120, 120, 120, 108, 120, 120, 132, 108, 108, 120, 120, 108, 120, 120, 120], [120, 120, 120, 132, 120, 132, 108, 108, 108, 108, 120, 132, 132, 132, 132, 120, 132, 120, 108, 120, 132, 132, 132, 132, 132], [120, 132, 120, 132, 108, 132, 120, 120, 120, 108, 120, 120, 120, 120, 120, 120, 132, 108, 108, 120, 120, 108, 120, 120, 120], [108, 132, 108, 132, 120, 132, 120, 132, 132, 132, 132, 132, 132, 132, 132, 120, 132, 120, 108, 120, 132, 132, 132, 132, 132], [120, 132, 120, 132, 120, 132, 120, 120, 108, 120, 108, 120, 108, 120, 120, 120, 132, 108, 108, 120, 120, 108, 120, 108, 120], [120, 132, 120, 132, 108, 132, 108, 108, 108, 108, 108, 108, 108, 120, 132, 120, 132, 120, 108, 108, 108, 108, 108, 108, 108], [108, 132, 120, 132, 120, 132, 120, 108, 120, 120, 108, 120, 108, 120, 120, 120, 120, 120, 108, 120, 108, 120, 108, 120, 120], [120, 132, 108, 132, 108, 132, 120, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108], [120, 132, 120, 132, 120, 132, 120, 108, 120, 108, 120, 120, 108, 120, 108, 120, 120, 108, 120, 108, 120, 120, 108, 120, 108], [120, 132, 108, 132, 108, 132, 120, 108, 108, 108, 120, 132, 132, 132, 132, 132, 132, 132, 132, 132, 132, 132, 132, 132, 132], [108, 132, 120, 132, 120, 132, 120, 108, 120, 108, 120, 120, 108, 120, 120, 108, 120, 120, 120, 120, 108, 120, 108, 120, 108], [120, 132, 108, 132, 120, 132, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108], [120, 132, 120, 132, 120, 132, 120, 120, 108, 120, 108, 120, 108, 120, 108, 120, 120, 108, 120, 120, 120, 108, 120, 108, 120], [120, 120, 120, 120, 120, 132, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 120, 132, 120, 108, 108, 108, 108], [132, 132, 132, 132, 120, 132, 120, 120, 108, 120, 120, 108, 120, 120, 108, 120, 120, 108, 120, 132, 120, 108, 120, 108, 120], [108, 120, 108, 120, 120, 120, 120, 132, 132, 132, 132, 132, 132, 120, 108, 108, 108, 108, 120, 132, 120, 108, 120, 108, 108], [132, 132, 132, 132, 132, 132, 120, 120, 120, 120, 120, 108, 120, 120, 108, 120, 120, 108, 108, 132, 120, 108, 108, 108, 120], [108, 120, 108, 120, 108, 120, 120, 132, 120, 132, 132, 132, 132, 120, 108, 108, 108, 108, 120, 132, 120, 108, 120, 108, 108], [108, 108, 108, 108, 108, 108, 108, 132, 120, 120, 120, 120, 120, 120, 108, 120, 120, 108, 108, 132, 120, 108, 120, 108, 120], [120, 120, 108, 120, 120, 108, 120, 132, 120, 132, 132, 132, 132, 132, 132, 132, 120, 108, 120, 132, 120, 108, 120, 108, 108], [132, 120, 108, 108, 108, 108, 120, 120, 120, 120, 108, 120, 120, 120, 108, 120, 120, 108, 108, 132, 108, 108, 108, 108, 120], [120, 120, 108, 120, 120, 108, 120, 132, 132, 132, 132, 132, 132, 120, 108, 108, 108, 108, 120, 132, 120, 120, 120, 108, 108]]
    pixel_4 = [[156, 156, 156, 48, 156, 48, 156, 48, 156, 156, 156, 156, 156, 156, 156, 156, 156, 48, 156, 156, 156, 156, 156, 48, 156], [156, 168, 156, 168, 156, 168, 156, 168, 156, 168, 48, 168, 156, 168, 48, 168, 156, 168, 156, 168, 48, 168, 156, 168, 156], [156, 48, 156, 156, 156, 156, 156, 48, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156], [156, 168, 156, 168, 48, 168, 156, 168, 156, 168, 156, 168, 156, 168, 48, 168, 48, 168, 48, 168, 48, 168, 48, 168, 156], [156, 48, 156, 156, 156, 156, 156, 48, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156], [156, 168, 156, 168, 156, 168, 156, 168, 156, 168, 48, 168, 48, 168, 48, 168, 156, 168, 48, 168, 156, 168, 156, 168, 156], [156, 48, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 48, 156, 48, 156], [156, 168, 156, 168, 48, 168, 156, 168, 48, 168, 48, 168, 48, 168, 48, 168, 48, 168, 156, 168, 156, 168, 156, 168, 156], [156, 48, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 48, 156, 156, 156, 48, 156], [156, 168, 156, 168, 156, 168, 156, 168, 156, 168, 48, 168, 156, 168, 156, 168, 156, 168, 156, 168, 156, 168, 156, 168, 156], [156, 156, 156, 48, 156, 48, 156, 156, 156, 156, 156, 156, 156, 156, 156, 48, 156, 156, 156, 156, 156, 156, 156, 48, 156], [156, 168, 156, 168, 156, 168, 156, 168, 156, 168, 48, 168, 48, 168, 156, 168, 156, 168, 156, 168, 156, 168, 156, 168, 156], [156, 48, 156, 48, 156, 48, 156, 48, 156, 156, 156, 156, 156, 156, 156, 48, 156, 48, 156, 48, 156, 156, 156, 48, 156], [156, 168, 156, 168, 156, 168, 156, 168, 156, 168, 48, 168, 156, 168, 156, 168, 156, 168, 156, 168, 156, 168, 156, 168, 156], [156, 48, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 48, 156, 48, 156, 156, 156, 48, 156, 48, 156, 48, 156], [156, 168, 156, 168, 48, 168, 48, 168, 48, 168, 156, 168, 156, 168, 156, 168, 156, 168, 156, 168, 156, 168, 156, 168, 156], [156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 48, 156, 156, 156, 48, 156, 156, 156, 156, 156, 156, 156, 156, 156], [156, 168, 156, 168, 48, 168, 48, 168, 48, 168, 156, 168, 156, 168, 156, 168, 156, 168, 156, 168, 156, 168, 156, 168, 156], [156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 48, 156, 48, 156], [48, 168, 48, 168, 48, 168, 48, 168, 48, 168, 156, 168, 48, 168, 156, 168, 156, 168, 156, 168, 156, 168, 156, 168, 156], [156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 48, 156, 48, 156, 48, 156], [156, 168, 156, 168, 48, 168, 156, 168, 156, 168, 156, 168, 48, 168, 156, 168, 48, 168, 156, 168, 156, 168, 156, 168, 156], [156, 48, 156, 156, 156, 156, 156, 48, 156, 48, 156, 156, 156, 156, 156, 156, 156, 156, 156, 48, 156, 156, 156, 48, 156], [156, 168, 156, 168, 156, 168, 156, 168, 156, 168, 156, 168, 48, 168, 48, 168, 156, 168, 156, 168, 156, 168, 156, 168, 156], [156, 156, 156, 48, 156, 48, 156, 48, 156, 48, 156, 156, 156, 156, 156, 156, 156, 48, 156, 156, 156, 48, 156, 156, 156]]
    pixel_5 = [[84, 84, 144, 84, 84, 84, 84, 84, 84, 84, 72, 84, 96, 84, 72, 84, 144, 84, 96, 84, 72, 84, 96, 84, 96], [96, 84, 72, 84, 96, 84, 96, 84, 72, 84, 72, 84, 84, 84, 84, 84, 144, 84, 84, 84, 144, 84, 84, 84, 84], [84, 84, 84, 84, 84, 84, 84, 84, 144, 84, 144, 84, 96, 84, 72, 84, 144, 84, 96, 84, 144, 84, 96, 84, 96], [84, 72, 84, 72, 72, 84, 72, 84, 72, 84, 72, 84, 84, 84, 84, 84, 72, 84, 84, 84, 72, 84, 84, 84, 84], [84, 84, 84, 84, 84, 84, 144, 84, 72, 84, 72, 84, 72, 84, 96, 84, 144, 84, 96, 84, 72, 84, 96, 84, 72], [84, 96, 84, 72, 72, 84, 144, 84, 144, 84, 84, 84, 84, 84, 84, 84, 72, 84, 84, 84, 84, 84, 84, 84, 84], [84, 84, 84, 84, 84, 84, 72, 84, 144, 84, 96, 84, 96, 84, 72, 84, 72, 84, 96, 84, 72, 72, 72, 144, 144], [72, 84, 72, 84, 96, 84, 72, 84, 72, 84, 84, 84, 84, 84, 72, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84], [72, 84, 144, 84, 84, 84, 84, 84, 144, 84, 96, 84, 96, 84, 72, 84, 72, 72, 72, 84, 72, 144, 72, 144, 72], [72, 84, 72, 84, 96, 84, 96, 84, 72, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84], [144, 84, 84, 84, 84, 84, 84, 84, 72, 84, 72, 72, 72, 72, 144, 144, 72, 72, 144, 72, 72, 144, 72, 144, 144], [72, 84, 96, 84, 96, 84, 96, 84, 144, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84], [84, 84, 84, 84, 84, 84, 84, 84, 72, 84, 96, 84, 96, 84, 72, 72, 84, 72, 84, 72, 84, 72, 84, 72, 84], [144, 72, 144, 72, 72, 84, 72, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 144, 84, 144, 84, 144, 84, 144, 84], [84, 84, 84, 84, 84, 84, 72, 84, 72, 84, 96, 84, 96, 84, 72, 72, 84, 72, 84, 144, 84, 72, 84, 144, 84], [96, 84, 96, 84, 96, 84, 72, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 144, 84, 72, 84, 144, 84, 144, 84], [84, 84, 84, 84, 84, 84, 144, 84, 96, 84, 96, 84, 72, 144, 72, 72, 84, 72, 84, 144, 84, 144, 84, 144, 84], [96, 84, 96, 84, 96, 84, 72, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 72, 84, 144, 84, 72, 84], [84, 84, 84, 84, 84, 84, 144, 84, 96, 84, 96, 84, 96, 84, 96, 84, 72, 72, 84, 72, 84, 144, 84, 144, 84], [72, 72, 144, 144, 72, 84, 72, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 72, 84, 144, 84, 72, 84], [84, 84, 84, 84, 84, 84, 72, 84, 72, 72, 84, 96, 84, 72, 84, 96, 84, 96, 84, 84, 84, 72, 84, 84, 84], [96, 84, 72, 84, 72, 84, 72, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 72, 84, 144, 84, 72, 84], [84, 84, 72, 84, 72, 84, 144, 84, 72, 84, 72, 84, 72, 84, 96, 84, 72, 72, 84, 72, 84, 72, 84, 72, 84], [72, 84, 72, 84, 84, 84, 144, 84, 144, 84, 72, 84, 72, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84], [72, 84, 144, 84, 72, 84, 144, 84, 72, 84, 72, 84, 72, 84, 72, 144, 72, 72, 144, 72, 72, 72, 72, 72, 84]]
    pixel_6 = [[36, 48, 36, 36, 36, 48, 36, 48, 36, 36, 36, 48, 36, 48, 36, 36, 48, 36, 36, 48, 60, 48, 36, 36, 48], [48, 48, 48, 48, 48, 48, 36, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48], [48, 36, 36, 48, 60, 48, 36, 48, 60, 48, 36, 48, 36, 36, 48, 36, 36, 36, 36, 36, 36, 36, 48, 60, 48], [48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48], [48, 60, 48, 36, 36, 36, 48, 60, 48, 36, 48, 36, 48, 36, 48, 60, 48, 60, 48, 60, 48, 36, 48, 60, 48], [48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48], [48, 36, 48, 36, 36, 48, 60, 48, 60, 48, 36, 36, 36, 36, 48, 36, 48, 60, 48, 60, 48, 60, 48, 60, 48], [48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48], [48, 60, 48, 36, 48, 36, 48, 60, 48, 36, 36, 48, 60, 48, 36, 36, 48, 60, 48, 60, 48, 36, 48, 60, 48], [48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48], [36, 48, 36, 48, 60, 48, 60, 48, 60, 48, 60, 48, 36, 48, 36, 36, 36, 36, 48, 36, 48, 60, 48, 60, 48], [48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48], [60, 48, 36, 36, 36, 36, 36, 36, 48, 60, 48, 60, 48, 36, 48, 36, 48, 60, 48, 60, 48, 60, 48, 60, 48], [48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 36, 48, 36, 48, 48, 48, 48, 48, 48, 48, 48, 48], [48, 60, 48, 60, 48, 36, 48, 60, 48, 60, 48, 60, 48, 36, 48, 48, 48, 36, 48, 60, 48, 36, 48, 60, 48], [48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 36, 48, 60, 48, 48, 48, 48, 48, 36, 48, 48, 48], [36, 36, 48, 60, 48, 36, 48, 60, 48, 60, 48, 60, 48, 48, 48, 48, 48, 60, 48, 60, 48, 36, 48, 36, 48], [48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 36, 36, 36, 48, 48, 48, 48, 48, 48, 48, 36, 48], [36, 48, 60, 48, 36, 48, 36, 48, 60, 48, 36, 36, 48, 48, 48, 48, 48, 36, 48, 36, 48, 60, 48, 48, 48], [48, 48, 48, 48, 36, 48, 48, 48, 48, 48, 48, 48, 48, 60, 48, 36, 48, 48, 48, 36, 48, 48, 48, 60, 48], [60, 48, 36, 48, 36, 48, 60, 48, 36, 36, 48, 60, 48, 48, 48, 36, 48, 60, 48, 36, 48, 36, 48, 48, 48], [48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 36, 48, 36, 48, 48, 48, 48, 48, 48, 48, 36, 48], [48, 36, 48, 36, 48, 36, 48, 60, 48, 36, 36, 36, 48, 36, 48, 36, 48, 60, 48, 60, 48, 60, 48, 48, 48], [48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 60, 48], [48, 36, 48, 60, 48, 36, 36, 36, 48, 60, 48, 60, 48, 36, 48, 60, 48, 60, 48, 60, 48, 36, 48, 48, 48]]
    pixel_7 = [[24, 12, 24, 12, 0, 0, 0, 0, 24, 0, 0, 12, 0, 12, 0, 12, 0, 12, 24, 24, 24, 24, 12, 0, 0], [24, 12, 24, 0, 0, 12, 0, 12, 24, 12, 0, 0, 0, 0, 0, 12, 0, 12, 12, 0, 12, 12, 12, 0, 12], [24, 0, 24, 12, 0, 0, 0, 12, 12, 12, 0, 12, 0, 12, 0, 12, 0, 0, 0, 0, 0, 0, 0, 0, 12], [24, 12, 24, 12, 0, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12, 0, 12, 12, 0, 12, 0, 0], [12, 12, 12, 12, 0, 12, 0, 12, 0, 12, 0, 12, 0, 12, 12, 12, 0, 0, 0, 0, 0, 0, 0, 0, 12], [24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 12, 0, 12, 0, 12, 0, 12, 12, 0, 0], [12, 12, 12, 12, 12, 12, 0, 12, 12, 0, 12, 0, 12, 0, 12, 12, 0, 0, 0, 0, 0, 0, 0, 0, 12], [12, 24, 12, 24, 24, 24, 24, 24, 12, 0, 12, 0, 0, 0, 0, 0, 0, 12, 0, 12, 12, 0, 12, 0, 12], [12, 24, 12, 12, 12, 12, 0, 12, 12, 0, 0, 0, 12, 12, 12, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 24, 0, 0, 0, 0, 0, 0, 0, 0, 12, 0, 12, 24, 24, 12, 0, 12, 0, 12, 12, 12, 12, 12, 0], [12, 24, 12, 0, 12, 0, 12, 12, 12, 0, 0, 0, 12, 12, 12, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0], [12, 24, 12, 0, 12, 0, 0, 0, 0, 0, 12, 0, 12, 24, 24, 12, 0, 12, 12, 12, 0, 12, 12, 0, 12], [12, 12, 12, 0, 12, 0, 12, 0, 12, 0, 0, 0, 12, 12, 12, 12, 0, 0, 0, 0, 0, 12, 24, 24, 24], [0, 0, 0, 0, 0, 0, 12, 0, 0, 0, 12, 0, 0, 0, 0, 0, 0, 12, 12, 12, 0, 12, 12, 12, 12], [0, 12, 0, 12, 12, 0, 0, 0, 12, 0, 12, 0, 12, 0, 12, 12, 0, 12, 24, 24, 24, 24, 24, 12, 24], [0, 0, 0, 0, 0, 0, 12, 0, 0, 0, 0, 0, 12, 0, 0, 0, 0, 12, 12, 0, 12, 0, 12, 12, 24], [12, 12, 12, 0, 12, 0, 12, 0, 12, 0, 12, 0, 12, 0, 12, 12, 0, 0, 0, 0, 0, 0, 0, 0, 24], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12, 12, 12, 0, 12, 0, 12, 24], [12, 0, 12, 12, 0, 12, 12, 12, 0, 12, 12, 12, 0, 12, 0, 12, 0, 0, 0, 0, 0, 12, 0, 12, 12], [0, 0, 0, 0, 0, 12, 24, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12, 0, 12, 0, 0, 0, 0, 0], [12, 0, 12, 12, 0, 0, 24, 12, 0, 12, 12, 0, 12, 12, 0, 12, 0, 12, 0, 12, 0, 12, 0, 12, 0], [24, 24, 24, 12, 0, 12, 24, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [12, 12, 12, 12, 0, 12, 24, 12, 0, 12, 12, 12, 0, 12, 12, 12, 0, 12, 0, 12, 12, 12, 12, 0, 12], [24, 12, 24, 12, 0, 12, 12, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12], [12, 12, 24, 0, 0, 12, 24, 12, 0, 12, 12, 12, 12, 12, 0, 12, 0, 12, 12, 0, 12, 0, 12, 0, 12]]

    

    print(final_pixels)
    old_pixels = pixel_1 + pixel_2 + pixel_3 + pixel_4 + pixel_5 + pixel_6 + pixel_7
    combined_pixels=   old_pixels+ final_pixels

    if show_old_map == True:
        plt.imshow(combined_pixels, cmap=default_color, vmin=0, vmax=255)
        plt.show()

    logging.info("end main loop")





    # count= 0
    # while not is_fully_collapsed():
    #     count+=1
    #     min_entropy_pos = observe()
    #     logging.info(f'min entropy total {count}')
    #     propagate(min_entropy_pos)                    
    # logging.info("end main loop")

    # final_pixels = []
    
    # for coefficient in coefficients:
    #     row = []
    #     for item in coefficient:
    #         first_pixel = item.pixels[0][0] if not isinstance(item, list) else item[0].pixels[0][0]
    #         row.append(first_pixel)


    #     logging.info(f'row: {row}')
        
    #     final_pixels.append(row)

    # plt.imshow(final_pixels, cmap=default_color, vmin=0, vmax=255)
    # plt.show()


    
def start_main():
    if show_steps == True:
        show_plots(difficulty)
    else:
        main()

start_main()
import matplotlib.pyplot as plt
import numpy as np
import math

def generate_gradient_arr(w, h, c_start, c_end, direction='ltr', angle=45):
    c_start, c_end = np.array(c_start) / 255.0, np.array(c_end) / 255.0
    img = np.zeros(shape=(w,h,3), dtype=np.float64)
    if direction == 'ltr':
        for i in range(h):
            t = i/(h-1)
            img[:,i] = np.array([(1-t)*c_start[j] + t*c_end[j] for j in range(3)], dtype=np.float64)
    elif direction == 'rtl':
        for i in range(h):
            t = i/(h-1)
            img[:,i] = np.array([(1-t)*c_end[j] + t*c_start[j] for j in range(3)], dtype=np.float64)
    elif direction == 'ttb':
        for i in range(w):
            t = i/(w-1)
            img[i,:] = np.array([(1-t)*c_start[j] + t*c_end[j] for j in range(3)], dtype=np.float64)
    elif direction == 'btt':
        for i in range(w):
            t = i/(w-1)
            img[i,:] = np.array([(1-t)*c_end[j] + t*c_start[j] for j in range(3)], dtype=np.float64)
    elif direction == 'diag':
        u = (math.cos(math.radians(angle)), math.sin(math.radians(angle)))
        corners = [(0,0),(w-1,0),(0,h-1),(w-1,h-1)]
        distances = [c[0]*u[0] + c[1]*u[1] for c in corners]
        d_max, d_min = max(distances), min(distances)
        if d_max == d_min: d_max += 1
        for i in range(w):
            for k in range(h):
                d = i*u[0] + k*u[1]
                # t = (i+(h-k))/(w+h)
                t = (d - d_min) / (d_max - d_min)
                img[i,k,:] = np.array([(1-t)*c_end[j] + t*c_start[j] for j in range(3)], dtype=np.float64)
    return img

def shuffle_gradient(img, anchors):
    w, h, c = img.shape
    shuffled_img = img.copy()
    
    # 1. Identify which positions are "Loose" (not anchors)
    all_coords = [(i, k) for i in range(w) for k in range(h)]
    # Convert anchors to a set for faster lookup
    anchor_set = set(anchors)
    loose_coords = [c for c in all_coords if c not in anchor_set]
    
    # 2. Extract the colors of the loose pixels
    loose_colors = [img[r, c].copy() for r, c in loose_coords]
    
    # 3. Shuffle those colors
    np.random.shuffle(loose_colors)
    
    # 4. Put the shuffled colors back into the loose positions
    for i, coord in enumerate(loose_coords):
        shuffled_img[coord[0], coord[1]] = loose_colors[i]
        
    return shuffled_img
    
def compare_images(img1, img2, title1="Original", title2="Shuffled"):
    # Create a figure with 1 row and 2 columns
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    
    # Display first image
    axes[0].imshow(img1)
    axes[0].set_title(title1)
    axes[0].axis('off') # Hide coordinate axes for a cleaner "game" look
    
    # Display second image
    axes[1].imshow(img2)
    axes[1].set_title(title2)
    axes[1].axis('off')
    
    plt.tight_layout()
    plt.show()

def identical(a1,a2):
    return np.array_equal(a1,a2)

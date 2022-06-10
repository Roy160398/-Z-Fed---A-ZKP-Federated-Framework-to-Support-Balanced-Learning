import matplotlib.pyplot as plt
from PIL import Image
# PROPERTIES #################################################################

properties = {
    # Ethnicity labels
    'ETHNICITIES' : { 
        0: 'White', 
        1: 'Black',
        2: 'Asian',
        3: 'Indian',
        4: 'Other'
    },
    
    # Gender labels
    'GENDERS' : { 
        0: 'Male', 
        1: 'Female'
    },
    
    'REVERSE_GENDERS' : {
        'Male' : 0,
        'Female' : 1
    },
    
    #Color channel
    'color_channel' : 255,
    
    #Image size
    'img_size' : 48,
    
    #Age range
    'age_min' : 0,
    'age_max' : 49,
    'age_range' : lambda: properties['age_max'] - properties['age_min'],
    'age_bins' : 10,
    'bins' : lambda: create_bins(properties['age_min'], 
                                 properties['age_bins'], 
                                 int(properties['age_range']() / properties['age_bins'])),
    
    #Train features
    #Use
    'feature_to_use' : 'pixels',
    #To predict
    'feature_to_predict' : 'age',

    #Number of data samples
    'data_samples' : 10000,

    #Randomness
    'seed' : 19101995,    
    
}


# GRAPHICS ###################################################################

def render_row(row):
    pixels = bytearray([int(px) for px in row['pixels'].split(' ')])
    img = Image.frombytes('L', (img_size, img_size), bytes(pixels))
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(2, 2), dpi=100)
    axes.axis('off')
    imgplot = plt.imshow(img, cmap='gray')
    x_offset_text = 52
    plt.text(x_offset_text, 5, 'Age: ' + str(row['age']))
    plt.text(x_offset_text, 12, 'Ethnicity: ' + ETHNICITIES[row['ethnicity']])
    plt.text(x_offset_text, 19, 'Gender: ' + GENDERS[row['gender']])
    plt.show()


# FUNCTIONS ##################################################################
    
def age_to_out(age, age_range):
    return age / age_range

def create_bins(lower_bound, width, quantity):
    bins = []
    for low in range(lower_bound, 
                     lower_bound + quantity * width + 1 , width):
        bins.append((low, low + width - 1))
    return bins

def one_hot(number, bins):
    oh = [0] * len(bins)
    for i in range(len(bins)):
        if bins[i][0] <= number <= bins[i][1]:
            oh[i] = 1
            return oh
    raise ValueError('invalid number passed to one-hot function, check bins for details')
    
def print_summary(dataset, name='dataset'):
    n_bins = len(properties['bins']())
    fig, axs = plt.subplots(1, 3, sharey=True, tight_layout=True, figsize=(12, 3))
    fig.suptitle(name + f', #records: {len(dataset)}')
    axs[0].title.set_text('Age')
    axs[0].hist(dataset['age'], bins=n_bins)
    axs[1].title.set_text('Ethnicity')
    axs[1].hist(dataset['ethnicity'], bins=5*2-1)
    axs[2].title.set_text('Gender')
    axs[2].hist(dataset['gender'], bins=2*2-1)
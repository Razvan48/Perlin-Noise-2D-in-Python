import numpy as np
import matplotlib.pyplot as plt



def hashCoordinates(x: int, y: int):
    MAX_COORDINATE_Y = 666017 # y va lua valori in intervalul [0, MAX_COORDINATE_Y - 1]
    return x * MAX_COORDINATE_Y + y


def calculateGradient(seed: int):
    np.random.seed(seed)

    possible_gradients = np.array(
        [
            #[1.0, 0.0],
            #[0.0, 1.0],
            #[-1.0, 0.0],
            #[0.0, -1.0],
            [1.0, 1.0],
            [-1.0, 1.0],
            [1.0, -1.0],
            [-1.0, -1.0]
        ]
    )

    gradient = possible_gradients[np.random.randint(0, len(possible_gradients))]
    #gradient = np.random.rand(2)

    # normalize (doar din cauza ca avem vectori nenormalizati pe diagonale, ca e mai usor de vizualizat asa)
    if np.linalg.norm(gradient) != 0.0:
        gradient /= np.linalg.norm(gradient)

    return gradient


def calculateInitialHeight(seed: int):
    DEFAULT_INITIAL_HEIGHT = 0.0
    HEIGHT_AMPLITUDE = 1.0
    np.random.seed(seed)
    return DEFAULT_INITIAL_HEIGHT + np.random.rand() * HEIGHT_AMPLITUDE


def fadeFunction(t: float):
    return 6 * (t * 5) - 15 * (t * 4) + 10 * (t ** 3)

def fadeFunctionXY(x: float, y: float):
    return fadeFunction(x) * fadeFunction(y)


def noisePerGrid(x: int, y: int, currentGridSize: int):
    x0 = (x // currentGridSize) * currentGridSize
    x1 = x0 + currentGridSize
    y0 = (y // currentGridSize) * currentGridSize
    y1 = y0 + currentGridSize

    seed00 = hashCoordinates(x0, y0)
    seed01 = hashCoordinates(x0, y1)
    seed10 = hashCoordinates(x1, y0)
    seed11 = hashCoordinates(x1, y1)

    gradient00 = calculateGradient(seed00)
    gradient01 = calculateGradient(seed01)
    gradient10 = calculateGradient(seed10)
    gradient11 = calculateGradient(seed11)

    dist00 = np.array([x - x0, y - y0])
    dist01 = np.array([x - x0, y - y1])
    dist10 = np.array([x - x1, y - y0])
    dist11 = np.array([x - x1, y - y1])

    dist00Norm = dist00 / currentGridSize
    dist01Norm = dist01 / currentGridSize
    dist10Norm = dist10 / currentGridSize
    dist11Norm = dist11 / currentGridSize

    dot00 = np.dot(gradient00, dist00Norm)
    dot01 = np.dot(gradient01, dist01Norm)
    dot10 = np.dot(gradient10, dist10Norm)
    dot11 = np.dot(gradient11, dist11Norm)

    dot00Added = dot00 + calculateInitialHeight(seed00)
    dot01Added = dot01 + calculateInitialHeight(seed01)
    dot10Added = dot10 + calculateInitialHeight(seed10)
    dot11Added = dot11 + calculateInitialHeight(seed11)

    fade00 = fadeFunctionXY(1 - dist00Norm[0], 1 - dist00Norm[1])
    fade01 = fadeFunctionXY(1 - dist01Norm[0], 1 + dist01Norm[1])
    fade10 = fadeFunctionXY(1 + dist10Norm[0], 1 - dist10Norm[1])
    fade11 = fadeFunctionXY(1 + dist11Norm[0], 1 + dist11Norm[1])

    output = dot00Added * fade00 + dot01Added * fade01 + dot10Added * fade10 + dot11Added * fade11
    return output


def perlinNoise2D(x: int, y: int):
    NUM_OCTAVES = 3

    GRID_MULTIPLIER = 2
    AMPLITUDE_DIMINISHMENT = 0.5

    INITIAL_GRID_SIZE = 17
    INITIAL_AMPLITUDE = 1.0
    STARTING_VALUE = 0.0

    currentGridSize = INITIAL_GRID_SIZE
    currentAmplitude = INITIAL_AMPLITUDE
    output = STARTING_VALUE

    for _ in range(NUM_OCTAVES):
        output += (currentAmplitude * noisePerGrid(x, y, currentGridSize))
        currentGridSize *= GRID_MULTIPLIER
        currentAmplitude *= AMPLITUDE_DIMINISHMENT

    return output





IMAGE_WIDTH = 150
IMAGE_HEIGHT = 150
image = np.empty((IMAGE_HEIGHT, IMAGE_WIDTH))

for i in range(IMAGE_HEIGHT):
    for j in range(IMAGE_WIDTH):
        image[i, j] = perlinNoise2D(j, i)


imageMaximum = np.max(image)
imageMinimum = np.min(image)
image = (image - imageMinimum) / (imageMaximum - imageMinimum)


plt.imshow(image, cmap='gray')
plt.axis('off')
plt.show()


WATER_THRESHOLD = 0.37
SAND_THRESHOLD = 0.41
SNOW_THRESHOLD = 0.81
displayedImage = np.empty((IMAGE_HEIGHT, IMAGE_WIDTH, 3))

for i in range(IMAGE_HEIGHT):
    for j in range(IMAGE_WIDTH):
        if image[i, j] < WATER_THRESHOLD:
            displayedImage[i, j] = [0, 0, 1]
        elif image[i, j] < SAND_THRESHOLD:
            displayedImage[i, j] = [1, 1, 0]
        elif image[i, j] < SNOW_THRESHOLD:
            displayedImage[i, j] = [0, 1, 0]
        else:
            displayedImage[i, j] = [1, 1, 1]


plt.imshow(displayedImage)
plt.axis('off')
plt.show()

print('Maximum: ', imageMaximum)
print('Minimum: ', imageMinimum)
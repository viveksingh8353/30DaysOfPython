import cv2

# 1. Read image
image = cv2.imread("myphoto.jpg")

# Check if image loaded
if image is None:
    print("Error: Image not found. Make sure 'myphoto.jpg' is in the same folder.")
    exit()

# 2. Convert to gray
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 3. Invert image
inverted = cv2.bitwise_not(gray_image)

# 4. Blur the inverted image
blurred = cv2.GaussianBlur(inverted, (21, 21), 0)

# 5. Invert the blurred image
inverted_blur = cv2.bitwise_not(blurred)

# 6. Create pencil sketch
sketch = cv2.divide(gray_image, inverted_blur, scale=256.0)

# 7. Save the sketch
cv2.imwrite("sketch_output.jpg", sketch)

print("✅ Pencil sketch saved as 'sketch_output.jpg'")

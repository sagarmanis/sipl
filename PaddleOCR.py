import paddleocr
from paddleocr import PaddleOCR

# Initialize the PaddleOCR instance
ocr = PaddleOCR(lang='en')

# Load and process the image
image_path = 'Images/ICard.jpg'
result = ocr.ocr(image_path,det=True)
print(result)
# Extract and print the recognized text
# line_text=''
# for line in result:
#     line_text = line_text+line[0][0]
#     print(line_text)
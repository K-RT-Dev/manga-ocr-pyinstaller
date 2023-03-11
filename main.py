import time
from manga_ocr import MangaOcr

# Basic example. We translate the same image 10 times and calculate the average time of the process.
# Depending on whether CPU or GPU (CUDA) is used, the processing speed will vary

mocr = MangaOcr()

lapses = 10

start = time.process_time()
for i in range(lapses):
    text = mocr('img/example.jpg')
    print(text)
print((time.process_time() - start)/lapses)

time.sleep(10)
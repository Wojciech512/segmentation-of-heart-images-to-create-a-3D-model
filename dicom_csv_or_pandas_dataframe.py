# -*- coding: utf-8 -*-
"""dicom_csv_or_pandas_dataframe.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tp5RxdtCBOVWwbPqAWXxUbRD47YnjEGX

#załadowanie pliku, utworzenie folderów, zestawienia, przetworzenie dicom na .jpg, sprawdzenie kolejności
"""

#usuwanie folderów
# !rm -rf dicom_to_jpg
# !rm -rf log_jpg
# !rm -rf otsu
# !rm -rf segmented_images
# !rm -rf stretch_and_cut
# !rm -rf stretched_jpg
# !rm -rf filled_images
#!rm -rf test

!pip install pydicom
!mkdir dicom_to_jpg

#tworzy połączneie colaba z dyskiem
from google.colab import drive

drive.mount('/content/drive')

import pydicom
import os
import numpy as np
import cv2

#folder zdjęc dicom
dicom_folder = '/content/drive/MyDrive/E774S5-shortAxis' 

#folder w którym zapisywany jest podgląd zdjęć w postaci .jpg
jpg_folder = '/content/dicom_to_jpg' 

#sortowanie losty nazw obrazów dicom
list_dicom_names = os.listdir(dicom_folder)
list_dicom_names.sort()
# stworzenie słownika z zestawieniem .dicom = .jpg
dcm_jpg_map = {}

for dicom_f in list_dicom_names:
    dicom_filepath = os.path.join(dicom_folder, dicom_f)
    jpg_f = dicom_f.replace('.dcm', '.jpg') 
    jpg_filepath = os.path.join(jpg_folder,jpg_f)
    dcm_jpg_map[dicom_filepath] = jpg_filepath

# na podstawie słownika zostają przetworzone obrazy na jpg. i macierze 256x256
pixel_array_list=[]

for dicom_filepath, jpg_filepath in dcm_jpg_map.items():
    dicom = pydicom.read_file(dicom_filepath)
    np_pixel_array=dicom.pixel_array

    #dodanie macierzy obrazu dicom do listy
    pixel_array_list.append(np_pixel_array)
    
    #przetworzenie obrazu dicom na jpg
    cv2.imwrite(jpg_filepath, np_pixel_array)

"""#Wyświetlanie zestawienia zdjęć"""

import os
import matplotlib.pyplot as plt

#metoda do wyświetlania zestawienia z zawartości folderu
def display_images(folder_path, num_images):
  
    # Pobierz listę plików w folderze
    file_list = os.listdir(folder_path)
    file_list.sort()

    # Wybierz tylko pliki z rozszerzeniem .jpg
    image_files = [file for file in file_list if file.endswith('.jpg')]

    # Utwórz listę zdjęć i nazw plików
    images = []
    image_names = []

    # Wczytaj każde zdjęcie i dodaj je do listy wraz z jego nazwą
    for i in range(num_images):
        image_path = os.path.join(folder_path, image_files[i])
        image = plt.imread(image_path)
        images.append(image)
        image_names.append(image_files[i])

    # Utwórz zestawienie zdjęć
    fig, axs = plt.subplots(20, 20, figsize=(80, 80))
    axs = axs.ravel()

    for i in range(num_images):
        axs[i].imshow(images[i], cmap='gray')
        axs[i].set_title(image_names[i], fontsize=12)
        axs[i].axis('off')

    plt.subplots_adjust(wspace=0, hspace=0.4)
    plt.show()

#użycie funkcji display_images (ścieżka, ilość zdjęć w folderze)
display_images('/content/dicom_to_jpg',400)

#podgląd macierzy
# with np.printoptions(threshold=np.inf):
#   print(pixel_array_list[0])

"""#Logarytmowanie (brak zastosowania)"""

#logarytmowanie dla wszystkich
!mkdir log_jpg

jpg_folder = '/content/dicom_to_jpg' #folder z jpg
jpg_to_log_folder = '/content/log_jpg' #folder ze zlogarytmowanymi jpg

jpg_folder_names = os.listdir(jpg_folder) #znowu robimy listę nazw do iteracji
jpg_folder_names.sort()

jpg_filepaths_list=[] #lista obrazów jpg
jpg_to_log_list = []

for name in jpg_folder_names: 
  jpg_filepath = os.path.join(jpg_folder,name)
  jpg_filepaths_list.append(jpg_filepath) #dołączanie do ścieżki

  jpg_to_log_zm = os.path.join(jpg_to_log_folder,name)
  
  img = cv2.imread(jpg_filepath,1) #wczytujemy po jednym jpg
  image_in_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #zmieniamy na skalę szarości

  # c - współczynnik skalujący
  c = 255 / np.log(1 + np.max(image_in_gray))

  log_output = c * np.log(1 + image_in_gray)

  # Przekonwertuj z powrotem na format 8-bitowy
  log_output = np.uint8(log_output)
  jpg_to_log_list.append(log_output)
#   cv2.imwrite(jpg_to_log_zm, log_output)

"""#Wyświetlenie histogramu"""

import cv2
import matplotlib.pyplot as plt

def display_histograms(img_before_path, img_after_path):
    # Wczytaj zdjęcie przed operacją rozciągnięcia histogramu i oblicz jego histogram
    img_before = plt.imread(img_before_path)
    hist_before = cv2.calcHist(img_before,[0],None,[256],[0,256])

    # Wczytaj zdjęcie po operacji rozciągnięcia histogramu i oblicz jego histogram
    img_after = plt.imread(img_after_path)
    hist_after = cv2.calcHist(img_after,[0],None,[256],[0,256])

    # Utwórz zestawienie histogramów
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    
    axs[0].imshow(img_before, cmap='gray')
    axs[0].set_title(f'Obraz 1: {img_before_path}', fontsize=12)
    axs[0].axis('off')
    
    axs[1].imshow(img_after, cmap='gray')
    axs[1].set_title(f'Obraz 2: {img_after_path}', fontsize=12)
    axs[1].axis('off')
    
    fig2, axs2 = plt.subplots(1, 2, figsize=(10, 5))
    
    axs2[0].plot(hist_before)
    axs2[0].set_title(f'Obraz 1: {img_before_path}', fontsize=12)
    
    axs2[1].plot(hist_after)
    axs2[1].set_title(f'Obraz 2: {img_after_path}', fontsize=12)
    
    plt.show()

"""#Wyrównanie histogramu
>aby uzyskać optymale zdjęcia należy manewrować tymi 3 zmiennymi
```
clahe = cv2.createCLAHE(clipLimit = **10**, tileGridSize=**(8, 8)**)
  final_img = clahe.apply(image_bw) + **10**
```


"""

!mkdir equalization_jpg

import cv2
import matplotlib.pyplot as plt
import numpy as np

#folder z jpg
jpg_folder = '/content/dicom_to_jpg' 
jpg_stretched_folder = '/content/equalization_jpg'

jpg_folder_names = os.listdir(jpg_folder)
jpg_folder_names.sort()

jpg_filepaths_list = []
jpg_stretched_list = []

for name in jpg_folder_names: 
  jpg_filepath = os.path.join(jpg_folder,name)
  
  #dołączanie do ścieżki
  jpg_filepaths_list.append(jpg_filepath)

  jpg_stretched_zm = os.path.join(jpg_stretched_folder,name)
  
  # Reading the image from the present directory
  image = cv2.imread(jpg_filepath,1)
  
  # The initial processing of the image
  #image = cv2.medianBlur(image, 3)
  image_bw = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  #Wyrównanie histogramu
  clahe = cv2.createCLAHE(clipLimit = 12  , tileGridSize=(8, 8))
  final_img = clahe.apply(image_bw)

  s_output = np.uint8(final_img)
  jpg_stretched_list.append(s_output)
  cv2.imwrite(jpg_stretched_zm, s_output)

display_images('/content/equalization_jpg',400)

img_before_path = '/content/equalization_jpg/I0280.jpg'
img_after_path ='/content/dicom_to_jpg/I0280.jpg'
display_histograms(img_before_path,img_after_path)

#filtr medianowy albo dyfuzija anizotropowa przed otsu
#wyrównać-> rozciągnąc (zły efekt)

"""#Rozciąganie histogramu"""

# rozciąganie histogramu
!mkdir stretched_jpg

import cv2
import matplotlib.pyplot as plt

#folder z jpg
jpg_folder = '/content/dicom_to_jpg' 
jpg_stretched_folder = '/content/stretched_jpg'

jpg_folder_names = os.listdir(jpg_folder)
jpg_folder_names.sort()

jpg_filepaths_list = []
jpg_stretched_list = []

for name in jpg_folder_names: 
  jpg_filepath = os.path.join(jpg_folder,name)
  
  #dołączanie do ścieżki
  jpg_filepaths_list.append(jpg_filepath)

  jpg_stretched_zm = os.path.join(jpg_stretched_folder,name)
  
  #wczytujemy po jednym jpg
  img = cv2.imread(jpg_filepath,1) 

  #zmieniamy na skalę szarości
  image_in_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) 

  constant = (255-0)/(image_in_gray.max()-image_in_gray.min())
  img_stretched = image_in_gray * constant

  s_output = np.uint8(img_stretched)
  jpg_stretched_list.append(s_output)
  cv2.imwrite(jpg_stretched_zm, s_output)

#użycie funkci display_histograms(scieżka do zdjęcia przed, scieżka do zdjęcia po rozciąganiu histogramu)
img_before_path = '/content/equalization_jpg/I0001.jpg'
img_after_path ='/content/stretched_jpg/I0001.jpg'

display_histograms(img_before_path, img_after_path)

"""#Dyfuzja anizotropowa"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import skimage.io as io
import skimage.filters as flt
# %matplotlib inline
# since we can't use imports
import numpy as np
import scipy.ndimage.filters as flt
import warnings

def anisodiff(img,niter=1,kappa=50,gamma=0.1,step=(1.,1.),sigma=0, option=1,ploton=False):

	# Anisotropic diffusion.

	# Usage:
	# imgout = anisodiff(im, niter, kappa, gamma, option)

	# Arguments:
	#         img    - input image
	#         niter  - number of iterations
	#         kappa  - conduction coefficient 20-100 ?
	#         gamma  - max value of .25 for stability
	#         step   - tuple, the distance between adjacent pixels in (y,x)
	#         option - 1 Perona Malik diffusion equation No 1
	#                  2 Perona Malik diffusion equation No 2
	#         ploton - if True, the image will be plotted on every iteration

	# Returns:
	#         imgout   - diffused image.

	# ...you could always diffuse each color channel independently if you
	# really want
	if img.ndim == 3:
		warnings.warn("Only grayscale images allowed, converting to 2D matrix")
		img = img.mean(2)

	# initialize output array
	img = img.astype('float32')
	imgout = img.copy()

	# initialize some internal variables
	deltaS = np.zeros_like(imgout)
	deltaE = deltaS.copy()
	NS = deltaS.copy()
	EW = deltaS.copy()
	gS = np.ones_like(imgout)
	gE = gS.copy()

	# create the plot figure, if requested
	if ploton:
		import pylab as pl
		from time import sleep

		fig = pl.figure(figsize=(20,5.5),num="Anisotropic diffusion")
		ax1,ax2 = fig.add_subplot(1,2,1),fig.add_subplot(1,2,2)

		ax1.imshow(img,interpolation='nearest')
		ih = ax2.imshow(imgout,interpolation='nearest',animated=True)
		ax1.set_title("Original image")
		ax2.set_title("Iteration 0")

		fig.canvas.draw()

	for ii in np.arange(1,niter):

		# calculate the diffs
		deltaS[:-1,: ] = np.diff(imgout,axis=0)
		deltaE[: ,:-1] = np.diff(imgout,axis=1)

		if 0<sigma:
			deltaSf=flt.gaussian_filter(deltaS,sigma);
			deltaEf=flt.gaussian_filter(deltaE,sigma);
		else: 
			deltaSf=deltaS;
			deltaEf=deltaE;
			
		# conduction gradients (only need to compute one per dim!)
		if option == 1:
			gS = np.exp(-(deltaSf/kappa)**2.)/step[0]
			gE = np.exp(-(deltaEf/kappa)**2.)/step[1]
		elif option == 2:
			gS = 1./(1.+(deltaSf/kappa)**2.)/step[0]
			gE = 1./(1.+(deltaEf/kappa)**2.)/step[1]

		# update matrices
		E = gE*deltaE
		S = gS*deltaS

		# subtract a copy that has been shifted 'North/West' by one
		# pixel. don't as questions. just do it. trust me.
		NS[:] = S
		EW[:] = E
		NS[1:,:] -= S[:-1,:]
		EW[:,1:] -= E[:,:-1]

		# update the image
		imgout += gamma*(NS+EW)

		if ploton:
			iterstring = "Iteration %i" %(ii+1)
			ih.set_data(imgout)
			ax2.set_title(iterstring)
			fig.canvas.draw()
			# sleep(0.01)

	return imgout

!mkdir anisotropic_diffusion

import cv2
import matplotlib.pyplot as plt
import numpy as np

#folder z jpg
input_folder = '/content/equalization_jpg'
output_folder = '/content/anisotropic_diffusion'

jpg_folder_names = os.listdir(input_folder)
jpg_folder_names.sort()

jpg_filepaths_list = []
jpg_stretched_list = []

for name in jpg_folder_names: 
  jpg_filepath = os.path.join(input_folder,name)
  
  #dołączanie do ścieżki
  jpg_filepaths_list.append(jpg_filepath)

  jpg_stretched_zm = os.path.join(output_folder,name)
  
  # Odczytanie zdjęcia i wywołanie 'anisotropic diffusion'
  image = cv2.imread(jpg_filepath)
  final_img = anisodiff(image, niter=3, kappa=25, gamma=0.25, option=1)
  
  s_output = np.uint8(final_img)
  jpg_stretched_list.append(s_output)
  cv2.imwrite(jpg_stretched_zm, s_output)

img_before_path = '/content/equalization_jpg/I0001.jpg'
img_after_path ='/content/anisotropic_diffusion/I0001.jpg'

display_histograms(img_before_path, img_after_path)

"""#Wycinanie z jpg (brak zastoswania)"""

# # wycinanie z jpg

# !mkdir jpg_to_cut_jpg
# #utworzenie listy z ścieżką do folderu z .jpg
# # haszami zaznaczone wszystko co poszło wyżej
# jpg_cut_filepath='/content/jpg_to_cut_jpg' #
# jpg_folder = '/content/dicom_to_jpg' #

# jpg_folder_names = os.listdir(jpg_folder) #
# jpg_folder_names.sort() #

# jpg_filepaths_list=[] #
# hist_list=[]
# cut_jpg_list=[]

# for name in jpg_folder_names: #
#   jpg_filepath = os.path.join(jpg_folder,name) #
#   jpg_filepaths_list.append(jpg_filepath) #

#   jpg_filepath_cut = os.path.join(jpg_cut_filepath,name) #

#   img = cv2.imread(jpg_filepath,1) #
#   image_in_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #
#   hist = cv2.calcHist([image_in_gray],[0],None,[256],[0,256])
#   hist_list.append(hist)

#   img_to_cut = cv2.imread(jpg_filepath,cv2.IMREAD_GRAYSCALE)
#   #ustawianie progu
#   threshhold = 33
#   img_height = img_to_cut.shape[0]
#   img_width = img_to_cut.shape[1]

#   for x in range(0, img_height):
#     for y in range(0, img_width):
#       if img_to_cut[x,y] > threshhold:
#         img_to_cut[x,y] = 0
#     cut_jpg_list.append(img_to_cut)

#     cv2.imwrite(jpg_filepath_cut, img_to_cut)

"""#Metoda Otsu"""

!mkdir otsu

import cv2
import matplotlib.pyplot as plt

#folder z jpg
input_folder = '/content/equalization_jpg'
# input_folder = '/content/anisotropic_diffusion' 
output_folder = '/content/otsu'

jpg_folder_names = os.listdir(input_folder)
jpg_folder_names.sort()

jpg_filepaths_list = []
jpg_stretched_list = []

for name in jpg_folder_names: 
  jpg_filepath = os.path.join(input_folder,name)

  #dołączanie do ścieżki
  jpg_filepaths_list.append(jpg_filepath) 

  jpg_stretched_zm = os.path.join(output_folder,name)
  
  #wczytujemy po jednym jpg
  img = cv2.imread(jpg_filepath,1)

  #zmieniamy na skalę szarości
  image_in_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) 

  ret,thresh = cv2.threshold(image_in_gray, 120, 255, cv2.THRESH_TOZERO_INV+cv2.THRESH_OTSU)

  s_output = np.uint8(thresh)
  jpg_stretched_list.append(s_output)
  cv2.imwrite(jpg_stretched_zm, s_output)

#Wyświetlenie zestawienia dla otsu
display_images('/content/otsu',400)

"""#Wycinanie najjaśnieszych wartości z rozciągniętych obrazów za pomocą jednego progu dla wszystkich obrazów (brak zastosowania)"""

!mkdir stretch_and_cut

#utworzenie listy z ścieżką do folderu z .jpg
jpg_cut_filepath='/content/stretch_and_cut' 
jpg_folder = '/content/stretched_jpg' 

jpg_folder_names = os.listdir(jpg_folder) 
jpg_folder_names.sort() 

jpg_filepaths_list=[] 
hist_list=[]
cut_jpg_list=[]

#tworzenie nowego katalogu
for name in jpg_folder_names: 
  jpg_filepath = os.path.join(jpg_folder,name) 
  jpg_filepaths_list.append(jpg_filepath) 

  jpg_filepath_cut = os.path.join(jpg_cut_filepath,name) 

  img = cv2.imread(jpg_filepath,0) 

  #wyznaczenie histogramu 
  hist = cv2.calcHist([image_in_gray],[0],None,[256],[0,256])
  hist_list.append(hist)

  img_to_cut = cv2.imread(jpg_filepath,cv2.IMREAD_GRAYSCALE)


 
  #ustawianie progu
  threshhold = 90
  img_height = img_to_cut.shape[0]
  img_width = img_to_cut.shape[1]

  for x in range(0, img_height):
    for y in range(0, img_width):
      if img_to_cut[x,y] > threshhold:
        img_to_cut[x,y] = 0
    cut_jpg_list.append(img_to_cut)

    cv2.imwrite(jpg_filepath_cut, img_to_cut)

#Wyświetlenie zestawienia dla obrobionych zdjęć (stretch_and_cut)
display_images('/content/stretch_and_cut',400)

"""#Wypełnienie otworów za pomocą operacji morfologicznego zamknięcia (brak zastosowania)"""

# !mkdir jpg_with_filled_holes
# import cv2
# import numpy as np

# #wypełnienie obrazów po operacji wycięcia (operacja zamknięcia openCV)
# jpg_filepath_filled='/content/jpg_with_filled_holes/I0001.jpg'
# img = cv2.imread('/content/jpg_to_cut_jpg/I0001.jpg',0)
# kernel = np.ones((4,4),np.uint8)
# img_temp = img.copy()
# # with np.printoptions(threshold=np.inf):
# #    print(img)
# plt.imshow(img)
# for x in range(0,img.shape[0]):
#   for y in range(0,img.shape[1]):
#     if img_temp[x,y]==0:
#       img[x,y]=img[x-1,y-1]

# img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
# #plt.imshow(img)    
# cv2.imwrite(jpg_filepath_filled, img)

# #wziac oryginalny obraz bez cuta i piksele x y oryginalnego przepisać w zera

!mkdir jpg_with_filled_holes
jpg_filepath_filled='/content/jpg_with_filled_holes/I0001.jpg'

#image = cv2.imread('/content/jpg_to_cut_jpg/I0001.jpg',1)
image = cv2.imread('/content/stretch_and_cut/I0001.jpg',1)
image_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
# plt.imshow(image_gray)

#Erosion
import cv2
import numpy as np
import matplotlib.pyplot as plt

# binarize the image
binr_for_erosion = cv2.threshold(image_gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
  
# define the kernel
kernel = np.ones((3, 3), np.uint8)
  
# invert the image
invert = cv2.bitwise_not(binr_for_erosion)
  
# erode the image
img_after_erosion = cv2.erode(invert, kernel, iterations=2)

# print the output
plt.imshow(img_after_erosion, cmap='gray')

#Dilation
image_for_dylation=image_gray.copy()

# binarize the image
binr = cv2.threshold(image_for_dylation, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
  
# define the kernel
kernel = np.ones((3, 3), np.uint8)

#kernel - dics?
  
# invert the image
invert = cv2.bitwise_not(binr)
  
# dilate the image
img_after_dilation = cv2.dilate(invert, kernel, iterations=1)
  
# print the output
plt.imshow(img_after_dilation, cmap='gray')

#and operation
blank_matrix = np.zeros((img_after_dilation.shape[0],img_after_dilation.shape[1]),img.dtype) 

for x in range(0,img_after_dilation.shape[0]):
  for y in range(0,img_after_dilation.shape[1]):
    blank_matrix[x,y]=img_after_dilation[x,y]*img_after_erosion[x,y]
plt.imshow(blank_matrix, cmap='gray')

#and operation
blank_matrix = np.zeros((img_after_dilation.shape[0],img_after_dilation.shape[1]),img.dtype) 

for x in range(0,img_after_dilation.shape[0]):
  for y in range(0,img_after_dilation.shape[1]):
    if img_after_dilation[x,y]==img_after_erosion[x,y]:
      blank_matrix[x,y]=1
plt.imshow(blank_matrix, cmap='gray')

"""#Erozja->dylacja->segmentacja->wypełnianie na podstawie zdjęcia pierwotnego 
**czas ładowania około 10 min!**


> do zrobienia: dobrać tak zmienne aby segmentacja poprawnie wyznaczała pole zainteresowania, zmienia się ono wraz z każdą kompilacją kodu więc należy zadbać o powtarzalność segmentacji. Zmienne określania położenia koła oraz jego kształtu zostały wyciągnięte w osobne zmienne dzięki czemu można zaimplementować dostosowywujący się obszar działania. W samym algorytmie aktywnych konturów należy zwrócić uwagę na zmienną **w_edge** odpowiedzialną za dopasowanie powstałego kształtu do obiektu. W najlepszymp rzykładzie musi on odstawać na tyle aby wstawienie w późniejszym etapie pierwotnego obrazu skutkowało dodaniem całego obszaru zainteresowania.


"""

!mkdir segmented_images
!mkdir filled_images

import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import points_in_poly
from skimage.color import rgb2gray
from skimage import data
from skimage.filters import gaussian
from skimage.segmentation import active_contour

#folder z jpg
base_img_folder = '/content/equalization_jpg'
filled_folder = '/content/filled_images'
output_folder = '/content/segmented_images' 
input_folder = '/content/equalization_jpg' #nie musimy robic otsu skoro obszar zainteresowania wycina najjaśniejsze

jpg_folder_names = os.listdir(input_folder)
jpg_folder_names.sort()

jpg_filepaths_list = []
jpg_list_dilation = []

# Ustaw promień dysku
radius = 1

# Utwórz macierz w kształcie dysku
kernel = np.zeros((radius*2+1, radius*2+1))
for i in range(radius*2+1):
  for j in range(radius*2+1):
    if ((i - radius)**2 + (j - radius)**2) <= radius**2:
      kernel[i, j] = 1

kern = np.uint8(kernel)

#do zrobienia (zmienic kernel dla dylacji: dysk itp)
kernel_d = np.ones((3,3), np.uint8)

for name in jpg_folder_names: 
  jpg_filepath_input = os.path.join(input_folder,name)
  jpg_filepath_output = os.path.join(output_folder,name)
  jpg_filepath_base = os.path.join(base_img_folder,name)
  jpg_filepath_filled = os.path.join(filled_folder,name)

  #dołączanie do ścieżki
  jpg_filepaths_list.append(jpg_filepath_input) 

  #wczytujemy po jednym jpg
  img = cv2.imread(jpg_filepath_input, 0)
  image_base = cv2.imread(jpg_filepath_base, 0)

# tez niepotrzebne 
  #Erozja
  #img_erosion = cv2.erode(image, kern, iterations=1)

  #Dylacja
  #img_dilation = cv2.dilate(img_erosion, kernel_d, iterations=1)
  #jpg_list_dilation.append(img_dilation)

  #Segmentacja
  #img=img_dilation

  #utworzenie 256 punktów równomiernie rozmieszczonych na okręgu o promieniu 70 i środku w punkcie (130, 130)
  up_down_circle_center=150
  right_left_circle_center=140

  flattening_circle=70
  slimming_circle=75

  s = np.linspace(0, 2*np.pi, 256)
  r = up_down_circle_center + flattening_circle*np.sin(s)
  c = right_left_circle_center + slimming_circle*np.cos(s)
  init = np.array([r, c]).T

  #dostosować aktywny kontur tak aby okalał obszar zainteresowania (do zrobienia sprawdzić alpha beta gamma możer należy wywalić gausowski filtr) 
  if previous_snake is None:
    snake = active_contour(gaussian(img, 3, preserve_range=False), init, alpha=0.002, beta=0.001, w_line=-0.05, w_edge=-0.25, gamma=0.001, max_px_move=1, boundary_condition='periodic')
    previous_snake = snake
  else:
    snake = active_contour(gaussian(img, 3, preserve_range=False), previous_snake, alpha=0.002, beta=0.001, w_line=-0.05, w_edge=-0.25, gamma=0.001, max_px_move=1, boundary_condition='periodic')
    previous_snake = snake
  #użycie algorytmu Active Contour na przetworzonym filtracją Gaussa obrazie w celu znalezienia konturu obiektu
  snake = active_contour(gaussian(img, 2, preserve_range=False), init, alpha=0.002, beta=0.001, w_line=-0.05, w_edge=-0.25, gamma=0.001, max_px_move=1, boundary_condition='periodic')

  #wyświetlenie obrazu wraz z rysowaniem na nim pierwotnej linii (punkty zdefiniowane jako init) oraz znalezionego konturu
  fig, ax = plt.subplots(figsize=(7, 7))
  ax.imshow(img, cmap=plt.cm.gray)
  ax.plot(init[:, 1], init[:, 0], '--r', lw=1)
  ax.plot(snake[:, 1], snake[:, 0], '-b', lw=1)
  ax.set_xticks([]), ax.set_yticks([])
  ax.axis([0, img.shape[1], img.shape[0], 0])

  #Zapis wysegmentowanego obrazu
  plt.savefig(jpg_filepath_output)

  #Wypełnienie
  #stworzenie siatki pikseli o rozmiarze obrazu
  rows, cols = img.shape[:2]
  xx, yy = np.meshgrid(np.arange(cols), np.arange(rows))

  #wykorzystanie funkcji points_in_poly() do uzyskania maski pikseli wewnątrz konturu
  mask = points_in_poly(np.column_stack((yy.ravel(), xx.ravel())), snake).reshape(rows, cols)

  #zastosowanie operatora maskowania
  masked_im = np.zeros_like(image_base)
  masked_im[mask] = image_base[mask]

  #wyświetlenie obrazów
  fig, ax = plt.subplots(figsize=(5, 5))
  fig.subplots_adjust(bottom=0, top=1, left=0, right=1)
  ax.imshow(masked_im, cmap='gray')
  ax.axis('off')
  plt.savefig(jpg_filepath_filled)

display_images('/content/segmented_images', 400)

display_images('/content/filled_images', 400)

"""# segmentacja backup code (brak zastosowania)"""

import numpy as np
import matplotlib.pyplot as plt
from skimage.color import rgb2gray
from skimage import data
from skimage.filters import gaussian
from skimage.segmentation import active_contour

img=img_dilation

#utworzenie 256 punktów równomiernie rozmieszczonych na okręgu o promieniu 70 i środku w punkcie (130, 130)
up_down_circle_center=150
right_left_circle_center=140

flattening_circle=70
slimming_circle=70

s = np.linspace(0, 2*np.pi, 256)
r = up_down_circle_center + flattening_circle*np.sin(s)
c = right_left_circle_center + slimming_circle*np.cos(s)
init = np.array([r, c]).T

#dostosować aktywny kontur tak aby okalał obszar zainteresowania (do zrobienia) 

#użycie algorytmu Active Contour na przetworzonym filtracją Gaussa obrazie w celu znalezienia konturu obiektu
snake = active_contour(gaussian(img, 3, preserve_range=False), init, alpha=0.004, beta=0.001, w_line=-0.05, w_edge=1.5, gamma=0.001, max_px_move=1, boundary_condition='periodic')

#wyświetlenie obrazu wraz z rysowaniem na nim pierwotnej linii (punkty zdefiniowane jako init) oraz znalezionego konturu
fig, ax = plt.subplots(figsize=(7, 7))
ax.imshow(img, cmap=plt.cm.gray)
ax.plot(init[:, 1], init[:, 0], '--r', lw=1)
ax.plot(snake[:, 1], snake[:, 0], '-b', lw=1)
ax.set_xticks([]), ax.set_yticks([])
ax.axis([0, img.shape[1], img.shape[0], 0])

from skimage.measure import points_in_poly

# stworzenie siatki pikseli o rozmiarze obrazu
rows, cols = img.shape[:2]
xx, yy = np.meshgrid(np.arange(cols), np.arange(rows))

# wykorzystanie funkcji points_in_poly() do uzyskania maski pikseli wewnątrz konturu
mask = points_in_poly(np.column_stack((yy.ravel(), xx.ravel())), snake).reshape(rows, cols)

import matplotlib.pyplot as plt

# wyświetlenie samej maski w kolorze
plt.imshow(mask, cmap=plt.cm.jet)

from skimage.measure import points_in_poly

# stworzenie siatki pikseli o rozmiarze obrazu
rows, cols = img.shape[:2]
xx, yy = np.meshgrid(np.arange(cols), np.arange(rows))

# wykorzystanie funkcji points_in_poly() do uzyskania maski pikseli wewnątrz konturu
mask = points_in_poly(np.column_stack((yy.ravel(), xx.ravel())), snake).reshape(rows, cols)

import cv2
import matplotlib.pyplot as plt

# wczytanie obrazu oryginalnego
im_org = cv2.imread('/content/stretched_jpg/I0001.jpg', 0)

# zastosowanie operatora maskowania
masked_im = np.zeros_like(im_org)
masked_im[mask] = im_org[mask]

# wyświetlenie obrazów
fig, ax = plt.subplots( figsize=(5, 5))
ax.imshow(masked_im, cmap='gray')
ax.set_title('Maskowany obraz')
fname='img'
plt.savefig(fname)

"""#Segmentacja lvl set 
>problem z segmentacją zdjęć w lvl set, prawdopodobnie obrazy jakie wychodzą ze snake są źle zapisywane co powoduje że następny proces zaczyna segmentować po kszrałcie maski. Można porównać że lvl set dobrze działa na wyrównanym zdjęciu a na zdjęciu po segmentacji przestaje działać.
"""

import sys
import numpy as np
import cv2
import matplotlib.pyplot as plt
import math
from pylab import*

img_dilation = cv2.imread('/content/equalization_jpg/I0200.jpg', 0)
img=np.array(img_dilation,dtype=np.float64) 

#celowanie kwadratem
IniLSF = np.ones((img.shape[0],img.shape[1]),img.dtype) 
IniLSF[250:300,250:300]= -1
IniLSF=-IniLSF 

img_dilation = cv2.cvtColor(img_dilation,cv2.COLOR_BGR2RGB) 
plt.figure(1),plt.imshow(img_dilation),plt.xticks([]), plt.yticks([])   # to hide tick values on X and Y axis
plt.contour(IniLSF,[0],color = 'b',linewidth=2)  
plt.draw(),plt.show(block=False) 

def mat_math (intput,str):
    output=intput 
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if str=="atan":
                output[i,j] = math.atan(intput[i,j]) 
            if str=="sqrt":
                output[i,j] = math.sqrt(intput[i,j]) 
    return output 


def CV (LSF, img, mu, nu, epison,step):

    Drc = (epison / math.pi) / (epison*epison+ LSF*LSF)
    Hea = 0.5*(1 + (2 / math.pi)*mat_math(LSF/epison,"atan")) 
    Iy, Ix = np.gradient(LSF) 
    s = mat_math(Ix*Ix+Iy*Iy,"sqrt") 
    Nx = Ix / (s+0.000001) 
    Ny = Iy / (s+0.000001) 
    Mxx,Nxx =np.gradient(Nx) 
    Nyy,Myy =np.gradient(Ny) 
    cur = Nxx + Nyy 
    Length = nu*Drc*cur 

    Lap = cv2.Laplacian(LSF,-1) 
    Penalty = mu*(Lap - cur) 

    s1=Hea*img 
    s2=(1-Hea)*img 
    s3=1-Hea 
    C1 = s1.sum()/ Hea.sum() 
    C2 = s2.sum()/ s3.sum() 
    CVterm = Drc*(-1 * (img - C1)*(img - C1) + 1 * (img - C2)*(img - C2)) 

    LSF = LSF + step*(Length + Penalty + CVterm) 
    #plt.imshow(s, cmap ='gray'),plt.show() 
    return LSF 

#parametry (z jaką siłą się rozchodzi)
mu = 1  
nu = 0.003 * 255 * 255 
num = 50 # liczba iteracji czyli jak jest dokładny 
epison = 1 
step = 0.1 # nie do zmiany
LSF=IniLSF 

for i in range(1,num):
    LSF = CV(LSF, img, mu, nu, epison,step) 
    if i % 1 == 0:   
        plt.imshow(img_dilation),plt.xticks([]), plt.yticks([])  
        plt.contour(LSF,[0],colors='r',linewidth=2) 
        plt.draw(),plt.show(block=False),plt.pause(0.01)

"""#**Segmentacja**"""

import numpy as np
import matplotlib.pyplot as plt
from skimage.color import rgb2gray
from skimage import data
from skimage.filters import gaussian
from skimage.segmentation import active_contour


img = cv2.imread('/content/stretched_jpg/I0001.jpg', 0)


s = np.linspace(0, 2*np.pi, 256)
r = 130 + 70*np.sin(s)
c = 130 + 70*np.cos(s)
init = np.array([r, c]).T

snake = active_contour(gaussian(img, 3, preserve_range=False), init, alpha=0.004, beta=0.001, w_line=-0.05, w_edge=1.5, gamma=0.001, max_px_move=1, boundary_condition='periodic')
#snake = active_contour(img, init, alpha=0.015, beta=10, w_line=0, w_edge=-1, gamma=0.001, boundary_condition='periodic')
    #img, 3, preserve_range=False,  alpha=0.002, beta=0.05, gamma=0.001)

fig, ax = plt.subplots(figsize=(7, 7))
ax.imshow(img, cmap=plt.cm.gray)
ax.plot(init[:, 1], init[:, 0], '--r', lw=1)
ax.plot(snake[:, 1], snake[:, 0], '-b', lw=1)
ax.set_xticks([]), ax.set_yticks([])
ax.axis([0, img.shape[1], img.shape[0], 0])

plt.show()

import sys
import numpy as np
import cv2
import matplotlib.pyplot as plt
import math
from pylab import*

Image = cv2.imread('/content/jpg_with_filled_holes/I0001.jpg',1) 
# Image = cv2.imread('/content/jpg_to_cut_jpg/I0001.jpg',1)  
image = cv2.cvtColor(Image,cv2.COLOR_BGR2GRAY)
img=np.array(image,dtype=np.float64) 

#celowanie kwadratem
IniLSF = np.ones((img.shape[0],img.shape[1]),img.dtype) 
# IniLSF[30:80,30:80]= -1 
# IniLSF[110:140,110:140]= -1
IniLSF[90:120,90:120]= -1
IniLSF=-IniLSF 


Image = cv2.cvtColor(Image,cv2.COLOR_BGR2RGB) 
plt.figure(1),plt.imshow(Image),plt.xticks([]), plt.yticks([])   # to hide tick values on X and Y axis
plt.contour(IniLSF,[0],color = 'b',linewidth=2)  
plt.draw(),plt.show(block=False) 

def mat_math (intput,str):
    output=intput 
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if str=="atan":
                output[i,j] = math.atan(intput[i,j]) 
            if str=="sqrt":
                output[i,j] = math.sqrt(intput[i,j]) 
    return output 


def CV (LSF, img, mu, nu, epison,step):

    Drc = (epison / math.pi) / (epison*epison+ LSF*LSF)
    Hea = 0.5*(1 + (2 / math.pi)*mat_math(LSF/epison,"atan")) 
    Iy, Ix = np.gradient(LSF) 
    s = mat_math(Ix*Ix+Iy*Iy,"sqrt") 
    Nx = Ix / (s+0.000001) 
    Ny = Iy / (s+0.000001) 
    Mxx,Nxx =np.gradient(Nx) 
    Nyy,Myy =np.gradient(Ny) 
    cur = Nxx + Nyy 
    Length = nu*Drc*cur 

    Lap = cv2.Laplacian(LSF,-1) 
    Penalty = mu*(Lap - cur) 

    s1=Hea*img 
    s2=(1-Hea)*img 
    s3=1-Hea 
    C1 = s1.sum()/ Hea.sum() 
    C2 = s2.sum()/ s3.sum() 
    CVterm = Drc*(-1 * (img - C1)*(img - C1) + 1 * (img - C2)*(img - C2)) 

    LSF = LSF + step*(Length + Penalty + CVterm) 
    #plt.imshow(s, cmap ='gray'),plt.show() 
    return LSF 

#parametry (z jaką siłą się rozchodzi)
mu = 1  
nu = 0.003 * 255 * 255 
num = 30 # liczba iteracji czyli jak jest dokładny 
epison = 1 
step = 0.1 # nie do zmiany
LSF=IniLSF 

for i in range(1,num):
    LSF = CV(LSF, img, mu, nu, epison,step) 
    if i % 1 == 0:   
        plt.imshow(Image),plt.xticks([]), plt.yticks([])  
        plt.contour(LSF,[0],colors='r',linewidth=2) 
        plt.draw(),plt.show(block=False),plt.pause(0.01)

import sys
import numpy as np
import cv2
import matplotlib.pyplot as plt
import math
from pylab import*

#Image = img_dilation 
# Image = cv2.imread('/content/jpg_to_cut_jpg/I0001.jpg',1)  
#img_dilation = image
img=np.array(img_dilation,dtype=np.float64) 

#celowanie kwadratem
IniLSF = np.ones((img.shape[0],img.shape[1]),img.dtype) 
# IniLSF[30:80,30:80]= -1 
IniLSF[110:140,110:140]= -1
#IniLSF[90:120,90:120]= -1
IniLSF=-IniLSF 


img_dilation = cv2.cvtColor(img_dilation,cv2.COLOR_BGR2RGB) 
plt.figure(1),plt.imshow(img_dilation),plt.xticks([]), plt.yticks([])   # to hide tick values on X and Y axis
plt.contour(IniLSF,[0],color = 'b',linewidth=2)  
plt.draw(),plt.show(block=False) 

def mat_math (intput,str):
    output=intput 
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if str=="atan":
                output[i,j] = math.atan(intput[i,j]) 
            if str=="sqrt":
                output[i,j] = math.sqrt(intput[i,j]) 
    return output 


def CV (LSF, img, mu, nu, epison,step):

    Drc = (epison / math.pi) / (epison*epison+ LSF*LSF)
    Hea = 0.5*(1 + (2 / math.pi)*mat_math(LSF/epison,"atan")) 
    Iy, Ix = np.gradient(LSF) 
    s = mat_math(Ix*Ix+Iy*Iy,"sqrt") 
    Nx = Ix / (s+0.000001) 
    Ny = Iy / (s+0.000001) 
    Mxx,Nxx =np.gradient(Nx) 
    Nyy,Myy =np.gradient(Ny) 
    cur = Nxx + Nyy 
    Length = nu*Drc*cur 

    Lap = cv2.Laplacian(LSF,-1) 
    Penalty = mu*(Lap - cur) 

    s1=Hea*img 
    s2=(1-Hea)*img 
    s3=1-Hea 
    C1 = s1.sum()/ Hea.sum() 
    C2 = s2.sum()/ s3.sum() 
    CVterm = Drc*(-1 * (img - C1)*(img - C1) + 1 * (img - C2)*(img - C2)) 

    LSF = LSF + step*(Length + Penalty + CVterm) 
    #plt.imshow(s, cmap ='gray'),plt.show() 
    return LSF 

#parametry (z jaką siłą się rozchodzi)
mu = 1  
nu = 0.003 * 255 * 255 
num = 30 # liczba iteracji czyli jak jest dokładny 
epison = 1 
step = 0.1 # nie do zmiany
LSF=IniLSF 

for i in range(1,num):
    LSF = CV(LSF, img, mu, nu, epison,step) 
    if i % 1 == 0:   
        plt.imshow(img_dilation),plt.xticks([]), plt.yticks([])  
        plt.contour(LSF,[0],colors='r',linewidth=2) 
        plt.draw(),plt.show(block=False),plt.pause(0.01)
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import cv2
import numpy as np
from keras.models import load_model
import time
import functools
import operator
import CNNModelp

global fn
fn = ""

root = tk.Tk()
root.configure(background="seashell2")

w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry(f"{w}x{h}+0+0")
root.title("Detection and Classification of Agricultural Pests")

# Background image
image2 = Image.open('z.jpeg')
image2 = image2.resize((w, h))
background_image = ImageTk.PhotoImage(image2)
background_label = tk.Label(root, image=background_image)
background_label.image = background_image
background_label.place(x=0, y=0)

# Header label
lbl = tk.Label(root, text="Detection and Classification of Agricultural Pests", font=('times', 35, 'bold'), height=1, width=60, bg="black", fg="white")
lbl.place(x=0, y=20)

# Frame for buttons
frame_alpr = tk.LabelFrame(root, text="", width=220, height=550, bd=5, font=('times', 14, 'bold'), bg="black")
frame_alpr.grid(row=0, column=0, sticky='nw')
frame_alpr.place(x=10, y=90)

# Pest information
pest_info = {
    "Aphids": {"causes": "Overcrowding, excessive nitrogen", "prevention": "Introduce natural predators, use insecticidal soap"},
    "Armyworm": {"causes": "Overripe crops, dense foliage", "prevention": "Handpick worms, use natural predators"},
    "Beetle": {"causes": "Crop debris, favorable climate", "prevention": "Crop rotation, use of traps"},
    "Bollworm": {"causes": "Overripe crops, lack of natural enemies", "prevention": "Use of BT crops, natural predators"},
    "Grasshopper": {"causes": "Warm, dry weather", "prevention": "Use of insecticidal bait, natural predators"},
    "Mites": {"causes": "Hot, dry weather", "prevention": "Maintain humidity, use miticides"},
    "Mosquito": {"causes": "Standing water", "prevention": "Eliminate standing water, use mosquito nets"},
    "Sawfly": {"causes": "Dense foliage", "prevention": "Prune infected parts, use insecticides"},
    "Stem_borer": {"causes": "Infested crop residue", "prevention": "Destroy crop residue, use resistant varieties"},
}

def update_label(text):
    result_label = tk.Label(root, text=text, width=60, font=("bold", 20), bg='bisque2', fg='black')
    result_label.place(x=250, y=400)

def train_model():
    update_label("Model Training Start...............")
    start = time.time()
    # Replace CNNModelp.main() with your actual model training function
    X = CNNModelp.main()
    end = time.time()
    ET = f"Execution Time: {end - start:.4} seconds \n"
    msg = "Model Training Completed..\n" + ET
    print(msg)
    update_label(msg)

def convert_str_to_tuple(tup):
    return functools.reduce(operator.add, tup)

def test_model_proc(fn):
    IMAGE_SIZE = 64
    model = load_model('pest.h5', compile=False)
    img = Image.open(fn)
    img = img.resize((IMAGE_SIZE, IMAGE_SIZE))
    img = np.array(img)
    img = img.reshape(1, IMAGE_SIZE, IMAGE_SIZE, 3)
    img = img.astype('float32') / 255.0
    prediction = model.predict(img)
    confidence = np.max(prediction)
    plant = np.argmax(prediction)
    pests = ["Aphids", "Armyworm", "Beetle", "Bollworm", "Grasshopper", "Mites", "Mosquito", "Sawfly", "Stem_borer"]
    #return pests[plant]
    if confidence < 0.8:  # Threshold for unknown
        return "Unknown"
    else:
        return pests[plant]


def test_model():
    global fn
    if fn:
        update_label("Model Testing Start...............")
        start = time.time()
        pest = test_model_proc(fn)
        causes = pest_info.get(pest, {}).get("causes", "N/A")
        prevention = pest_info.get(pest, {}).get("prevention", "N/A")
        x2 = f"{pest} pest is detected"
        end = time.time()
        ET = f"Execution Time: {end - start:.4} seconds \n"
        msg = f"Image Testing Completed..\n{x2}\nCauses: {causes}\nPrevention: {prevention}\n{ET}"
        fn = ""
    else:
        msg = "Please Select Image For Prediction...."
    update_label(msg)

def openimage():
    global fn
    fileName = askopenfilename(initialdir='D:/Agri PEST/100% code Agri pest classification/100% code Agri pest classification/dataset/testing', title='Select image for Analysis', filetypes=[("all files", "*.*")])
    if fileName:
        IMAGE_SIZE = 200
        imgpath = fileName
        fn = fileName
        img = Image.open(imgpath)
        img = img.resize((IMAGE_SIZE, IMAGE_SIZE))
        imgtk = ImageTk.PhotoImage(img)
        img_label = tk.Label(root, image=imgtk)
        img_label.image = imgtk
        img_label.place(x=300, y=100)

def convert_grey():
    global fn
    if fn:
        IMAGE_SIZE = 200
        img = Image.open(fn)
        img = img.resize((IMAGE_SIZE, IMAGE_SIZE))
        img_array = np.array(img)
        x1, y1 = img_array.shape[0], img_array.shape[1]
        gs = cv2.cvtColor(cv2.imread(fn), cv2.COLOR_RGB2GRAY)
        gs = cv2.resize(gs, (x1, y1))
        retval, threshold = cv2.threshold(gs, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        im_gs = Image.fromarray(gs)
        im_gs_tk = ImageTk.PhotoImage(im_gs)
        img2 = tk.Label(root, image=im_gs_tk, height=200, width=200, bg='white')
        img2.image = im_gs_tk
        img2.place(x=580, y=100)
        im_thresh = Image.fromarray(threshold)
        im_thresh_tk = ImageTk.PhotoImage(im_thresh)
        img3 = tk.Label(root, image=im_thresh_tk, height=200, width=200)
        img3.image = im_thresh_tk
        img3.place(x=880, y=100)
    else:
        update_label("Please Select Image For Conversion....")
'''
def detect_objects():
    global fn
    if fn:
        model = load_model('pest.h5', compile=False)
        IMAGE_SIZE = 64
        img = Image.open(fn)
        img = img.resize((IMAGE_SIZE, IMAGE_SIZE))
        img_array = np.array(img)
        img_array = img_array.reshape(1, IMAGE_SIZE, IMAGE_SIZE, 3)
        img_array = img_array.astype('float32') / 255.0
        prediction = model.predict(img_array)
        pest_classes = ["Aphids", "Armyworm", "Beetle", "Bollworm", "Grasshopper", "Mites", "Mosquito", "Sawfly", "Stem_borer"]
        #detected_pests = [pest_classes[i] for i in np.argmax(prediction, axis=1)]
        confidences = np.max(prediction, axis=1)
        indices = np.argmax(prediction, axis=1)
        detected_pests = [] 
        for idx, conf in zip(indices, confidences):
            if conf < 0.8:
                detected_pests.append("Unknown")
            else:
                detected_pests.append(pest_classes[idx])
        
        img_cv = cv2.imread(fn)
        img_cv_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
        
        # Draw example bounding boxes; replace with actual model output if available
        (x, y, w, h) = (10, 15, 30, 30)
        for pest in detected_pests:
            cv2.rectangle(img_cv_rgb, (x, y), (x + w, y + h), (0, 255, 0), 1)
            cv2.putText(img_cv_rgb, pest, (x, y - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
        
        display_size = 200
        img_cv_rgb = cv2.resize(img_cv_rgb, (display_size, display_size))
        im = Image.fromarray(img_cv_rgb)
        imgtk = ImageTk.PhotoImage(image=im)
        
        # Clear previous images and labels
        for widget in root.winfo_children():
            if isinstance(widget, tk.Label) and widget != background_label:
                widget.destroy()

        img_label = tk.Label(root, image=imgtk)
        img_label.image = imgtk
        img_label.place(x=300, y=100)
    else:
        update_label("Please Select Image For Object Detection....")
'''
def detect_objects():
    global fn
    if fn:
        model = load_model('pest.h5', compile=False)
        IMAGE_SIZE = 64

        # Prepare the image
        img = Image.open(fn)
        img = img.resize((IMAGE_SIZE, IMAGE_SIZE))
        img_array = np.array(img).reshape(1, IMAGE_SIZE, IMAGE_SIZE, 3).astype('float32') / 255.0

        # Prediction
        prediction = model.predict(img_array)
        pest_classes = ["Aphids", "Armyworm", "Beetle", "Bollworm", "Grasshopper", "Mites", "Mosquito", "Sawfly", "Stem_borer"]
        confidence = np.max(prediction)
        index = np.argmax(prediction)

        # Determine detected pest or Unknown
        if confidence < 0.8:
            detected_pest = "Unknown"
        else:
            detected_pest = pest_classes[index]

        # Load and draw image
        img_cv = cv2.imread(fn)
        img_cv_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
        (x, y, w, h) = (10, 15, 30, 30)

        if detected_pest != "Unknown":
            cv2.rectangle(img_cv_rgb, (x, y), (x + w, y + h), (0, 255, 0), 1)
            cv2.putText(img_cv_rgb, f"{detected_pest}", (x, y - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        else:
            cv2.rectangle(img_cv_rgb, (x, y), (x + w, y + h), (0, 255, 0), 1)
            cv2.putText(img_cv_rgb, "Unknown", (x, y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        # Resize image
        img_cv_rgb = cv2.resize(img_cv_rgb, (200, 200))
        im = Image.fromarray(img_cv_rgb)
        imgtk = ImageTk.PhotoImage(image=im)

        # Clear previous images and labels
        for widget in root.winfo_children():
            if isinstance(widget, tk.Label) and widget != background_label:
                widget.destroy()

        img_label = tk.Label(root, image=imgtk)
        img_label.image = imgtk
        img_label.place(x=300, y=100)

        # Update the status message
        if detected_pest != "Unknown":
            update_label(f"Detected: {detected_pest} (Confidence: {confidence:.2f})")
        else:
            update_label("No known pest detected.")
    else:
        update_label("Please Select Image For Object Detection....")

# Button styling
button_style = {
    "font": ('times', 14, 'bold'),
    "bg": "black",
    "fg": "white",
    "activebackground": "#7a3b2e",
    "width": 15,
    "height": 1
}

# Buttons
open_image_button = tk.Button(frame_alpr, text="Select Image", command=openimage, **button_style)
open_image_button.grid(row=0, column=0, pady=10)

train_model_button = tk.Button(frame_alpr, text="Train Model", command=train_model, **button_style)
train_model_button.grid(row=4, column=0, pady=10)

test_model_button = tk.Button(frame_alpr, text="Test Model", command=test_model, **button_style)
test_model_button.grid(row=3, column=0, pady=10)

convert_grey_button = tk.Button(frame_alpr, text="Convert to Grey", command=convert_grey, **button_style)
convert_grey_button.grid(row=1, column=0, pady=10)

detect_objects_button = tk.Button(frame_alpr, text="Detect Objects", command=detect_objects, **button_style)
detect_objects_button.grid(row=2, column=0, pady=10)

btn_exit = tk.Button(frame_alpr, text="Exit", command=root.destroy, font=('times', 14, 'bold'), bg='black', fg='white')
btn_exit.grid(row=5, column=0, pady=10)

root.mainloop()

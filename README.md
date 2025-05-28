# Precision-Agriculture-ML-and-DL-Techniques-for-pest-detection-and-Classification 🌱🐛

This project is a **deep learning-based pest classification system** built using a Convolutional Neural Network (CNN) model in Keras.  
It helps detect and classify agricultural pests from images, with a Tkinter-based GUI for user interaction.

If the model encounters an unknown or untrained pest image, it reports the result as **"Unknown"** (based on a confidence threshold).

---

## 🌟 Features

✅ Pest classification using a trained CNN (`pest.h5`)  

✅ Tkinter-based graphical user interface (GUI)  

✅ Confidence thresholding to reject unknown images 

✅ Simple image upload and display with bounding box annotation

✅ Detects common agricultural pests like:
- Aphids
- Armyworm
- Beetle
- Bollworm
- Grasshopper
- Mites
- Mosquito
- Sawfly
- Stem Borer

✅ Tkinter-based GUI with buttons for:
- Image upload
- Model testing
- Grayscale conversion
- Object detection with bounding boxes

✅ Displays causes and prevention suggestions for each detected pest.

✅ Rejects random/unrelated images as **Unknown** when confidence is low.

---
## 📦 Requirements

The key libraries used are:

* `tensorflow`
* `keras`
* `numpy`
* `opencv-python`
* `pillow`
* `matplotlib`
* `scikit-learn`
* `tkvideo`
* `mediapipe`
* `gtts`
* `pandas`
* `flask`
* `mlxtend`

Full list included in `requirements.txt`.

## 💡 Future Improvements

✨ Add live webcam detection mode

✨ Improve model accuracy with more training data

✨ Package as an executable (using PyInstaller) for easy distribution

✨ Add Docker support for consistent deployment

## 🙌 Credits

Developed by **Prerana Jangid**

For questions: [jangidprerana790@gmail.com](mailto:jangidprerana790@gmail.com)




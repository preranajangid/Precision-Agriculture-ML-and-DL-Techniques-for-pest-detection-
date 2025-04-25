def main():
    import numpy as np
    from keras.models import Sequential
    from keras.layers import Convolution2D, MaxPooling2D, Flatten, Dense, Dropout
    from keras import optimizers
    from keras.preprocessing.image import ImageDataGenerator
    from sklearn.metrics import classification_report, precision_recall_fscore_support
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd

    basepath = "D:/Agri PEST/100% code Agri pest classification/100% code Agri pest classification/dataset"

    # Initializing the CNN
    classifier = Sequential()

    # Step 1 - Convolution Layer
    classifier.add(Convolution2D(32, (3, 3), input_shape=(64, 64, 3), activation='relu'))

    # Step 2 - Pooling
    classifier.add(MaxPooling2D(pool_size=(2, 2)))

    # Adding second convolution layer
    classifier.add(Convolution2D(32, (3, 3), activation='relu'))
    classifier.add(MaxPooling2D(pool_size=(2, 2)))

    # Adding third convolution layer
    classifier.add(Convolution2D(64, (3, 3), activation='relu'))
    classifier.add(MaxPooling2D(pool_size=(2, 2)))

    # Step 3 - Flattening
    classifier.add(Flatten())

    # Step 4 - Full Connection
    classifier.add(Dense(256, activation='relu'))
    classifier.add(Dropout(0.5))
    classifier.add(Dense(9, activation='softmax'))  # change class no.

    # Compiling The CNN
    classifier.compile(
        optimizer=optimizers.SGD(learning_rate=0.01),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    # Part 2 Fitting the CNN to the image
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True
    )

    test_datagen = ImageDataGenerator(rescale=1./255)

    training = train_datagen.flow_from_directory(
        basepath + '/training',
        target_size=(64, 64),
        batch_size=32,
        class_mode='categorical'
    )

    testing = test_datagen.flow_from_directory(
        basepath + '/testing',
        target_size=(64, 64),
        batch_size=32,
        class_mode='categorical'
    )

    steps_per_epoch = int(np.ceil(training.samples / 32))
    val_steps = int(np.ceil(testing.samples / 32))

    model = classifier.fit_generator(
        training,
        steps_per_epoch=steps_per_epoch,
        epochs=450,
        validation_data=testing,
        validation_steps=val_steps
    )

    # Saving the model
    classifier.save(basepath + '/pest.h5')

    # Evaluating the model
    scores = classifier.evaluate(testing, verbose=1)
    B = "Testing Accuracy: %.2f%%" % (scores[1] * 100)
    print(B)
    scores = classifier.evaluate(training, verbose=1)
    C = "Training Accuracy: %.2f%%" % (scores[1] * 100)
    print(C)

    msg = B + '\n' + C

    # Predictions and Classification Report
    Y_pred = classifier.predict(testing, val_steps)
    y_pred = np.argmax(Y_pred, axis=1)
    y_true = testing.classes
    target_names = list(testing.class_indices.keys())

    report = classification_report(y_true, y_pred, target_names=target_names)
    print(report)

    precision, recall, f1_score, _ = precision_recall_fscore_support(y_true, y_pred, average=None, labels=np.unique(y_true))

    # Create a DataFrame for visualization
    metrics_df = pd.DataFrame({
        'Class': target_names,
        'Precision': precision,
        'Recall': recall,
        'F1-Score': f1_score
    })

    # Plot metrics
    plt.figure(figsize=(12, 8))
    sns.barplot(x='Class', y='Precision', data=metrics_df, color='b', label='Precision')
    sns.barplot(x='Class', y='Recall', data=metrics_df, color='r', label='Recall', alpha=0.7)
    sns.barplot(x='Class', y='F1-Score', data=metrics_df, color='g', label='F1-Score', alpha=0.5)
    plt.title('Precision, Recall, and F1-Score by Class')
    plt.ylabel('Score')
    plt.xlabel('Class')
    plt.legend()
    plt.xticks(rotation=45)
    plt.savefig(basepath + "/metrics.png", bbox_inches='tight')
    plt.show()

    # Plot accuracy
    plt.plot(model.history.history['accuracy'])
    plt.plot(model.history.history['val_accuracy'])
    plt.title('Model Accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.savefig(basepath + "/accuracy.png", bbox_inches='tight')
    plt.show()

    # Plot loss
    plt.plot(model.history.history['loss'])
    plt.plot(model.history.history['val_loss'])
    plt.title('Model Loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.savefig(basepath + "/loss.png", bbox_inches='tight')
    plt.show()

    return msg

# Call the main function
if __name__ == "__main__":
    main()

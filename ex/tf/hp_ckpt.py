import tensorflow as tf
import matplotlib.pyplot as plt
import os


CKPT_PATH = 'ckpts/mnist.ckpt'
CKPT_DIR = os.path.dirname(CKPT_PATH)


ckpt_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath=CKPT_PATH,
    save_weights_only=True,
    verbose=1,
    # monitor='val_accuracy',
    # mode='max',
    # save_best_only=True
)

mnist = tf.keras.datasets.mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(60, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

trained_model = model.fit(
    x_train, y_train,
    validation_split=0.3,
    epochs=10,
    callbacks=[ckpt_callback])

plt.plot(trained_model.history['loss'], 'r--')
plt.plot(trained_model.history['accuracy'], 'b-')
plt.legend(['Training Loss', 'Training Accuracy'])
plt.xlabel('Epoch')
plt.ylabel('Percent')
plt.show()

eval_result = model.evaluate(x_test, y_test, verbose=1)
print(f"Evaluation Result: {eval_result}")

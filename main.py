import tensorflow as tf
import tensorflow_hub as hub
import numpy as np

def main():

    video_rgb_features = np.load("test_rgb.npy")

    # inputs_frames must be normalized in [0, 1] and of the shape Batch x T x H x W x 3
    input_frames = tf.placeholder(tf.float32, shape=(None, None, None, None, 3))
    # inputs_words are just a list of sentences (i.e. ['the sky is blue', 'someone cutting an apple'])
    input_words = tf.placeholder(tf.string, shape=(None,))

    module = hub.Module("https://tfhub.dev/deepmind/mil-nce/s3d/1")

    vision_output = module(input_frames, signature='video', as_dict=True)
    text_output = module(input_words, signature='text', as_dict=True)

    video_embedding = vision_output['video_embedding']
    text_embedding = text_output['text_embedding']
    # We compute all the pairwise similarity scores between video and text.
    similarity_matrix = tf.matmul(text_embedding, video_embedding, transpose_b=True)

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())

        sess.run(tf.tables_initializer())

        print(sess.run([similarity_matrix], feed_dict={input_words: ['the sky is blue'], input_frames: video_rgb_features}))


if __name__ == "__main__":
    main()
#rephrase

##Introduction
Can we determine the topic of a song based on sound alone?

We start with two assumptions:
 - If a song has lyrics, the lyrics tell you what the song is about.
 - Songs that sound similar may also be about similar things.

###Objective:
Use songs with lyrics to predict the topic of songs without lyrics

##Data
Million Song Dataset - sound features and metadata for a million modern songs

musiXmatch Dataset - lyric data in bag-of-word format for ~237,000 songs in MSD

##Pipeline
The pipeline is divided in two parts:

  1.) LDA Topic Modeling
        First, we apply topic modeling to the lyric data to discover latent topics in music.
        Then we label our songs with their predicted topic.

  2.) Boosted Trees Classifier
        We pass our classifier features that quantify sound:
            - Tempo
            - Pitch
            - Timbre
            - Loudness
            - Duration
            - Key
        We use these features to predict the topic of our songs found from LDA.

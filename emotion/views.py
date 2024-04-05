from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from deepface import DeepFace
import cv2
from django.db import transaction
import threading
from django.http import JsonResponse
from time import sleep
import os
import base64
from django.core.files.base import ContentFile

def result(request, detected_emotion):
    return render(request, 'emotion/result.html', {'detected_emotion': detected_emotion})
@login_required
def detect_emotion(request):
    if request.method == 'POST':
        form = EmotionDetectionForm(request.POST, request.FILES)
        if form.is_valid():
            image_data = form.cleaned_data['image']
            
            emotion_record = EmotionRecord(user=request.user, image=image_data)
            emotion_record.save()

            thread1 = threading.Thread(target=emotion_recognition, args=(emotion_record,))
            thread1.start()
            thread1.join()
        return render(request, 'emotion/result.html', {'detected_emotion': emotion_record.emotion_level})
    else:
        form = EmotionDetectionForm()

    return render(request, 'emotion/detect_emotion.html', {'form': form})

# total rewrite of the code here
def emotion_recognition(emotion_record):
    
    model = DeepFace.build_model("Emotion")

    emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    image_path = emotion_record.image.path

    frame = cv2.imread(image_path)

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    print(f"Number of faces detected: {len(faces)}")
    for (x, y, w, h) in faces:
        face_roi = gray_frame[y:y + h, x:x + w]
        print("11111111")
        resized_face = cv2.resize(face_roi, (48, 48), interpolation=cv2.INTER_AREA)
        print("2222222222")
        normalized_face = resized_face / 255.0
        print("33333333333333333")
        reshaped_face = normalized_face.reshape(1, 48, 48, 1)
        print("4444444444444444")
        preds = model.predict(reshaped_face)[0]
        print("55555555555555")
        emotion_idx = preds.argmax()
        print("66666666666666")
        detected_emotion = emotion_labels[emotion_idx]

        print(f"Detected emotion: {detected_emotion}")  

        emotion_record.emotion_level = detected_emotion

        if detected_emotion == "sad":
            
           notify_counselor(emotion_record)
           print(f"been there")


        emotion_record.save()

        print(f"Saved emotion: {emotion_record.emotion_level}")  

    cv2.destroyAllWindows()

@login_required
def start_live_emotion_detection(request):
    emotion_record = EmotionRecord(user=request.user)
    emotion_record.save()

    setattr(emotion_record, 'live_emotion_detection', True)

    thread1 = threading.Thread(target=emotion_recognition, args=(emotion_record,))
    thread1.start()

    return render(request, 'emotion/live_emotion_feed.html', {'emotion_record_id': emotion_record.id})

@login_required
def stop_live_emotion_detection(request, emotion_record_id):
    emotion_record = EmotionRecord.objects.get(id=emotion_record_id)

    setattr(emotion_record, 'live_emotion_detection', False)
    emotion_record.save()

    return redirect('detect_emotion')


def get_random_counselor():
    return CustomUser.objects.filter(role='counselor').first()




def get_emotion_level(emotion):
    
    if emotion in ['happy', 'neutral', 'surprise']:
        return 1  
    elif emotion in ['sad', 'angry', 'disgust', 'fear']:
        return 3  
    else:
        return 2

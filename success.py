def done(message="Success!"):
    from playsound import playsound
    if message != None:
        print(f"\n{message}")
    playsound(
        r'D:\OneDrive - CARNET\Documents\INFORMATIKA\PYTHON\VSA\autoscript\sound.mp3')

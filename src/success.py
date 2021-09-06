def done(message="Success!"):
    import winsound
    if message != None:
        print(f"\n{message}")
    winsound.PlaySound(r"src/sound.wav", winsound.SND_FILENAME)

import ollama

MODEL = "llama3"

def gen(txt):
    return ollama.generate(prompt=txt, model=MODEL)["response"]

if __name__ == "__main__":
    print(gen("Format this .csv file into notes with a summary."))
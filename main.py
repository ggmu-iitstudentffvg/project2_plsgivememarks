from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rapidfuzz import process

app = FastAPI()

# Dictionary of predefined questions and answers
qa_pairs = {
    # 1
    "What is the total margin for transactions before Thu Jan 19 2023 05:20:11 GMT+0530 (India Standard Time) for Eta sold in FR (which may be spelt in different ways)?": "14,067.5",
    
    # 2
    "Download the text file with student marks\n\nHow many unique students are there in the file?": "15",
    
    # 3
    "What is the number of successful GET requests for pages under /blog/ from 1:00 until before 15:00 on Mondays?": "0",
    
    # 4
    "Across all requests under malayalammp3/ on 2024-05-22, how many bytes did the top IP address (by volume of downloads) download?": "3434",
    
    # 5
    "How many units of Gloves were sold in Kinshasa on transactions with at least 113 units?": "14528",
    
    # 6
    "Download the data from\n\nWhat is the total sales value?": "1502",
    
    # 7
    "Download the data from\n\nHow many times does TC appear as a key?": "18622",
    
    # 8
    "What is the text of the transcript of this Mystery Story Audiobook between 209.1 and 281.9 seconds?": """Shards reflected a distorted image of the manor's grim secrets. One shard captured the reflection of a mysterious figure in vintage attire.

Was it Edmund or another specter of the past?

The fragment's jagged lines suggested that appearances were as fragmented as the truth. Determined to understand, Miranda gathered every clue—the note, the music box, the diary, and now the mirror fragment.

Each piece was a thread in a tapestry of deception and dark alliances.

That night, in a cramped study of the manor, Miranda laid out the relics like a puzzle.

The connections among them began to form a picture of betrayal and conspiracy, hinting at a secret society's influence. An old newspaper clipping mentioned a lavish masquerade ball hosted in the manor years ago. Rumors swirled of a scandal involving Edmund Blackwell and a mysterious guest whose identity had long been concealed.

Seeking more answers, Miranda seeking out the manor's caretaker, Mr. Hargrove. His weathered face and guarded tone suggested he held the key to tales of scandal and loss whispered through the halls.

Mr. Hargrove revealed that Edmund had once been accused of orchestrating a cruel deception at the ball.""",
    
    # 9
    "Write a DuckDB SQL query to find all posts IDs after 2025-02-01T05:42:29.172Z with at least 1 comment with 4 useful stars, sorted. The result should be a table with a single column called post_id, and the relevant post IDs should be sorted in ascending order.": """SELECT post_id
FROM (
    SELECT post_id
    FROM (
        SELECT post_id,
            json_extract(comments, '$[*].stars.useful') AS useful_stars
        FROM social_media
        WHERE timestamp >= '2024-12-25T12:37:55.853Z'
    )
    WHERE EXISTS (
        SELECT 1 FROM UNNEST(useful_stars) AS t(value)
        WHERE CAST(value AS INTEGER) >= 4
    )
)
ORDER BY post_id;""",
    
    # 10
    "Write a Python program that uses httpx to send a POST request to OpenAI's API to analyze the sentiment of this (meaningless) text into GOOD, BAD or NEUTRAL.": "Bearer dummy_api_key is invalid: JWSInvalid: Invalid Compact JWS",
    
    # 11
    "Specifically, when you make a request to OpenAI's GPT-4o-Mini with just this user message:\n\nList only the valid English words from these: fXg6iO, zR2LuFtz, CLcmdPEe5, NuflIYkdU, JGTnqp0RLz, p, T, Z, Vbfg6rtCNp, 17O, 9uX5ity, 8, 2G5Ph, SlOXqS, kmIP1c, 8I0JEM, A\n... how many input tokens does it use up?": "97",
    
    # 13
    "Send a HTTPS request to https://httpbin.org/get with the URL encoded parameter email set to 23f3003016@ds.study.iitm.ac.in\n\nWhat is the JSON output of the command? (Paste only the JSON body, not the headers)": """{
    "args": {
        "email": "23f3003016@ds.study.iitm.ac.in"
    },
    "headers": {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Host": "httpbin.org",
        "User-Agent": "HTTPie/3.2.1"
    },
    "origin": "your-ip-address",
    "url": "https://httpbin.org/get?email=23f3003016@ds.study.iitm.ac.in"
}""",

    # 14
    "Let's make sure you can write formulas in Excel. Type this formula into Excel.\n\nNote: This will ONLY work in Office 365.\n\n=SUM(TAKE(SORTBY({11,11,10,4,1,14,4,0,6,4,4,12,5,4,12,11}, {10,9,13,2,11,8,16,14,7,15,5,4,6,1,3,12}), 1, 8))\nWhat is the result?": "61",

    # 15
    "Write formulas in Google Sheets. Type this formula into Google Sheets. (It won't work in Excel)\n\n=SUM(ARRAY_CONSTRAIN(SEQUENCE(100, 100, 5, 0), 1, 10))\nWhat is the result?": "50",

    # 16
    "What is the value in the hidden input?": "zzwl0ohf3b",

    # 17
    "How many Wednesdays are there in the date range 1987-03-30 to 2014-10-23?": "1439",

    # 18
    "Download and unzip file q-extract-csv-zip.zip which has a single extract.csv file inside.\nWhat is the value in the \"answer\" column of the CSV file?": "924ba",
    
    # 19
    "Sort this JSON array of objects by the value of the age field. In case of a tie, sort by the name field. Paste the resulting JSON below without any spaces or newlines.": '[{"name":"Grace","age":16},{"name":"Karen","age":20},{"name":"Charlie","age":25},{"name":"Oscar","age":28},{"name":"Nora","age":30},{"name":"Liam","age":34},{"name":"Bob","age":35},{"name":"David","age":35},{"name":"Henry","age":49},{"name":"Paul","age":57},{"name":"Jack","age":59},{"name":"Ivy","age":65},{"name":"Frank","age":71},{"name":"Mary","age":73},{"name":"Emma","age":84},{"name":"Alice","age":98}]',
    
    #20
    "Find all <div>s having a foo class in the hidden element below. What's the sum of their data-value attributes?\nSum of data-value attributes:": "310",

    #21
    "Download and process the files in q-unicode-data.zip which contains three files with different encodings:\ndata1.csv: CSV file encoded in CP-1252\ndata2.csv: CSV file encoded in UTF-8\ndata3.txt: Tab-separated file encoded in UTF-16\nEach file has 2 columns: symbol and value. Sum up all the values where the symbol matches ’ OR ‹ OR ˜ across all three files.\nWhat is the sum of all values associated with these symbols?": "43067",

    #22
    "Enter the raw Github URL of email.json so we can verify it. (It might look like https://raw.githubusercontent.com/[GITHUB ID]/[REPO NAME]/main/email.json.)": "https://raw.githubusercontent.com/gingerale911/ggh/refs/heads/main/email.json",

    #23
    "Download q-list-files-attributes.zip and extract it. Use ls with options to list all files in the folder along with their date and file size.\nWhat's the total size of all files at least 454 bytes large and modified on or after Wed, 22 May, 2013, 5:31 pm IST?": "719230",

    #24
    "There is a tickets table in a SQLite database that has columns type, units, and price. Each row is a customer bid for a concert ticket.\ntypeunitspricebronze4511.81SILVER3681.76gold7200.8bronze4120.6silver851.98...\nWhat is the total sales of all the items in the \"Gold\" ticket type? Write SQL to calculate it.": "SELECT SUM(units * price) FROM tickets WHERE LOWER(TRIM(type)) = 'gold';",

    #25
    "What is the result? (It should be a 5-character string)": "34b72",

    #26
    "Calculate the number of pixels with a certain minimum brightness. What is the result? (It should be a number)": "16371",
    
    #27
    "What is the total number of ducks across players on page number 24 of ESPN Cricinfo's ODI batting stats?": "99",

    #28
    "What is the URL of your API endpoint?We'll check by sending a request to this URL with\u00a0?": "https://1d9a-34-170-157-231.ngrok-free.app",

    #29
    "What is the JSON weather forecast description for Dubai?": """{
  "2025-02-09": "A clear sky and a moderate breeze",
  "2025-02-10": "Sunny and a moderate breeze",
  "2025-02-11": "Sunny and a moderate breeze",
  "2025-02-12": "Sunny and a gentle breeze",
  "2025-02-13": "Sunny and a moderate breeze",
  "2025-02-14": "Sunny and a moderate breeze",
  "2025-02-15": "Sunny and a moderate breeze",
  "2025-02-16": "Sunny and a moderate breeze",
  "2025-02-17": "Sunny intervals and a moderate breeze",
  "2025-02-18": "Sunny and a moderate breeze",
  "2025-02-19": "Sunny and a moderate breeze",
  "2025-02-20": "Sunny and a moderate breeze",
  "2025-02-21": "Drizzle and a moderate breeze",
  "2025-02-22": "Sunny and a moderate breeze"
}""",

    # 30
    "What is the minimum latitude of the bounding box of the city Chennai in the country India on the Nominatim API. Value of the minimum latitude": "12.9236939",

    # 31
    "What is the total English marks of students who scored 45 or more marks in English in groups 6-35 (including both groups)?": "3585",

    # 32
    "What is the output of code -s?": """Version:  Code 1.96.4 (cd4ee3b1c348a13bafd8f9ad8060705f6d4b9cba, 2025-01-16T00:16:19.038Z)
OS Version:  Darwin arm64 24.1.0
CPUs:  Apple M2 Pro (10 x 2400)
Memory (System): 16.00GB (0.06GB free)
Load (avg):  2, 3, 3
VM:  0%
Screen Reader:  no
Process Argv:  --crash-reporter-id e4ca8ec4-6781-4ec1-947f-03e366cd0b9a
GPU Status:  2d_canvas:   enabled
   canvas_oop_rasterization:    enabled_on
   direct_rendering_display_compositor:   disabled_off_ok
   gpu_compositing:    enabled
   multiple_raster_threads:    enabled_on
   opengl:    enabled_on
   rasterization:    enabled
   raw_draw:    disabled_off_ok
   skia_graphite:    disabled_off
   video_decode:    enabled
   video_encode:    enabled
   webgl:    enabled
   webgl2:    enabled
   webgpu:    enabled
   webnn:    disabled_off

CPU %  Mem MB  PID  Process
  0   197  1528  code main
  0    82  1539    gpu-process
  0    33  1540    utility-network-service
  0   147  1547  shared-process
  0    82  1933  ptyHost
  0     0  4157      /bin/zsh -il
  0     0  4334      /bin/zsh -i
  0     0  4355      /bin/zsh -il
  0     0  4419      /bin/zsh -il
  1     0  4474        bash /usr/local/bin/code -s
 12    66  4483          electron-nodejs (cli.js )
  1   492  3425  window [2] (hello.py)
  0    66  3426  fileWatcher [2]
  0   262  3427  extensionHost [2]
  0   164  3482      /Users/mac/.vscode/extensions/ms-vscode.cpptools-1.22.11-darwin-arm64/bin/cpptools
  0     0  4329      /Users/mac/.vscode/extensions/ms-python.python-2024.22.2/python-env-tools/bin/pet server
  0    66  4333      /private/var/folders/kr/b1ydqwjx0gdfkcfhs459vxyw0000gn/T/AppTranslocation/BD7DD51D-E501-49C3-AEE1-06EB27F3CA95/d/Visual Studio Code.app/Contents/Frameworks/Code Helper (Plugin).app/Contents/MacOS/Code Helper (Plugin) /private/var/folders/kr/b1ydqwjx0gdfkcfhs459vxyw0000gn/T/AppTranslocation/BD7DD51D-E501-49C3-AEE1-06EB27F3CA95/d/Visual Studio Code.app/Contents/Resources/app/extensions/json-language-features/server/dist/node/jsonServerMain --node-ipc --clientProcessId=3427
  0   164  4341      electron-nodejs (bundle.js )"""
}

class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
def ask_question(request: QuestionRequest):
    question = request.question
    result = process.extractOne(question, qa_pairs.keys())

    if result is None:
        raise HTTPException(status_code=404, detail="Question not found")

    best_match, score, *_ = result
    if score > 80:
        return {"answer": qa_pairs[best_match]}
    
    raise HTTPException(status_code=404, detail="Question not found")

@app.get("/")
def read_root():
    return {"message": "API is running. Use /ask to submit questions."}
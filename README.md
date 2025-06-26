This is a PDP Grader that uses ChatGPT.

Run app.py and follow the link that it gives to the webpage.

Enter a url. The program will scrape the webpage, give the content to ChatGPT, and ChatGPT will grade it and return a result.

You need to set an environment variable that contains an OpenAI API key to actually run the grader.
To do this, in the terminal, type $env:OPENAI_API_KEY = "YOUR API KEY"

If you don't have a working API key, you can still test and adjust things on the webpage. (webpage files are in the folder "templates")
Go to "original link/test-analysis" to test the analysis page. Ex: if my original link was 142.0.0.1, go to 142.0.0.1/test-analysis


For debugging:
The analyses from ChatGPT are stored in .json files and are in the folder "analysis_result"s".
The scraped webpage content is stored in the folder "extracted_text".

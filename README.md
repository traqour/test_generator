# Textbook Expert and Practice Test Generator App

An application that allows you to ingest a PDF of a textbook and leverage the content to generate an interactive query system and create practice tests. This app utilizes Llama-Index and UnstructuredReader to understand and extract knowledge from the textbook.

Link to show an example test created based on the CompTIA Network+ Exam textbook (IT certification test):

CompTIA® Network+ Exam Cram, Third Edition

ISBN-13: 978-0-7897-3796-0

ISBN-10: 0-7897-3796-5

 https://youtu.be/ocFLl9EpLAU

## Features

- **Textbook Ingestion:** Upload a PDF of the textbook you want to analyze and gain insights from.

- **Expert Query System:** The app processes the textbook's content to create an expert query system but requires some manual insertion of regex patterns to find chapter starts and endings depending on the format of your textbook. You can ask questions related to the textbook, and the app will provide accurate and relevant answers.

- **Practice Test Generation:** The app can generate practice tests based on the textbook's content.


## Install Dependencies

pip install -r requirements.txt

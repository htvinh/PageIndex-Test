# Testing with Sample Documents

This guide explains how to use your own sample documents for testing the application's RAG and Vision RAG pipelines.

## 📁 1. Use the Input Directory
The application is designed to work with documents you provide. You can maintain a library of test documents in the `input/` folder located in the project root.

1.  **Locate the directory:** Navigate to the `PageIndex-Test/input/` folder.
2.  **Add PDFs:** Place any PDF files you wish to test into this folder.

## 🚀 2. Testing Process

Since the application now requires you to upload documents manually (enforcing a clean, local-only workflow), you can use the files in your `input/` folder as follows:

1.  **Launch the app:** Run `./scripts/launch.sh`.
2.  **Navigate to a demo:** Go to either the **Simple RAG** or **Vision RAG** tab.
3.  **Upload:** Click the "Choose a PDF file" button and select the document from the `input/` folder (or anywhere else on your machine).
4.  **Process:** Click **"Process Document"** to trigger local text extraction and tree generation.

## 💡 Tips for Effective Testing

- **Keep Documents Small:** For faster processing, test with documents under 10 pages.
- **Visual Diversity:** For the **Vision RAG** demo, choose PDFs that contain diagrams, charts, or complex layouts to fully utilize the vision capabilities of your VLM.
- **Consistent Testing:** By keeping your primary test set in the `input/` folder, you can quickly upload them whenever you restart the application.

## 🛠️ Batch Processing (Advanced)
If you need to process many documents, you can add them to the `input/` folder and use the application's UI to process them one-by-one. Each document will be assigned a unique local ID and stored in `_local_storage/` until the application is reset.

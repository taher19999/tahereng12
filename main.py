import PyPDF2
import os
import telegram
from telegram.ext import Updater, CommandHandler


# Define the Telegram bot token
TOKEN = '6160836592:AAHfpPxpudcvCyT68zJmhAP4U8uzfrKtbUY'

# Define the command handler for the /combinepdf command
def combine_pdf(update, context):
    # Get the list of PDF file IDs from the user's message
    pdf_ids = update.message.text.split()[1:]
    
    # Download the PDF files and combine them
    pdf_paths = []
    for pdf_id in pdf_ids:
        # Download the PDF file from Telegram
        file_obj = context.bot.get_file(pdf_id)
        file_path = os.path.join(os.getcwd(), 'downloads', pdf_id + '.pdf')
        file_obj.download(file_path)
        # Add the PDF file to the list of PDF paths
        pdf_paths.append(file_path)
    
    # Create a new PDF file to write the combined PDFs to
    output_pdf = PyPDF2.PdfFileWriter()

    # Loop through each PDF file and add its pages to the output PDF
    for pdf_path in pdf_paths:
        # Open the PDF file
        with open(pdf_path, 'rb') as pdf_file:
            # Read the PDF file using PyPDF2
            pdf_reader = PyPDF2.PdfFileReader(pdf_file)
            # Loop through each page of the PDF file and add it to the output PDF
            for page_num in range(pdf_reader.getNumPages()):
                page = pdf_reader.getPage(page_num)
                output_pdf.addPage(page)

    # Write the combined PDF to a new file
    output_file_path = os.path.join(os.getcwd(), 'downloads', 'combined.pdf')
    with open(output_file_path, 'wb') as output_file:
        output_pdf.write(output_file)

    # Send the combined PDF file to the user
    context.bot.send_document(chat_id=update.message.chat_id, document=open(output_file_path, 'rb'))

# Set up the Telegram bot
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Add the command handler for the /combinepdf command
combine_pdf_handler = CommandHandler('combinepdf', combine_pdf)
dispatcher.add_handler(combine_pdf_handler)

# Start the bot
updater.start_polling()

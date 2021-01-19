#! python3

import PyPDF2, os, sys, logging

class PdfManager (): 
    """
    Manage pdf files: merge, split convert pdff to img or convert img to pdfi
    """

    def __init__ (self, input_files = "", replace = False, debug = False):
        """
        Constructor of class. Generate empty list of files an get dir path and file ouput
        """

        # Debug configuration
        logging.basicConfig( level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s' )
        if not debug: 
            logging.disable()


        self.pdfFiles = []
        self.imgFiles = []
        self.input_files = input_files
        self.output_file = ""
        
        self.replace = replace

        self.list_extensions = ["pdf", "jpg"]


        self.__verify_files()


    def __verify_files (self):
        """
        Varify that the files already exist in the local storage
        """

        # Convert only element to list 
        if type(self.input_files) == str: 
            file = self.input_files
            self.input_files = []
            self.input_files.append (file)

        # Loop for each file
        for file in self.input_files: 
            
            # No found error
            if not os.path.isfile (file): 
                raise FileNotFoundError (file)

    def __verify_extension_input_files (self, pdf, function_name): 
        """ 
        Validate the extension of each file
        """

        # Generate a local list of extensions
        if pdf: 
            list_extensions = ["pdf"]
        else: 
            list_extensions = self.list_extensions.remove ("pdf")


        # Loop for each file
        for file in self.input_files: 
            
            # Extension error
            extension_index = file.rfind (".")
            extension = file [extension_index + 1 :]

            if extension not in list_extensions: 
                raise AttributeError ("'{}'. \
                    \nFunction {} doesn't support the extension: '{}'" \
                    .format (file, function_name, extension))

    def __verify_outputh_file (self, file, default_name, extension): 
        """
        Verify the name of the output file and if the file will be replace or not
        """

        # verify path and make file name
        if os.path.isdir (file): 
            self.output_file = os.path.join(file, default_name + extension)
        else:
            if file.endswith(extension): 
                self.output_file = file
            else: 
                self.output_file = file + extension

        # Verify replace outputh file
        if os.path.isfile (self.output_file):
            if self.replace: 
                logging.debug ("Replacing file")
            else: 
                message = 'File "{}" already exist'.format (self.output_file)
                raise ValueError(message)

    def merge (self, merged_file): 
        """
        Merge a specific list of pdf files inside the output file
        """

        self.__verify_extension_input_files (pdf=True, function_name = "merge")

        self.__verify_outputh_file (merged_file, "merged_file", ".pdf")

        
        pdfWriter = PyPDF2.PdfFileWriter()

        # loop through all the pdf files
        if self.input_files: 
            for currentFile in self.input_files: 
                pdfFileObj = open (currentFile, 'rb')
                pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
                
                logging.debug ("Merging {}... ".format (currentFile))

                # loop through all the pages (except the first) and add them
                if pdfReader.numPages: 
                    for pageNum in range (0, pdfReader.numPages): 
                        pageObj = pdfReader.getPage(pageNum)
                        pdfWriter.addPage (pageObj)            
            
            # Save the resulting pdf to a file
            pdfOutput = open (self.output_file, 'wb')
            pdfWriter.write(pdfOutput)
            pdfOutput.close()

            logging.debug ('Done. Pages are now in "{}".'.format (os.path.basename(self.output_file)))
        else: 
            logging.debug ("List of files empty.")

    def split (self, split_base_name = " - split -"): 
        """
        Merge a specific list of pdf files inside the output file
        """

        self.__verify_extension_input_files (pdf=True, function_name = "merge")
        

        # loop through all the pdf files
        if self.input_files: 
            for currentFile in self.input_files: 
                pdfFileObj = open (currentFile, 'rb')
                pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
                
                logging.debug ("Merging {}... ".format (currentFile))

                # loop through all the pages (except the first) and add them
                if pdfReader.numPages: 
                    for pageNum in range (0, pdfReader.numPages): 

                        # Save page of file, as new pdf file
                        pdfWriter = PyPDF2.PdfFileWriter()
                        pageObj = pdfReader.getPage(pageNum)
                        pdfWriter.addPage (pageObj)            

                        # Save file
                        file_name = currentFile[:-4] + "{} {}.{}".format (split_base_name, str(pageNum + 1), ".pdf")
                        self.__verify_outputh_file (file_name, "", ".pdf") 
                        pdfOutput = open (self.output_file, 'wb')
                        pdfWriter.write(pdfOutput)
                        pdfOutput.close()

                        logging.debug ('Done. File "{}" generated.'.format (file_name))
                else: 
                    logging.debug ('File "{}" has not pages.'.format (file_name))

        else: 
            logging.debug ("List of files empty.")






    
    # def merge_folder (self, folder):
    #     """
    #     Merge all files from a specific folder and save inside the output file
    #     """

    #     # Verify is folder exist
    #     if not os.path.isdir (folder): 
    #         raise FileNotFoundError(folder)
        
    #     # Get files
    #     for filename in os.listdir(folder):
    #         if filename.endswith('.pdf'): 
    #             self.pdfFiles.append(os.path.join(folder, filename))
        
    #     # Order files
    #     self.pdfFiles.sort(key = str.lower)

    #     self.__make_merge()
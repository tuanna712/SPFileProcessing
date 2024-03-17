import fitz
import uuid
from uuid import UUID
from .document import PdfDocument
from .document import Image, Table, Text
from fitz import Rect, Point, IRect
from fitz import Pixmap
import os
from typing import List, Tuple

# STATIC VARIABLES
CAPTION_START_WORDS = ['figure', 'image', 'ảnh', 'minh', 'hình', 'picture', 'bảng', 'fig', 'summary', 'table']

ROOT = os.getcwd() + '/data/temp'
# while os.path.split(ROOT)[-1] != "epdatabase":
#     print(os.path.split(ROOT)[-1])
#     ROOT = os.path.dirname(ROOT)


# STATIC METHODS
def _check_valid_caption(text: str) -> bool:
    """
    Helper function to check if a text starts with valid caption convention
    such as 'figure', 'image', 'anh', 'minh hoa', 'hinh', ...
    Args:
        text (str)

    Returns:
        bool: True if this text is valid caption, and False otherwise.
    """
    if not text:
        return False
    #Get the first word of the text
    text = text.strip().lower().split()[0]
    #If the first word of the text is in the list of valid caption start words, return True
    return any(text == i for i in CAPTION_START_WORDS)


def check_split_image(rect1: Rect,
                      rect2: Rect) -> bool:
    """
    Helper function to check if two images are actually split parts of one large image.
    Args:
        rect1 (Rect): Rectangle bound of image 1
        rect2 (Rect): Rectangle bound of image 2

    Returns:
        bool: True if the images are join-able, or false otherwise.
    """

    #Define a threshold (in distance between two images' edges)
    eps = 20
    #Check if the two images are join-able
    if abs(rect1.y1 - rect2.y0) < eps or \
            abs(rect1.x1 - rect2.x0) < eps or \
            abs(rect1.x0 - rect2.x1) < eps or \
            abs(rect1.y0 - rect2.y1) < eps or \
            rect1.intersects(rect2):
        return True
    else:
        # Use these to debug
        # print("x1 - x0: {} - {} = {}".format(rect1.x1, rect2.x0, rect1.x1 - rect2.x0))
        # print("x0 - x1: {} - {} = {}".format(rect1.x0, rect2.x1, rect1.x0 - rect2.x1))
        # print("y0 - y1: {} - {} = {}".format(rect1.y0, rect2.y1, rect1.y0 - rect2.y1))
        # print("y1 - y0: {} - {} = {}".format(rect1.y1, rect2.y0, rect1.y1 - rect2.y0))
        return False


def join_rects(join_list: list) -> Rect:
    """
    Helper function to join list of Rects into one large Rect
    Args:
        join_list: list of Rects

    Returns:
        large_rect: Rectangle object
    """
    #Initiate the list of x and y coordinates
    x = []
    y = []

    #Loop through all Rects in the join list, and append their x and y coordinates to the x and y lists
    for rect in join_list:
        x.append(rect.x0)
        x.append(rect.x1)
        y.append(rect.y0)
        y.append(rect.y1)
    
    #Return a large rectangle that contains all the Rects in the join list
    return Rect(min(x), min(y), max(x), max(y))


def download_image(pixmap: Pixmap,
                   rect: Rect,
                   username: str,
                   id: UUID) -> str:
    """
    Function to download image within a bound.
    Args:
        pixmap (Pixmap): pixmap context
        rect (Rect): Rectangle bound for the image
        username: name of the user request
        id : UUID instance of the file
    """
    try:
        #Get the Imamge's corner coordinates as integers.
        i_rect = rect.irect
        #Create a new Pixmap object with the same width and height as the original Pixmap, but with the new corner coordinates.
        pix = Pixmap(pixmap, pixmap.width, pixmap.height, i_rect)
        #Create a new path to save the new Pixmap
        saved_path = os.path.join(ROOT, "usercontent", username, "{}.png".format(str(id)))
        #Create a new directory if it doesn't exist
        os.makedirs(os.path.dirname(saved_path), exist_ok=True)
        #Save the new Pixmap
        pix.save(saved_path)
        #Return the path of the saved Pixmap
        return saved_path
    except AttributeError as e:
        print(e)
        pass


def _get_all_images_rects_on_one_page(image_list: list,
                                      page: fitz.Page) -> list:
    """
    Helper function to find split image fragments and join them.
    Args:
        image_list (list): List of images in one page.
        page (fitz.Page): a fitz.Page document

    Returns:
        list: list of Rects represent joined images.
    """

    #Initiate the list of Rects (images to extract)
    rect_list = []
    #Index of Image in page
    img_idx = 0
    #Index of Image in the loop
    idx = 0

    #Loop through all images in the page
    while img_idx in range(0, len(image_list)) and len(image_list) > 1:
        #Get the first image
        rect1 = page.get_image_rects(image_list[img_idx])[0]
        #Get the second image
        rect2 = page.get_image_rects(image_list[img_idx + 1])[0]
        #Set the first image as the first element of the join list
        join_list = [rect1]

        #Check if the two images are joinable
        while check_split_image(rect1, rect2):
            #If True, add the second image to the join list
            join_list.append(rect2)

            #Increment the index
            idx += 1
            #If the index is greater than the length of the image list, break the loop
            if idx >= len(image_list) - 1:
                break

            #Get the next image
            rect1 = page.get_image_rects(image_list[idx])[0]
            #Get the next second image
            rect2 = page.get_image_rects(image_list[idx + 1])[0]

        #Join the images in the join list by expanding the join list to a large rectangle
        large_rect = join_rects(join_list)

        #Append the large rectangle to the list of rectangles (independent images)
        rect_list.append(large_rect)

        #Increment the index
        idx += 1
        img_idx = idx

        #If the index is greater than the length of the image list, break the loop
        if img_idx >= len(image_list) - 1:
            break

    #If there is only one image in the page, append the rectangle of the image to the list of rectangles
    if len(image_list) == 1:
        rect_list.append(page.get_image_rects(image_list[0])[0])
    #If there is no image in the page, return the list of rectangles (empty list)
    elif len(image_list) == 0:
        return rect_list
    
    return rect_list


class PdfExtractor:
    """
    A class for extracting from PDF file.


    Attributes
    -----------
    file_name : str.
        link to the pdf file.
    pdf_file : fitz.Document
        a fitz.Document object to interact with pdf file.
    document : Document object.
        Document object.

    Methods
    -------
    get_caption(rect, page_index)
        Get the caption of a specific image in a page.

    """

    # DEFAULT INDEXES FOR TEXT BLOCK
    TEXT_BLOCK_X0 = 0 #X coordinate of the text block
    TEXT_BLOCK_Y0 = 1 #Y coordinate of the text block
    TEXT_BLOCK_X1 = 2 #X1 coordinate of the text block
    TEXT_BLOCK_Y1 = 3 #Y1 coordinate of the text block
    TEXT_BLOCK_CAPTION = 4 #Text content of the text block

    def __init__(self,
                 file_path: str,
                 file_uuid: str):
        """
        Parameters:
            file_path (str): link to a file.

        """

        # Get the file path and file name
        dir_path, self.file_name = os.path.split(file_path)
        # Get the file extension
        __, ext = os.path.splitext(self.file_name)
        # Generate an UUID for the filename
        temp_id = file_uuid #uuid.uuid4()
        # Create a new file path with file name = the UUID
        new_file_path = os.path.join(dir_path, f"{str(temp_id)}{ext}")
        # Rename the file
        os.rename(file_path, new_file_path)

        # Update new file path property
        self.file_path = new_file_path

        # Get file using fitz
        self.pdf_file = fitz.open(self.file_path)
        # Read document
        self.document = PdfDocument(temp_id, self.file_name, self)
        # Update document properties
        self.document.properties.update(self.get_file_info())

    def get_file_info(self):
        return {
            "file_name": self.file_name,
            "file_ext": self.file_name.split('.')[-1],
            "file_size": os.path.getsize(self.file_path),
            "file_pages": self.pdf_file.page_count,
            "file_metadata": self.pdf_file.metadata,
            "file_path": self.file_path,
        }

    def download(self, username: str):
        """
        Function to download all images, tables and text to local server.
        If PDF Document hasn't been process, this method will throw an exception.
        Args:
            username: name of the user request
        """

        if not self.document.is_extracted:
            raise Exception("PdfDocument has not been extracted.")

        for image in self.document.get_images():
            print("Processing image:", image.id)
            pixmap = self.pdf_file[image.page - 1].get_pixmap()
            download_image(pixmap, image.rect, username, image.id)
            print("Image downloaded: {}".format(image.id))

        for table in self.document.get_tables():
            pixmap = self.pdf_file[table.page - 1].get_pixmap()
            download_image(pixmap, table.rect, username, table.id)
            print("Table downloaded: {}".format(table.id))
        self.document.is_downloaded = True

    def extract(self) -> PdfDocument:
        """
        Extract all information, images, tables, and text.

        Returns:
            document: instance of PdfDocument class after extracting.
        """
        print("strart extracting")
        print("strart image extracting")
        self.extract_images()
        print("strart table extracting")
        self.extract_tables()
        print("strart text extracting")
        self.extract_text()
        self.document.is_extracted = True
        print("Extracted")
        return self.document

    def extract_images(self) -> List[Image]:
        """
        Core function to extract images in a PDF file.
        For each image extracted, this function create an Image object 
        and append to image list in Document.

        Returns:
            List[Image]: list of images in document
        """

        # Go through all pages.
        for page_idx in range(0, len(self.pdf_file)):
            # Get page by page number
            page = self.pdf_file[page_idx]
            # Initiate pixmap
            image_list = page.get_images()
            all_rect_list = _get_all_images_rects_on_one_page(image_list, page)

            rect_list = []
            for rect in all_rect_list:
                if rect.height > 100:
                    rect_list.append(rect)

            # print("Page: {}".format(page_idx + 1))
            # print(rect_list)
            # Go through all rect in the page.
            for rect in rect_list:
                caption = self.get_caption(rect, page_idx)
                # print('Processing image:', caption)
                image = Image(uuid=uuid.uuid4(),
                              caption=caption,
                              page=page_idx + 1,
                              parent_id=self.document.id
                              )
                image.set_rect(rect)
                # Append image into image list in Document object.
                self.document.add_image(image)
        return self.document.images

    def _check_text_inside_image(self,
                                 rect: Rect,
                                 text_block: list) -> bool:
        """
        Helper function to check if a text box is inside an image or a table.

        Args:
            rect (Rect): fitz.Rectangle bound of the image or table.
            text_block (list): a list representation of text block.

        Returns:
            bool: True if the text is inside the image, and False otherwise.
        """

        text_rect = Rect(text_block[self.TEXT_BLOCK_X0],
                         text_block[self.TEXT_BLOCK_Y0],
                         text_block[self.TEXT_BLOCK_X1],
                         text_block[self.TEXT_BLOCK_Y1])
        return rect.contains(text_rect)

    def _get_closest_caption_block(self,
                                   rect: Rect,
                                   text_blocks: list) -> list:
        """
        Helper function to get the closest text block to the image.

        Args:
            rect (Rect): Rectangle bound of the image or table.
            text_blocks (list): list of text blocks

        Returns:
            list: nearest text block to the image represent by list
        """
        #Define the threshold for the distance between the image and the text block by Y coordinate
        eps_y = 80
        #Get the center position of the image
        image_center = Point(
            (rect.x0 + rect.x1) / 2,
            (rect.y0 + rect.y1) / 2
        )
        #Initiate the minimum distance and the index of the nearest text block
        min_distance = 1000.0


        min_idx = 0
        for idx, block in enumerate(text_blocks, start=0):
            if self._check_text_inside_image(rect, block):
                continue
            block_center = Point(
                (block[self.TEXT_BLOCK_X0]
                 + block[self.TEXT_BLOCK_X1]) / 2,
                (block[self.TEXT_BLOCK_Y0]
                 + block[self.TEXT_BLOCK_Y1]) / 2
            )
            distance = image_center.distance_to(block_center)
            if distance < min_distance:
                min_distance = distance
                min_idx = idx

        if rect.y0 - text_blocks[min_idx][self.TEXT_BLOCK_Y1] > eps_y or \
                text_blocks[min_idx][self.TEXT_BLOCK_Y0] - rect.y1 > eps_y:
            return None
        return text_blocks[min_idx]

    def _valid_caption(self, text_blocks) -> list:
        """
        Helper function to get valid captions from text blocks in a page.
        Args:
            text_blocks: all text blocks in one page

        Returns:
            list of valid caption blocks.
        """
        #Initiate the list of valid captions
        valid_captions = []

        #Loop through all text blocks in the page
        for block in text_blocks:
            #If the text block is a valid caption, append it to the list of valid captions
            if _check_valid_caption(block[self.TEXT_BLOCK_CAPTION]):
                valid_captions.append(block)
        
        #Return the list of valid captions
        if len(valid_captions) == 0:
            return None
        else:
            return valid_captions

    def get_caption(self,
                    img_rect: Rect,
                    page_idx: int) -> str:
        """
        Gets the caption of an image.

        Args:
            img_rect (Rect): Rect bound of the image.
            page_idx (int): page number.

        Returns:
            str: caption of the image.
        """
        #Get page by page number
        page = self.pdf_file[page_idx]
        #Get all text blocks in the page
        text_blocks = page.get_text('blocks')

        try:
            #Retrieve all text blocks has available valid caption
            text_blocks = self._valid_caption(text_blocks)
            #Get the closest caption block to the image
            block = self._get_closest_caption_block(img_rect, text_blocks)

            # Normalize captions
            caption = block[self.TEXT_BLOCK_CAPTION].replace('\n', '')
            caption = caption.replace(':', '.')
            caption = caption.replace('/', '_')
            return caption.strip()

        except Exception as e:
            # print("Exception:", e)
            pass

    def extract_tables(self):
        for page_idx in range(len(self.pdf_file) - 1):
            page = self.pdf_file[page_idx]
            try:
                # print("Page:", page_idx)
                table_list = page.find_tables()
                for table in table_list:
                    rect = Rect(table.bbox)
                    caption = self.get_caption(rect, page_idx)
                    # print("Processing table:", caption)
                    table = Table(uuid.uuid4(),
                                  caption,
                                  page_idx + 1,
                                  self.document.id)
                    table.set_rect(rect)
                    self.document.add_table(table)
            except Exception as e:
                print(e)
                pass
        return self.document.tables

    def extract_text(self):
        import re
        for page_idx in range(0, len(self.pdf_file)):
            page = self.pdf_file[page_idx]
            content = page.get_text()
            # Remove redundant whitespace and newline
            # text = re.sub(r'\s+', ' ', text).strip()
            text = Text(uuid.uuid4(),
                        content,
                        page_idx + 1,
                        self.document.id)
            self.document.add_text(text)

        return self.document.text

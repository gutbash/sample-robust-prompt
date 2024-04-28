"""Contains message classes for the OpenAI and DeepMind models."""

from typing import List, Literal, Union
from pathlib import Path
from PIL import Image
from util.log import Logger

logger = Logger(__name__)

from util.image import encode_image

Roles = Literal["user", "model", "system"]

class UserMessage:
    """
    User message for the model.
    
    Attributes
    ----------
    role : Roles
        the role of the message
    content : str
        the content of the message
    images : List[Union[Path, str]]
        the images of the message
    """
    
    turn: int = 0
    role: Roles = "user"
    content: str = None
    images: List[Union[Path, str]] = None
    
    def __init__(self, content: str = None, images: List[Union[Path, str]] = None, turn: int = 0) -> None:
        """
        Initializes the UserMessage.
        
        Parameters
        ----------
        content : str
            the content of the message
        images : List[Union[Path, str]]
            the images of the message
        """
        self.turn = turn
        self.content = content
        self.images = images
        
        if self.images:
            for image in self.images:
                if isinstance(image, str) and image != "{{image}}":
                    logger.error("Image must be be either a Path or a string with the placerholder '{{image}}'.")
        
    def to_openai(self) -> dict:
        """
        Converts message to OpenAI API format.
        
        Returns
        -------
        dict
            the message in API format
        """
        content_list = [{"type": "text", "text": f"{self.content}"}] if self.content else []
        images_list = [
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{encode_image(image_url)}"}}
            for image_url in self.images
        ] if self.images else []

        return {
            "role": "user",
            "content": content_list + images_list
        }
        
    def to_deepmind(self) -> dict:
        """
        Converts message to DeepMind API format.
        
        Returns
        -------
        dict
            the message in API format
        """
        content_list = [{"text": self.content}] if self.content else []
        images_list = [
            {"inline_data": {"mime_type":"image/png", "data": encode_image(image_url)}}
            for image_url in self.images
        ] if self.images else []
        
        return {"parts": images_list + content_list, "role": "user"}
   
    def to_anthropic(self) -> dict:
        """
        Converts message to Anthropic API format.
        
        Returns
        -------
        dict
            the message in API format
        """
        content_list = [{"type": "text", "text": f"{self.content}"}] if self.content else []
        images_list = [
            {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": encode_image(image_url)}}
            for image_url in self.images
        ] if self.images else []

        return {
            "role": "user",
            "content": images_list + content_list
        }
    
class ModelMessage:
    """
    Model message for the model.
    
    Attributes
    ----------
    role : Roles
        the role of the message
    content : str
        the content of the message
    """
    turn: int = 0
    role: Roles = "model"
    content: str
    
    def __init__(self, content: str, turn: int = 0) -> None:
        """
        Initializes the ModelMessage.
        
        Parameters
        ----------
        content : str
            the content of the message
        """
        self.turn = turn
        self.content = content
    
    def to_openai(self) -> dict:
        """
        Converts message to OpenAI API format.
        
        Returns
        -------
        dict
            the message in API format
        """
        return {
            "role": "assistant",
            "content": f"{self.content}"
        }
        
    def to_deepmind(self) -> dict:
        """
        Converts message to DeepMind API format.
        
        Returns
        -------
        dict
            the message in API format
        """
        content_list = [{"text": self.content}] if self.content else []
        
        return {"parts": content_list, "role": "model"}
    
    def to_anthropic(self) -> dict:
        """
        Converts message to Anthropic API format.
        
        Returns
        -------
        dict
            the message in API format
        """
        return {
            "role": "assistant",
            "content": f"{self.content}"
        }
        
class SystemMessage:
    """
    System message for the OpenAI model.
    
    Attributes
    ----------
    role : Roles
        the role of the message
    content : str
        the content of the message
    """
    
    turn: int = 0
    role: Roles = "system"
    content: str
    
    def __init__(self, content: str, turn: int = 0) -> None:
        """
        Initializes the SystemMessage.
        
        Parameters
        ----------
        content : str
            the content of the message
        """
        self.turn = turn
        self.content = content
    
    def to_openai(self) -> dict:
        """
        Converts message to OpenAI API format.
        
        Returns
        -------
        dict
            the message in API format
        """
        return {
            "role": "system",
            "content": f"{self.content}"
        }
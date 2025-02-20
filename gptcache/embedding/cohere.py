from gptcache.utils import import_cohere
import_cohere()

import numpy as np
import cohere

from .base import BaseEmbedding


class Cohere(BaseEmbedding):
    """Generate text embedding for given text using Cohere.

    :param model: model name (size), defaults to 'large'.
    :type model: str
    :param api_key: Cohere API Key.
    :type api_key: str

    Example:
        .. code-block:: python

            from gptcache.embedding import Cohere
            
            test_sentence = 'Hello, world.' 
            encoder = Cohere(model='small', api_key='your_cohere_key')
            embed = encoder.to_embeddings(test_sentence)
    """
    def __init__(self, model: str='large', api_key: str=None, **kwargs):
        self.co = cohere.Client(api_key)
        self.model = model

        if model in self.dim_dict():
            self.__dimension = self.dim_dict()[model]
        else:
            self.__dimension = None
    
    def to_embeddings(self, data):
        """Generate embedding given text input

        :param data: text in string.
        :type data: str

        :return: a text embedding in shape of (dim,).
        """
        if not isinstance(data, list):
            data = [data]
        response = self.co.embed(texts=data, model=self.model)
        embeddings = response.embeddings
        return np.array(embeddings).astype('float32').squeeze(0)

    @property
    def dimension(self):
        """Embedding dimension.

        :return: embedding dimension
        """
        if not self.__dimension:
            foo_emb = self.to_embeddings('foo')
            self.__dimension = len(foo_emb)
        return self.__dimension
    
    @staticmethod
    def dim_dict():
        return {
            'large': 4096,
            'small': 1024
        }

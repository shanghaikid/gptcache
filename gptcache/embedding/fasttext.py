from gptcache.utils import import_fasttext
import_fasttext()

import fasttext.util
import numpy as np
import os

from .base import BaseEmbedding


class FastText(BaseEmbedding):
    """Generate sentence embedding for given text using pretrained models of different languages from fastText.

    :param model: model name, defaults to 'en'.
    :type model: str
    :param dim: reduced dimension of embedding. If this parameter is not provided, the embedding dimension (300) will not change.
    :type dim: int

    Example:
        .. code-block:: python
        
            from gptcache.embedding import FastText
            
            test_sentence = 'Hello, world.' 
            encoder = FastText(model='en', dim=100)
            embed = encoder.to_embeddings(test_sentence)
    """
    def __init__(self, model: str='en', dim: int=None):
        self.model_path = os.path.abspath(fasttext.util.download_model(model))
        self.ft = fasttext.load_model(self.model_path)

        if dim:
            fasttext.util.reduce_model(self.ft, dim)
        self.__dimension = self.ft.get_dimension()

    def to_embeddings(self, data, **kwargs):
        """Generate embedding given text input

        :param data: text in string.
        :type data: str

        :return: a text embedding in shape of (dim,).
        """
        assert isinstance(data, str), 'Only allow string as input.'
        emb = self.ft.get_sentence_vector(data)
        return np.array(emb).astype('float32')

    @property
    def dimension(self):
        """Embedding dimension.

        :return: embedding dimension
        """
        return self.__dimension

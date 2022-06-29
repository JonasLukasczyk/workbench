from .Core import *

# import pytorch stuff

class ImageGeneratorCNN(Filter):

  def __init__(self):
    super().__init__();
    self.addInputPort("Query", "SELECT * FROM input");
    self.addInputPort("Model", "PathToModel");
    self.addOutputPort("Images", []);

  def update(self):
    super().update()

    # Black Magic
    generatedImage = Image(
        {
            'RGB': [] # get numpy array from pytorch
        },
        {
            # Meta data goes here
            'Time': 2.5,
            'Phi': 4,
            'Theta': 3
        }
    )

    self.outputs.Images.set([generatedImage]);

    return 1;

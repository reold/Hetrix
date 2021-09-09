class KeyframeHandler:
    def __init__(self, layer_variables, all_layers):
        self.layer_variables = layer_variables
        self.all_layers = all_layers

    def normalize(self):
        for layer in range(len(self.all_layers)):
            print(layer)

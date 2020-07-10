from Path.Generator import Generator
from AlgorithmPicker import AlgorithmPicker

if __name__ == '__main__':
        generator = Generator()
        algo_picker = AlgorithmPicker()

        #executes algorithm on all of our generated 50 maps.

        for i in range(50):
            print("Executing forward on Map"+str(i))
            algo_picker.executeForwardAstar("resources/map"+str(i))
            print("Executing backwards on Map" + str(i))
            algo_picker.executeBackwardsAStar("resources/map"+str(i))
            print("Executing Adaptive on Map" + str(i))
            algo_picker.executeAdaptiveAStar("resources/map"+str(i))







